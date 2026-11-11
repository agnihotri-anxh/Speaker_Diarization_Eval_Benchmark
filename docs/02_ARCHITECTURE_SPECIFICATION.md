# Voice Arena: Speaker Diarization Benchmark & Leaderboard
## Document 02: Full System Architecture & Technical Specification

---

### 1. High-Level Benchmark Architecture

The Voice Arena Diarization Benchmark operates as an automated, reproducible testing platform that bridges raw audio capture with a public, multi-dimensional decision leaderboard:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              VOICE ARENA PIPELINE FLOW                                 │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [1. AUDIO COLLECTION & CURATION]
        │
        ├── Domain 1: Multi-party Corporate Meetings (3–8 speakers, 16kHz, high overlap)
        ├── Domain 2: Contact Center Telephony (2 speakers, 8kHz, G.711 / Opus)
        ├── Domain 3: Ambient Clinical Encounters (2–4 speakers, far-field tablet, reverb)
        └── Domain 4: Broadcast Debates & Panel Discussions (4–10 speakers, dynamic turns)
        │
        ▼
  [2. REFERENCE GROUND-TRUTH ENGINE]
        │
        ├── Dual Independent Human Annotation (Tool: Label Studio / Praat)
        ├── Forced Alignment on Word Boundaries (Montreal Forced Aligner)
        ├── Inter-Annotator Agreement Check (Cohen's Kappa > 0.92; boundary diff < 100ms)
        └── Adjudication Master Pass (Golden RTTM Reference Files)
        │
        ▼
  [3. MODEL EXECUTION & NORMALIZATION HARNESS]
        │
        ├── Standalone Diarizers (pyannote 3.1, NeMo Sortaformer, Picovoice Falcon)
        ├── ASR + Diarization APIs (Deepgram Nova-3, AssemblyAI Universal-2, AWS, Google, Rev)
        └── Normalization Engine:
              ├── Canonical RTTM Exporter (Interval standard)
              ├── Word-Level Speaker Mapper (Alignment with reference words)
              └── Determinism & Latency Logger (RTF, TTFB, P95 processing time, cost)
        │
        ▼
  [4. SCORING ENGINE (dscore + pyannote.metrics + MeetEval)]
        │
        ├── Primary Metric: DER @ 0ms collar & DER @ 250ms collar (with Overlap)
        ├── Secondary Metrics: JER (Jaccard Error Rate), cpWER, Word Flop Error Rate (WFER)
        └── Operational Metrics: Real-Time Factor (RTF), Streaming Latency, Cost ($/hour)
        │
        ▼
  [5. STATISTICAL VALIDATION ENGINE]
        │
        ├── Non-Parametric Bootstrap Resampling (10,000 iterations -> 95% Confidence Intervals)
        └── Paired Permutation Significance Tests (p < 0.01 threshold for leaderboard rank flip)
        │
        ▼
  [6. PUBLIC WEB LEADERBOARD & DECISION API]
        │
        ├── Filterable Table by Persona, Streaming vs Batch, Cost Bracket, Speaker Count
        ├── Sensitivity Curves (Collar vs DER; Overlap Fraction vs DER)
        └── Audio Inspector (Visual waveform, Reference vs Prediction comparison)
```

---

### 2. The Model Zoo: 10 Evaluated Systems & Execution Modalities

To ensure industrial relevance, Voice Arena benchmarks 10 leading systems across four architectural categories:

| System Name | Provider / Creator | Architectural Category | Deployment Modality | Input Format & Execution Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **pyannote.audio 3.1** | Open Source (Hugging Face) | Standalone Neural Diarizer | Self-Hosted (GPU: NVIDIA A10G) | Raw audio -> Voice Activity Detection (VAD) + Overlap Detection + ResNet Embedding + HBDSC Clustering. Blind $k$. |
| **NVIDIA NeMo Sortaformer** | NVIDIA | End-to-End Diarizer (EEND) | Self-Hosted (Triton Server / TensorRT-LLM) | Streaming & Offline Transformer-based diarization directly mapping acoustic frames to speaker activations. |
| **Picovoice Falcon** | Picovoice | On-Device Standalone Diarizer | Self-Hosted (Local CPU / Edge) | Ultra-lightweight edge acoustic engine; outputs speaker intervals without cloud round-trip. |
| **WhisperX + pyannote** | Open Source (m-bain) | Pipeline (ASR + Forced Alignment + Diarization) | Self-Hosted (GPU: RTX 4090 / A10) | Whisper ASR -> Phoneme Forced Alignment -> pyannote segment clustering. Outputs word-level speaker labels. |
| **Deepgram Nova-3** | Deepgram Inc. | Speech-to-Text with Native Diarization | Cloud REST & WebSocket API | End-to-end multi-task model; word-level speaker tags with streaming real-time capability. |
| **AssemblyAI Universal-2** | AssemblyAI | Speech-to-Text with Speaker Diarization | Cloud REST API | Two-pass neural diarizer; outputs word timestamps with speaker assignments. |
| **Google Cloud Speech-to-Text v2** | Google Cloud | Cloud Speech API | Cloud REST / gRPC API | Chirp 2 / Gemini-powered speech pipeline with `diarization_config` enabled. |
| **AWS Transcribe** | Amazon Web Services | Cloud Speech Service | Cloud SDK (boto3) | Turn-based acoustic clustering with speaker label partition; supports MaxSpeakers hint. |
| **Rev AI Diarization API** | Rev.com | Speech-to-Text with Diarization | Cloud REST API | Human-informed trained acoustic model specialized in conversational turns. |
| **Microsoft Azure Speech Service** | Microsoft Cognitive Services | Multi-Channel & Single-Channel Diarization | Cloud SDK & Container | Real-time conversation transcription engine with speaker diarization. |

---

### 3. Solving the Fairness Challenge Across Heterogeneous Systems

Benchmarking a standalone acoustic interval engine (e.g., `pyannote`) against a speech-to-text API (e.g., `Deepgram`) introduces fundamental apples-to-oranges pitfalls. Voice Arena resolves these through four strict protocols:

#### A. Dual Evaluation Tracks: Acoustic-Interval Track vs. Word-Level Track
* **Track 1: Acoustic Interval Diarization (Standard RTTM)**
  * Evaluates purely "who is speaking during continuous millisecond intervals".
  * Standalone diarizers output RTTM naturally.
  * For ASR APIs: Word tokens with speaker labels are converted to continuous intervals by joining consecutive words of the same speaker, bridging inter-word pauses $<300\text{ms}$.
* **Track 2: Word-Attribution Diarization (Word-Level)**
  * Evaluates "did the system assign word $w_i$ to the right speaker?".
  * ASR APIs output word speaker tags directly.
  * For Standalone diarizers: An external frozen reference transcript (via Whisper-Large-v3 with forced alignment) is projected onto the predicted acoustic intervals.

#### B. The Speaker Count Knowledge Trap: Blind Diarization Rule
* Many commercial APIs allow passing `min_speakers` and `max_speakers`. If a system is given `num_speakers=2`, clustering accuracy artificially surges by 30–50%.
* **Voice Arena Rule:** All systems are evaluated in **Blind Mode** ($k=\text{unknown}$). Passing oracle speaker counts is strictly forbidden on the primary leaderboard. (An optional "Oracle $k$" secondary filter is provided to analyze clustering ceiling).

#### C. Fixed Standard Audio Feeds
* All models receive identical, unadulterated 16-bit PCM WAV audio.
* For telephony benchmarks, audio is downsampled to 8 kHz mono prior to submission to simulate true telecom trunks.
* No system is permitted pre-enrolled voice profiles.

---

### 4. Mathematical Definition of Metrics

#### 1. Diarization Error Rate (DER) - The Primary Metric
DER measures the fraction of time that is not attributed correctly to the true speaker:

$$\text{DER} = \frac{T_{\text{miss}} + T_{\text{fa}} + T_{\text{spkerr}}}{T_{\text{total}}}$$

Where:
* $T_{\text{total}}$ = Total duration of all ground-truth speech segments.
* $T_{\text{miss}}$ = **Missed Speech Time** (Reference speaker active, but system predicts silence).
* $T_{\text{fa}}$ = **False Alarm Time** (Reference indicates silence, but system predicts speech).
* $T_{\text{spkerr}}$ = **Speaker Error / Confusion Time** (System detects speech, but maps it to the wrong speaker cluster after optimal Hungarian matching).

#### 2. Jaccard Error Rate (JER) - Equal Speaker Weighting
Traditional DER can be skewed by a dominant speaker who talks for 80% of a meeting. JER evaluates each speaker equally:

$$\text{JER} = 1 - \frac{1}{|S_{\text{ref}}|} \sum_{s \in S_{\text{ref}}} \max_{s' \in S_{\text{hyp}}} \frac{|T(s) \cap T(s')|}{|T(s) \cup T(s')|}$$

Where $|S_{\text{ref}}|$ is the number of reference speakers, and $T(s)$ is the total active duration of speaker $s$.

#### 3. Word Flop Error Rate (WFER) & cpWER
For product teams relying on transcripts, WFER measures the percentage of transcribed words that are assigned to the wrong speaker:

$$\text{WFER} = \frac{\text{Number of Words Assigned to Wrong Speaker}}{\text{Total Spoken Words}}$$

---

### 5. Scoring Configurations: Collar & Overlap Rules

| Scoring Setting | Value | Engineering Rationale |
| :--- | :--- | :--- |
| **Collar Tolerance** | **Dual Reporting: 0ms & 250ms** | Academic benchmarks historically use 250ms to forgive human boundary imprecision. However, modern real-time voice products demand tight turn-taking. Voice Arena ranks by **0ms collar** by default and provides a 250ms toggle. |
| **Overlapping Speech** | **Included (Scored)** | Overlapping speech accounts for 5% to 15% of enterprise meetings, but causes 40%+ of downstream user errors. Benchmarks that exclude overlap hide fatal real-world model failures. |
| **Speaker Count** | **Unknown (Blind)** | In real applications, the server never knows beforehand whether 3 or 7 people will speak in a call. |

