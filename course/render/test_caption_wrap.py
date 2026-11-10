"""Captions wrap inside a 64px margin and stay above the footer."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_tutorial as rt


def test_long_line_wraps_inside_the_safe_width():
    text = (
        "Elite is the paper map you finish before a trip, after Blueprint "
        "already named the range, the spacing, and the stop."
    )
    lines = rt.wrap_caption(text)
    assert len(lines) >= 2
    for line in lines:
        assert rt.caption_px(line) <= rt.CAPTION_MAX_W
        assert rt.caption_px(line) + 2 * rt.CAPTION_BORDER <= 1920 - 2 * rt.CAPTION_MARGIN


def test_short_line_stays_one_line_at_the_old_position():
    lines = rt.wrap_caption("Hook.")
    assert lines == ["Hook."]
    assert rt.caption_y_offset(1) == 160
    assert rt.caption_y_offset(2) == 160


def test_three_lines_clear_the_footer_and_the_frame():
    offset = rt.caption_y_offset(3)
    text_h = 3 * rt.CAPTION_SIZE + 2 * rt.CAPTION_LINE
    box_bottom_from_top = (rt.FRAME_H - offset) + text_h + rt.CAPTION_BORDER
    assert box_bottom_from_top <= rt.FRAME_H - rt.FOOTER_Y - 16
    assert rt.FRAME_H - offset - rt.CAPTION_BORDER >= 0


def test_every_elite_caption_fits():
    root = Path(__file__).resolve().parents[1] / "scripts"
    for path in sorted(root.glob("el-*.json")):
        data = json.loads(path.read_text())
        for beat in data["beats"]:
            lines = rt.wrap_caption(beat["cap"])
            assert 1 <= len(lines) <= 4, (path.name, beat["n"], lines)
            for line in lines:
                width = rt.caption_px(line) + 2 * rt.CAPTION_BORDER
                assert width <= 1920 - 2 * rt.CAPTION_MARGIN, (path.name, beat["n"], line)
            offset = rt.caption_y_offset(len(lines))
            text_h = len(lines) * rt.CAPTION_SIZE + max(0, len(lines) - 1) * rt.CAPTION_LINE
            box_top = rt.FRAME_H - offset - rt.CAPTION_BORDER
            box_bottom = box_top + text_h + 2 * rt.CAPTION_BORDER
            assert box_top >= 120, (path.name, beat["n"], box_top)
            assert box_bottom <= rt.FRAME_H - rt.FOOTER_Y - 16


if __name__ == "__main__":
    test_long_line_wraps_inside_the_safe_width()
    test_short_line_stays_one_line_at_the_old_position()
    test_three_lines_clear_the_footer_and_the_frame()
    test_every_elite_caption_fits()
    print("ok")
