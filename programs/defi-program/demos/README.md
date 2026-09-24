# Screen demos

Each `<id>.json` here is a demo spec: the steps to click through and the shots to take for a
`cutaway` scene. Capture with:

```bash
cd ../export
node capture_demo.js ../demos/<id>.json
```

Output: screenshots in `assets/demos/<id>/`, and `<id>.scene.json` here, a ready-made
`cutaway` scene with highlight and blur boxes measured. Full guide:
`.claude/skills/screen-demo-cutaways/SKILL.md`.

Logged-in or wallet-connected screens are captured by the owner on a testnet or practice
account (the tool never logs in or connects a wallet), then saved into `assets/demos/<id>/`.

| Demo | Shows | Used in |
|---|---|---|
| `course-hub-tour` | Course Hub navigation and search | Welcome / Lesson 0.0 |
