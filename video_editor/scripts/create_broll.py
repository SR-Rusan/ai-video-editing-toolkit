#!/usr/bin/env python3
"""
create_broll.py - Creates or formats visual B-roll assets with smooth Ken Burns scale/pan motion.
"""

import sys
import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_concept_broll(title, subtitle, output_mp4_path, duration=3.0, accent_color=(0, 229, 255)):
    """Creates a sleek, animated concept visual for B-roll moments."""
    ffmpeg_exe = os.path.expanduser("~/.local/bin/ffmpeg")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    # 1. Create 1080x1920 high-res background card
    bg_img = Image.new("RGB", (1080, 1920), (8, 12, 20))
    draw = ImageDraw.Draw(bg_img)

    # Gradient / ambient glow circles
    for r in range(500, 100, -30):
        alpha_val = int(25 * (1 - r / 500))
        draw.ellipse([540 - r, 960 - r, 540 + r, 960 + r], fill=(accent_color[0]//4, accent_color[1]//4, accent_color[2]//4))

    # Center card
    card_w, card_h = 920, 520
    cx, cy = (1080 - card_w) // 2, (1920 - card_h) // 2
    draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=32, fill=(16, 24, 38), outline=(255, 255, 255, 50), width=2)

    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw Title & Subtitle
    draw.text((cx + 48, cy + 80), title.upper(), fill=(255, 255, 255), font=font_large)
    draw.text((cx + 48, cy + 180), subtitle, fill=accent_color, font=font_small)

    temp_png = output_mp4_path.replace(".mp4", "_bg.png")
    os.makedirs(os.path.dirname(output_mp4_path), exist_ok=True)
    bg_img.save(temp_png)

    # 2. Render with subtle zoom-in Ken Burns effect (1.0 -> 1.08 over duration)
    total_frames = int(duration * 30)
    cmd = [
        ffmpeg_exe, "-y", "-loop", "1", "-i", temp_png,
        "-vf", f"zoompan=z='min(zoom+0.0005,1.08)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30",
        "-t", str(duration),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        output_mp4_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(temp_png):
        os.remove(temp_png)

    print(f"Generated B-roll clip: {output_mp4_path}")
    return output_mp4_path

if __name__ == "__main__":
    out = "video_editor/broll/broll_concept_01.mp4"
    create_concept_broll("CORE METHODOLOGY", "Streamlined Execution & High Retention", out, 3.0)
