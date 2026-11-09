# How to use AI with the Slack channel

Staff walkthrough for Audience Asset Co / Market Pros.

| | |
| --- | --- |
| Video | `ops/slack-ai-howto/out/how-to-use-ai-with-slack.mp4` |
| Length | 2:59 (179.26 seconds), 1920×1080, 30 fps |
| Audio | Clara voiceover reused from `audio/clara-vo.mp3` (2:19). Short holds were added so each click can be read. Integrated loudness measured at −17.2 LUFS. |
| Captions | `ops/slack-ai-howto/out/how-to-use-ai-with-slack.vtt` |
| QA notes | `ops/slack-ai-howto/QA.md` |

Nothing was posted to Slack.

## What the video teaches

Open Slack, find Channels, open `#all-audience-asset-co` (or `#staff-chat` for a smaller note), type `@` and choose Orchestrator Bot, write one ask with who / what / by when, keep follow-ups in the thread, and read the reply there.

The walkthrough uses two threads that were already in `#all-audience-asset-co`:

- Jess’s remaining-tasks ask, `1794230823.008249`, and the Orchestrator replies in that thread
- The Lea Power Session ask, `1794230545.108409`

The composer shot is a draft. The send button on that frame says it was not posted.

## Stills

`shots/S01_title.png` and `shots/S09_recap.png` came from the Creative Studio handoff.

`shots/S02`–`S08` (plus `S08b_followup.png`) were drawn from that live thread text. This environment’s browser hits the Audience Asset Co sign-in wall (`capture-notes/signin-wall.png`), so these are not a logged-in screen recording. Email addresses from the threads are left off the frames.

Rebuild the stills and the mp4:

```bash
NODE_PATH=programs/defi-program/export/node_modules node ops/slack-ai-howto/capture_shots.js
python3 ops/slack-ai-howto/assemble.py
```
