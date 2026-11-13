# Evaluation of the engine plates Stewart reviewed

Date: 13 Nov 2026. Compared with the ChatGPT stills in `course/images/bp-01-introduction/` (001, 002, 007, 009) and with the engine gallery as it stood after the Bold-type pass.

The engine's own QA reported zero failures. That report measured stem width, font name, and how much of the frame was brighter than the navy. Those numbers can all pass on a plate that is not fit to publish. The pass bar is now `skills/image-quality-standard/`. Scores below are 1–5. A shippable plate needs 4 in every category and no hard fail.

## What the reference stills do

The ChatGPT plates are open. The headline is huge. The subject is a chart line or one glass object with a tight rim and some depth. Navy and a fine grid do the rest. Labels are few and quiet. Nothing is built out of a circle stacked on a rectangle.

## Scores of the plates Stewart saw

| Type | Clarity | Composition | Craft | Brand | Legibility | Character | Accuracy | Hard fail |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Mascot | 3 | 2 | 1 | 2 | 4 | 1 | 4 | inconsistent mascot |
| Cover (mascot on it) | 3 | 2 | 1 | 2 | 4 | 1 | 4 | inconsistent mascot |
| Grid ladder | 4 | 2 | 2 | 3 | 4 | n/a | 4 | none |
| Candle anatomy | 4 | 2 | 2 | 3 | 4 | n/a | 4 | none |
| Three-step | 3 | 2 | 2 | 2 | 4 | n/a | 4 | none |
| Checklist / flowchart | 3 | 2 | 2 | 2 | 4 | n/a | 4 | none |
| Warning / liquidation | 3 | 2 | 2 | 3 | 4 | n/a | 4 | none |
| Analogy scenes | 3 | 2 | 2 | 2 | 4 | n/a | 4 | none |
| Elite | 4 | 2 | 2 | 3 | 4 | n/a | 4 | none |

None of these pass. The highest craft score is 2.

## Root causes

1. The mascot is not a character. It is a head rectangle, a body rectangle, two leg rectangles, a pill for a visor, and lines for arms. The silhouette is a snowman. There is no line-weight hierarchy and no constructed form. Calling the eye a single bar did not make it a brand character. **Code-drawn SVG of this kind cannot reach a professional mascot in this pipeline.** A real sheet has to be drawn once, as a picture, and reused. The engine now refuses to invent one. See `illustration_engine/assets/character/README.md`.

2. The quality check rewarded the wrong thing. A 32px blur and a coverage target of 30–55% made the frame a milky cyan rounded rectangle. The chart inside it was thinner and quieter than the frame. The reference stills do the opposite: the line is the subject, and most of the frame is navy.

3. Empty panels. Three-step cards held a number and a word. Candle anatomy held one stick in a large void. That reads as a template, not a lesson picture.

4. Labels were glowing chips that competed with the diagram. The reference labels sit beside the mark and stay small.

5. Four documents were scoring different things (illustration-qa, beat prompts, engine QA, Creative Studio). A plate could "pass" one and fail the work Stewart was looking at.

## What changed after this note

The generated mascot is withdrawn. Diagrams use a tight rim instead of the milk halo, the ladder sits on the open grid, and step cards carry a small mark so they are not empty. Those plates are re-scored in `skills/image-quality-standard/test-outputs/SCORES.md`. They are not declared a pass in this file.
