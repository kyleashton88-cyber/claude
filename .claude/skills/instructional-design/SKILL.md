---
name: instructional-design
description: Design how a lesson teaches before it is scripted - objectives, prior knowledge, misconceptions, the understand, see it, do it, check, teach it back arc, cognitive load and multimedia principles. Use when planning a lesson, module or course video, when a lesson "feels like a lecture", when learners aren't implementing, or when asked to make content easier to understand, more practical or more teachable.
---

# Instructional Design for Course Lessons

A lesson succeeds when the learner can **do** something afterwards that they
couldn't before, and can explain why. Everything in this skill serves that.

## 1. Write the teach plan first

Before any script, fill in this plan (keep it at the top of the gold script's `use` field or in a scratch note):

```
Lesson:            3.2 LTV, liquidation threshold & health factor
Learner can:       calculate health factor and liquidation price for any position, and pick a safe buffer
Proof:             given collateral, LT and debt, they compute HF and the price that liquidates them (quiz 2)
Already knows:     what a lending pool is (3.1), collateral, borrowing
Misconceptions:    "max LTV is safe", "HF 1.1 is fine", "the protocol will warn me"
Mechanism to show: collateral → oracle price → HF → liquidator (flow)
Real screen:       the position panel on a lending app: where HF and liquidation price appear (cutaway)
Worked example:    $50k ETH, LT 0.8, $20k debt → HF 2.0 → liquidation at ETH -50%
Your turn:         same, with $30k debt (faded example)
Teach-back prompt: "Explain to a friend why HF 1.1 is dangerous, in two sentences"
```

Objectives use doing verbs (calculate, choose, spot, set up, compare, decide), never
"understand" or "know about". One lesson, one main objective, at most three sub-skills.

## 2. The lesson arc: understand → see it → do it → check → teach it back

| Beat | Purpose | Typical scenes | Share of runtime |
|---|---|---|---|
| Hook | Why this matters, what goes wrong without it | `statement`, `strike`, `stats` | 5 to 10% |
| Objective | What they'll be able to do | `pillars` | 3% |
| Understand | The idea, built from what they know, with an analogy | `bullets`, `compare`, `image` | 20% |
| See it | The mechanism moving | `flow`, annotated `image` | 20% |
| Do it | The real screen, step by step | `cutaway`, `steps` | 25% |
| Worked example | Real numbers, every step shown | `steps` with `result` | 10% |
| Check | Retrieval, spaced through the lesson | `quiz` | 10% |
| Teach it back + recap | Say it in their own words; three-line summary; next lesson | `statement`, `bullets`, `cta` | 5 to 10% |

Quizzes go after each major section, not all at the end. Retrieval spread through
the lesson is what makes it stick.

## 3. Principles to apply (Mayer's multimedia principles, adapted)

- **Signalling:** highlight what the voice is talking about. The renderer does this for items, flow nodes and cutaway boxes; write the voice so it names the thing on screen.
- **Redundancy:** don't put paragraphs on screen that the voice reads word for word. Screen shows keywords, numbers and diagrams; voice explains.
- **Coherence:** cut interesting-but-irrelevant detail. Put it in the written lesson instead.
- **Segmenting:** one idea per scene. If a scene's voice runs past about 45 seconds, split it.
- **Pre-training:** define new terms (with a quick picture) before they're used in a mechanism.
- **Contiguity:** labels sit on the diagram, not in a legend. Numbers appear when they're spoken.
- **Personalisation:** talk to "you". Short sentences. Conversational, not academic.
- **Worked examples, then fading:** show a full example, then one with the last step missing, then one they do alone.

## 4. Cognitive load checklist

- New terms per lesson: 5 or fewer. More means split the lesson.
- Every abstract idea gets a concrete example with numbers within 30 seconds.
- Every analogy is followed by where the analogy breaks ("unlike a bank, nobody calls you").
- Formulas are shown once in words, once in symbols, once with numbers.
- Beginners (Stages 0 to 1): slower pace, more pictures, every click shown. Experts (Stages 4 to 5): faster, denser, more trade-offs and edge cases.

## 5. Implementation: make them do it

Every lesson ends in an action inside the learner's own setup, sized to 5 to 20 minutes:
"Open your wallet on testnet and...", "Fill in worksheet 4 for your current position...",
"Run the grid calculator with your pair and note the spacing...". Link the matching
worksheet in `programs/defi-program/08-worksheets.md`. The action is spoken in the video
(`statement` scene titled "Your turn") and written in the lesson page.

## 6. Misconception-first teaching

For each misconception: state it fairly, show the case where it fails (ideally with
numbers or a real incident from Lesson 6.5), then give the correct model. A `compare`
scene with the wrong belief on the left (`tone: bad`) and the right one on the right works well.

## Handoff

Pass the teach plan to `visual-storyboard`. Pass the misconceptions and proof task to
`practice-and-assessment`.
