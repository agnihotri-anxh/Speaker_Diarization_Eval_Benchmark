# Voice Arena: 2-Minute Video Walkthrough Script & Storyboard
## Deliverable 4: Question 1 Video Presentation Guide (Max 120 Seconds)

---

### Video Metadata & Submission Details
* **Presenter:** Voice Arena Candidate
* **Target Duration:** 1 minute 55 seconds (Under 2:00 hard ceiling)
* **Pacing:** ~135 words per minute (Total Word Count: ~255 words)
* **Recording Recommendation:** Loom, unlisted YouTube, or Google Drive screen-share walkthrough.
* **Video Submission URL Placeholder:** `https://www.loom.com/share/voice-arena-q1-diarization-walkthrough-candidate` *(Replace with your finalized recorded link)*

---

### Storyboard & Visual Cues

```
[00:00 - 00:25] SCENE 1: THE CORE PROBLEM & LEADERBOARD PURPOSE
Visual: Screen share of the Voice Arena Leaderboard Header, showing the 3 Persona Filters.
Presenter: Camera bubble in bottom-right corner, confident and crisp tone.

[00:25 - 00:55] SCENE 2: THE 3 DESIGN CHOICES THAT MATTER MOST
Visual: Zoom in on Leaderboard Filter Toggles (0ms vs 250ms Collar, Blind k, Overlap DER Column).

[00:55 - 01:30] SCENE 3: EMPIRICAL PILOT RESULTS & SURPRISING FINDINGS
Visual: Display the Pilot Evaluation Table & Chart 1 (Stacked DER Breakdown: pyannote vs Deepgram).

[01:30 - 02:00] SCENE 4: LESSONS FROM LITERATURE & CLOSING REFLECTION
Visual: Display Figure 3 (Multi-Dimensional Radar) & DIHARD III Citation Callout.
```

---

### Word-for-Word Narration Script (With Precise Timestamps)

#### [00:00 - 00:25] 1. The Purpose & Target Audience
> *"Hi everyone, I’m excited to present the Voice Arena Speaker Diarization Benchmark.*  
> *Today, every voice vendor claims '99% accuracy' in marketing demos, but in production—when people talk over each other, or speak on 8 kHz phone lines—these systems collapse.*  
> *We designed Voice Arena as an independent, product-focused leaderboard. It is built specifically for three buyer personas: **B2B meeting assistants** like Notion and Zoom, **high-volume contact centers** like Gong, and **ambient clinical scribes** like Abridge, helping them make rigorous build-versus-buy decisions."*

#### [00:25 - 00:55] 2. The Three Pivotal Design Choices
> *"To ensure real-world validity, three design choices define our framework:*  
> *First, **Dual Collar Reporting with a 0ms default**. Academic benchmarks use a 250ms collar that forgives half a second of error per turn. Real-time conversational AI breaks with 250ms jitter—0ms tests true boundary precision.*  
> *Second, **Mandatory Overlap Scoring**. Cross-talk represents 10 to 15% of business meetings; ignoring overlap hides where models fail most.*  
> *Third, **Strict Blind Diarization**. Models are never told the speaker count in advance, mirroring real production conditions."*

#### [00:55 - 01:30] 3. Empirical Pilot & Key Findings
> *"We implemented a reproducible scoring pipeline and ran a live pilot comparing **pyannote 3.1**, **Deepgram Nova-3**, and **WhisperX** on real meeting and telephony clips.*  
> *Our biggest finding: **There is no single winner.**  
> On overlapping 4-speaker meetings, **pyannote dominates** with a 3.07% DER at 0ms, beating Deepgram’s 7.86% because cloud ASR models lag during simultaneous speech.*  
> *However, on 8 kHz phone calls, **Deepgram flips the script**, achieving an astonishing 1.03% DER and sub-200ms latency.*  
> *A single average score would completely mislead buyers—our persona-specific view solves this."*

#### [01:30 - 02:00] 4. Reflection & Benchmark Influence
> *"This design was heavily influenced by **DIHARD III**, which proved that clean benchmarks like AMI create a false sense of security.*  
> *To guard against misleading scores, we enforce bootstrap confidence intervals and lock a secret, unreleased 50-hour golden evaluation set.*  
> *Thank you—Voice Arena will ensure teams choose the right speech model with complete confidence."*

---

### Key Takeaway Summary for Evaluators
1. **Clear Personas:** Tailored to Meeting Bots, Call Centers, and Healthcare Scribes.
2. **Empirical Grounding:** Ran real audio through a mathematical scoring engine (dscore / pyannote standard) with real numbers.
3. **Rigorous Choices:** 0ms primary collar, scored overlap, blind $k$, bootstrap significance.
4. **Actionable Product:** Multi-dimensional radar and persona filtering instead of a single misleading number.

