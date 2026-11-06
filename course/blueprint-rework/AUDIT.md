# Blueprint master audit

Scope: the eleven Grid Bot Blueprint masters in `course/masters/bp-01` through `bp-11`. Elite files were not opened.

## Standards this audit used

Professional e-learning edits, applied to a 1080p online lesson, are:

- A branded ident opens the lesson and a branded outro closes it. The ident carries the course and the lesson title. The outro carries a recap, the next lesson, and the education-only line. Music is allowed to rise on those two cards and should sit under the voice everywhere else.
- The lesson arc is hook, objective, sections, check, recap, next step. The objective uses a doing verb. The recap is three lines, not a repeat of the section.
- Pictures change with the narration. A still may hold while a callout steps, but a frozen frame past about 20 seconds fails pacing. Mayer's signalling rule: the thing being said is the thing that changes on screen. One diagram can stay up, but it cannot sit unchanged through a dozen sentences.
- On-screen text is a key point, in complete phrases, at a size you can read on a phone. It does not cover the diagram, and a chapter label does not sit on top of the illustration's own title. About seven words on a line is the comfortable maximum.
- Music is a licence-safe bed, ducked under the voice (about −20 to −24 LUFS in the pauses) and present for the whole lesson, including the pauses. Two beds do not play at once.
- Online-video loudness is about −16 LUFS integrated, true peak at or under −1.5 dBTP, AAC, 48 kHz. A flat loudness range under about 3 LU means the bed and the pauses are missing.
- A/V sync: picture changes land on the words they belong to. A boundary error past one frame (about 40 ms) is a sync error. Drift is that error growing through the lesson. Dead air is a gap at or over 1 second with nothing under it. A hard cut with no fade is acceptable between ideas; it is not acceptable as the only transition in a 16 minute slideshow.
- No exchange or brand name on a picture or a burned-in caption. Education only. No income claim.

## How it was measured

- `ffprobe` for codec, 1920×1080, 30 fps, BT.709, AAC channel layout, sample rate, and stream durations.
- `ffmpeg` `silencedetect` at −36 dBFS, minimum 0.45 s, for dead air.
- `ffmpeg` `ebur128=peak=true` on the audio stream alone, for integrated loudness, loudness range, and true peak. A first combined filter mis-read the summary line; the numbers below are from this dedicated pass.
- `ffmpeg` scene detect at a score of 0.12, which on these slideshows is one cut per still. Holds between cuts were checked against a 20 second pacing limit. `freezedetect` on bp-01 confirmed each hold is a pixel-frozen frame, not a slow move.
- Picture boundaries were compared with the script timeline the renderer uses (143 words per minute, intro floor 5.5 s, legal floor 12 s, outro floor 8 s, then rounded to frames). That difference is the per-section sync offset.
- One frame per section, 0.4 s after the cut, was OCR'd with Tesseract on the title band and the caption band. Four lessons were also looked at directly: bp-01, bp-02, bp-07, and bp-11.

## What is true of every lesson

| Lesson | Duration | LUFS | LRA | True peak | Sample rate | Holds over 20 s |
|---|---:|---:|---:|---:|---:|---:|
| `bp-01-introduction` | 16:53 | -16.3 | 2.5 LU | -1.2 dBFS | 96 kHz mono | 16 |
| `bp-02-what-you-need` | 17:37 | -16.3 | 2.5 LU | -1.1 dBFS | 96 kHz mono | 18 |
| `bp-03-what-is-a-grid-bot` | 16:47 | -16.3 | 2.5 LU | -1.2 dBFS | 96 kHz mono | 17 |
| `bp-04-market-regimes` | 17:00 | -16.4 | 2.6 LU | -1.2 dBFS | 96 kHz mono | 18 |
| `bp-05-spacing-and-range` | 16:42 | -16.3 | 2.5 LU | -1.2 dBFS | 96 kHz mono | 17 |
| `bp-06-entry-and-exit` | 16:42 | -16.4 | 2.6 LU | -1.2 dBFS | 96 kHz mono | 18 |
| `bp-07-spot-paper-trading` | 17:26 | -16.4 | 2.6 LU | -1.2 dBFS | 96 kHz mono | 18 |
| `bp-08-managing-and-monitoring` | 16:39 | -16.4 | 2.6 LU | -1.2 dBFS | 96 kHz mono | 18 |
| `bp-09-common-mistakes` | 17:16 | -16.4 | 2.5 LU | -1.2 dBFS | 96 kHz mono | 19 |
| `bp-10-scaling-up` | 16:55 | -16.3 | 2.5 LU | -1.2 dBFS | 96 kHz mono | 19 |
| `bp-11-advanced-liquidation` | 17:07 | -16.3 | 2.6 LU | -1.2 dBFS | 96 kHz mono | 16 |

Shared problems, so they are not repeated as if they were surprises in each lesson:

- Integrated loudness is already about −16.3 LUFS and true peak is about −1.2 dBFS. The loudness target is met. The mix is still wrong: loudness range is 2.5 to 2.6 LU, which is a wall of voice.
- There is no usable music bed. The only pauses fall through −36 dBFS, so the CC0 Komiku beds in `course/music/` are not in the mix. Nothing rises on the ident or the outro, because there is no ident and no bed.
- Audio is AAC mono at 96 kHz, about 196 kbps. Online delivery is 48 kHz. Video and audio start together and end together (timeline delta 0.0 s on every file), so the container is not drifting. The failure is inside the section, where the still never moves.
- Every picture change is a one-frame hard cut. There is no fade.
- The lesson does not open on a branded ident. It opens on the hook still, which then holds for about a minute. A title card exists as a later still, and the word "Title card" is drawn through that still's own headline.
- There is no learning-objectives card in any lesson.
- The burned-in "caption" is the start of the narration, cut at about 100 characters, almost always mid-sentence. It sits on top of the diagram. The chapter name is drawn at the top left, through the illustration title. Confirmed by looking at frames, not only by OCR: bp-01 at 0:00 ("Hook" through SIDEWAYS), 1:09 ("Disclaimer" through EDUCATION), 7:13 ("We do not run it" through NO ORDER), and 16:42 ("Outro" through NEXT); bp-02 at 0:01 ("Hook" through PAGE); bp-07 at 1:35 ("Title card" through SPOT); bp-11 at 4:40 ("Isolated" through the headline).
- Fourteen sections in every lesson end with the same spoken tail: "Say the opening line once more... The point of the beat is the pointing." That is dead teaching time, and it is why each still is held for 45 to 72 seconds.
- No separate caption track. The only text is the burned-in line.
- Resolution, frame rate, and H.264 High / BT.709 are fine: 1920×1080, 30 fps, progressive.

## Per lesson

### bp-01-introduction

Title: Introduction. Duration 16:53. Next on the script card: What you are going to need.
Loudness -16.3 LUFS, range 2.5 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 2:33 (0.69 s), 5:08 (0.59 s), 10:18 (0.73 s).
- Hard cuts, one frame, no fade: 1:09, 1:31, 1:42, 2:50, 3:52, 4:57, 6:06, 7:13, 8:24, 9:33, 10:40, 11:39, 12:45, 13:44, 14:47, 15:38, 16:42.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 1:09 | 69 s | 0.0 s | hook | Hook | frozen 69 s; caption cut: Price often chops sideways, weaving through the same band instead o...; spoken pointing tail; The still is one chart titled SIDEWAYS BAND, but the path leaves the band and steps down. The narration's first sentence is the weave; the exit is a later sentence. Both are on screen from 0:00, and the caption ends "A grid is a ladder of limit."; opens on the hook still, not a branded ident |
| 1:09 | 1:31 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:31 | 1:42 | 11 s | 0.0 s | intro | Title card | caption cut: This is the Grid Bot Blueprint. The lesson is Introduction. Navy an...; title card is a content still; chapter label reads Title card |
| 1:42 | 2:50 | 68 s | 0.0 s | body | The three parts | frozen 68 s; caption cut: A grid has three parts you can name: the range, the levels, and the...; spoken pointing tail |
| 2:50 | 3:52 | 63 s | 0.0 s | body | The range | frozen 63 s; caption cut: The range is a top and a bottom you draw before any rung. Without a...; spoken pointing tail |
| 3:52 | 4:57 | 64 s | 0.0 s | body | The levels | frozen 64 s; caption cut: The levels are limit orders that wait on the rungs. A limit order s...; spoken pointing tail |
| 4:57 | 6:06 | 70 s | 0.0 s | diagram | Buys and sells | frozen 70 s; caption cut: One approach places buy orders below the mark and sell orders above...; spoken pointing tail |
| 6:06 | 7:13 | 66 s | 0.0 s | body | The stop | frozen 66 s; caption cut: The stop is a sentence you write, not a feeling that the trade is o...; spoken pointing tail |
| 7:13 | 8:24 | 71 s | 0.0 s | body | We do not run it | frozen 71 s; caption cut: We do not sell or run a trading bot. No order is sent from this les...; spoken pointing tail; Narration tells the viewer to look for a notebook and a blank form. The still is a crossed send icon reading NO ORDER / NOT SENT. The caption covers NOT SENT. |
| 8:24 | 9:33 | 69 s | 0.0 s | map | The map | frozen 69 s; caption cut: The course is a map, and this introduction is only the first square...; spoken pointing tail |
| 9:33 | 10:40 | 68 s | 0.0 s | body | When the drawing fails | frozen 68 s; caption cut: Draw a path that leaves the top of the band and does not return. Th...; spoken pointing tail |
| 10:40 | 11:39 | 58 s | 0.0 s | body | No result number | frozen 58 s; caption cut: There is no result number in this lesson. A result number would pre...; spoken pointing tail |
| 11:39 | 12:45 | 66 s | 0.0 s | demo | Eight ticks | frozen 66 s; caption cut: A slow sketch uses eight even ticks inside the band, only as a way ...; spoken pointing tail |
| 12:45 | 13:44 | 59 s | 0.0 s | action | The checklist is next | frozen 59 s; caption cut: The next step is the setup checklist, on paper, before any screen. ...; spoken pointing tail |
| 13:44 | 14:47 | 63 s | 0.0 s | demo | Paper first | frozen 63 s; caption cut: A paper or demo account is a fence around practice. Inside the fenc...; spoken pointing tail |
| 14:47 | 15:38 | 51 s | 0.0 s | demo | Your turn | frozen 51 s; caption cut: Your turn, still inside The three parts. Cover the notes and say th... |
| 15:38 | 16:42 | 64 s | 0.0 s | recap | One sentence to keep | frozen 64 s; spoken pointing tail; This is the recap, and it is 64 seconds of the pointing template rather than three lines. |
| 16:42 | 16:53 | 10 s | 0.0 s | outro | Outro | hard cut only |

Objectives card: missing. Branded outro: the last still is an outro role (16:42) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-02-what-you-need

Title: What you are going to need. Duration 17:37. Next on the script card: What is a grid bot.
Loudness -16.3 LUFS, range 2.5 LU, true peak -1.1 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air (gap at or over 1 s, floor below −36 dBFS, no music under it): 7:43 for 1.40 s.
- Bare pauses under 1 s: 2:35 (0.58 s), 10:18 (0.58 s), 12:53 (0.54 s).
- Hard cuts, one frame, no fade: 0:56, 1:18, 1:31, 2:34, 3:34, 4:37, 5:36, 6:41, 7:42, 8:42, 9:39, 10:38, 11:36, 12:40, 13:40, 14:32, 15:17, 16:07, 16:26, 17:27.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 0:56 | 56 s | 0.0 s | hook | Hook | frozen 56 s; caption cut: You need a page before you need a screen. People lose the lesson wh...; spoken pointing tail; opens on the hook still, not a branded ident |
| 0:56 | 1:18 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:18 | 1:31 | 13 s | 0.0 s | intro | Title card | title card is a content still; chapter label reads Title card |
| 1:31 | 2:34 | 64 s | 0.0 s | body | Seven items | frozen 64 s; caption cut: The setup check has seven lines: notebook, the three words, pair na...; spoken pointing tail |
| 2:34 | 3:34 | 60 s | 0.0 s | body | The three words | frozen 60 s; caption cut: The three words are range, levels, and stop, carried forward from t...; spoken pointing tail |
| 3:34 | 4:37 | 63 s | 0.0 s | body | Pair name | frozen 63 s; caption cut: A pair name is two assets written with a slash, such as the base an...; spoken pointing tail |
| 4:37 | 5:36 | 59 s | 0.0 s | body | Paper or demo | frozen 59 s; caption cut: The screen, when you reach it, is paper or demo. Paper lets you see...; spoken pointing tail |
| 5:36 | 6:41 | 64 s | 0.0 s | body | No secrets | frozen 64 s; caption cut: You never type a seed phrase, a private key, or an API secret into ...; spoken pointing tail |
| 6:41 | 7:42 | 62 s | 0.0 s | body | Written stop | frozen 62 s; caption cut: The stop line on the checklist is a sentence, not a tick. The sente...; spoken pointing tail |
| 7:42 | 8:42 | 59 s | 0.0 s | body | The word Example | frozen 59 s; caption cut: Every number and every pair on the page carries the word Example. T...; spoken pointing tail |
| 8:42 | 9:39 | 57 s | 0.0 s | body | Not on the list | frozen 57 s; caption cut: A profit target is not on the list. A leverage multiple is not on t...; spoken pointing tail |
| 9:39 | 10:38 | 59 s | 0.0 s | diagram | The form copies the page | frozen 59 s; caption cut: A later button, on paper, is only a copy of the page. If the page i...; spoken pointing tail |
| 10:38 | 11:36 | 59 s | 0.0 s | map | You are early | frozen 59 s; caption cut: You are early in the course. The definition, the regime, and the sp...; spoken pointing tail |
| 11:36 | 12:40 | 63 s | 0.0 s | demo | Empty pair | frozen 63 s; caption cut: Look at the pair row and imagine it empty on purpose. The rest of t...; spoken pointing tail |
| 12:40 | 13:40 | 60 s | 0.0 s | body | Common miss | frozen 60 s; caption cut: The common miss is to skip the list and open the screen. The screen...; spoken pointing tail |
| 13:40 | 14:32 | 52 s | 0.0 s | demo | Your turn | frozen 52 s; caption cut: Your turn, still inside Seven items. Cover the notes and say this f... |
| 14:32 | 15:17 | 45 s | 0.0 s | demo | Your turn | frozen 45 s; caption cut: Your turn, still inside The three words. Cover the notes and say th... |
| 15:17 | 16:07 | 50 s | 0.0 s | demo | Your turn | frozen 50 s; caption cut: Your turn, still inside Pair name. Cover the notes and say this fro... |
| 16:07 | 16:26 | 18 s | 0.0 s | recap | Recap | caption cut: Recap for What you are going to need. Say the hook in one line, nam...; The recap is 18 seconds and is not the close. A 61 second action still follows it. |
| 16:26 | 17:27 | 61 s | 0.0 s | action | Finish the seven | frozen 61 s; caption cut: The action is to complete the seven lines on paper today. Read each...; spoken pointing tail |
| 17:27 | 17:37 | 10 s | 0.0 s | outro | Outro | caption cut: Next lesson: What is a grid bot. Bring the page you just wrote. Lea... |

Objectives card: missing. Branded outro: the last still is an outro role (17:27) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-03-what-is-a-grid-bot

Title: What is a grid bot. Duration 16:47. Next on the script card: Market regimes.
Loudness -16.3 LUFS, range 2.5 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 5:08 (0.76 s), 15:27 (0.61 s).
- Hard cuts, one frame, no fade: 1:08, 1:29, 1:42, 2:46, 3:49, 4:59, 6:00, 7:02, 8:03, 9:04, 10:04, 11:02, 11:57, 13:02, 14:00, 14:47, 15:35, 16:39.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 1:08 | 68 s | 0.0 s | hook | Hook | frozen 68 s; spoken pointing tail; opens on the hook still, not a branded ident |
| 1:08 | 1:29 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:29 | 1:42 | 13 s | 0.0 s | intro | Title card | title card is a content still; chapter label reads Title card |
| 1:42 | 2:46 | 64 s | 0.0 s | body | Five labels | frozen 64 s; caption cut: Five labels cover the picture: upper, lower, levels, side, and stop...; spoken pointing tail |
| 2:46 | 3:49 | 63 s | 0.0 s | body | Limit orders wait | frozen 63 s; caption cut: Limit orders wait at a price. They do not jump the queue. A market ...; spoken pointing tail |
| 3:49 | 4:59 | 70 s | 0.0 s | diagram | Price steps down | frozen 70 s; caption cut: When price steps down through a rung, a buy limit that was waiting ...; spoken pointing tail |
| 4:59 | 6:00 | 60 s | 0.0 s | diagram | Price steps up | frozen 60 s; caption cut: When price steps up through a rung, a sell limit that was waiting t...; spoken pointing tail |
| 6:00 | 7:02 | 62 s | 0.0 s | body | Inventory | frozen 62 s; caption cut: Inventory is what you hold when the fills are uneven. If price leav...; spoken pointing tail |
| 7:02 | 8:03 | 61 s | 0.0 s | body | The bot's job | frozen 61 s; caption cut: The bot's job, if you use one, is to keep the written rungs in the ...; spoken pointing tail |
| 8:03 | 9:04 | 61 s | 0.0 s | demo | Say the five | frozen 61 s; caption cut: Say the five labels while you point: upper, lower, levels, side, st...; spoken pointing tail |
| 9:04 | 10:04 | 60 s | 0.0 s | body | Hypothetical path | frozen 60 s; caption cut: The path on the diagram is hypothetical noise, drawn so you can see...; spoken pointing tail |
| 10:04 | 11:02 | 58 s | 0.0 s | body | Common miss | frozen 58 s; caption cut: A common miss is to describe the bot as earning while price chops. ...; spoken pointing tail |
| 11:02 | 11:57 | 55 s | 0.0 s | body | Not affiliated | frozen 55 s; caption cut: No exchange is a partner in this definition. The picture is generic...; spoken pointing tail |
| 11:57 | 13:02 | 65 s | 0.0 s | recap | One-breath definition | frozen 65 s; caption cut: In one breath: waiting limit orders, inside a band, with a written ...; spoken pointing tail |
| 13:02 | 14:00 | 58 s | 0.0 s | action | Paper check | frozen 58 s; caption cut: On paper, label a band with the five words and tell the step-down o...; spoken pointing tail |
| 14:00 | 14:47 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Five labels. Cover the notes and say this f... |
| 14:47 | 15:35 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Limit orders wait. Cover the notes and say ... |
| 15:35 | 16:39 | 63 s | 0.0 s | body | What the bot is not | frozen 63 s; caption cut: It is not a signal, not a fund, and not a person watching the marke...; spoken pointing tail |
| 16:39 | 16:47 | 9 s | 0.0 s | outro | Outro | caption cut: Next lesson: Market regimes. Bring the page you just wrote. Leave e... |

Objectives card: missing. Branded outro: the last still is an outro role (16:39) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-04-market-regimes

Title: Market regimes. Duration 17:00. Next on the script card: Choosing grid spacing and range.
Loudness -16.4 LUFS, range 2.6 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 7:44 (0.60 s), 12:52 (0.73 s), 15:28 (0.65 s).
- Hard cuts, one frame, no fade: 1:00, 1:22, 1:33, 2:32, 3:32, 4:32, 5:30, 6:33, 7:33, 8:35, 9:37, 10:40, 11:43, 12:39, 13:35, 14:19, 15:04, 15:52, 16:50.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 1:00 | 60 s | 0.0 s | hook | Hook | frozen 60 s; caption cut: The same ladder is a different idea in a different regime. A weave ...; spoken pointing tail; opens on the hook still, not a branded ident |
| 1:00 | 1:22 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:22 | 1:33 | 11 s | 0.0 s | intro | Title card | caption cut: This is the Grid Bot Blueprint. The lesson is Market regimes. Navy ...; title card is a content still; chapter label reads Title card |
| 1:33 | 2:32 | 59 s | 0.0 s | body | Three shapes | frozen 59 s; caption cut: Three shapes are enough for this lesson: range, trend, and break. R...; spoken pointing tail |
| 2:32 | 3:32 | 60 s | 0.0 s | body | Sort first | frozen 60 s; caption cut: You sort the path before you choose a spacing. Spacing a band you h...; spoken pointing tail |
| 3:32 | 4:32 | 60 s | 0.0 s | diagram | Range fit | frozen 60 s; caption cut: A range is the shape where a grid's waiting orders can be crossed m...; spoken pointing tail |
| 4:32 | 5:30 | 57 s | 0.0 s | body | Trend | frozen 57 s; caption cut: A trend on this page is a path that makes higher highs or lower low...; spoken pointing tail |
| 5:30 | 6:33 | 63 s | 0.0 s | body | Break | frozen 63 s; caption cut: A break leaves the band and does not return on the sketch. Orders l...; spoken pointing tail |
| 6:33 | 7:33 | 60 s | 0.0 s | demo | Worked sort | frozen 60 s; caption cut: Work one example path from left to right and give it one label. Say...; spoken pointing tail |
| 7:33 | 8:35 | 62 s | 0.0 s | body | What you do with the label | frozen 62 s; caption cut: The label decides whether the ladder is even the tool on the page. ...; spoken pointing tail |
| 8:35 | 9:37 | 63 s | 0.0 s | body | Ordinary day | frozen 63 s; caption cut: An ordinary day on this page means the size of weave you already dr...; spoken pointing tail |
| 9:37 | 10:40 | 63 s | 0.0 s | body | News and thin books | frozen 63 s; caption cut: A path into a major news bar, or a thin book, is a poor place to pr...; spoken pointing tail |
| 10:40 | 11:43 | 63 s | 0.0 s | body | Common miss | frozen 63 s; caption cut: The common miss is to pick the grid first and the regime second. Th...; spoken pointing tail |
| 11:43 | 12:39 | 55 s | 0.0 s | recap | One sentence | frozen 55 s; caption cut: The sentence to keep: name the shape, then decide whether a ladder ...; spoken pointing tail |
| 12:39 | 13:35 | 57 s | 0.0 s | action | Paper sort | frozen 57 s; caption cut: Sort one hypothetical path on paper into range, trend, or break, an...; spoken pointing tail |
| 13:35 | 14:19 | 44 s | 0.0 s | demo | Your turn | frozen 44 s; caption cut: Your turn, still inside Three shapes. Cover the notes and say this ... |
| 14:19 | 15:04 | 45 s | 0.0 s | demo | Your turn | frozen 45 s; caption cut: Your turn, still inside Sort first. Cover the notes and say this fr... |
| 15:04 | 15:52 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Range fit. Cover the notes and say this fro... |
| 15:52 | 16:50 | 58 s | 0.0 s | body | No score | frozen 58 s; caption cut: This lesson does not give you a score that says go. A score would h...; spoken pointing tail |
| 16:50 | 17:00 | 10 s | 0.0 s | outro | Outro | caption cut: Next lesson: Choosing grid spacing and range. Bring the page you ju... |

Objectives card: missing. Branded outro: the last still is an outro role (16:50) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-05-spacing-and-range

Title: Choosing grid spacing and range. Duration 16:42. Next on the script card: Entry and exit rules.
Loudness -16.3 LUFS, range 2.5 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is -0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 15:28 (0.60 s).
- Hard cuts, one frame, no fade: 1:01, 1:22, 1:35, 2:36, 3:45, 4:58, 5:57, 7:08, 8:08, 9:06, 10:07, 11:07, 12:03, 12:58, 13:58, 14:43, 15:36, 16:33.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 1:01 | 61 s | 0.0 s | hook | Hook | frozen 61 s; caption cut: A band that is too tight can break on an ordinary weave you already...; spoken pointing tail; opens on the hook still, not a branded ident |
| 1:01 | 1:22 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:22 | 1:35 | 13 s | 0.0 s | intro | Title card | title card is a content still; chapter label reads Title card |
| 1:35 | 2:36 | 61 s | 0.0 s | body | Gaps and orders | frozen 61 s; caption cut: Twenty order lines make nineteen gaps. You multiply the step by the...; spoken pointing tail |
| 2:36 | 3:45 | 69 s | 0.0 s | demo | The span | frozen 69 s; caption cut: Nineteen gaps times a half of one percent is a span of nine and a h...; spoken pointing tail |
| 3:45 | 4:58 | 73 s | 0.0 s | body | Half spacing | frozen 73 s; caption cut: Halving the step without recounting the gaps doubles the line count...; spoken pointing tail |
| 4:58 | 5:57 | 59 s | 0.0 s | body | Range first | frozen 59 s; caption cut: A spacing percent without a range is a number in the margin. The ra...; spoken pointing tail |
| 5:57 | 7:08 | 70 s | 0.0 s | body | Fees | frozen 70 s; caption cut: A gap smaller than the cost of a buy and a sell can be flat or nega...; spoken pointing tail |
| 7:08 | 8:08 | 60 s | 0.0 s | body | Too many lines | frozen 60 s; caption cut: More lines are not more thorough if each gap fails the cost check. ...; spoken pointing tail |
| 8:08 | 9:06 | 58 s | 0.0 s | demo | Worked recount | frozen 58 s; caption cut: Recount once from a wrong page: the wrong page says twenty times a ...; spoken pointing tail |
| 9:06 | 10:07 | 61 s | 0.0 s | body | Wicks | frozen 61 s; caption cut: A range needs room for the wicks you drew, not only for the closes....; spoken pointing tail |
| 10:07 | 11:07 | 60 s | 0.0 s | body | Common miss | frozen 60 s; caption cut: The common miss is to change the step and the range in the same edi...; spoken pointing tail |
| 11:07 | 12:03 | 56 s | 0.0 s | action | What you write | frozen 56 s; caption cut: The line you keep contains a percent, the word gaps, and the word o...; spoken pointing tail |
| 12:03 | 12:58 | 55 s | 0.0 s | body | Quiet page | frozen 55 s; caption cut: A quiet page shows the band, the gap count, and the cost check, and...; spoken pointing tail |
| 12:58 | 13:58 | 60 s | 0.0 s | recap | Recap | frozen 60 s; caption cut: Recap: range first, gaps not lines, nineteen gaps in the house exam...; spoken pointing tail |
| 13:58 | 14:43 | 44 s | 0.0 s | demo | Your turn | frozen 44 s; caption cut: Your turn, still inside Gaps and orders. Cover the notes and say th... |
| 14:43 | 15:36 | 53 s | 0.0 s | demo | Your turn | frozen 53 s; caption cut: Your turn, still inside The span. Cover the notes and say this from... |
| 15:36 | 16:33 | 57 s | 0.0 s | demo | Stay on paper | frozen 57 s; caption cut: Leave the recount on paper. Do not type it into a live ticket. The ...; spoken pointing tail |
| 16:33 | 16:42 | 10 s | 0.0 s | outro | Outro | caption cut: Next lesson: Entry and exit rules. Bring the page you just wrote. L... |

Objectives card: missing. Branded outro: the last still is an outro role (16:33) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-06-entry-and-exit

Title: Entry and exit rules. Duration 16:42. Next on the script card: Spot paper trading.
Loudness -16.4 LUFS, range 2.6 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air (gap at or over 1 s, floor below −36 dBFS, no music under it): 10:18 for 1.02 s.
- Bare pauses under 1 s: 5:08 (0.67 s), 12:52 (0.67 s).
- Hard cuts, one frame, no fade: 1:00, 1:21, 1:33, 2:28, 3:26, 4:31, 5:34, 6:36, 7:34, 8:32, 9:29, 10:27, 11:22, 12:17, 13:12, 13:57, 14:42, 15:33, 16:31.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 1:00 | 60 s | 0.0 s | hook | Hook | frozen 60 s; caption cut: Entry without an exit is a page that cannot finish. The exit is the...; spoken pointing tail; opens on the hook still, not a branded ident |
| 1:00 | 1:21 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:21 | 1:33 | 12 s | 0.0 s | intro | Title card | caption cut: This is the Grid Bot Blueprint. The lesson is Entry and exit rules....; title card is a content still; chapter label reads Title card |
| 1:33 | 2:28 | 55 s | 0.0 s | body | Two columns | frozen 55 s; caption cut: The page has two columns: what must be true before you would start,...; spoken pointing tail |
| 2:28 | 3:26 | 58 s | 0.0 s | body | Stop first | frozen 58 s; spoken pointing tail |
| 3:26 | 4:31 | 65 s | 0.0 s | demo | A finish sentence | frozen 65 s; caption cut: A finish sentence names a path: price leaves the band and does not ...; spoken pointing tail |
| 4:31 | 5:34 | 63 s | 0.0 s | body | A before sentence | frozen 63 s; caption cut: A before sentence names the sort: the path you drew is a range, the...; spoken pointing tail |
| 5:34 | 6:36 | 62 s | 0.0 s | demo | Worked columns | frozen 62 s; caption cut: Read a worked pair of sentences aloud and point at the drawing that...; spoken pointing tail |
| 6:36 | 7:34 | 59 s | 0.0 s | body | What hope is not | frozen 59 s; caption cut: Hope is not an entry rule. A wish that the weave continues is not a...; spoken pointing tail |
| 7:34 | 8:32 | 58 s | 0.0 s | body | Invalidation | frozen 58 s; caption cut: Invalidation is the name for the finish path. When that path is on ...; spoken pointing tail |
| 8:32 | 9:29 | 57 s | 0.0 s | body | Common miss | frozen 57 s; caption cut: The common miss is a stop that cites a feeling: I will know. A late...; spoken pointing tail |
| 9:29 | 10:27 | 57 s | 0.0 s | body | Copy order | frozen 57 s; caption cut: If a paper form comes later, you copy the finish sentence before th...; spoken pointing tail |
| 10:27 | 11:22 | 55 s | 0.0 s | body | No size yet | frozen 55 s; spoken pointing tail |
| 11:22 | 12:17 | 55 s | 0.0 s | action | The action | frozen 55 s; caption cut: Write both sentences today, finish first, and read them to the draw...; spoken pointing tail |
| 12:17 | 13:12 | 55 s | 0.0 s | recap | Recap | frozen 55 s; caption cut: Recap: two columns, finish first, sentences that point, hope crosse...; spoken pointing tail |
| 13:12 | 13:57 | 45 s | 0.0 s | demo | Your turn | frozen 45 s; caption cut: Your turn, still inside Two columns. Cover the notes and say this f... |
| 13:57 | 14:42 | 45 s | 0.0 s | demo | Your turn | frozen 45 s |
| 14:42 | 15:33 | 51 s | 0.0 s | demo | Your turn | frozen 51 s; caption cut: Your turn, still inside A finish sentence. Cover the notes and say ... |
| 15:33 | 16:31 | 59 s | 0.0 s | demo | Audit | frozen 59 s; caption cut: Audit one page by asking: can a classmate point at the finish path ...; spoken pointing tail |
| 16:31 | 16:42 | 10 s | 0.0 s | outro | Outro | caption cut: Next lesson: Spot paper trading. Bring the page you just wro...; the venue on the burned-in caption; The burned-in caption names the venue. |

Objectives card: missing. Branded outro: the last still is an outro role (16:31) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-07-spot-paper-trading

Title: Spot paper trading. Duration 17:26. Next on the script card: Managing and monitoring.
Loudness -16.4 LUFS, range 2.6 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 5:08 (0.56 s).
- Hard cuts, one frame, no fade: 1:02, 1:34, 1:46, 2:50, 3:55, 4:58, 5:55, 6:53, 7:52, 8:56, 9:58, 10:58, 11:58, 12:58, 13:49, 14:37, 15:27, 16:15, 17:17.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 1:02 | 62 s | 0.0 s | hook | Hook | frozen 62 s; caption cut: This lesson walks fields on a paper or demo spot screen. It does no...; spoken pointing tail; opens on the hook still, not a branded ident |
| 1:02 | 1:34 | 31 s | 0.0 s | legal | Disclaimer | frozen 31 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:34 | 1:46 | 13 s | 0.0 s | intro | Title card | the venue on the burned-in caption; The burned-in caption names the venue. The illustration itself says SPOT PAPER.; title card is a content still; chapter label reads Title card |
| 1:46 | 2:50 | 63 s | 0.0 s | body | Not affiliated | frozen 63 s; caption cut: the venue is a name you may see on a venue. This course is not affiliat...; spoken pointing tail; the venue on the burned-in caption; The burned-in caption names the venue twice. |
| 2:50 | 3:55 | 66 s | 0.0 s | body | Fields from the page | frozen 66 s; caption cut: The fields you are allowed to copy are the ones you already wrote: ...; spoken pointing tail |
| 3:55 | 4:58 | 62 s | 0.0 s | body | Spot, not a contract | frozen 62 s; caption cut: The path is spot. A contract with leverage is a different product a...; spoken pointing tail |
| 4:58 | 5:55 | 58 s | 0.0 s | body | Keys | frozen 58 s; caption cut: You do not paste an API key, a seed phrase, or a password into a co...; spoken pointing tail |
| 5:55 | 6:53 | 57 s | 0.0 s | demo | Walk the pair | frozen 57 s; caption cut: Walk the pair field first. Read your Example pair aloud and point a...; spoken pointing tail |
| 6:53 | 7:52 | 60 s | 0.0 s | demo | Walk the band | frozen 60 s; caption cut: Walk upper, then lower. Read the numbers from the page, including t...; spoken pointing tail |
| 7:52 | 8:56 | 63 s | 0.0 s | demo | Walk the count | frozen 63 s; caption cut: Walk the gap count, not the line count, if the form's word is ambig...; spoken pointing tail |
| 8:56 | 9:58 | 63 s | 0.0 s | demo | Walk the sentences | frozen 63 s; caption cut: There may be no field for your finish sentence. You still read it b...; spoken pointing tail |
| 9:58 | 10:58 | 59 s | 0.0 s | body | Common miss | frozen 59 s; caption cut: The common miss is to treat a default the form already filled as if...; spoken pointing tail |
| 10:58 | 11:58 | 60 s | 0.0 s | body | No order | frozen 60 s; spoken pointing tail |
| 11:58 | 12:58 | 60 s | 0.0 s | action | The action | frozen 60 s; caption cut: On a paper or demo spot screen, match five fields to the page and s...; spoken pointing tail |
| 12:58 | 13:49 | 51 s | 0.0 s | recap | Recap | frozen 51 s; caption cut: Recap: paper spot, page wins, translate the count, ignore defaults,...; spoken pointing tail |
| 13:49 | 14:37 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Not affiliated. Cover the notes and say thi...; the venue on the burned-in caption; The first of the three Your turn stills puts the venue in the burned-in caption. |
| 14:37 | 15:27 | 50 s | 0.0 s | demo | Your turn | frozen 50 s; caption cut: Your turn, still inside Fields from the page. Cover the notes and s...; The first of the three Your turn stills puts the venue in the burned-in caption. |
| 15:27 | 16:15 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Spot, not a contract. Cover the notes and s...; The first of the three Your turn stills puts the venue in the burned-in caption. |
| 16:15 | 17:17 | 63 s | 0.0 s | body | If the screen differs | frozen 63 s; caption cut: Venue screens move. If a label differs, you translate it onto your ...; spoken pointing tail |
| 17:17 | 17:26 | 9 s | 0.0 s | outro | Outro | caption cut: Next lesson: Managing and monitoring. Bring the page you just wrote... |

Objectives card: missing. Branded outro: the last still is an outro role (17:17) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-08-managing-and-monitoring

Title: Managing and monitoring. Duration 16:39. Next on the script card: Common mistakes.
Loudness -16.4 LUFS, range 2.6 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 2:33 (0.62 s), 7:44 (0.64 s).
- Hard cuts, one frame, no fade: 0:58, 1:20, 1:31, 2:32, 3:35, 4:32, 5:35, 6:34, 7:34, 8:37, 9:36, 10:32, 11:26, 12:22, 13:13, 13:58, 14:46, 15:31, 16:31.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 0:58 | 58 s | 0.0 s | hook | Hook | frozen 58 s; caption cut: Monitoring is a short list you can finish, not a vigil. A vigil pre...; spoken pointing tail; opens on the hook still, not a branded ident |
| 0:58 | 1:20 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:20 | 1:31 | 12 s | 0.0 s | intro | Title card | caption cut: This is the Grid Bot Blueprint. The lesson is Managing and monitori...; title card is a content still; chapter label reads Title card |
| 1:31 | 2:32 | 60 s | 0.0 s | body | Three questions | frozen 60 s; caption cut: The questions are: is the example path inside the band, which side ...; spoken pointing tail |
| 2:32 | 3:35 | 63 s | 0.0 s | diagram | Inside the band | frozen 63 s; caption cut: Inside means the path you are looking at still crosses the band you...; spoken pointing tail |
| 3:35 | 4:32 | 57 s | 0.0 s | body | Which side | frozen 57 s; caption cut: Side means which asset you hold more of after the example fills. If...; spoken pointing tail |
| 4:32 | 5:35 | 63 s | 0.0 s | body | The sentence | frozen 63 s; caption cut: The third row is a reread of the finish sentence, not a new sentenc...; spoken pointing tail |
| 5:35 | 6:34 | 59 s | 0.0 s | body | Cadence | frozen 59 s; caption cut: A cadence is a day you choose to reread the same three rows. The le...; spoken pointing tail |
| 6:34 | 7:34 | 61 s | 0.0 s | body | What you do not open | frozen 61 s; caption cut: You do not open a result chart, a ranking, or a leverage control as...; spoken pointing tail |
| 7:34 | 8:37 | 63 s | 0.0 s | demo | Worked check | frozen 63 s; caption cut: Run the three rows on a hypothetical path that starts inside and en...; spoken pointing tail |
| 8:37 | 9:36 | 59 s | 0.0 s | body | Alerts | frozen 59 s; caption cut: An alert, if you ever set one, is a nudge to come read the three ro...; spoken pointing tail |
| 9:36 | 10:32 | 56 s | 0.0 s | body | Common miss | frozen 56 s; caption cut: The common miss is to add a result row to the card. The result row ...; spoken pointing tail |
| 10:32 | 11:26 | 54 s | 0.0 s | body | After the check | frozen 54 s; caption cut: After the three answers, you stop or you write an edit. You do not ...; spoken pointing tail |
| 11:26 | 12:22 | 56 s | 0.0 s | action | The action | frozen 56 s; caption cut: Build the three-row card on paper and run it once on a path you dra...; spoken pointing tail |
| 12:22 | 13:13 | 51 s | 0.0 s | recap | Recap | frozen 51 s; caption cut: Recap: inside, side, sentence, a cadence you chose, no result row, ...; spoken pointing tail |
| 13:13 | 13:58 | 46 s | 0.0 s | demo | Your turn | frozen 46 s; caption cut: Your turn, still inside Three questions. Cover the notes and say th... |
| 13:58 | 14:46 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Inside the band. Cover the notes and say th... |
| 14:46 | 15:31 | 44 s | 0.0 s | demo | Your turn | frozen 44 s; caption cut: Your turn, still inside Which side. Cover the notes and say this fr... |
| 15:31 | 16:31 | 60 s | 0.0 s | body | Paper screen optional | frozen 60 s; caption cut: If you completed the paper walk, you may point the three rows at th...; spoken pointing tail |
| 16:31 | 16:39 | 9 s | 0.0 s | outro | Outro | caption cut: Next lesson: Common mistakes. Bring the page you just wrote. Leave ... |

Objectives card: missing. Branded outro: the last still is an outro role (16:31) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-09-common-mistakes

Title: Common mistakes. Duration 17:16. Next on the script card: Scaling up on spot.
Loudness -16.4 LUFS, range 2.5 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 2:34 (0.66 s), 10:19 (0.54 s), 12:53 (0.67 s).
- Hard cuts, one frame, no fade: 0:56, 1:17, 1:29, 2:31, 3:33, 4:35, 5:36, 6:31, 7:29, 8:32, 9:24, 10:19, 11:19, 12:14, 13:06, 13:53, 14:42, 15:28, 16:13, 17:06.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 0:56 | 56 s | 0.0 s | hook | Hook | frozen 56 s; caption cut: The mistakes in this lesson are pages, not personalities. A blank s...; spoken pointing tail; opens on the hook still, not a branded ident |
| 0:56 | 1:17 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:17 | 1:29 | 11 s | 0.0 s | intro | Title card | title card is a content still; chapter label reads Title card |
| 1:29 | 2:31 | 63 s | 0.0 s | body | Blank stop | frozen 63 s; caption cut: A blank stop means the finish column was skipped. Every later copy ...; spoken pointing tail |
| 2:31 | 3:33 | 62 s | 0.0 s | body | Tight band | frozen 62 s; caption cut: A tight band is a band shorter than the weave you drew for an ordin...; spoken pointing tail |
| 3:33 | 4:35 | 62 s | 0.0 s | body | Ending early | frozen 62 s; caption cut: Ending the course at the mistakes page skips scaling and the opt-in...; spoken pointing tail |
| 4:35 | 5:36 | 61 s | 0.0 s | body | Counting lines | frozen 61 s; caption cut: Counting lines as gaps is the spacing miss, and it shows up again h...; spoken pointing tail |
| 5:36 | 6:31 | 55 s | 0.0 s | body | Default size | frozen 55 s; caption cut: A default size on a form is the form's idea. The mistake is to keep...; spoken pointing tail |
| 6:31 | 7:29 | 59 s | 0.0 s | body | Result language | frozen 59 s; caption cut: A promise of income, or a claim that a result cannot fail, is a mis...; spoken pointing tail |
| 7:29 | 8:32 | 63 s | 0.0 s | demo | Worked audit | frozen 63 s; caption cut: Audit a sample page that has a blank stop and a ten percent span on...; spoken pointing tail |
| 8:32 | 9:24 | 51 s | 0.0 s | body | One fix at a time | frozen 51 s; caption cut: Fix one miss, then reread, then fix the next. Fixing the band and t...; spoken pointing tail |
| 9:24 | 10:19 | 55 s | 0.0 s | body | Not a score | frozen 55 s; caption cut: The audit does not produce a grade you can trade. It produces a lis...; spoken pointing tail |
| 10:19 | 11:19 | 60 s | 0.0 s | body | Leverage mention | frozen 60 s; caption cut: If a page has picked up a leverage multiple, that multiple is a mis...; spoken pointing tail |
| 11:19 | 12:14 | 55 s | 0.0 s | action | The action | frozen 55 s; caption cut: Audit your own notebook for a blank stop, a tight band, and a missi...; spoken pointing tail |
| 12:14 | 13:06 | 51 s | 0.0 s | recap | Recap | frozen 51 s; caption cut: Recap: blank stop, tight band, early ending, line-count mixup, defa...; spoken pointing tail |
| 13:06 | 13:53 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Blank stop. Cover the notes and say this fr... |
| 13:53 | 14:42 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside Tight band. Cover the notes and say this fr... |
| 14:42 | 15:28 | 46 s | 0.0 s | demo | Your turn | frozen 46 s; caption cut: Your turn, still inside Ending early. Cover the notes and say this ... |
| 15:28 | 16:13 | 45 s | 0.0 s | demo | Your turn | frozen 45 s; caption cut: Your turn, still inside Counting lines. Cover the notes and say thi... |
| 16:13 | 17:06 | 53 s | 0.0 s | demo | Keep the pages | frozen 53 s; caption cut: Keep the marked-up pages. The marks are the lesson. A clean copy th...; spoken pointing tail |
| 17:06 | 17:16 | 10 s | 0.0 s | outro | Outro | caption cut: Next lesson: Scaling up on spot. Bring the page you just wrote. Lea... |

Objectives card: missing. Branded outro: the last still is an outro role (17:06) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-10-scaling-up

Title: Scaling up on spot. Duration 16:55. Next on the script card: Advanced: liquidation scenarios.
Loudness -16.3 LUFS, range 2.5 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is -0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 2:34 (0.65 s), 15:27 (0.57 s).
- Hard cuts, one frame, no fade: 0:55, 1:16, 1:29, 2:26, 3:27, 4:25, 5:19, 6:18, 7:13, 8:07, 9:07, 10:04, 11:04, 11:59, 12:57, 13:42, 14:26, 15:13, 15:53, 16:45.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 0:55 | 55 s | 0.0 s | hook | Hook | frozen 55 s; caption cut: Scaling on this page means a second written page, not a bigger numb...; spoken pointing tail; opens on the hook still, not a branded ident |
| 0:55 | 1:16 | 21 s | 0.0 s | legal | Disclaimer | frozen 21 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:16 | 1:29 | 12 s | 0.0 s | intro | Title card | title card is a content still; chapter label reads Title card |
| 1:29 | 2:26 | 58 s | 0.0 s | body | A second page | frozen 58 s; caption cut: The second page repeats the gates: regime sort, range, gaps, finish...; spoken pointing tail |
| 2:26 | 3:27 | 60 s | 0.0 s | body | Buckets | frozen 60 s; caption cut: Two grids on one asset can fight if they share inventory. A bucket ...; spoken pointing tail |
| 3:27 | 4:25 | 58 s | 0.0 s | body | Same size is allowed | frozen 58 s; caption cut: A review that keeps the size the same is a complete review. Scaling...; spoken pointing tail |
| 4:25 | 5:19 | 54 s | 0.0 s | body | One change | frozen 54 s; caption cut: Change one thing between page one and page two. If you change the p...; spoken pointing tail |
| 5:19 | 6:18 | 59 s | 0.0 s | demo | Worked pair | frozen 59 s; caption cut: Work an example where page two uses the same band and a different p...; spoken pointing tail |
| 6:18 | 7:13 | 55 s | 0.0 s | body | Not the end | frozen 55 s; caption cut: Scaling is not the end of the course. An opt-in lesson on liquidati...; spoken pointing tail |
| 7:13 | 8:07 | 53 s | 0.0 s | body | Spot only | frozen 53 s; caption cut: The second page is still spot. Scaling by adding leverage is a diff...; spoken pointing tail |
| 8:07 | 9:07 | 60 s | 0.0 s | body | Capital is not a target | frozen 60 s; caption cut: The page does not tell you how much money to assign. A blank size t...; spoken pointing tail |
| 9:07 | 10:04 | 57 s | 0.0 s | body | Common miss | frozen 57 s; caption cut: The common miss is to double a count because the first page felt fi...; spoken pointing tail |
| 10:04 | 11:04 | 60 s | 0.0 s | body | Correlation | frozen 60 s; caption cut: Two pairs that move together can fill the same way at the same time...; spoken pointing tail |
| 11:04 | 11:59 | 55 s | 0.0 s | action | The line | frozen 55 s; caption cut: The line to write: page two passes the same gates, or it does not e...; spoken pointing tail |
| 11:59 | 12:57 | 58 s | 0.0 s | recap | Recap | frozen 58 s; caption cut: Recap: second page, same gates, buckets, one change, spot, size not...; spoken pointing tail |
| 12:57 | 13:42 | 45 s | 0.0 s | demo | Your turn | frozen 45 s; caption cut: Your turn, still inside A second page. Cover the notes and say this... |
| 13:42 | 14:26 | 44 s | 0.0 s | demo | Your turn | frozen 44 s; caption cut: Your turn, still inside Buckets. Cover the notes and say this from ... |
| 14:26 | 15:13 | 47 s | 0.0 s | demo | Your turn | frozen 47 s; caption cut: Your turn, still inside Same size is allowed. Cover the notes and s... |
| 15:13 | 15:53 | 41 s | 0.0 s | demo | Your turn | frozen 41 s; caption cut: Your turn, still inside One change. Cover the notes and say this fr... |
| 15:53 | 16:45 | 52 s | 0.0 s | demo | File them | frozen 52 s; caption cut: File page one and page two together only if both passed. If page tw...; spoken pointing tail |
| 16:45 | 16:55 | 9 s | 0.0 s | outro | Outro | caption cut: Next lesson: Advanced: liquidation scenarios. Bring the page you ju... |

Objectives card: missing. Branded outro: the last still is an outro role (16:45) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

### bp-11-advanced-liquidation

Title: Advanced: liquidation scenarios. Duration 17:07. Next on the script card: None.
Loudness -16.3 LUFS, range 2.6 LU, true peak -1.2 dBFS. Section-boundary sync versus the 143 wpm plan is 0.0 s wherever a cut exists. Video duration minus the scripted picture timeline is 0.0 s.

- Dead air at or over 1 s: none. The shorter pauses below are still bare, with no bed under them.
- Bare pauses under 1 s: 15:27 (0.65 s).
- Hard cuts, one frame, no fade: 1:01, 1:30, 1:42, 2:38, 3:41, 4:40, 6:43, 8:44, 9:50, 10:52, 11:48, 12:47, 13:43, 14:27, 15:15, 16:01, 16:58.
- Frozen frame on every hold below. The picture does not change inside the hold, so each later sentence is visually late by the time since the cut.

| In | Out | Hold | Sync | Role | Chapter | Problem on this still |
|---:|---:|---:|---:|---|---|---|
| 0:00 | 1:01 | 61 s | 0.0 s | hook | Hook | frozen 61 s; caption cut: This lesson is opt-in. The losing path comes first. A leveraged pos...; spoken pointing tail; opens on the hook still, not a branded ident |
| 1:01 | 1:30 | 29 s | 0.0 s | legal | Disclaimer | frozen 29 s; caption cut: Education only, not financial advice. Crypto and DeFi carry signifi... |
| 1:30 | 1:42 | 12 s | 0.0 s | intro | Title card | title card is a content still; chapter label reads Title card |
| 1:42 | 2:38 | 56 s | 0.0 s | body | Spot is complete | frozen 56 s; caption cut: The paper spot path is already complete without this lesson. Nothin...; spoken pointing tail |
| 2:38 | 3:41 | 63 s | 0.0 s | body | What liquidation means | frozen 63 s; caption cut: Liquidation here means the venue closes the position because the ma...; spoken pointing tail |
| 3:41 | 4:40 | 59 s | 0.0 s | diagram | Losing path | frozen 59 s; spoken pointing tail |
| 4:40 | 5:39 | 123 s | 0.0 s | body | Isolated | frozen 123 s; caption cut: Isolated margin, in plain words, means the venue looks at the inven...; spoken pointing tail |
| 5:39 | 6:43 | 123 s | change is 63 s late | body | Cross | frozen 123 s; caption cut: Cross margin, in plain words, means the venue may look at other bal...; spoken pointing tail; No picture change at 5:39. The Isolated still stays up for the whole Cross narration, until 6:43. |
| 6:43 | 7:40 | 122 s | 0.0 s | body | No multiple | frozen 122 s; caption cut: Do not write a times-number in either box. A times-number is what p...; spoken pointing tail |
| 7:40 | 8:44 | 122 s | change is 64 s late | body | Funding | frozen 122 s; caption cut: Contracts can also carry a funding payment between sides, on a time...; spoken pointing tail; No picture change at 7:40. The previous still stays up for the whole Funding narration, until 8:44. |
| 8:44 | 9:50 | 66 s | 0.0 s | body | What was deleted | frozen 66 s; caption cut: Older drafts of this lesson that gave a leverage multiple, or a mul...; spoken pointing tail |
| 9:50 | 10:52 | 61 s | 0.0 s | body | Flags | frozen 61 s; spoken pointing tail |
| 10:52 | 11:48 | 56 s | 0.0 s | body | Not a venue guide | frozen 56 s; spoken pointing tail |
| 11:48 | 12:47 | 60 s | 0.0 s | action | The sentence | frozen 60 s; spoken pointing tail |
| 12:47 | 13:43 | 56 s | 0.0 s | recap | Recap | frozen 56 s; caption cut: Recap: opt-in, loss first, isolated fence, cross can pull, no multi...; spoken pointing tail |
| 13:43 | 14:27 | 44 s | 0.0 s | demo | Your turn | frozen 44 s; caption cut: Your turn, still inside Spot is complete. Cover the notes and say t... |
| 14:27 | 15:15 | 48 s | 0.0 s | demo | Your turn | frozen 48 s; caption cut: Your turn, still inside What liquidation means. Cover the notes and... |
| 15:15 | 16:01 | 47 s | 0.0 s | demo | Your turn | frozen 47 s; caption cut: Your turn, still inside Losing path. Cover the notes and say this f... |
| 16:01 | 16:58 | 57 s | 0.0 s | body | If you skip | frozen 57 s; caption cut: If you skip this lesson, write Skipped on purpose on the spot noteb...; spoken pointing tail |
| 16:58 | 17:07 | 9 s | 0.0 s | outro | Outro | caption cut: This is the last Blueprint lesson. The spot path stands without thi... |

Objectives card: missing. Branded outro: the last still is an outro role (16:58) but it is the same slideshow card, with the chapter word through the headline, and no music lift.

