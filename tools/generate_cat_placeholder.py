#!/usr/bin/env python3
"""Generate original transparent placeholder cat PNG assets for loader testing."""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PET_ROOT = ROOT / "VPet-Simulator.Windows" / "mod" / "0000_core" / "pet" / "cat"
SIZE = 500


ANIMATIONS = {
    "Default": ["cat_default_000_125.png"],
    "IDEL/Boring": ["cat_boring_000_125.png", "cat_boring_001_125.png"],
    "IDEL/Squat": ["cat_squat_000_125.png"],
    "Sleep/A": ["cat_sleep_000_125.png"],
    "Move/walk.left": ["cat_walk_left_000_125.png", "cat_walk_left_001_125.png"],
    "Move/walk.right": ["cat_walk_right_000_125.png", "cat_walk_right_001_125.png"],
    "Raised/Static": ["cat_raised_static_000_125.png"],
    "Touch/Head": ["cat_touch_head_000_125.png"],
    "Touch/Body": ["cat_touch_body_000_125.png"],
}


def chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path: Path, pixels: bytearray) -> None:
    rows = bytearray()
    stride = SIZE * 4
    for y in range(SIZE):
        rows.append(0)
        rows.extend(pixels[y * stride : (y + 1) * stride])
    payload = b"\x89PNG\r\n\x1a\n"
    payload += chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0))
    payload += chunk(b"IDAT", zlib.compress(bytes(rows), 9))
    payload += chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def set_pixel(pixels: bytearray, x: int, y: int, color: tuple[int, int, int, int]) -> None:
    if 0 <= x < SIZE and 0 <= y < SIZE:
        idx = (y * SIZE + x) * 4
        pixels[idx : idx + 4] = bytes(color)


def fill_circle(pixels: bytearray, cx: int, cy: int, radius: int, color: tuple[int, int, int, int]) -> None:
    r2 = radius * radius
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                set_pixel(pixels, x, y, color)


def fill_ellipse(pixels: bytearray, cx: int, cy: int, rx: int, ry: int, color: tuple[int, int, int, int]) -> None:
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                set_pixel(pixels, x, y, color)


def fill_triangle(pixels: bytearray, points: tuple[tuple[int, int], tuple[int, int], tuple[int, int]], color: tuple[int, int, int, int]) -> None:
    (x1, y1), (x2, y2), (x3, y3) = points
    min_x, max_x = max(0, min(x1, x2, x3)), min(SIZE - 1, max(x1, x2, x3))
    min_y, max_y = max(0, min(y1, y2, y3)), min(SIZE - 1, max(y1, y2, y3))
    denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denom
            b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denom
            c = 1 - a - b
            if a >= 0 and b >= 0 and c >= 0:
                set_pixel(pixels, x, y, color)


def draw_line(pixels: bytearray, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int, int], width: int = 3) -> None:
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for i in range(steps + 1):
        t = i / steps
        x = round(x1 + (x2 - x1) * t)
        y = round(y1 + (y2 - y1) * t)
        fill_circle(pixels, x, y, width, color)


def draw_cat(path: Path, pose: str, frame: int) -> None:
    pixels = bytearray(SIZE * SIZE * 4)
    fur = (235, 186, 116, 255)
    fur_dark = (190, 132, 74, 255)
    inner = (245, 165, 150, 255)
    ink = (57, 47, 40, 255)

    bob = 4 if frame % 2 else 0
    body_y = 312 + bob
    head_y = 210 + bob
    if "sleep" in pose:
        body_y = 330
        head_y = 262
    if "squat" in pose:
        body_y = 336
        head_y = 230
    if "raised" in pose:
        body_y = 300
        head_y = 190

    fill_ellipse(pixels, 250, body_y, 88, 78, fur)
    fill_circle(pixels, 250, head_y, 74, fur)
    fill_triangle(pixels, ((192, head_y - 35), (216, head_y - 112), (244, head_y - 54)), fur)
    fill_triangle(pixels, ((256, head_y - 54), (284, head_y - 112), (308, head_y - 35)), fur)
    fill_triangle(pixels, ((207, head_y - 49), (219, head_y - 83), (235, head_y - 56)), inner)
    fill_triangle(pixels, ((265, head_y - 56), (281, head_y - 83), (293, head_y - 49)), inner)

    if "sleep" in pose:
        draw_line(pixels, 218, head_y - 4, 238, head_y - 4, ink, 2)
        draw_line(pixels, 262, head_y - 4, 282, head_y - 4, ink, 2)
    else:
        fill_circle(pixels, 226, head_y - 8, 8, ink)
        fill_circle(pixels, 274, head_y - 8, 8, ink)
    fill_circle(pixels, 250, head_y + 12, 5, ink)
    draw_line(pixels, 250, head_y + 18, 238, head_y + 28, ink, 2)
    draw_line(pixels, 250, head_y + 18, 262, head_y + 28, ink, 2)

    for side in (-1, 1):
        draw_line(pixels, 250 + side * 18, head_y + 16, 250 + side * 66, head_y + 6, fur_dark, 2)
        draw_line(pixels, 250 + side * 18, head_y + 24, 250 + side * 70, head_y + 26, fur_dark, 2)

    leg_offset = 10 if frame % 2 else -6
    draw_line(pixels, 215, body_y + 58, 205 + leg_offset, body_y + 95, fur_dark, 6)
    draw_line(pixels, 285, body_y + 58, 295 - leg_offset, body_y + 95, fur_dark, 6)
    draw_line(pixels, 323, body_y - 8, 375, body_y - 48, fur_dark, 8)
    fill_circle(pixels, 381, body_y - 52, 12, fur_dark)

    if "touch" in pose:
        fill_circle(pixels, 250, head_y - 128, 18, (130, 185, 235, 210))
    if "boring" in pose:
        draw_line(pixels, 206, body_y + 20, 180, body_y + 38, fur_dark, 5)
    if "raised" in pose:
        draw_line(pixels, 185, body_y - 28, 145, body_y - 82, fur_dark, 5)
        draw_line(pixels, 315, body_y - 28, 355, body_y - 82, fur_dark, 5)

    write_png(path, pixels)


def main() -> None:
    for rel_dir, names in ANIMATIONS.items():
        for i, name in enumerate(names):
            draw_cat(PET_ROOT / rel_dir / name, rel_dir.lower(), i)


if __name__ == "__main__":
    main()
