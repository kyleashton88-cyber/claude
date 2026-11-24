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

## BP-01 after S1–S9 and fix order 10, 23 Nov

Source commit `f308e46`. Duration 875.7s. 2,393 spoken words. Gate PASS: −14.3 LUFS, −3.6 dBTP.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-01 S1–S9 | `f308e46` | `master.mp4` | 875.7s | 300316448 | `2fc0c97b78939f16c29027c59a161e7f471b6c4db904695e39532e6dc1c219d0` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp01-f308e46/` |
| BP-01 S1–S9 | `f308e46` | `master.mp4.part01` | | 104857600 | `85b2ae225bb9c5b789b6f4aa0a69d95cb050f3c2bfae1cc3c2f61a48b18d749e` | Same folder |
| BP-01 S1–S9 | `f308e46` | `master.mp4.part02` | | 104857600 | `c18cd81dcfe052bc1086e7c7299dd7ae65cb828db751763c576ae95d254b87d5` | Same folder |
| BP-01 S1–S9 | `f308e46` | `master.mp4.part03` | | 90601248 | `59c2bade675e94f2bd029436f66579889a82391fdfb2428b4f9f19b72465b548` | Same folder |

Join: `cat master.mp4.part01 master.mp4.part02 master.mp4.part03 > master.mp4`

`SHA256SUMS` lists the parts, captions, spoken script, gate report, and the card stills that are actually in the folder.

## BP-01 after fix order 12, 24 Nov

Source commit `3c06f47` (spoken sign-off `7b849b1` plus the stop-lane motion). Duration 876.4s. 2,395 spoken words. Gate PASS: −14.3 LUFS, −3.6 dBTP. BP-02 was not rendered.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-01 X1 | `3c06f47` | `master.mp4` | 876.4s | 302431831 | `0db87a7e85425a1286e4e9c8a3e91b0d8c9e4ad7428dd0d0c16c94ae9bb0dd98` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp01-3c06f47/` |
| BP-01 X1 | `3c06f47` | `master.mp4.part01` | | 104857600 | `49064c09b13927c2c7f220a53d6ff5326933a8c88e697757c2e8ccbd54303e14` | Same folder |
| BP-01 X1 | `3c06f47` | `master.mp4.part02` | | 104857600 | `d251ffe87d0757f2cd513abb638a4228e05bbfe2dcac55d5e1efdac7f833a450` | Same folder |
| BP-01 X1 | `3c06f47` | `master.mp4.part03` | | 92716631 | `b8449a0e839c8f17af73cef3806f85d49a64e69419d352ccc5514a7e48898677` | Same folder |

Join: `cat master.mp4.part01 master.mp4.part02 master.mp4.part03 > master.mp4`

`SHA256SUMS` lists the parts, captions, spoken script, gate report, and the card stills that are actually in the folder.

## BP-01 after fix order 13, 24 Nov

Source commit `b4ba1f4`. Duration 879.6s. 2,395 spoken words. No spoken word changed. Gate PASS: −14.3 LUFS, −3.6 dBTP. BP-02 was not rendered.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-01 fix 13 | `b4ba1f4` | `master.mp4` | 879.6s | 307907257 | `86465f18efbf6091e8391d2afff0c998923841b93b03397008d49998ec17f0f5` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp01-b4ba1f4/` |
| BP-01 fix 13 | `b4ba1f4` | `master.mp4.part01` | | 104857600 | `232ef3d92c5f8b03912e88e48d2f4c52224fc67f850f3e7b90289196de2f83e4` | Same folder |
| BP-01 fix 13 | `b4ba1f4` | `master.mp4.part02` | | 104857600 | `e08e7fb1e2ba6898762a923e0703d66bd8efa0c97ca45bf140573cb8cd6ae7f8` | Same folder |
| BP-01 fix 13 | `b4ba1f4` | `master.mp4.part03` | | 98192057 | `3be7d1bc11c4fc94303e8ea38c7e8a2162907aab8fe81719054cb96033be86b9` | Same folder |

Join: `cat master.mp4.part01 master.mp4.part02 master.mp4.part03 > master.mp4`

`SHA256SUMS` lists only the files that are in the folder.

## BP-01 after fix order 14, 24 Nov

Source commit `a487eb4` (pictures `6ad473d`, captions extended so the last cue ends at the film). Duration 878.9s. No spoken word changed. Gate PASS: −14.3 LUFS, −3.6 dBTP. The 720p watch copy is in the same folder. Google Drive's file tool cannot take a 67 MB video, so there is no Drive link for this copy.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-01 fix 14 | `a487eb4` | `master.mp4` | 878.9s | 309229915 | `f456ba17294fa3461fd44622b0abfb346364c83e5b31aefbfa910b637774a1d5` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp01-a487eb4/` |
| BP-01 fix 14 | `a487eb4` | `master.mp4.part01` | | 104857600 | `0fc97151959413c0be599037b77e536f0b1465c6afeb2760ce12ab9154d1b551` | Same folder |
| BP-01 fix 14 | `a487eb4` | `master.mp4.part02` | | 104857600 | `0f8475a92c45e4aa00ffefcd56b865b897830c68d5d7ccec8b3cd3fbb14d02e9` | Same folder |
| BP-01 fix 14 | `a487eb4` | `master.mp4.part03` | | 99514715 | `4c26d6b6cda37626f1fbae36a2f064500b9858d02f6393937e389f64c675cb10` | Same folder |
| BP-01 fix 14 | `a487eb4` | `watch-720p.mp4` | 878.9s | 70069526 | `5b3cbf3ad8e77206eb0c371327d5e8fa6f62ab268ba852d0a3a0adc7b776049e` | Same folder |

Join: `cat master.mp4.part01 master.mp4.part02 master.mp4.part03 > master.mp4`

`SHA256SUMS` lists only the files that are in the folder. The joined master matches `f456ba17294fa3461fd44622b0abfb346364c83e5b31aefbfa910b637774a1d5`.

## BP-02 after the signed script, 24 Nov

Source commit `229bdae`. The spoken script is the canonical script from `b958dff` with X1–X6. BP-03 is titled "How a grid bot works, order by order." Duration 661.4s. 1,805 spoken words. Gate PASS: −14.4 LUFS, −3.6 dBTP. The 720p watch copy is in the same folder. Google Drive's file tool cannot take a video this size, so there is no Drive link.

| Lesson | Commit | File | Duration | Bytes | SHA-256 | Where it lives |
|---|---|---|---|---|---|---|
| BP-02 | `229bdae` | `master.mp4` | 661.4s | 208193411 | `82b3a9b783c620a7caac9aa58f19a6169041061c54e64700e775c41f62bb41f2` | Agent store `/cursor/stores/self/artifacts/bp-23nov/bp02-229bdae/` |
| BP-02 | `229bdae` | `master.mp4.part01` | | 104857600 | `28495ab96d6a459f6396cf9af128049e576af717910668d5e5bcdba718a4b459` | Same folder |
| BP-02 | `229bdae` | `master.mp4.part02` | | 103335811 | `66b745a64b203f22fcdf70113b1ef23b3cbde53064cfa567cc80fdd80173380e` | Same folder |
| BP-02 | `229bdae` | `watch-720p.mp4` | 661.4s | 49567434 | `55b12a503ef4604805d96cbc93d09a533767dfd28b63d01fa5f260e2d6dfd79d` | Same folder |

Join: `cat master.mp4.part01 master.mp4.part02 > master.mp4`

`SHA256SUMS` lists only the files that are in the folder. The joined master matches `82b3a9b783c620a7caac9aa58f19a6169041061c54e64700e775c41f62bb41f2`.
