---
name: market-check-clip
description: Turn a daily Market Check post into a 60 to 90 second 16:9 lesson and a vertical clip under 60 seconds. Use when a Market Check write-up should become a narrated video. Kokoro af_heart, the house mix, captions, and the quality gate. Does not post or fetch live posts.
---

# Market Check clip

Reads a markdown post and the Market Check lesson shape. Writes a `lesson.yaml`, builds it with `skills/production-pipeline`, and checks the master with the quality gate format `market-check` (60–90 seconds, 1920×1080). A second command cuts a 9:16 clip under 60 seconds from the first chapter.

Narration is Kokoro `af_heart`. The mix is `lib/mix.py`. Figures in the post need the word EXAMPLE. The spoken line and the end card carry "education" and "not financial advice".

```bash
cd skills/video-production/market-check-clip
python3 cli.py build fixtures/sample-post.md --out test-outputs/demo
python3 cli.py vertical --master test-outputs/demo/master.mp4 --chapters test-outputs/demo/chapters.txt --vtt test-outputs/demo/captions.vtt --out test-outputs/demo/vertical.mp4
```

This does not fetch a live post, and it does not publish the files.
