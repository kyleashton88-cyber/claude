---
name: practice-and-assessment
description: Build the practice and checking parts of a lesson - quiz questions that test understanding rather than recall, worked examples that fade into "your turn", implementation tasks, teach-back prompts, worksheets and capstone links. Use when writing quizzes, exercises, homework, assessments or certification checks for course lessons and videos, or when learners "watch but don't do".
---

# Practice and Assessment

Watching isn't learning. Each lesson video needs retrieval (quizzes), practice (worked
example, then faded, then alone), an implementation task, and a teach-back.

## Quiz questions that test understanding

Use `quiz` scenes: question, `[[pause 4]]`, "The answer..." sentence with the reason.
Two or three per lesson, spread out. Write them at these levels (easy to hard):

| Level | Asks the learner to | Example |
|---|---|---|
| Apply | Use the rule on new numbers | "Collateral $50k, LT 0.8, debt $20k. Health factor?" |
| Diagnose | Spot what's wrong in a scenario | "Sam borrowed at max LTV. What's the risk?" |
| Decide | Choose between options and say why | "Buffer to HF 1.5 or HF 2.5 for a volatile asset?" |
| Predict | Say what happens next | "ETH drops 30%. What happens to this position?" |

Avoid pure definition recall ("What does LTV stand for?") except in Stage 0.
The answer line always explains *why* in one sentence, so a wrong guess still teaches.
Use a common misconception from the teach plan as the tempting wrong answer.

## Worked example, then fading

1. **Full example** (`steps` with `result`): every step shown and spoken.
2. **Faded example** (`quiz` or `steps` with the last line as a question): same method, new numbers, final step left to the viewer, then revealed.
3. **Alone** (in "Your turn"): new numbers, no help, answer in the lesson page or worksheet.

## "Your turn": the implementation task

A `statement` scene in the "Your turn" chapter, spoken clearly:

- One concrete action, 5 to 20 minutes, in the learner's own setup (testnet, paper account, calculator or worksheet).
- A visible result they can check ("You should see a health factor above 2").
- The worksheet to use (`programs/defi-program/08-worksheets.md`) or calculator (Course Hub, `defi_calc.py`, `grid_calc.py`).
- Never a task with real money at risk in Stages 0 to 2; always "practice mode first".

## Teach-back

Ask the learner to explain the idea in two sentences, as if to a friend. Put the prompt
in the recap ("Explain to someone why a health factor of 1.1 is dangerous"). In the
community, a weekly teach-back thread turns this into engagement.

## Linking to the bigger picture

- Map each quiz to the lesson objective; if a quiz doesn't test the objective, replace it.
- Each module's final lesson points to the capstone and rubric in `07-program-operations.md`.
- Mastery Starters (N.0) preview the module's hardest quiz so learners know where they're heading.

## Quality checks

- At least one quiz asks the learner to *apply* or *decide*, not recall.
- Every quiz's answer is supported by something shown earlier in the video.
- Numbers in quizzes are checked with the calculators (`defi-strategies/defi_calc.py`, `grid-bot-design/scripts/grid_calc.py`) before rendering.
