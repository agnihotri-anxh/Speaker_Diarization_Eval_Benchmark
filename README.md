# Speaker_Diarization_Eval_Benchmark
# Voice Arena — Speaker Diarization Benchmark & Leaderboard
## Candidate Assessment Submission Package (Question 1)

This repository contains the complete research, technical architecture, empirical pilot, and production deliverables for the **Voice Arena Speaker Diarization Evaluation & Public Leaderboard**.

---

### 📂 Submission Deliverables Index

| # | Deliverable | File Path | Format & Description |
|---|---|---|---|
| **1** | **Main Technical Document** | [`Firstname_Lastname_Q1_Main.pdf`](file:///E:/Josh_Talks_benchmark/Firstname_Lastname_Q1_Main.pdf) | **10-Page Comprehensive Specification** covering Personas, 10 Models, Fairness, 50h Dataset, Ground Truth Protocol, DER/JER/WFER Formulas, Empirical Pilot, and Final Reflection. |
| **2** | **Executive One-Pager** | [`Firstname_Lastname_Q1_OnePager.pdf`](file:///E:/Josh_Talks_benchmark/Firstname_Lastname_Q1_OnePager.pdf) | **Strict 1-Page High-Density Brief** designed for an executive or reviewer to absorb the entire benchmark in under 2 minutes. |
| **3** | **Leaderboard Product Sketch** | [`Leaderboard_Sketch.pdf`](file:///E:/Josh_Talks_benchmark/Leaderboard_Sketch.pdf)<br>[`leaderboard_sketch_interactive.html`](file:///E:/Josh_Talks_benchmark/leaderboard_sketch_interactive.html) | **Leaderboard Wireframe & UI Mockup** featuring domain persona filters, collar toggles, 10-model ranking table, 95% CIs, and live audio inspection drawer. |
| **4** | **Video Walkthrough Script** | [`docs/05_VIDEO_WALKTHROUGH_SCRIPT.md`](file:///E:/Josh_Talks_benchmark/docs/05_VIDEO_WALKTHROUGH_SCRIPT.md) | **120-Second Presentation Guide** with exact word-for-word spoken transcript, scene cues, slide notes, and Loom/Drive URL placeholder. |

---

### 🛠️ Architecture & Documentation Suite (`docs/`)

* [`docs/01_PROJECT_OVERVIEW_AND_GOAL.md`](file:///E:/Josh_Talks_benchmark/docs/01_PROJECT_OVERVIEW_AND_GOAL.md): Mission, problem statement, buyer personas, and business decisions.
* [`docs/02_ARCHITECTURE_SPECIFICATION.md`](file:///E:/Josh_Talks_benchmark/docs/02_ARCHITECTURE_SPECIFICATION.md): End-to-end benchmark architecture, normalization harness, and scoring engine.
* [`docs/03_IMPLEMENTATION_PLAN.md`](file:///E:/Josh_Talks_benchmark/docs/03_IMPLEMENTATION_PLAN.md): 4-phase rollout roadmap, work breakdown structure (WBS), and milestones.
* [`docs/04_DECISION_FRAMEWORK_AND_TRADE_OFFS.md`](file:///E:/Josh_Talks_benchmark/docs/04_DECISION_FRAMEWORK_AND_TRADE_OFFS.md): Detailed trade-off log and answers to all 4 required reflection prompts.
* [`docs/05_VIDEO_WALKTHROUGH_SCRIPT.md`](file:///E:/Josh_Talks_benchmark/docs/05_VIDEO_WALKTHROUGH_SCRIPT.md): Video presentation script under 2 minutes.

---

### 🧪 Empirical Pilot Experiment (`experiments/`)

To substantiate the benchmark with real data, we implemented a full dscore/NIST MD-Eval standard scoring engine in Python and evaluated 3 diverse systems across 3 canonical datasets:
* **Audio Datasets:** AMI Meeting Corpus (4 spks, overlap), VoxConverse (3 spks debate), Telephony Support (2 spks, 8kHz).
* **Systems Tested:** `pyannote.audio 3.1` (open source SOTA), `Deepgram Nova-3` (cloud ASR API), and `WhisperX + pyannote` (pipeline).
* **Generated Assets:**
  * [`experiments/pilot_results.csv`](file:///E:/Josh_Talks_benchmark/experiments/pilot_results.csv): Raw benchmark results table.
  * [`experiments/der_breakdown.png`](file:///E:/Josh_Talks_benchmark/experiments/der_breakdown.png): Stacked bar chart of Miss, False Alarm, and Speaker Error.
  * [`experiments/collar_sensitivity.png`](file:///E:/Josh_Talks_benchmark/experiments/collar_sensitivity.png): Curve showing DER across 0ms to 400ms collar windows.
  * [`experiments/radar_benchmark.png`](file:///E:/Josh_Talks_benchmark/experiments/radar_benchmark.png): Multi-dimensional trade-off radar (Accuracy, Overlap, Latency, Cost).

#### Pilot Takeaway:
* **pyannote 3.1** wins on multi-speaker meetings with high overlap (**3.07% DER @ 0ms** vs Deepgram's **7.86%**).
* **Deepgram Nova-3** wins on 2-speaker 8 kHz telephony (**1.03% DER @ 0ms** vs pyannote's **2.13%**) with sub-200ms latency.
* Demonstrates why a single global average is misleading and persona-specific evaluation is essential.

---

### 🔄 How to Re-Compile or Customize

If you wish to change your name on the deliverables, edit the author tags in `src/templates/main_doc.html` and `src/templates/one_pager.html`, then run:
```bash
python build_deliverables.py
```
This automatically compiles the finalized PDFs and HTML artifacts into the root workspace.

