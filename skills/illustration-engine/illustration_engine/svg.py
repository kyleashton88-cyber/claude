"""Small SVG builder. The document is XML, not a picture until it is rasterised."""

from __future__ import annotations

from contextlib import contextmanager
from xml.sax.saxutils import escape


def _num(value: float) -> str:
    return f"{float(value):.2f}".rstrip("0").rstrip(".")


class Svg:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._defs: list[str] = []
        self._body: list[str] = []
        self._seq = 0

    def uid(self, prefix: str) -> str:
        self._seq += 1
        return f"{prefix}{self._seq}"

    def linear_gradient(self, gid: str, stops: list[tuple[str, str]]) -> None:
        parts = "".join(
            f'<stop offset="{offset}" stop-color="{color}"/>' for offset, color in stops
        )
        self._defs.append(
            f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{parts}</linearGradient>'
        )

    def radial_gradient(self, gid: str, inner: str, outer: str) -> None:
        self._defs.append(
            f'<radialGradient id="{gid}" cx="50%" cy="42%" r="72%">'
            f'<stop offset="58%" stop-color="{inner}" stop-opacity="0"/>'
            f'<stop offset="100%" stop-color="{outer}" stop-opacity="0.72"/>'
            "</radialGradient>"
        )

    def ensure_glow(self, wide: float, tight: float) -> str:
        gid = "bloom"
        if not any(f'id="{gid}"' in item for item in self._defs):
            self._defs.append(
                f'<filter id="{gid}" x="-80%" y="-80%" width="260%" height="260%" '
                f'color-interpolation-filters="sRGB">'
                f'<feGaussianBlur in="SourceGraphic" stdDeviation="{_num(wide)}" result="wide"/>'
                f'<feGaussianBlur in="SourceGraphic" stdDeviation="{_num(tight)}" result="tight"/>'
                f'<feComposite in="wide" in2="tight" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="add"/>'
                f'<feMerge><feMergeNode in="add"/><feMergeNode in="SourceGraphic"/></feMerge>'
                f"</filter>"
            )
        return gid

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=0, rx=0, opacity=1, stroke_opacity=1, filt=None) -> None:
        filter_attr = f' filter="url(#{filt})"' if filt else ""
        self._body.append(
            f'<rect x="{_num(x)}" y="{_num(y)}" width="{_num(w)}" height="{_num(h)}" '
            f'rx="{_num(rx)}" ry="{_num(rx)}" fill="{fill}" fill-opacity="{opacity}" '
            f'stroke="{stroke}" stroke-width="{_num(sw)}" stroke-opacity="{stroke_opacity}"{filter_attr}/>'
        )

    def circle(self, cx, cy, r, fill="none", stroke="none", sw=0, opacity=1) -> None:
        self._body.append(
            f'<circle cx="{_num(cx)}" cy="{_num(cy)}" r="{_num(r)}" fill="{fill}" '
            f'fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{_num(sw)}"/>'
        )

    def ellipse(self, cx, cy, rx, ry, fill="none", stroke="none", sw=0, opacity=1) -> None:
        self._body.append(
            f'<ellipse cx="{_num(cx)}" cy="{_num(cy)}" rx="{_num(rx)}" ry="{_num(ry)}" '
            f'fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{_num(sw)}"/>'
        )

    def line(self, x1, y1, x2, y2, stroke, sw=2, dash=None, opacity=1, filt=None) -> None:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        filter_attr = f' filter="url(#{filt})"' if filt else ""
        self._body.append(
            f'<line x1="{_num(x1)}" y1="{_num(y1)}" x2="{_num(x2)}" y2="{_num(y2)}" '
            f'stroke="{stroke}" stroke-width="{_num(sw)}" stroke-linecap="round" '
            f'stroke-opacity="{opacity}"{dash_attr}{filter_attr}/>'
        )

    def polyline(self, points: list[tuple[float, float]], stroke, sw=2, opacity=1, filt=None) -> None:
        pts = " ".join(f"{_num(x)},{_num(y)}" for x, y in points)
        filter_attr = f' filter="url(#{filt})"' if filt else ""
        self._body.append(
            f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="{_num(sw)}" '
            f'stroke-linejoin="round" stroke-linecap="round" stroke-opacity="{opacity}"{filter_attr}/>'
        )

    def polygon(self, points: list[tuple[float, float]], fill, stroke="none", sw=0, opacity=1) -> None:
        pts = " ".join(f"{_num(x)},{_num(y)}" for x, y in points)
        self._body.append(
            f'<polygon points="{pts}" fill="{fill}" fill-opacity="{opacity}" '
            f'stroke="{stroke}" stroke-width="{_num(sw)}" stroke-linejoin="round"/>'
        )

    def path(self, d: str, fill="none", stroke="none", sw=2, opacity=1, cap="round") -> None:
        self._body.append(
            f'<path d="{d}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" '
            f'stroke-width="{_num(sw)}" stroke-linecap="{cap}" stroke-linejoin="round"/>'
        )

    def text(self, content, x, y, size, fill, family, anchor="start", opacity=1, rotate=None,
             weight="bold", filt=None) -> None:
        transform = ""
        if rotate is not None:
            transform = f' transform="rotate({_num(rotate)} {_num(x)} {_num(y)})"'
        filter_attr = f' filter="url(#{filt})"' if filt else ""
        self._body.append(
            f'<text x="{_num(x)}" y="{_num(y)}" fill="{fill}" fill-opacity="{opacity}" '
            f'font-family="{family}" font-weight="{weight}" font-size="{int(size)}" '
            f'text-anchor="{anchor}"{transform}{filter_attr}>'
            f"{escape(content)}</text>"
        )

    @contextmanager
    def group(self, transform: str | None = None, opacity: float | None = None):
        attrs = []
        if transform:
            attrs.append(f'transform="{transform}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        extra = (" " + " ".join(attrs)) if attrs else ""
        self._body.append(f"<g{extra}>")
        yield
        self._body.append("</g>")

    def tostring(self, font_css: str) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}">\n'
            "<defs>\n<style><![CDATA[\n"
            f"{font_css}\n"
            "]]></style>\n"
            + "".join(self._defs)
            + "\n</defs>\n"
            + "".join(self._body)
            + "\n</svg>\n"
        )
