#!/usr/bin/env python3
"""Format templates, thumbnails, shorts, chapters, and the end card.

Nothing here publishes or uploads.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
VP = HERE.parent
if str(VP) not in sys.path:
    sys.path.insert(0, str(VP))

from pack.distribute import (  # noqa: E402
    cut_short,
    load_lesson,
    make_thumbnail,
    write_description,
)
from pack.paint import paint_endcard  # noqa: E402

FORMATS = HERE / "formats"


def refuse_course(path: Path) -> None:
    if "course" in path.resolve().parts:
        raise SystemExit(f"refusing to write into course/: {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lesson templates and distribution stills")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list format templates")
    show = sub.add_parser("show")
    show.add_argument("name")

    thumb = sub.add_parser("thumbnail")
    thumb.add_argument("--title", required=True)
    thumb.add_argument("--label", required=True)
    thumb.add_argument("--out", type=Path, required=True)
    thumb.add_argument("--engine", default="auto", choices=("auto", "pil", "illustration"))

    short = sub.add_parser("short")
    short.add_argument("--master", type=Path, required=True)
    short.add_argument("--chapters", type=Path, required=True)
    short.add_argument("--vtt", type=Path)
    short.add_argument("--chapter", default=None)
    short.add_argument("--out", type=Path, required=True)

    chapters = sub.add_parser("chapters")
    chapters.add_argument("--lesson", type=Path, required=True)
    chapters.add_argument("--out", type=Path, required=True)

    end = sub.add_parser("endcard")
    end.add_argument("--title", required=True)
    end.add_argument("--next", required=True)
    end.add_argument("--out", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.cmd == "list":
        for path in sorted(FORMATS.glob("*.yaml")):
            print(path.name)
        return 0
    if args.cmd == "show":
        path = FORMATS / f"{args.name}.yaml"
        if not path.is_file():
            print(f"no template {args.name}", file=sys.stderr)
            return 2
        print(path.read_text(encoding="utf-8"))
        return 0
    if args.cmd == "thumbnail":
        refuse_course(args.out)
        meta = make_thumbnail(args.title, args.label, args.out, engine=args.engine)
        print(json.dumps(meta))
        return 0
    if args.cmd == "short":
        refuse_course(args.out)
        meta = cut_short(args.master, args.chapters, args.out, vtt=args.vtt, chapter=args.chapter)
        print(json.dumps(meta))
        return 0
    if args.cmd == "chapters":
        refuse_course(args.out)
        path = write_description(load_lesson(args.lesson), args.out)
        print(path)
        return 0
    if args.cmd == "endcard":
        refuse_course(args.out)
        meta = paint_endcard(args.title, args.next, args.out)
        args.out.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"path": meta["path"], "hold_seconds": meta["hold_seconds"]}))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
