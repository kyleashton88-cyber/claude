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

## BP-01 after W1–W8, 23 Nov

Source commit `dea5f0a` (wording `20bf182`, then the card fix). Duration 845.6s. 2,305 spoken words. Gate PASS: −14.3 LUFS, −3.6 dBTP. No review file was uploaded to Drive.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-01 W1–W8 | `dea5f0a` | `master.mp4` | 845.6s | 288910509 | `54d9d40450ae64e83cab756ad4383e31bb4a107c8699863a638026158521b1ee` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp01-w1-dea5f0a/` |
| BP-01 W1–W8 | `dea5f0a` | `master.mp4.part01` | | 104857600 | `b546dfee2eb93efe0eb8c5fb091a4fc5af4981d8ccb8fd2fe78960db85d5c9b9` | Same folder |
| BP-01 W1–W8 | `dea5f0a` | `master.mp4.part02` | | 104857600 | `125203f7f1ae7ee6006e94f8e1b92bed6ffbc16ab0af1ef016dd648cbe694917` | Same folder |
| BP-01 W1–W8 | `dea5f0a` | `master.mp4.part03` | | 79195309 | `7a88f29b0231014a08822c0cf8306ed4383e6a7437c5ae7b74798ff1dcd5e147` | Same folder |

Join: `cat master.mp4.part01 master.mp4.part02 master.mp4.part03 > master.mp4`

The same folder holds `captions.vtt`, `spoken-script.txt`, `gate-report.md`, and `cards/` for the changed pictures.

## BP-02 after W6–W8 and Part A, 23 Nov

Source at render start: `b9c0230`, plus the picture beat that keeps long cards from sitting still. Duration 641.6s. 1,768 spoken words. Gate PASS: −14.4 LUFS, −3.6 dBTP.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-02 W6–W8 | `b9c0230` | `master.mp4` | 641.6s | 194954562 | `35452af20c6aef64a3e42cdedb5ff912c393e7147402e5f63619a64358684d07` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp02-b9c0230/` |
| BP-02 W6–W8 | `b9c0230` | `master.mp4.part01` | | 104857600 | `357ce63cd2dacf903e26b8e42f4204af05588d9db3e6cf45fa2a63cdfa6916c0` | Same folder |
| BP-02 W6–W8 | `b9c0230` | `master.mp4.part02` | | 90096962 | `cb1d6ca7bed86cb1a5a6837fa7796e0d2134a932c742b113761f07aa20c1265d` | Same folder |

Join: `cat master.mp4.part01 master.mp4.part02 > master.mp4`

`SHA256SUMS` in that folder lists only files that are in the folder.
