# Audio licence

The beds, the effects, and the ident sting are synthesized by `music/compose.py` and `music/sfx.py`. They are not recordings. They do not include a soundfont, a commercial loop, or a sample from a library.

The mix that plays them under a voice is `lib/mix.py`: voice at −14 LUFS / −1 dBTP, bed 20 dB under that, then one sidechain. That replaced a −16 LUFS voice master, a −16 LUFS bed master, a −16 LUFS ducked mix, and a −1.5 dBTP ceiling with a fixed music volume.

You can regenerate the files from the code. The seed is fixed, so a re-run matches after the same loudness pass.

Piper and Kokoro speech used beside these files is stock and self-hosted. This note does not cover those voice models. The voice skill documents where they come from.
