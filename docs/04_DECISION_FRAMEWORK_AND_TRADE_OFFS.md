# Voice Arena: Speaker Diarization Benchmark & Leaderboard
## Document 04: Decision Framework, Trade-Offs & Reflection

---

### 1. Architectural Decisions Taken by Step and Turn

Every design choice in an evaluation benchmark trades off one desirable property against another. Below is the explicit decision log justifying our choices:

| Decision Point | Chosen Approach | Rejected Alternative | Core Justification & Trade-Off |
| :--- | :--- | :--- | :--- |
| **1. Collar Window** | **Dual Reporting: 0ms (Primary Default) & 250ms (Secondary Toggle)** | Single fixed 250ms collar (academic standard) | A 250ms collar forgives 0.5s of error around every turn boundary. While fine for loose meeting summaries, conversational AI and voice agents break if boundaries are off by 250ms. Reporting 0ms reveals true precision; offering 250ms maintains backwards compatibility with academic literature. |
| **2. Overlapping Speech** | **Included in Primary DER + Dedicated Overlap DER Column** | Excluding overlapping speech segments | In corporate meetings and debates, 5–15% of speech overlaps. Systems that cannot detect cross-talk hallucinate or miss critical dialogue. Scoring overlap is non-negotiable for real-world utility, even though it raises raw DER numbers. |
| **3. Speaker Count Prior** | **Strict Blind Mode ($k = \text{unknown}$) as Primary** | Passing known speaker counts ($k = \text{oracle}$) | In real-world production (e.g., Zoom calls, telehealth), the system is never told the exact number of speakers in advance. Allowing oracle speaker counts inflates scores by 30–50% and masks clustering failures. |
| **4. Word-Level vs Interval Normalization** | **300ms Inter-Word Pause Bridge for ASR APIs** | Evaluating ASR APIs purely on word-level cpWER | Standalone diarizers (pyannote) output continuous acoustic intervals, whereas ASR APIs (Deepgram) output word timestamps with speaker tags. Merging consecutive same-speaker words separated by $<300\text{ms}$ into a continuous segment standardizes both into canonical RTTMs fairly. |
| **5. Runtime Hardware Baseline** | **NVIDIA A10G Cloud GPU as Standard for Self-Hosted Models** | Running on arbitrary heterogeneous local machines | Standardizing self-hosted open-source models on a cloud NVIDIA A10G (24GB VRAM) provides a stable, reproducible reference for Real-Time Factor (RTF) and cost-per-hour calculations compared to commercial SaaS APIs. |
| **6. Statistical Rigor** | **Bootstrap Resampling (10,000 iterations) + 95% Confidence Intervals** | Simple point-estimate mean DER ranking | Small test sets can rank System A above System B due to lucky segmentation on one long file. Bootstrap intervals ensure buyers only trust rankings when the performance delta is statistically significant ($p < 0.01$). |

---

### 2. Deep-Dive on Pivotal Trade-Offs

#### Trade-Off A: The Collar Dilemma (0ms vs. 250ms)
* **The Academic View:** Human annotators naturally disagree on the exact onset/offset of fricatives, plosives, and trailing whispers by 100–200ms. Applying a 250ms collar avoids penalizing models for human annotator jitter.
* **The Production Reality:** If a voice agent interrupts a user with a 250ms error margin, the user experiences awkward double-talk or clipped words. 
* **Voice Arena Solution:** We use **Forced Alignment (Montreal Forced Aligner)** to pin reference boundaries to acoustic phonemes (reducing human jitter to $<30\text{ms}$), allowing us to make **0ms collar the default ranker** while retaining a 250ms filter for historical comparison.

#### Trade-Off B: Standalone Diarization vs. Integrated ASR Diarization
* A pure acoustic diarizer has no concept of words; it clusters acoustic feature vectors.
* An ASR-integrated diarizer (like Deepgram Nova-3) can use linguistic context (e.g., questions and syntactic turns) to reinforce speaker clustering.
* **Voice Arena Solution:** We establish two parallel evaluation tracks:
  1. **Acoustic Diarization Track (RTTM):** Tests pure acoustic voice segmentation.
  2. **Transcript Attribution Track (cpWER / WFER):** Tests whether the final readable transcript assigned each word to the correct speaker.

---

### 3. Final Reflection (Addressing Assessment Prompts)

#### Q1: Which design choice are you least sure about, and why?
> **Answer:** *The 300ms pause-bridging heuristic used to convert word-level ASR diarization into continuous acoustic RTTM intervals.*  
> When an ASR system outputs word timestamps, natural pauses between words (breathing, hesitation) are empty. If we bridge pauses up to 300ms to form a continuous speech segment, we risk artificially absorbing short interjections from another speaker or creating false alarms during deliberate dramatic pauses. While 300ms aligns well with standard phonetic turn-taking, there is no universal mathematical constant for human conversational silence.

#### Q2: Which benchmark you read influenced you most, and how?
> **Answer:** *The Third DIHARD Diarization Challenge (Ryant et al., 2020).*  
> DIHARD III fundamentally challenged the field by proving that models performing well on clean academic datasets (like AMI) completely collapse on diverse acoustic domains. It pioneered the dual evaluation of Full DER vs Overlap DER and showed why blind diarization ($k$ unknown) is the only realistic test. Voice Arena adopts DIHARD's multi-domain rigor and uncollared evaluation, but redirects it from academic YouTube clips toward high-value enterprise domains (telephony, meetings, clinical).

#### Q3: What could make your leaderboard misleading, and how did you guard against it?
> **Answer:** *Two major risks: Domain Averaging Fallacy and Audio Data Contamination.*  
> 1. *Domain Averaging Fallacy:* A single composite average score can hide that Model A is stellar at 2-person phone calls but atrocious at 6-person meetings. We guard against this by providing **Persona-Specific Leaderboard Views** and radar charts.  
> 2. *Contamination:* If vendors train on public audio (e.g., VoxConverse or AMI), their benchmark scores are artificially inflated. We guard against this by maintaining a **Secret Golden Evaluation Split** composed of newly recorded, proprietary conversational sessions that have never been uploaded to the public internet.

#### Q4: What would you improve with more time?
> **Answer:** *Three future enhancements:*  
> 1. **Dynamic Streaming Window Evaluation:** Explicitly testing streaming APIs under varying network jitter and packet loss conditions to measure latency-accuracy degradation curves.  
> 2. **Multi-Lingual Code-Switching Slice:** Curating conversations where bilingual speakers alternate between languages (e.g., English and Spanish, or Hindi and English) within the same sentence, which frequently causes current acoustic embedding models to mistakenly split a single speaker into two personas.  
> 3. **Downstream LLM Impact Metric:** Measuring how diarization errors directly affect the accuracy of downstream LLM summaries and action-item extraction (e.g., Hallucinated Action Items per Meeting).

