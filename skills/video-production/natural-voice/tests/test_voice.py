"""Voice markup, the ElevenLabs mock, and a short Piper render."""

from __future__ import annotations

import io
import json
import os
import sys
import unittest
import urllib.error
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from voice.elevenlabs import ElevenLabsEngine, VoiceError, assert_stock
from voice.markup import chunk_text, estimate, parse_segments, spoken_text
from voice.speak import Speaker


def _wav(seconds: float = 0.4, rate: int = 22050) -> bytes:
    buf = io.BytesIO()
    n = int(seconds * rate)
    samples = (np.sin(2 * np.pi * 220 * np.arange(n) / rate) * 0.2 * 32767).astype(np.int16)
    with wave.open(buf, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(samples.tobytes())
    return buf.getvalue()


class MarkupTests(unittest.TestCase):
    def test_pauses_and_breaks(self):
        segments = parse_segments('Hello there. [[pause 0.4]] <break time="200ms"/> Next line.')
        kinds = [kind for kind, _ in segments]
        self.assertEqual(kinds, ["text", "pause", "pause", "text"])
        self.assertAlmostEqual(segments[1][1], 0.4)
        self.assertAlmostEqual(segments[2][1], 0.2)
        self.assertNotIn("pause", spoken_text('Hello [[pause 1]] there.'))

    def test_chunks_stay_under_the_limit(self):
        text = " ".join(f"Sentence number {i} is long enough to matter." for i in range(30))
        chunks = chunk_text(text, limit=180)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 180 for chunk in chunks))

    def test_cost_is_zero_for_piper_and_positive_for_elevenlabs(self):
        text = "One two three."
        self.assertEqual(estimate(text, "piper", None)["estimated_credits"], 0)
        paid = estimate(text, "elevenlabs", "eleven_multilingual_v2")
        self.assertEqual(paid["characters"], len("One two three."))
        self.assertEqual(paid["estimated_credits"], paid["characters"])

    def test_cloning_is_refused(self):
        with self.assertRaises(VoiceError):
            assert_stock("my-clone", "eleven_multilingual_v2")
        with self.assertRaises(VoiceError):
            assert_stock("Brian", "eleven_multilingual_v2", {"use_pvc_as_ivc": True})
        self.assertEqual(assert_stock("Brian", "eleven_multilingual_v2"), "nPczCjzI2devNBz1zQrb")


class ElevenMockTests(unittest.TestCase):
    def _payload(self, text: str) -> dict:
        chars = list(text)
        step = 0.4 / max(1, len(chars))
        return {
            "audio_base64": __import__("base64").b64encode(_wav()).decode(),
            "alignment": {
                "characters": chars,
                "character_start_times_seconds": [i * step for i in range(len(chars))],
                "character_end_times_seconds": [(i + 1) * step for i in range(len(chars))],
            },
        }

    def test_retry_then_cache(self):
        calls = {"n": 0}

        def opener(req, timeout=0):
            calls["n"] += 1
            if calls["n"] == 1:
                raise urllib.error.HTTPError(req.full_url, 429, "rate", hdrs={"Retry-After": "0"}, fp=io.BytesIO(b"busy"))
            body = json.loads(req.data.decode())
            raw = json.dumps(self._payload(body["text"])).encode()

            class Resp:
                def read(self):
                    return raw

                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    return False

            return Resp()

        cache = Path("/tmp/voice-cache-test")
        if cache.exists():
            for child in cache.iterdir():
                child.unlink()
        cache.mkdir(exist_ok=True)
        engine_kwargs = {"opener": opener, "sleep": lambda _s: None}
        speaker = Speaker(engine="elevenlabs", voice="Brian", cache_dir=cache, **engine_kwargs)
        os.environ.pop("ELEVENLABS_API_KEY", None)
        audio, rate, words, method = speaker.render("Orders fill when price crosses.")
        self.assertGreater(len(audio), 100)
        self.assertEqual(rate, 22050)
        self.assertEqual(method, "elevenlabs character alignment")
        self.assertEqual(
            [word.text.strip(".,") for word in words],
            "Orders fill when price crosses".split(),
        )
        self.assertTrue(all(words[i].end <= words[i + 1].start + 1e-6 for i in range(len(words) - 1)))
        before = calls["n"]
        speaker.render("Orders fill when price crosses.")
        self.assertEqual(calls["n"], before)

    def test_dry_path_does_not_need_a_key(self):
        quote = estimate("Hello there.", "elevenlabs", None)
        self.assertGreater(quote["estimated_credits"], 0)


class PiperTests(unittest.TestCase):
    def test_piper_line_has_words_and_a_pause(self):
        model = Path.home() / ".cache" / "piper-voices" / "en_US-lessac-medium.onnx"
        if not model.is_file():
            self.skipTest("Piper voice is not installed")
        speaker = Speaker(engine="piper", voice="lessac", cache_dir=None)
        audio, rate, words, method = speaker.render("Price moves in candles. [[pause 0.35]] The figures are illustrative.")
        self.assertEqual(rate, 22050)
        self.assertGreater(len(audio) / rate, 1.0)
        self.assertIn("sentence-exact", method)
        texts = [word.text for word in words]
        self.assertIn("Price", texts)
        self.assertIn("illustrative.", texts)
        # The pause is real silence, not a spoken word.
        self.assertNotIn("pause", " ".join(texts))
        gap = words[texts.index("The")].start - words[texts.index("candles.")].end
        self.assertGreater(gap, 0.3)
        self.assertLess(gap, 0.55)


if __name__ == "__main__":
    unittest.main()
