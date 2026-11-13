"""Command line for the in-house illustration engine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .gallery import build_gallery
from .llm import LlmUnavailable
from .parser import ParseError
from .policy import RefusedPrompt
from .qa import check_pixels, check_scene
from .render import UnsafeOutput, render_prompt
from .spec import TYPES
from .theme import PRESET_NAMES, get_theme


def _render(args) -> int:
    try:
        result = render_prompt(
            args.prompt,
            Path(args.out),
            preset=args.preset,
            size=args.size,
            seed=args.seed,
            use_llm=args.llm,
            strict=args.strict,
            fallback=args.fallback,
            allow_generic=args.allow_generic,
        )
    except (ParseError, RefusedPrompt, LlmUnavailable, UnsafeOutput, RuntimeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if result.notes:
        print("rewrote: " + ", ".join(result.notes))
    print(result.png_path)
    print(f"renderer {result.renderer} checksum {result.checksum} qa {'pass' if result.qa.ok else 'fail'}")
    return 0 if result.qa.ok else 1


def _batch(args) -> int:
    from .batch import render_lesson

    try:
        render_lesson(
            Path(args.source), Path(args.out), lesson=args.lesson, preset=args.preset,
            strict=args.strict, fallback=args.fallback, allow_generic=args.allow_generic,
        )
    except (ParseError, RefusedPrompt, UnsafeOutput, RuntimeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


def _gallery(args) -> int:
    try:
        build_gallery(
            Path(args.out),
            requests=Path(args.requests) if args.requests else None,
            lesson=args.lesson,
            originals=Path(args.originals) if args.originals else None,
            strict=not args.no_strict,
        )
    except (ParseError, UnsafeOutput, RuntimeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


def _qa(args) -> int:
    path = Path(args.path)
    meta_path = path.with_suffix(".json") if path.suffix == ".png" else None
    if path.is_dir():
        manifest = path / "MANIFEST.json"
        if not manifest.is_file():
            print("no MANIFEST.json in that directory", file=sys.stderr)
            return 1
        data = json.loads(manifest.read_text(encoding="utf-8"))
        failed = [row["file"] for row in data["images"] if not row.get("qa_ok")]
        print(f"{len(data['images'])} plates, {len(failed)} failed")
        return 1 if failed else 0
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1
    png = path.read_bytes()
    theme = get_theme(args.preset)
    ok, detail = check_pixels(png, theme)
    print(detail)
    if meta_path and meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        report = check_scene(meta, theme)
        for line in report.checks:
            print(line)
        ok = ok and report.ok
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="illustration_engine", description="Draw course diagrams in-house.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    render = sub.add_parser("render", help="draw one prompt")
    render.add_argument("prompt")
    render.add_argument("--preset", default="house", choices=PRESET_NAMES)
    render.add_argument("--out", required=True)
    render.add_argument("--size", default=None, help="WxH, for example 1536x1024")
    render.add_argument("--seed", type=int, default=None)
    render.add_argument("--llm", action="store_true", help="draft a JSON spec with a chat model, then draw locally")
    render.add_argument("--fallback", action="store_true", help="diagram types only, for the fallback router")
    render.add_argument("--allow-generic", action="store_true", help="rewrite an exchange name to the word exchange")
    render.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    render.set_defaults(func=_render)

    batch = sub.add_parser("batch", help="draw every slot in a lesson file")
    batch.add_argument("source")
    batch.add_argument("--lesson", default=None)
    batch.add_argument("--preset", default="house", choices=PRESET_NAMES)
    batch.add_argument("--out", required=True)
    batch.add_argument("--fallback", action="store_true", help="diagram types only, for the fallback router")
    batch.add_argument("--allow-generic", action="store_true", help="rewrite an exchange name to the word exchange")
    batch.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    batch.set_defaults(func=_batch)

    gallery = sub.add_parser("gallery", help="draw the test gallery")
    gallery.add_argument("--out", required=True)
    gallery.add_argument("--requests", default=None)
    gallery.add_argument("--lesson", default="bp-01-introduction")
    gallery.add_argument("--originals", default=None)
    gallery.add_argument("--no-strict", action="store_true")
    gallery.set_defaults(func=_gallery)

    qa = sub.add_parser("qa", help="re-check a plate or a manifest directory")
    qa.add_argument("path")
    qa.add_argument("--preset", default="house", choices=PRESET_NAMES)
    qa.set_defaults(func=_qa)

    types = sub.add_parser("types", help="list visual types")
    types.set_defaults(func=lambda _args: (print("\n".join(TYPES)) or 0))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
