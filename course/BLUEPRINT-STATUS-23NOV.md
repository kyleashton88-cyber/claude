# Blueprint status, 23 Nov 2026

BP-01 v14 and BP-02 are rendered. Their reviews are still open. This note covers BP-03 to BP-11 only. No spoken line was changed while writing it.

Estimated minutes use the finished-film pace of the two new renders, about 165 words a minute at Kokoro af_heart speed 1.0. The render gate still requires 1,600 to 2,400 spoken words, which is the 10 to 15 minute window at 160 words a minute.

The stills count has two sources. `course/images/FALLBACK_MANIFEST.json` marks the older picture folders. The render gate uses `blueprint-image-qa/BP01-03_PASS_LIST.json` and only that file. A folder can be marked pass in the fallback manifest and still fail the render gate.

| Lesson | Words | Est. minutes | In the 10–15 min window | Stills the render uses | Folder PNGs / fallback pass | Blueprint pass list | Blocking gap |
|---|---:|---:|---|---:|---|---|---|
| BP-03 What is a grid bot | 1,229 | 7.4 | No | 13 | 19 / 19 pass | 28 rows, all marked pass, but 11 no longer match the files the render would use | Script is short. Three code-drawn charts are missing from the pass list, and five scored files have a different blob than the file on disk. |
| BP-04 Market regimes | 1,185 | 7.2 | No | 11 | 20 / 20 pass | None | Script is short. No Blueprint pass list. The render gate rejects the shared title art and mascot because they are scored only under BP-01. |
| BP-05 Spacing and range | 1,216 | 7.4 | No | 10 | 19 / 19 pass | None | Same as BP-04. Five code-drawn charts are not on a pass list. |
| BP-06 Entry and exit | 1,228 | 7.4 | No | 12 | 20 / 20 pass | None | Script is short. One lesson still and six code-drawn charts are not on a pass list. |
| BP-07 Spot paper trading | 1,114 | 6.8 | No | 13 | 20 / 20 pass | None | Shortest script of the set. The list analogy, one lesson still, and six charts are not on a pass list. |
| BP-08 Managing and monitoring | 1,193 | 7.2 | No | 11 | 20 / 20 pass | None | Script is short. Six code-drawn charts are not on a pass list. |
| BP-09 Common mistakes | 1,154 | 7.0 | No | 12 | 21 / 21 pass | None | Script is short. Seven code-drawn charts are not on a pass list. |
| BP-10 Scaling up | 1,548 | 9.4 | No | 14 | 21 / 21 pass | None | Closest to the word floor, still about 50 words short. The buckets analogy, two lesson stills, and six charts are not on a pass list. |
| BP-11 Advanced liquidation | 1,257 | 7.6 | No | 12 | 20 / 20 pass | None | Script is short. The buckets analogy and six charts are not on a pass list. It also depends on the spot page from the earlier lessons. |

## Render order

1. BP-03, after the script is brought into the 10 to 15 minute window and Creative Studio re-scores the charts and the two lesson stills the gate names.
2. BP-04, BP-05, BP-06, then BP-07. These are the next lessons in the course, and each needs a lengthened script plus a new pass-list row for every image the gate uses.
3. BP-08, then BP-09.
4. BP-10, then BP-11. BP-10 is the second measured page. BP-11 is the optional liquidation lesson and should follow the spot lessons it refers to.

Do not render any of these until that lesson's script is in the word window and its pass list matches the files on disk.
