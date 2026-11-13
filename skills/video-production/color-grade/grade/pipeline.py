"""Measure a clip and build the ffmpeg grade graph."""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np

from lib.ffmpeg_util import ffmpeg_bin, run


def sample_frames(path: Path, count: int = 8, width: int = 160, height: int = 90) -> np.ndarray:
    proc = subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(path),
            "-vf",
            f"fps=2,scale={width}:{height}:flags=area",
            "-frames:v",
            str(count),
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-",
        ],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or b"").decode()[-1500:])
    frame = width * height * 3
    n = len(proc.stdout) // frame
    if n < 1:
        raise RuntimeError(f"no frames decoded from {path}")
    return np.frombuffer(proc.stdout[: n * frame], dtype=np.uint8).reshape(n, height, width, 3).astype(np.float32) / 255.0


def _means(frames: np.ndarray) -> tuple[np.ndarray, float]:
    r, g, b = frames[..., 0], frames[..., 1], frames[..., 2]
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mask = (y > 0.06) & (y < 0.94)
    if int(mask.sum()) < 64:
        mask = np.ones(y.shape, dtype=bool)
    means = np.array([r[mask].mean(), g[mask].mean(), b[mask].mean()], dtype=np.float64)
    return means, float(y[mask].mean())


def white_balance(frames: np.ndarray) -> np.ndarray:
    """Gray-world gains, green-referenced, clipped so a graphic is not yanked off its palette."""
    means, _y = _means(frames)
    target = float(means.mean())
    gains = target / np.maximum(means, 1e-4)
    gains = np.clip(gains, 0.82, 1.22)
    gains = gains / gains[1]
    return gains


def exposure_ev(frames: np.ndarray, target_y: float = 0.42) -> float:
    _means_rgb, y = _means(frames)
    return float(np.clip(np.log2(target_y / max(y, 1e-4)), -1.5, 1.5))


def match_to(source: np.ndarray, reference: np.ndarray) -> tuple[np.ndarray, float]:
    """Gains and exposure so source mean colour and luma meet the reference."""
    src, src_y = _means(source)
    ref, ref_y = _means(reference)
    gains = np.clip(ref / np.maximum(src, 1e-4), 0.7, 1.4)
    gains = gains / max(gains[1], 1e-4)
    ev = float(np.clip(np.log2(max(ref_y, 1e-4) / max(src_y, 1e-4)), -1.5, 1.5))
    return gains, ev


def grade_filter(lut: Path, gains: np.ndarray, ev: float, *, legal: bool = True) -> str:
    rr, gg, bb = (float(v) for v in gains)
    parts = [
        f"colorchannelmixer=rr={rr:.5f}:gg={gg:.5f}:bb={bb:.5f}",
        f"exposure=exposure={ev:.4f}",
        f"lut3d=file={lut}:interp=tetrahedral",
    ]
    if legal:
        parts.append("scale=in_range=full:out_range=tv:flags=accurate_rnd")
        # Saturated colours can land a code or two outside 16–235. Clip to legal.
        parts.append("lutyuv=y=clip(val\\,16\\,235):u=clip(val\\,16\\,240):v=clip(val\\,16\\,240)")
        parts.append("setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709")
    parts.append("format=yuv420p")
    return ",".join(parts)


def apply_grade(src: Path, dest: Path, lut: Path, gains: np.ndarray, ev: float, *, crf: int = 18) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            ffmpeg_bin(),
            "-y",
            "-hide_banner",
            "-i",
            str(src),
            "-vf",
            grade_filter(lut, gains, ev),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            "-color_range",
            "tv",
            "-color_primaries",
            "bt709",
            "-color_trc",
            "bt709",
            "-colorspace",
            "bt709",
            "-movflags",
            "+faststart",
            "-an",
            str(dest),
        ]
    )


def signal_range(path: Path) -> dict[str, float]:
    proc = subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-i",
            str(path),
            "-vf",
            "signalstats,metadata=print:file=-",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    text = (proc.stderr or "") + (proc.stdout or "")
    found: dict[str, list[float]] = {"YMIN": [], "YMAX": [], "UMIN": [], "UMAX": [], "VMIN": [], "VMAX": []}
    for line in text.splitlines():
        for key in found:
            token = f"signalstats.{key}="
            if token in line:
                try:
                    found[key].append(float(line.split(token, 1)[1].split()[0]))
                except ValueError:
                    pass
    if not found["YMIN"]:
        raise RuntimeError(f"signalstats missing for {path}\n{text[-800:]}")
    return {key: (min(vals) if key.endswith("MIN") else max(vals)) for key, vals in found.items()}


def write_scopes(src: Path, wave: Path, vectors: Path) -> None:
    wave.parent.mkdir(parents=True, exist_ok=True)
    font = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
    run(
        [
            ffmpeg_bin(), "-y", "-hide_banner", "-ss", "0.4", "-i", str(src),
            "-vf",
            "waveform=m=column:d=parade:c=7:f=color:g=green:s=digital,"
            f"scale=1280:720:flags=neighbor,drawtext=fontfile={font}:text=WAVEFORM:x=24:y=24:fontsize=28:fontcolor=white",
            "-frames:v", "1", str(wave),
        ]
    )
    run(
        [
            ffmpeg_bin(), "-y", "-hide_banner", "-ss", "0.4", "-i", str(src),
            "-vf",
            "vectorscope=m=color3:g=color,"
            f"scale=900:900:flags=neighbor,drawtext=fontfile={font}:text=VECTORSCOPE:x=24:y=24:fontsize=28:fontcolor=white",
            "-frames:v", "1", str(vectors),
        ]
    )


def write_split(before: Path, after: Path, dest: Path, label: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    font = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
    filt = (
        f"[0:v]scale=960:1080:flags=lanczos,drawtext=fontfile={font}:text='BEFORE':"
        f"x=32:y=32:fontsize=40:fontcolor=white:box=1:boxcolor=0x00000099[a];"
        f"[1:v]scale=960:1080:flags=lanczos,drawtext=fontfile={font}:text='AFTER  {label}':"
        f"x=32:y=32:fontsize=40:fontcolor=white:box=1:boxcolor=0x00000099[b];"
        "[a][b]hstack,format=yuv420p"
    )
    run(
        [
            ffmpeg_bin(),
            "-y",
            "-hide_banner",
            "-i",
            str(before),
            "-i",
            str(after),
            "-filter_complex",
            filt,
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "medium",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-an",
            str(dest),
        ]
    )
