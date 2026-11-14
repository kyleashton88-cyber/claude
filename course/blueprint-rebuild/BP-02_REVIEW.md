# BP-02 review

Source reviewed: `course/masters-stills/bp-02-what-you-need.mp4`.

Probe: 1920×1080, H.264 High, 21:55 (1315.4 s), AAC LC stereo 48 kHz at about 194 kbps. Frames at 0:00, 0:15, 0:45, 1:30, 3:00, 6:40, 11:40, 16:40, and 20:50. `freezedetect` at 8 seconds found no hold. One pause under −36 dBFS, at about 10:18 for 0.74 s. Integrated −16.2 LUFS, loudness range 2.1 LU, true peak −1.3 dBFS.

## What is weak

Layout. The open is a text card, "GRID BOT" only, with the rest of the frame empty. The chapter word is clipped at the top left. There is no Grid Bot Builder wordmark and no mascot. By 0:15 the lesson is already the packing-list still beside a chart, so the disclaimer is not the first card. At 6:40 the chart card is almost empty: a short squiggle sits in the upper left and the rails are far from the line.

Typography. The caption is a readable sentence. The footer is small and grey. There is no lower-third term with a plain definition. The date tag is smaller than 36 px.

Pacing. 21:55. The same summer chart carries long stretches of the lesson. The open does not hold the lesson title on screen with the brand art before the teaching starts.

Frozen frames. No 8-second pixel hold, because the grid drifts. At 6:40 the teaching picture is a nearly empty card. The drift is not a new idea.

Clutter. Twin dots on the line. Most dashed levels have no label. "ANALOGY" is stamped on the still, and the chapter name collides with the top edge.

Text overflow. The chapter is cut off at 0:00. The date tag sits on the line.

Audio. −16.2 LUFS and −1.3 dBTP are in range. The 0.74 s gap under −36 dBFS is bare. AAC is about 194 kbps.

Music. Not an audible bed. Nothing fades up on the open.

Names and sign-off. The frames that were read show no company name, no company number, and no email. The footer is the old education line, not the required risk sentence.

## Current scores

| Area | Score | Why |
| --- | --- | --- |
| Layout | 4 | Text-only open, clipped chapter, empty chart card at 6:40 |
| Typography | 5 | Caption is fine; footer and date tag are small |
| Pacing | 3 | 22 minutes, disclaimer not first, long holds on one chart |
| Frozen frames | 4 | Pixels drift; the picture at the stops does not teach |
| Clutter | 4 | Twin dots, unlabelled rules, chapter in the edge |
| Text overflow | 4 | Chapter clipped; tag sits on the path |
| Audio | 5 | Loudness is close; one bare pause; 194 kbps |
| Music | 2 | No bed you can hear in the pause |

Bar for the rebuild: every area at least 8 before the final encode.

## Checklist for the rebuild

- [ ] Open on the Grid Bot Builder wordmark and the visor mascot, with lesson 02 and the title
- [ ] Disclaimer card, full sentence, on screen at least 5 seconds, read aloud
- [ ] No company name, company number, email, or sign-off
- [ ] Original pad, faded, about −28 to −30 LUFS under the voice
- [ ] Master about −16 LUFS, true peak at or under −1 dBTP, AAC 320 kbps, 48 kHz
- [ ] Title bar, one idea, type at least 36 px, lower-third term plus a definition
- [ ] Charts labelled, EXAMPLE badge on numbers, safe margins
- [ ] No empty chart card

## Rebuilt cut

File: `course/blueprint-rebuild/masters/bp-02-what-you-need.mp4`. 4:43. 1920×1080 H.264 High, CRF 17. AAC 48 kHz stereo, encoder set to 320 kbps, measured average about 281 kbps. Integrated −16.0 LUFS, true peak −1.3 dBTP. No silence below −36 dBFS. `freezedetect` at 7.5 seconds: none.

The open shows the wordmark, the visor mascot, and "Lesson 02. What you are going to need." The disclaimer is on screen at 0:11 with the full risk sentence. The packing list sits beside a labelled chart. The worked check is four lines, each marked by the EXAMPLE badge. OCR of six frames found no company name, number, or email.

| Area | Score | Why |
| --- | --- | --- |
| Layout | 9 | Brand open, split analogy and chart, one worked card |
| Typography | 8 | Lesson title, rows, and the lower third are at 36 px or larger |
| Pacing | 8 | 4:43. Disclaimer first. The empty-card walk is gone |
| Frozen frames | 8 | No hold over 7.5 seconds |
| Clutter | 8 | One playhead, labelled rails, the list is the analogy |
| Text overflow | 8 | Chapter is inside the bar. The date tag stays in the plot |
| Audio | 8 | −16.0 LUFS, −1.3 dBTP, no bare pause |
| Music | 8 | Same original pad, faded, under the voice |
