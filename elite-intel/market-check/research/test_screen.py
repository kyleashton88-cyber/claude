"""Unit tests for screen tweaks D and F. No network.

Historical figures are from research/week_2026_11_22.json (select.py win()
on completed dailies before each pick's start, same as the 22 Nov weekly review).
"""
import json
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import screen

WEEK = json.loads((Path(__file__).resolve().parent / "week_2026_11_22.json").read_text())


class TestConstants(unittest.TestCase):
    def test_named_thresholds(self):
        self.assertEqual(screen.TREND_DRIFT30_MIN, 0.8)
        self.assertEqual(screen.TREND_ADX14_MIN, 40)
        self.assertEqual(screen.ROOM_ABOVE_STOP_MIN, 0.08)
        self.assertEqual(screen.REGIME_DRIFT30_MIN, 1.0)
        self.assertEqual(screen.REGIME_ADX14_MIN, 35)
        self.assertEqual(screen.RANGE_NOT_ACTIVE, "range not active")
        self.assertEqual(screen.BIG_FOUR, ("BTC", "ETH", "SOL", "XRP"))


class TestGateD(unittest.TestCase):
    def test_trend_cut_is_strict_and_needs_both(self):
        adx_above = math.nextafter(40, math.inf)
        drift_above = math.nextafter(0.8, math.inf)
        self.assertFalse(screen.trend_skip(0.8, adx_above))
        self.assertFalse(screen.trend_skip(math.nextafter(0.8, 0.0), adx_above))
        self.assertFalse(screen.trend_skip(drift_above, 40))
        self.assertFalse(screen.trend_skip(drift_above, math.nextafter(40, 0.0)))
        self.assertTrue(screen.trend_skip(drift_above, adx_above))
        self.assertFalse(screen.trend_skip(0.97, 30))
        self.assertFalse(screen.trend_skip(0.5, 55))

    def test_room_cut_is_strict(self):
        stop = 100.0
        exact = stop * (1 + screen.ROOM_ABOVE_STOP_MIN)
        self.assertEqual(screen.room_above_stop(exact, stop), screen.ROOM_ABOVE_STOP_MIN)
        self.assertFalse(screen.room_skip(exact, stop))
        self.assertTrue(screen.room_skip(math.nextafter(exact, 0.0), stop))
        self.assertFalse(screen.room_skip(math.nextafter(exact, math.inf), stop))
        self.assertTrue(screen.room_skip(stop, stop))
        self.assertTrue(screen.room_skip(stop * 0.99, stop))

    def test_bnb_16_nov_pm_blocked_by_room_not_trend(self):
        """BNB went live 16 Nov pm 0.9% above its example stop. D's 8% floor
        catches it. The trend leg misses (ADX 39.5 is not > 40)."""
        b = WEEK["BNB"]
        self.assertAlmostEqual(b["drift30"], 0.91, places=2)
        self.assertAlmostEqual(b["adx14"], 39.5, places=1)
        self.assertAlmostEqual(b["buffer"], 0.9, places=1)
        reasons = screen.skip_reasons_from_facts(b["drift30"], b["adx14"], b["c0"], b["stop"])
        self.assertTrue(any(r.startswith("room-to-stop:") for r in reasons), reasons)
        self.assertFalse(any(r.startswith("trend:") for r in reasons), reasons)
        self.assertTrue(screen.room_skip(b["c0"], b["stop"]))
        self.assertFalse(screen.trend_skip(b["drift30"], b["adx14"]))


class TestGateF(unittest.TestCase):
    def test_regime_cut_is_strict_and_needs_both(self):
        adx_above = math.nextafter(35, math.inf)
        drift_above = math.nextafter(1.0, math.inf)
        self.assertFalse(screen.btc_regime_blocks_rotation(1.0, adx_above))
        self.assertFalse(screen.btc_regime_blocks_rotation(math.nextafter(1.0, 0.0), adx_above))
        self.assertFalse(screen.btc_regime_blocks_rotation(drift_above, 35))
        self.assertFalse(screen.btc_regime_blocks_rotation(drift_above, math.nextafter(35, 0.0)))
        self.assertTrue(screen.btc_regime_blocks_rotation(drift_above, adx_above))

    def test_f_blocks_rotation_picks_on_15_nov(self):
        """Weekly review: BTC drift30 1.35 and ADX14 37.3 on 15 Nov."""
        btc = WEEK["BTC"]
        self.assertAlmostEqual(btc["drift30"], 1.35, places=2)
        self.assertAlmostEqual(btc["adx14"], 37.3, places=1)
        self.assertTrue(screen.btc_regime_blocks_rotation(btc["drift30"], btc["adx14"]))

        rotation = []
        for coin in ("DOGE", "XLM", "SHIB", "ASTER"):
            row = WEEK[coin]
            rotation.append({
                "coin": coin, "drift30": row["drift30"], "adx14": row["adx14"],
                "last_close": row["c0"], "stop": row["stop"],
            })
        four = []
        for coin in screen.BIG_FOUR:
            row = WEEK[coin]
            four.append({"coin": coin, "last_close": row["c0"], "stop": row["stop"], "now": row["c0"]})
        out = screen.evaluate_market(btc["drift30"], btc["adx14"], four, rotation)
        self.assertTrue(out["regime"])
        self.assertEqual(out["picks"], [])
        self.assertTrue(all(s["reasons"][0].startswith("BTC trending") for s in out["skipped"]))

    def test_big_four_below_stop_labelled_range_not_active(self):
        """At the 15 Nov week start, all four had already closed below the
        15 Nov am example stop (14 Nov close vs that stop)."""
        for coin in screen.BIG_FOUR:
            row = WEEK[coin]
            self.assertTrue(
                screen.is_range_not_active(row["c0"], row["stop"]),
                f"{coin} close {row['c0']} should be below stop {row['stop']}",
            )
        four = [
            {"coin": c, "last_close": WEEK[c]["c0"], "stop": WEEK[c]["stop"], "now": WEEK[c]["c0"]}
            for c in screen.BIG_FOUR
        ]
        out = screen.evaluate_market(WEEK["BTC"]["drift30"], WEEK["BTC"]["adx14"], four, [])
        self.assertEqual([r["status"] for r in out["four"]], [screen.RANGE_NOT_ACTIVE] * 4)

    def test_close_on_or_above_stop_stays_active(self):
        self.assertFalse(screen.is_range_not_active(100.0, 100.0))
        self.assertFalse(screen.is_range_not_active(100.01, 100.0))
        self.assertTrue(screen.is_range_not_active(99.99, 100.0))

    def test_template_line_does_not_reprint_range_when_inactive(self):
        line = screen.format_big_four_line("BTC", "64,146", screen.RANGE_NOT_ACTIVE)
        self.assertIn("range not active", line)
        self.assertIn("not in play", line)
        self.assertNotIn("enter", line.lower())
        self.assertIn("Education only", line)
        self.assertIn("Not financial advice", line)
        active = screen.format_big_four_line("BTC", "60,216", "active", "below", "unchanged")
        self.assertIn("example range", active)
        self.assertNotIn("range not active", active)


class TestEvaluateCombined(unittest.TestCase):
    def test_d_still_applies_when_regime_is_off(self):
        # Synthetic: BTC not trending, BNB too close to its stop.
        bnb = WEEK["BNB"]
        four = [{"coin": "BTC", "last_close": 110.0, "stop": 100.0, "now": 110.0}]
        rotation = [{
            "coin": "BNB", "drift30": bnb["drift30"], "adx14": bnb["adx14"],
            "last_close": bnb["c0"], "stop": bnb["stop"],
        }, {
            "coin": "OK", "drift30": 0.2, "adx14": 20.0,
            "last_close": 120.0, "stop": 100.0,
        }]
        out = screen.evaluate_market(0.5, 20.0, four, rotation)
        self.assertFalse(out["regime"])
        self.assertEqual([p["coin"] for p in out["picks"]], ["OK"])
        self.assertEqual(out["skipped"][0]["coin"], "BNB")
        self.assertEqual(out["four"][0]["status"], "active")


if __name__ == "__main__":
    unittest.main()

