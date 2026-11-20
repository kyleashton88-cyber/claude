# BP-01 review

Source reviewed: `course/masters-stills/bp-01-introduction.mp4` (the PR #9 / #15 stills master).

Probe: 1920×1080, H.264 High, 30 fps, 24:23 (1463.5 s), AAC LC stereo 48 kHz at about 194 kbps. Frames taken every 10 seconds (146 frames) plus a direct look at the open, the hook, the disclaimer, a summer-stop hold, the worked example, and the outro. OCR on all 146 frames. `silencedetect` at −36 dBFS. `freezedetect` at 8 seconds.

## What is weak

Layout. The open is a left-aligned text card, "GRID BOT BLUEPRINT" set in Inter, with the right two-thirds of the frame empty. There is no Grid Bot Builder wordmark, no mascot, and the lesson line is repeated in the caption bar. The chapter name sits in the top-left and is clipped ("Hook" is cut by the frame). On the range chart the high label collides with the card edge and cannot be read. At 7:20 the chart card is almost empty: a short squiggle sits in the upper left and the rest of the card is blank.

Typography. The caption line is a readable sentence. Axis tags and the footer are small, and the footer's grey line is soft enough that OCR reads it as broken words. The disclaimer’s second and third lines are dim grey on navy. Nothing on the content frames is a lower-third term with a plain definition. The minimum useful size is missed on labels and on the footer.

Pacing. The disclaimer card arrives after the hook and the objectives (about 1:10), not as the opening card. From roughly 4:30 through 20:00 the picture is the same summer chart and the caption is "Say it back" plus a date. That is one idea held for a quarter of an hour. The worked example near 23:10 is the clearest card in the film, and it lasts a moment.

Frozen frames. `freezedetect` at 8 seconds reports no hold, because the background grid drifts. The teaching picture does not. A drift that exists to beat the detector is not a new idea.

Clutter. Two dots ride the line (a white playhead and an amber scanner). Dashed levels are mostly unlabelled. Title and caption repeat the same sentence on the open and on the outro. "Say it back" is not a teaching line.

Text overflow. The chapter word is cut at the top edge. The high price on the range chart runs into the card border. The playhead tag sits on the line.

Audio. Pauses fall through −36 dBFS: 10:18 for 0.73 s, 12:52 for 0.92 s, 18:02 for 0.66 s. There is no bed you can hear when the voice stops. The encode is 194 kbps, not 320 kbps. Early sample peaks in the first two seconds reached about −3.5 dBFS, hotter than a −1 dBTP ceiling wants before limiting. Integrated loudness sits near −16 LUFS while the voice is running, which is the one number already in range.

Music. Not a calm bed. The gaps are bare. Nothing rises on the open or the close, and nothing fades.

Names and sign-off. OCR of all 146 frames found no Market Pros, no Stewart, no Crown, no ABN, ACN, or AFSL, and no email address. The failure is the missing brand art and the missing risk line, not a leaked company name. The outro is only the next lesson title. There is no spoken sign-off in the burned-in text.

## Current scores

| Area | Score | Why |
| --- | --- | --- |
| Layout | 4 | Empty title card, clipped chapter, high price in the border, blank chart card at the stops |
| Typography | 5 | Caption is fine; labels, footer, and disclaimer body are small or grey |
| Pacing | 3 | Disclaimer is late; a quarter hour of "say it back" on one chart |
| Frozen frames | 4 | Pixels drift; the lesson does not |
| Clutter | 4 | Twin dots, unlabelled rules, repeated title and caption |
| Text overflow | 3 | Chapter clipped; 30,331 collides with the card |
| Audio | 5 | Near −16 LUFS under voice; bare pauses; 194 kbps; hot sample peaks |
| Music | 2 | No audible bed, no fade, silence in the pauses |

Bar for the rebuild: every area at least 8 before the final encode.

## Checklist for the rebuild

- [ ] Open on the Grid Bot Builder wordmark and the visor mascot, with lesson number and title
- [ ] Disclaimer card, full sentence, on screen at least 5 seconds, read aloud: "Education only. Not financial advice. Trading involves risk; you can lose money."
- [ ] No company name, company number, email, or sign-off on screen or in the narration
- [ ] Original pad bed, faded in and out, about −28 to −30 LUFS under the voice
- [ ] Master about −16 LUFS integrated, true peak at or under −1 dBTP, AAC 320 kbps, 48 kHz
- [ ] Title bar, one idea, type at least 36 px, lower-third term plus a plain definition
- [ ] Charts labelled, EXAMPLE badge wherever a number appears, safe margins
- [ ] Short dissolves, no empty chart card, no "say it back" loop

## Rebuilt cut

File: `course/blueprint-rebuild/masters/bp-01-introduction.mp4`. 6:15. 1920×1080 H.264 High, CRF 17. AAC 48 kHz stereo (encoder set to 320 kbps; measured average 282 kbps on this quiet mix). Integrated −16.0 LUFS, true peak −1.4 dBTP. No silence below −36 dBFS. `freezedetect` at 7.5 seconds: none.

The open uses the committed Grid Bot Builder wordmark and the visor mascot. The disclaimer card is the next shot, the exact three lines, still on screen at 0:12 and gone by 0:20, and it is read aloud. The summer walk is six dated stops plus one full-path draw, not the "say it back" loop. Charts keep the high, the low, and the rungs labelled, with an EXAMPLE badge. A lower third names the term. The bed is an original pad, faded, with no melody.

OCR of the open, the disclaimer, a chart, a dated stop, and the recap found no company name, number, or email.

| Area | Score | Why |
| --- | --- | --- |
| Layout | 9 | Wordmark, mascot, title bar, one chart, lower third, safe margins |
| Typography | 8 | Body and labels at 36 px or larger; the wordmark in the bar is the art, not a caption |
| Pacing | 8 | 6:15. Disclaimer first. The path draws. Six stops, not a quarter hour of one chart |
| Frozen frames | 8 | No hold over 7.5 seconds. The line draws and a slow glow keeps a held card alive |
| Clutter | 8 | One playhead. Rails are labelled. No second title over the picture |
| Text overflow | 8 | Margin ink is clear. The date tag sits next to the playhead, inside the plot |
| Audio | 8 | −16.0 LUFS, −1.4 dBTP, no bare pauses. Average AAC lands at 282 kbps |
| Music | 8 | Original pad, no hook, faded in and out, about −29 LUFS under the voice |
