---
name: illustration-qa
description: Check course video stills and renders against the tutorial bar. Use before accepting a lesson render, after new ChatGPT images land, or when a review says pictures are thin, reused, code-drawn, or off-brand.
---

# Illustration QA checklist

Run this on a script and, once the PNGs exist, on the frames. A fail blocks the render. Do not restyle Elite; this checklist's navy-and-cyan items apply to On-Chain Operator and Grid Bot Blueprint only.

## Script, before any image

- Duration comes from `skills/video-production/quality-gate` profiles. Blueprint is about 4 to 10 minutes. This checklist does not apply a separate minute floor.
- Roles present: hook, legal, intro, demo, recap, action, outro.
- One image path per beat. No path is repeated.
- Each prompt names the shapes for that beat's sentence and is longer than a caption.
- No prompt asks for a blank page, grey placeholder bars, coins, a profit figure, or a real login.
- Spoken text has no "guaranteed", "risk-free", or promised income.
- Blueprint spacing beats say nineteen gaps, not twenty, for the house example.

## Still, after ChatGPT returns it

- The still shows the concept with the sound off. Cover the caption and ask what is being taught.
- It is not a thin icon on an empty card, and it is not the same composition as the neighbouring beat.
- Labels that appear are spelled correctly and there are only a few of them.
- The bottom fifth is quiet enough for a caption.
- Palette is navy and cyan. Teal-on-navy is the old On-Chain Operator render, not this pass. Elite teal is left alone.
- No exchange logo, no seed phrase, no API key, no result number presented as a win.

## Render

- `ffprobe` duration is checked by the quality gate for that lesson's format. This checklist does not use a 900 to 1,200 second window.
- The first frames are the hook, not a logo sting. A branded intro follows the hook.
- The last frames are the outro, with the next lesson or "last lesson", and the disclaimer is readable.
- A music bed is present. It is not the only thing you hear once a voice track exists.
- Captions do not cover the diagram's labels.
- Code did not draw the picture. If the frame is HTML cards, charts from `build_images.js`, or a flow of divs, it fails this pass.

## Command

`python3 course/render/render_tutorial.py --check` lists every lesson still missing PNGs. Do not upload anything to Whop from this check.
