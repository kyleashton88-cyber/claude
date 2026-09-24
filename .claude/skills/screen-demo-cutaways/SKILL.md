---
name: screen-demo-cutaways
description: Capture real app screens (wallets, exchanges, DeFi apps, block explorers, Pionex, the Course Hub) as step-by-step screenshots with highlight boxes and blurred private details, and turn them into cutaway scenes for course videos. Use when a lesson needs to show "click here, then here", an implementation walkthrough, a tool tour, or when asked for screen recordings, demos or B-roll.
---

# Screen Demo Cutaways

The "do it" part of a lesson must show the real screen. This skill captures it as a
sequence of screenshots (one per action) and produces a `cutaway` scene. The renderer
crossfades between shots, dims everything except a highlight box, pushes in towards it
and shows a "Step N" caption, all in time with the voice.

Screenshots beat raw screen recordings here: they're deterministic, easy to redo when
an app changes its UI, the zoom and highlight are exact, and there's no cursor wobble
or loading spinner.

## 1. Plan the shots

One shot per action or per thing to read. For each: the page, the element to highlight,
the caption (3 to 8 words, starting with a verb: "Open", "Find", "Set", "Confirm"), and
anything to blur.

## 2. Write a demo spec

`programs/defi-program/demos/<id>.json`:

```json
{
  "id": "course-hub-tour",
  "chapter": "Do it",
  "label": "On screen: the Course Hub",
  "showUrl": "course-hub / index.html",
  "url": "file:../course-hub/index.html",
  "viewport": [1600, 900],
  "steps": [
    { "shot": "01", "caption": "Pick your stage and module on the left", "highlight": "#tree" },
    { "click": "#q", "type": ["#q", "health factor"], "wait": 500 },
    { "shot": "02", "caption": "Search any topic across all 107 lessons", "highlight": "#q", "blur": [".account"] }
  ],
  "vo": "Here's the Course Hub. Pick your stage and module from the menu on the left. Then search any topic across all one hundred and seven lessons."
}
```

Step actions run in order: `goto`, `click`, `hover`, `type: [selector, text]`, `scroll` (px),
`wait` (ms), then `shot`. Selectors are Playwright selectors (`#id`, `.class`, `text=Borrow`,
`role=button[name="Supply"]`). `file:` URLs are relative to the spec file.

## 3. Capture

```bash
cd programs/defi-program/export
node capture_demo.js ../demos/course-hub-tour.json
```

Writes `assets/demos/<id>/NN.png` and `demos/<id>.scene.json`, a ready `cutaway` scene
with the highlight and blur boxes already measured. Paste it into the lesson script
and rewrite the `vo` to follow the shots (one sentence per shot, naming what's highlighted).

## Apps that need a login or a wallet

The capture tool runs a clean browser with no wallet and no logins, and it will refuse to
type into password, seed or private-key fields. For logged-in or wallet-connected screens:

1. The owner takes the screenshots on their own machine (1600×900 browser window, or crop to 16:9) using a **testnet or practice account with a tiny balance**.
2. Save them as `assets/demos/<id>/01.png`, `02.png`...
3. Write the `cutaway` scene by hand: estimate each `box` as fractions of the image (`[x, y, w, h]`), and add `blur` boxes over addresses, balances, emails, order IDs and QR codes.

Claude never logs into accounts, connects wallets, or handles keys to make a demo.

## Privacy and safety checklist (every shot)

- No seed phrase, private key, password, 2FA code or recovery QR code, ever. Not even a fake one that looks real.
- Wallet addresses, emails, account numbers, balances and order IDs blurred unless they're test values.
- Testnet, paper trading or a tiny practice amount. Say so in the voice ("I'm on testnet here").
- Third-party apps: show the UI as it is; don't imply endorsement or partnership. Link the official URL in the lesson page, never a referral link unless disclosed.
- Date the demo in the script's `use` field ("UI captured 2026-09-24"). App UIs change; re-capture when they do.

## Screen recordings (optional)

If a motion clip is truly needed (e.g. a live order book), record it with the OS recorder
at 1920×1080, and cut it into the final MP4 with ffmpeg after rendering; the renderer
itself works from still frames. Prefer a sequence of screenshots whenever possible.
