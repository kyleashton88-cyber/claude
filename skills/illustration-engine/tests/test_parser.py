import json
import unittest

from illustration_engine.llm import SYSTEM, build_request, endpoint, spec_from_llm
from illustration_engine.parser import ParseError, classify, parse, spec_from_request


class ParserTests(unittest.TestCase):
    def test_grid_sentence(self):
        spec = parse("grid ladder, range 90-110, 10 grids, price 100, label buy and sell")
        self.assertEqual(spec.type, "grid_ladder")
        self.assertEqual(spec.params["low"], 90)
        self.assertEqual(spec.params["high"], 110)
        self.assertEqual(spec.params["grids"], 10)
        self.assertEqual(spec.params["price"], 100)
        self.assertEqual(spec.params["labels"], ["BUY", "SELL"])

    def test_json_spec(self):
        spec = parse(json.dumps({"type": "checklist", "labels": ["RANGE", "STOP"], "headline": "ON PAPER"}))
        self.assertEqual(spec.type, "checklist")
        self.assertEqual(spec.params["labels"], ["RANGE", "STOP"])

    def test_yaml_spec(self):
        spec = parse("type: analogy_fence\nheadline: THE FENCE\nlabels: [INSIDE, FENCE]\n")
        self.assertEqual(spec.type, "analogy_fence")

    def test_unknown_type(self):
        with self.assertRaises(ParseError):
            parse('{"type": "not-a-type"}')

    def test_pointing_mascot_is_not_a_warning(self):
        spec = parse("mascot pointing")
        self.assertEqual(spec.type, "mascot_scene")
        self.assertEqual(spec.params["pose"], "pointing")
        self.assertEqual(spec.params["headline"], "LOOK HERE")

    def test_email_is_not_a_label(self):
        spec = parse("grid ladder, range 90-110, 8 grids, price 100, label buy and person@example.com")
        self.assertNotIn("@", " ".join(spec.params.get("labels") or []))

    def test_lesson_rows_cover_the_introduction(self):
        rows = [
            ("hook", "Hook", "Price often chops sideways, weaving through the same band instead of leaving.", "price_range"),
            ("legal", "Disclaimer", "Education only, not financial advice.", "steps"),
            ("intro", "Title card", "Introduction", "title_card"),
            ("body", "The three parts", "A grid has three parts you can name: the range, the levels, and the stop.", "steps"),
            ("body", "The range", "The range is a top and a bottom you draw before any rung.", "price_range"),
            ("body", "The levels", "The levels are limit orders that wait on the rungs.", "analogy_ladder"),
            ("diagram", "Buys and sells", "One approach places buy orders below the mark and sell orders above it.", "grid_ladder"),
            ("body", "The stop", "The stop is a sentence you write, not a feeling that the trade is over.", "price_range"),
            ("body", "No order", "We do not sell or run a trading bot. No order is sent from this lesson.", "mascot_scene"),
            ("map", "A map", "The course is a map, and this introduction is only the first square.", "flowchart"),
            ("body", "Leaving", "Draw a path that leaves the top of the band and does not return.", "price_range"),
            ("body", "No result", "There is no result number in this lesson.", "comparison"),
            ("demo", "Ticks", "A slow sketch uses eight even ticks inside the band, only as a way to see rungs.", "grid_ladder"),
            ("action", "Checklist", "The next step is the setup checklist, on paper, before any screen.", "checklist"),
            ("demo", "Fence", "A paper or demo account is a fence around practice.", "analogy_fence"),
            ("demo", "Practice", "Practice: A grid has three parts you can name: the range, the levels, and the stop.", "steps"),
            ("recap", "Recap", "If you keep one sentence, keep this: range, levels, and stop, drawn before any click.", "steps"),
            ("outro", "Outro", "Next lesson: what you are going to need.", "section_divider"),
        ]
        for role, chapter, concept, expected in rows:
            self.assertEqual(classify(concept, role, chapter), expected, concept)
            spec = spec_from_request({"role": role, "chapter": chapter, "concept": concept, "title": "Introduction", "beat": 1, "out_path": "course/images/bp-01-introduction/001.png", "size": "1536x1024"})
            self.assertEqual(spec.file, "001.png")
            self.assertGreaterEqual(len(spec.labels or []), 2)


class LlmTests(unittest.TestCase):
    def test_endpoint_is_chat_not_images(self):
        url = endpoint("https://example.test/v1")
        self.assertTrue(url.endswith("/chat/completions"))
        self.assertNotIn("/images", url)

    def test_system_prompt_forbids_pixels(self):
        self.assertIn("Do not return pixels", SYSTEM)
        body = build_request("a grid ladder")
        self.assertEqual(body["messages"][0]["content"], SYSTEM)
        self.assertNotIn("image", body["messages"][0]["content"].split("image URLs")[0].lower())

    def test_transport_result_is_a_spec_only(self):
        def transport(url, payload, headers):
            self.assertIn("/chat/completions", url)
            self.assertNotIn("images/generations", url)
            return {"choices": [{"message": {"content": json.dumps({
                "type": "grid_ladder",
                "params": {"low": 90, "high": 110, "grids": 10, "price": 100, "labels": ["BUY", "SELL"]},
            })}}]}

        spec = spec_from_llm("grid ladder", transport=transport)
        self.assertEqual(spec.type, "grid_ladder")
        self.assertEqual(spec.params["grids"], 10)

    def test_rejects_image_payload(self):
        def transport(url, payload, headers):
            return {"choices": [{"message": {"content": "data:image/png;base64,aaaa"}}]}

        with self.assertRaises(ParseError):
            spec_from_llm("anything", transport=transport)


if __name__ == "__main__":
    unittest.main()
