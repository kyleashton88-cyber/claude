---
name: tutorial-script-structure
description: Structure a course video script as a YouTube tutorial with a hook, a branded intro, a demo, a recap, and a paper action. Use when writing or extending an On-Chain Operator lesson or a Grid Bot Blueprint master, or when a lesson is under 15 minutes, missing a demo, or reading like a slide deck.
---

# Tutorial script structure

Use this before writing narration. A lesson that starts as prose becomes a slideshow. A lesson that starts as this outline becomes a tutorial.

## Length

15 to 20 minutes of speech at the measured On-Chain Operator rate of about 143 words a minute. That is 2,350 to 2,550 words. Under 15 minutes is not done. Over 20 minutes, cut a practice beat, not the hook or the recap. Module intros are the exception: a short branded intro is enough if it still has the plate, the disclaimer, music, and one still per beat. From Module 4 on, follow `series-continuity`: recap the previous lesson and name the next one.

## Order

1. **Hook.** One problem the viewer can see, in the first 20 seconds. No logo sting before it.
2. **Disclaimer.** Education only, not financial advice. Speak it and show it.
3. **Branded intro.** About 5 to 6 seconds. Lesson title over the navy and cyan plate. Elite lessons are not restyled and do not use this plate.
4. **Teach.** One idea per beat. Say the thing on screen as it appears.
5. **Demo.** The viewer does the idea on paper: a recount, a label, a checklist, or a worked example with the word Example on it.
6. **Quiz or teach-back.** The answer is spoken, including the sentence that starts "The answer".
7. **Recap.** Three lines the viewer can say without looking.
8. **Action.** One paper task for today. No live order, no seed phrase, no size filled in by the lesson.
9. **Outro.** Next lesson by name, or "this is the last lesson" when it is. 8 to 10 seconds.

## Voice

Sentences of about 8 to 20 words. "You". No "guaranteed", "risk-free", or a promised income. Numbers that are examples stay marked Example. The Blueprint house count is nineteen gaps between twenty lines, a half percent step, and a nine and a half percent span. That count is a teaching count, not a setting to copy.

## Where the files go

Write the script to `course/scripts/<id>.json` with one beat per idea: `vo`, `cap`, `role`, `concept`, `image`. Then run `python3 course/tools/build_course_scripts.py` only if you are regenerating the whole set. Do not upload to Whop.
