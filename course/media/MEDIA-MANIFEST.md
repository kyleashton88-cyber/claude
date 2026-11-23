# Lesson media

Rendered masters, review copies, and segment renders are not committed to git and are not stored in Git LFS. Update this file after every render.

A full master is split into parts of at most 100 MiB. Join the parts in order:

```
cat master.mp4.part01 master.mp4.part02 master.mp4.part03 master.mp4.part04 > master.mp4
```

Omit part files that do not exist. The joined file must match the SHA-256 in this table.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-01 v14 | `988308edfcaaf7118f7bdcd66d627906b908bd6f` | `master.mp4` | 818.4s | 323322188 | `a97def59982ea495e562f7827c40d0bab47808bb91e7f7e2d1f39b58ced42713` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp01-a93b5d5/` |
| BP-01 v14 | `988308edfcaaf7118f7bdcd66d627906b908bd6f` | `master.mp4.part01` | | 104857600 | `7f4ad48a5b21d0eade3b73759354965f76774ffc9a5c8ee40136b11f999db415` | Same folder |
| BP-01 v14 | `988308edfcaaf7118f7bdcd66d627906b908bd6f` | `master.mp4.part02` | | 104857600 | `f2dd69885e3617577bf3433be5ed501fce1b161857ec57df4ebbe4b5d4b233a2` | Same folder |
| BP-01 v14 | `988308edfcaaf7118f7bdcd66d627906b908bd6f` | `master.mp4.part03` | | 104857600 | `13a7e1e845adf37f740f9f7813f0ff26586ed66460e79d40025ad5eceb2d7154` | Same folder |
| BP-01 v14 | `988308edfcaaf7118f7bdcd66d627906b908bd6f` | `master.mp4.part04` | | 8749388 | `fd162ed290f035d7839bcee536df1971e24fdb1131630439313d248114bd5309` | Same folder |
| BP-01 v14 review 720p | `988308edfcaaf7118f7bdcd66d627906b908bd6f` | `review-720p.mp4` | | | `4004a7ac38ac65edea67a21b00e77151ef264da31bb0d46e9a59a24d3d9c141f` | https://drive.google.com/file/d/1DDULB_-A3Lqcy36LWs8kNH7Oc5-lY5l-/view |
| BP-02 | `49e5fb519775850dade2eb0e1b8929a3dc728820` | `master.mp4` | 635.4s | 198639365 | `6fdf01c2870055b502468cc8a5f6360b50ef9fde2da8ebb3c6ebd133e972a1b9` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp02-bf8c1b2/` |
| BP-02 | `49e5fb519775850dade2eb0e1b8929a3dc728820` | `master.mp4.part01` | | 104857600 | `27d8883eef0c1938b2211ce827ba7f5dd6b22e8926f351883e0a5882d331666e` | Same folder |
| BP-02 | `49e5fb519775850dade2eb0e1b8929a3dc728820` | `master.mp4.part02` | | 93781765 | `07934a2d26ac8249c9d38179a33546422f5638f06c5ddf9964be93fcb838323e` | Same folder |
| BP-02 review 720p | `49e5fb519775850dade2eb0e1b8929a3dc728820` | `review-720p.mp4` | | | `469091357fbc5f61ac5d3a67bb5b23b12a13746627e98286a0d633470ba12644` | https://drive.google.com/file/d/1eOyjIlG-vklph_hUEH1r-H3CxeRHeoS_/view |

The file hashes above are the renders Stewart named as `a93b5d5` (BP-01 v14) and `bf8c1b2` (BP-02). Those two local commits were rewritten before their first push so the videos were not uploaded. The commit column is the rewritten commit that carries the same source, captions, cards, and gate report.
