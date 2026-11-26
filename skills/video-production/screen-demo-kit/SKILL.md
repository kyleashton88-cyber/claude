---
name: screen-demo-kit
description: Blur secrets on a screen still and fail a check if any remain. Use after a screen recording or a captured demo shot, before that frame is allowed into a lesson. Covers API keys, wallet addresses, balances, and account numbers, plus manual blur boxes.
---

# Screen demo kit

`programs/defi-program/export/capture_demo.js` still grabs the shots. This kit is the blur and the check that follows.

It looks for an API-key shape, a 0x wallet address, a balance figure, and an account number. It also blurs any rectangle you pass. Then it reads the picture again. If a sensitive pattern is still readable, the check fails.

```bash
cd skills/video-production/screen-demo-kit
python3 cli.py blur --image in.png --out out.png --box 40,40,200,40
python3 cli.py qa --image out.png
```

The demo draws a fake screen. It does not open a live account and it does not publish the still.
