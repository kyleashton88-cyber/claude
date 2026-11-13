"""Tests for beds, effects, and the sidechain model."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from music.compose import SR, render_bed
from music.duck import sidechain
from music.sfx import render_effect


class MusicTests(unittest.TestCase):
    def test_bed_length_and_finite(self):
        audio, sr = render_bed(mood="calm", key="D", scale="major", bpm=80, seconds=4)
        self.assertEqual(sr, SR)
        self.assertEqual(audio.shape[0], 4 * SR)
        self.assertEqual(audio.shape[1], 2)
        self.assertTrue(np.isfinite(audio).all())
        self.assertGreater(float(np.sqrt(np.mean(audio**2))), 0.01)
        self.assertLess(float(np.max(np.abs(audio))), 0.95)

    def test_effects_are_short(self):
        for name in ("whoosh", "click", "riser", "tick", "mark-sting"):
            audio, sr = render_effect(name)
            self.assertLess(audio.shape[0] / sr, 4.0, name)
            self.assertTrue(np.isfinite(audio).all())

    def test_sidechain_drops_the_bed_under_the_voice(self):
        sr = 48000
        n = sr * 2
        music = np.full((n, 2), 0.2, dtype=np.float32)
        voice = np.zeros(n, dtype=np.float32)
        voice[sr // 2 : sr + sr // 2] = 0.4
        ducked = sidechain(music, voice, sr)
        quiet = float(np.sqrt(np.mean(ducked[: sr // 4] ** 2)))
        under = float(np.sqrt(np.mean(ducked[sr // 2 + 1000 : sr + sr // 2 - 1000] ** 2)))
        self.assertLess(under, quiet * 0.5)

    def test_house_loudness_is_the_one_standard(self):
        from lib.mix import BED_UNDER_VOICE_DB, TRUE_PEAK_DBTP, VOICE_LUFS
        self.assertEqual(VOICE_LUFS, -14.0)
        self.assertEqual(TRUE_PEAK_DBTP, -1.0)
        self.assertEqual(BED_UNDER_VOICE_DB, -20.0)


if __name__ == "__main__":
    unittest.main()
