# QA report: course video renders

Probed 4 Nov 2026 with ffprobe, a 250 ms audio-floor check, and frames at 1.2 s, mid-roll, and 6 s before the end.

The bar for this pass: 15–20 minutes, navy and cyan, branded intro and outro, a music bed, one ChatGPT still per beat, no code-drawn diagrams. Elite stays teal and was not restyled.

## On-Chain Operator lessons

These files are `programs/defi-program/video/lesson-*.mp4`. Speech rate on the renders is about 143 words a minute. A 15 minute lesson needs about 2,150 words; these scripts are about 1,300–1,570 words, and lesson 3.2 is 984.

| Video | Duration | Intro | Outro | Music | ChatGPT stills | Repeated stills | Code-drawn visuals | Palette | Result |
|---|---:|---|---|---|---:|---|---|---|---|
| `lesson-01-1` | 10:10 (610s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 27 HTML scenes plus 2 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-2` | 10:06 (606s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 1 repeated asset paths) | yes, 27 HTML scenes plus 2 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-3` | 10:10 (610s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 1 repeated asset paths) | yes, 27 HTML scenes plus 2 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-4` | 10:12 (612s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 2 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-5` | 10:10 (610s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 28 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-6` | 10:25 (625s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 2 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-7` | 10:17 (617s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 29 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-8` | 10:06 (606s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 27 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-01-9` | 10:13 (613s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 28 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-0` | 9:57 (597s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 25 HTML scenes plus 4 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-1` | 9:35 (575s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 27 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-2` | 10:05 (605s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 2 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-3` | 9:42 (582s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 25 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-4` | 9:57 (597s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-5` | 9:47 (587s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 27 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-6` | 9:28 (568s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-7` | 10:41 (641s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 27 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-02-8` | 10:06 (606s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-03-0` | 10:17 (617s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 5 code-rendered PNGs | navy + teal accent | fail |
| `lesson-03-1` | 10:03 (603s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 25 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-03-2` | 6:40 (400s) | title card only | CTA card only | no | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 16 HTML scenes plus 2 code-rendered PNGs | navy + teal accent | fail |
| `lesson-03-3` | 9:58 (598s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-03-4` | 10:01 (601s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 26 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |
| `lesson-03-5` | 9:18 (558s) | title card only | CTA card only | yes | 0 | n/a (no ChatGPT stills; 0 repeated asset paths) | yes, 27 HTML scenes plus 1 code-rendered PNGs | navy + teal accent | fail |

Lesson 3.2 is the short one: 6:40, and the quiet tenth of the audio sits at −82 dB, so there is no music bed. The other 23 lessons have a generated pad (quiet tenth around −37 to −40 dB) but they are still 9:18–10:41.

Frame samples: the open of lesson 3.2 and lesson 1.1 is a typeset title card (module kicker, giant number, teal-to-blue gradient type) on a navy starfield. Mid-roll is a numbered card or a bullet, with a burnt-in caption. The close is the program wordmark and a Next button. Those frames are drawn by `programs/defi-program/export/build_video.js` and `build_images.js`. They are not ChatGPT stills.

## Grid Bot Blueprint masters

There is no `course/masters/` tree in this repository, and commit `bdbc357` is not in the history. Five short masters were found as unnamed files in the bot store and probed. The other six (bp-05, bp-07, bp-08, bp-09, bp-10, bp-11) were not on disk as mp4s. Still counts are the PNG folders. The long-form beat sheet assigns only 12–21 of 45–49 beats to an existing file and marks the rest `new_image`, so a 17 minute cut cannot be built without reuse or new art.

| Video | Duration | Intro | Outro | Music | Stills on disk | Beats in the long sheet | Beats pointed at an existing file | Code-drawn visuals | Palette | Result |
|---|---:|---|---|---|---:|---:|---:|---|---|---|
| `bp-01-introduction` | 2:52 (172s) | no branded bumper; opens on the hook still | next-lesson card, text collides | yes | 45 | 47 | 18 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-02-what-you-need` | 2:18 (138s) | no branded bumper; opens on the hook still | next-lesson card, text collides | yes | 47 | 47 | 14 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-03-what-is-a-grid-bot` | 2:23 (143s) | no branded bumper; opens on the hook still | next-lesson card, text collides | yes | 48 | 48 | 14 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-04-market-regimes` | 2:21 (141s) | no branded bumper; opens on the hook still | next-lesson card, text collides | yes | 46 | 47 | 15 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-05-spacing-and-range` | no mp4 in the repo | not probed | not probed | not probed | 48 | 49 | 19 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-06-entry-and-exit` | 2:11 (131s) | no branded bumper; opens on the hook still | next-lesson card, text collides | yes | 45 | 46 | 14 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-07-spot-paper-trading` | no mp4 in the repo | not probed | not probed | not probed | 47 | 46 | 14 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-08-managing-and-monitoring` | no mp4 in the repo | not probed | not probed | not probed | 43 | 45 | 13 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-09-common-mistakes` | no mp4 in the repo | not probed | not probed | not probed | 46 | 47 | 12 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-10-scaling-up` | no mp4 in the repo | not probed | not probed | not probed | 43 | 46 | 15 | captions and cards only; pictures are stills | navy + cyan | fail |
| `bp-11-advanced-liquidation` | no mp4 in the repo | not probed | not probed | not probed | 46 | 47 | 21 | captions and cards only; pictures are stills | navy + cyan | fail |

The probed Blueprint shorts are 2:11–2:53. bp-01's open frame is a real range diagram, which is the right kind of picture, but the caption bar covers the character and the lower labels. The end frame stacks the next-lesson title, the spoken disclaimer, and the character on top of each other. A 2:53 file cannot give 45 stills their own beat.

Stewart's note matches the folder count: bp-01 has 45 stills. The long sheet has more beats than assigned files, so later beats would reuse or sit blank. The stills that do exist are often thin (a card, a grey line, a generic checklist) relative to the sentence they are meant to teach.

## What failed, in one list

1. Every On-Chain Operator lesson in scope is under 15 minutes. Lesson 3.2 is 6:40.

2. Lesson 3.2 has no music bed. The other Operator lessons have a generated pad, not the licensed bed used for Blueprint.

3. Operator opens are code-drawn title cards, not a hook followed by a branded image intro. Closes are code-drawn CTA cards.

4. Operator visuals are HTML and code-rendered PNGs. ChatGPT still count is 0. Accent colour is teal (`#2ee6a6`), not the cyan this pass asks for.

5. Blueprint masters that could be probed are about two and a half minutes. Six masters are not in the repo at all.

6. Blueprint long-form beats outnumber the files assigned to them. bp-01's 45 stills cannot cover a 17 minute beat sheet without reuse.

7. Existing Blueprint stills are not illustrative enough for a sound-off tutorial, and captions collide with the art.

8. Elite was not part of the fail list and was not restyled.

## Corrected scripts

New scripts are in `course/scripts/`. Each is 16.7–17.8 minutes at 143 words a minute, with hook, disclaimer, intro, demo, recap, action, and outro. `IMAGE_REQUESTS.json` has one unique prompt per beat (1,296 stills). No PNG has been generated in this step. `course/render/render_tutorial.py --check` reports all 35 lessons blocked on those files, and it will not reuse a still or draw a replacement.

Nothing was uploaded to Whop, and no lesson visibility was changed.

