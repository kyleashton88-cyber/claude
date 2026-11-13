"""Safe-margin placement. No video decode."""

from __future__ import annotations

import numpy as np

import repair_margins as rm


def test_title_sprite_sits_inside_the_margin():
    sprite = rm.render_title("Summer stops")
    assert sprite.shape[0] < rm.CHART_TOP - rm.TITLE_Y
    assert rm.TITLE_X >= rm.SAFE_X
    assert rm.TITLE_Y >= rm.SAFE_Y
    assert rm.TITLE_X + sprite.shape[1] <= rm.SAFE_R


def test_footer_and_title_clear_the_margin_on_a_bad_frame():
    frame = np.zeros((rm.H, rm.W, 3), dtype=np.uint8)
    frame[:] = rm.NAVY
    frame[910:934, 73:400] = (236, 241, 247)
    frame[1037:1055, 74:700] = (156, 180, 198)
    frame[400:430, 40:180] = (236, 241, 247)
    sprite = rm.render_title("Summer stops")
    rm.repair_frame(frame, sprite, 0.4)
    assert rm.text_outside(frame) == []
    ink = frame[200:800].max(axis=2) > 80
    xs = np.where(ink.any(axis=0))[0]
    assert int(xs.min()) >= rm.SAFE_X
    assert int(xs.max()) <= rm.SAFE_R


def test_elite_id_is_refused():
    try:
        rm.chapters_for("el-01-welcome")
    except SystemExit:
        return
    raise AssertionError("Elite id was accepted")


if __name__ == "__main__":
    test_title_sprite_sits_inside_the_margin()
    test_footer_and_title_clear_the_margin_on_a_bad_frame()
    test_elite_id_is_refused()
    print("ok")
