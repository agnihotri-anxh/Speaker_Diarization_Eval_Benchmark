# Voice Arena: Speaker Diarization Benchmark & Leaderboard
## Document 01: Project Overview, Scope & Master Goal

---

### 1. Executive Mission & Context
**Voice Arena** is an independent voice AI evaluation lab dedicated to answering the decisive question for audio AI engineers:
> *"Which speech system actually works best for a given real-world use case, where does it fail, and can published numbers be trusted?"*

Speaker Diarization—the algorithmic process of answering **"Who spoke when?"** without prior voice enrollment or knowledge of speaker counts—is the foundational layer for all conversational intelligence products. Today's commercial landscape is saturated with vendor claims of "99% diarization accuracy" tested on cherry-picked, synthetic audio. 

This project designs and specifies the **Voice Arena Speaker Diarization Benchmark & Public Leaderboard**: a rigorous, transparent, multi-dimensional evaluation system that reflects true production conditions across B2B meetings, telephony contact centers, ambient clinical consultations, and broadcast media.

---

### 2. The Core Problem We Are Solving

```
Raw Multi-Speaker Audio
    ├── "Hey, did you ship the patch?" (Eng Lead)
    ├── [Overlap] "Yes, 10 mins ago." (DevOps)
    └── "Wait, what about staging?" (PM)
               │
               ▼
   [Speaker Diarization Engine]
               │
               ▼
Timestamps + Anonymous Speaker Clusters
    ├── [00:01.20 - 00:03.10] Speaker_0: "Hey, did you ship the patch?"
    ├── [00:02.80 - 00:04.50] Speaker_1: "Yes, 10 mins ago."   <-- Overlapping Speech
    └── [00:04.20 - 00:06.10] Speaker_2: "Wait, what about staging?"
```

#### Why Traditional Academic Benchmarks Fail Production Buyers
1. **Outdated Hardware & Environments (AMI, ICSI):** AMI was recorded in 2005 with individual lapel/headset microphones in European academic meeting rooms. It ignores AirPods, Bluetooth packet drops, acoustic room reverberation, and modern browser-based web calling codecs (Opus 48kHz).
2. **Telephony Narrow-Band Artifacts (CALLHOME):** CALLHOME is strictly two-speaker PSTN telephone audio. It provides zero signal for 4–8 person cross-talk meetings.
3. **Hyper-Esoteric Test Sets (DIHARD III):** DIHARD evaluates YouTube baby babble, restaurant noise, and audiobooks. While scientifically fascinating, it fails to inform an enterprise choosing an engine for financial earnings calls or patient-doctor interviews.
4. **The Commercial Cloud Blindspot:** No existing academic challenge benchmarks the dominant enterprise APIs: Deepgram Nova-3, AssemblyAI Universal-2, Google Cloud Speech v2, AWS Transcribe, Rev AI, or Azure Speech.
5. **Single-Number Fallacy:** Academic leaderboards rank systems on a single global Diarization Error Rate (DER). In reality, a system with 12% DER that runs in 200ms at $0.004/min is dramatically superior for live sales assistance than an offline system with 9% DER that takes 4x real-time and costs $0.03/min.

---

### 3. Target Buyer Personas & Core Decision Matrices

| Persona | Core Environment | Primary Pain Points | Decisive Question on Leaderboard |
| :--- | :--- | :--- | :--- |
| **Persona 1: B2B Meeting Assistants** *(Zoom AI, Notion, Otter, Fireflies)* | 3–8 speakers, laptop mics / AirPods, heavy cross-talk, keyboard noise, laughter. | Speaker confusion during cross-talk; hallucinated phantom speakers during long pauses. | *"Which engine correctly tracks 6 people talking over each other in a sprint review with <15s turnaround at <$0.015/min?"* |
| **Persona 2: Contact Centers & CX** *(Gong, Balto, Talkdesk, Genesys)* | Exactly 2 speakers (Agent vs. Customer), 8 kHz telephony, cellular compression. | Speaker flipping (inverting Agent and Customer); slow streaming response. | *"Which model guarantees near-zero speaker flips on 8 kHz phone calls with streaming latency <500ms at <$0.006/min?"* |
| **Persona 3: Ambient Clinical Scribes** *(Abridge, Suki, Nuance DAX, Nabla)* | 2–4 speakers (Doctor, Patient, Caregiver), far-field tablet mic, tile floor reverberation. | Dropping quiet/hesitant patient speech; misattributing allergy/dosage statements. | *"Which system offers HIPAA/on-premise self-hosting, zero missed speech on soft voices, and no phantom speaker generation?"* |
| **Persona 4: Media & Legal Transcription** *(Descript, Rev, Court Reporting)* | 2–10 speakers, studio to courtroom, strict legal accountability. | Word boundary truncation; audio editing alignment mismatch. | *"Which system provides word-level diarization (Word Flop Error Rate <2%) with exact sub-100ms cut points?"* |

---

### 4. Master Deliverables Architecture

Per the Voice Arena mandate, this assessment produces four distinct, interconnected artifacts:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MASTER SUBMISSION PACK                          │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. Comprehensive Main Document │ Firstname_Lastname_Q1_Main.pdf        │
│    • Complete Methodology      │ (Full research, formulas, benchmark   │
│    • 10+ Models & Fairness     │  design, pilot data, reflection)      │
├────────────────────────────────┼───────────────────────────────────────┤
│ 2. Executive One-Pager         │ Firstname_Lastname_Q1_OnePager.pdf    │
│    • High-Density C-Suite Brief│ (2-minute scan for leadership)        │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. Leaderboard UI Mockup       │ Interactive Web Mockup / Sketch       │
│    • Product Architecture      │ (Filters, metric columns, drilldowns, │
│    • UX & Visual Specification │  confidence intervals, radar view)    │
├────────────────────────────────┼───────────────────────────────────────┤
│ 4. Video Walkthrough Script    │ 2-Minute Compact Pitch Script         │
│    • 120-second sharp delivery │ (Problem, 3 pivotal trade-offs,       │
│    • Slide deck / storyboarding│  lessons from literature)             │
└────────────────────────────────┴───────────────────────────────────────┘
```

