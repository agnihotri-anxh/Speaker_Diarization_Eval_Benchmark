# Voice Arena: Speaker Diarization Benchmark & Leaderboard
## Document 03: Implementation Plan & Work Breakdown Structure

---

### 1. Phased Execution Roadmap

The implementation of the Voice Arena Diarization Benchmark is organized into four sequential phases designed to deliver maximum empirical rigor and product utility:

```
Phase 1: Audio Curation & Ground Truth Protocol
  ├── Acoustic domain definition (Meetings, Telephony, Healthcare, Media)
  ├── Recording collection (50 hours total, 250 diverse sessions)
  └── Multi-stage human annotation + forced alignment verification
             │
             ▼
Phase 2: Model Ingestion Harness & Normalization
  ├── Integration of 10 target systems (3 Open Source, 7 Commercial APIs)
  ├── Format standardization (Canonical RTTM & JSON Word Stream)
  └── Blind execution & latency/cost instrumentation
             │
             ▼
Phase 3: Scoring Engine & Statistical Significance
  ├── Implementation of DER (0ms & 250ms), JER, cpWER, WFER via dscore/pyannote
  ├── Overlap sensitivity partition
  └── Non-parametric bootstrap resampling (10,000 iterations for 95% CIs)
             │
             ▼
Phase 4: Leaderboard Product & Pilot Validation
  ├── Interactive Leaderboard UI (Persona filters, radar charts, cost/latency trade-offs)
  ├── Hands-on empirical pilot experiment on public clips (AMI & VoxConverse)
  └── Publication of final PDF artifacts and walkthrough materials
```

---

### 2. Detailed Work Breakdown Structure (WBS)

#### Phase 1: Test Data Architecture & Reference Engineering (Weeks 1–3)
* **WBS 1.1: Corpus Stratification (50 Total Hours)**
  * **Meeting Slice (20 hrs):** 3–8 speakers; 40 sessions; recorded via Zoom/Google Meet on laptops, AirPods, and conference room mics.
  * **Telephony Slice (15 hrs):** Exactly 2 speakers; 60 calls; 8 kHz G.711/Opus; customer service and sales roleplays.
  * **Clinical Slice (10 hrs):** 2–4 speakers; 30 sessions; far-field tablet placement (8–10 ft away); doctor, patient, nurse dynamics.
  * **Broadcast/Debate Slice (5 hrs):** 4–10 speakers; 15 sessions; high turn density, contentious interruptions.
* **WBS 1.2: Human Ground-Truth Protocol**
  * Pass 1: Independent human transcription and coarse speaker labeling in Label Studio.
  * Pass 2: Phoneme/word forced alignment via Montreal Forced Aligner (MFA) to lock syllable boundaries.
  * Pass 3: Inter-Annotator Agreement (IAA) calculation. Flag all segments where boundary discrepancy $>100\text{ms}$ or speaker disagreement exists.
  * Pass 4: Senior phonetician adjudication to produce gold-standard RTTM files.

#### Phase 2: Model Testing Harness & Normalization (Weeks 4–5)
* **WBS 2.1: Model Integration Connectors**
  * Standalone local runners: Dockerized `pyannote.audio 3.1` (PyTorch/CUDA), `NVIDIA NeMo Sortaformer` (Triton), and `Picovoice Falcon` (C/Python SDK).
  * Cloud API workers: Async HTTP/gRPC connectors for Deepgram, AssemblyAI, Google Cloud STT v2, AWS Transcribe, Rev AI, and Azure Speech.
* **WBS 2.2: Normalization & Telemetry**
  * Automated mapping of word-level API outputs into interval RTTMs (merging inter-word pauses $<300\text{ms}$).
  * Recording wall-clock latency, Time-To-First-Byte (TTFB), Real-Time Factor ($\text{RTF} = \frac{\text{Processing Time}}{\text{Audio Duration}}$), and dollar cost per audio hour.

#### Phase 3: Scoring & Statistical Engine (Weeks 6–7)
* **WBS 3.1: Metric Computation Pipeline**
  * Primary metric computation: DER with 0ms collar (strict) and 250ms collar (forgiving).
  * Overlap-only DER vs Single-speaker DER breakdown.
  * JER (Jaccard Error Rate) and WFER (Word Flop Error Rate).
* **WBS 3.2: Statistical Significance Testing**
  * Non-parametric bootstrap resampling (sampling sessions with replacement 10,000 times).
  * Compute empirical 95% confidence intervals for every metric.
  * Paired permutation tests to verify whether the rank order between System $A$ and System $B$ is statistically significant ($p < 0.01$).

#### Phase 4: Product Delivery & Leaderboard Launch (Weeks 8–9)
* **WBS 4.1: Public Leaderboard UI**
  * Front-end table with multi-factor sorting (by persona, latency, cost, and collar).
  * Model inspection modal: Audio player with synchronized ground-truth vs model prediction timeline.
* **WBS 4.2: Deliverable Compilation**
  * Compile `Firstname_Lastname_Q1_Main.pdf`, `Firstname_Lastname_Q1_OnePager.pdf`, leaderboard sketches, and video script.
* **WBS 4.3: Empirical Pilot Harness (`data/` & `experiments/`)**
  * Modular NIST/dscore-compliant evaluation pipeline reading standard `.rttm` files.
  * Verified on AMI Meeting (`AMI_ES2004a.rttm`), VoxConverse Debate (`VoxConverse_Debate.rttm`), and Telephony Call Center (`Telephony_CallCenter.rttm`).
  * Validated empirical trade-off: pyannote 3.1 leads on meeting overlap (3.07% DER @ 0ms), Deepgram Nova-3 leads on 8kHz telephony (1.03% DER @ 0ms).

