#!/usr/bin/env python3
"""
create_graphics.py - Renders animated motion graphics overlays (RGBA ProRes 4444)
with smooth easing curves (ease-out-cubic, ease-out-back, ease-out-expo),
animated gold bars, pulsing glows, entrance shakes, and typewriter CTA cards.
"""

import sys
import os
import math
import shutil
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def ease_out_cubic(x):
    return 1.0 - (1.0 - x) ** 3

def ease_out_back(x, s=1.5):
    return 1.0 + (s + 1.0) * ((x - 1.0) ** 3) + s * ((x - 1.0) ** 2)

def ease_out_expo(x):
    return 1.0 if x == 1.0 else 1.0 - (2.0 ** (-10.0 * x))

def get_font(size=48, bold=True):
    font_path = "assets/fonts/Montserrat-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Helvetica.ttc"
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def render_clip_from_frames(frames_dir, output_mov_path, fps=30):
    ffmpeg_exe = os.path.expanduser("~/.local/bin/ffmpeg")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    os.makedirs(os.path.dirname(output_mov_path), exist_ok=True)
    cmd = [
        ffmpeg_exe, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-c:v", "prores_ks",
        "-profile:v", "4444",
        "-pix_fmt", "yuva444p10le",
        "-r", str(fps),
        output_mov_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)
    print(f"Rendered motion graphic MOV: {output_mov_path}", flush=True)

# ----------------------------------------------------
# TYPE 1: KEY PHRASE HIGHLIGHT
# ----------------------------------------------------
def render_motion_type1(headline, subtitle, output_mov_path, duration=3.5, fps=30):
    total_frames = int(duration * fps)
    frames_dir = output_mov_path.replace(".mov", "_frames")
    os.makedirs(frames_dir, exist_ok=True)

    font_head = get_font(62, bold=True)
    font_sub = get_font(34, bold=True)
    font_badge = get_font(22, bold=True)

    for f in range(total_frames):
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # In/Out Opacity
        fade_in = min(1.0, f / 9.0)
        fade_out = max(0.0, min(1.0, (total_frames - 1 - f) / 12.0))
        global_alpha = fade_in * fade_out

        # Slide-in from left with ease_out_expo
        slide_prog = min(1.0, f / 18.0)
        slide_x = -600.0 * (1.0 - ease_out_expo(slide_prog))

        # Scale-in overshoot
        scale_prog = min(1.0, f / 22.0)
        scale = ease_out_back(scale_prog, s=1.2) if scale_prog < 1.0 else 1.0

        # Bar width animation: 0 -> 400px ease-out-cubic over 24 frames
        bar_prog = min(1.0, max(0.0, (f - 4) / 20.0))
        bar_w = int(420 * ease_out_cubic(bar_prog))

        # Draw card container
        cx = int(80 + slide_x)
        cy = 340
        cw = 920
        ch = 260

        card_alpha = int(220 * global_alpha)
        if card_alpha > 0:
            # Shadow
            draw.rounded_rectangle([cx+8, cy+8, cx+cw+8, cy+ch+8], radius=24, fill=(0,0,0, int(100*global_alpha)))
            # Main Glass Panel
            draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=24, fill=(12, 18, 28, card_alpha), outline=(255, 215, 0, int(180*global_alpha)), width=2)
            
            # Gold Accent Bar
            if bar_w > 0:
                draw.rounded_rectangle([cx + 36, cy + 30, cx + 36 + bar_w, cy + 36], radius=3, fill=(255, 200, 0, int(255*global_alpha)))

            # Main Headline Text
            head_alpha = int(255 * global_alpha)
            draw.text((cx + 36, cy + 56), headline.upper(), fill=(255, 255, 255, head_alpha), font=font_head)
            
            # Subtitle (Gold) fades in after frame 8
            sub_alpha = int(255 * min(1.0, max(0.0, (f - 8) / 12.0)) * fade_out)
            if sub_alpha > 0:
                draw.text((cx + 36, cy + 155), subtitle, fill=(255, 215, 0, sub_alpha), font=font_sub)

        frame_path = os.path.join(frames_dir, f"frame_{f:05d}.png")
        img.save(frame_path, "PNG")

    render_clip_from_frames(frames_dir, output_mov_path, fps=fps)

# ----------------------------------------------------
# TYPE 2: WARNING / PROBLEM CARD
# ----------------------------------------------------
def render_motion_type2(headline, subtitle, output_mov_path, duration=3.5, fps=30):
    total_frames = int(duration * fps)
    frames_dir = output_mov_path.replace(".mov", "_frames")
    os.makedirs(frames_dir, exist_ok=True)

    font_head = get_font(60, bold=True)
    font_sub = get_font(32, bold=True)
    font_badge = get_font(24, bold=True)

    for f in range(total_frames):
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fade_in = min(1.0, f / 9.0)
        fade_out = max(0.0, min(1.0, (total_frames - 1 - f) / 12.0))
        global_alpha = fade_in * fade_out

        # Slide-in from right
        slide_prog = min(1.0, f / 16.0)
        slide_x = 600.0 * (1.0 - ease_out_expo(slide_prog))

        # Decaying shake effect (entrance shock)
        shake = 0.0
        if f < 15:
            shake = 8.0 * math.sin(f * 2.5) * (1.0 - f / 15.0)

        cx = int(80 + slide_x + shake)
        cy = 340
        cw = 920
        ch = 260

        card_alpha = int(230 * global_alpha)
        if card_alpha > 0:
            # Pulsing Red Glow
            pulse = 0.7 + 0.3 * math.sin(f * 0.3)
            draw.rounded_rectangle([cx-6, cy-6, cx+cw+6, cy+ch+6], radius=28, fill=(255, 40, 40, int(60 * pulse * global_alpha)))
            
            # Dark card with red border
            draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=24, fill=(25, 10, 14, card_alpha), outline=(255, 70, 70, int(220*global_alpha)), width=3)

            # Warning Badge
            draw.rounded_rectangle([cx + 36, cy + 28, cx + 220, cy + 68], radius=8, fill=(255, 50, 50, int(240*global_alpha)))
            draw.text((cx + 50, cy + 34), "⚠️ CAUTION", fill=(255, 255, 255, int(255*global_alpha)), font=font_badge)

            # Headline (Red/White)
            draw.text((cx + 36, cy + 86), headline.upper(), fill=(255, 80, 80, int(255*global_alpha)), font=font_head)
            draw.text((cx + 36, cy + 175), subtitle, fill=(255, 220, 220, int(220*global_alpha)), font=font_sub)

        frame_path = os.path.join(frames_dir, f"frame_{f:05d}.png")
        img.save(frame_path, "PNG")

    render_clip_from_frames(frames_dir, output_mov_path, fps=fps)

# ----------------------------------------------------
# TYPE 3: COMPARISON / SPLIT SCREEN
# ----------------------------------------------------
def render_motion_type3(left_text, right_text, output_mov_path, duration=3.5, fps=30):
    total_frames = int(duration * fps)
    frames_dir = output_mov_path.replace(".mov", "_frames")
    os.makedirs(frames_dir, exist_ok=True)

    font_title = get_font(28, bold=True)
    font_vs = get_font(38, bold=True)

    for f in range(total_frames):
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fade_in = min(1.0, f / 9.0)
        fade_out = max(0.0, min(1.0, (total_frames - 1 - f) / 12.0))
        global_alpha = fade_in * fade_out

        # Left panel slides from left, right panel slides from right
        prog = min(1.0, f / 18.0)
        left_slide = -400.0 * (1.0 - ease_out_expo(prog))
        right_slide = 400.0 * (1.0 - ease_out_expo(prog))

        cy = 320
        pw = 430
        ph = 300

        # Left Panel (Teal #4ECDC4)
        lx = int(80 + left_slide)
        if global_alpha > 0:
            draw.rounded_rectangle([lx, cy, lx+pw, cy+ph], radius=20, fill=(12, 24, 28, int(230*global_alpha)), outline=(78, 205, 196, int(230*global_alpha)), width=3)
            draw.text((lx + 24, cy + 24), "✅ ONLINE REVIEWS", fill=(78, 205, 196, int(255*global_alpha)), font=font_title)
            # Text content
            draw.text((lx + 24, cy + 80), left_text, fill=(255, 255, 255, int(240*global_alpha)), font=get_font(30, bold=False))

        # Right Panel (Red #FF6B6B)
        rx = int(570 + right_slide)
        if global_alpha > 0:
            draw.rounded_rectangle([rx, cy, rx+pw, cy+ph], radius=20, fill=(28, 14, 18, int(230*global_alpha)), outline=(255, 107, 107, int(230*global_alpha)), width=3)
            draw.text((rx + 24, cy + 24), "❌ CLASS REALITY", fill=(255, 107, 107, int(255*global_alpha)), font=font_title)
            draw.text((rx + 24, cy + 80), right_text, fill=(255, 255, 255, int(240*global_alpha)), font=get_font(30, bold=False))

        # Center VS Badge (Overshoot scale)
        vs_prog = min(1.0, max(0.0, (f - 6) / 16.0))
        vs_scale = ease_out_back(vs_prog, s=1.5) if vs_prog < 1.0 else 1.0
        vs_alpha = int(255 * min(1.0, max(0.0, (f - 6) / 8.0)) * fade_out)

        if vs_alpha > 0 and vs_scale > 0.05:
            vcx, vcy = 540, cy + ph // 2
            vr = int(48 * vs_scale)
            draw.ellipse([vcx - vr, vcy - vr, vcx + vr, vcy + vr], fill=(255, 215, 0, vs_alpha), outline=(255, 255, 255, vs_alpha), width=3)
            draw.text((vcx - int(24*vs_scale), vcy - int(20*vs_scale)), "VS", fill=(10, 15, 25, vs_alpha), font=font_vs)

        frame_path = os.path.join(frames_dir, f"frame_{f:05d}.png")
        img.save(frame_path, "PNG")

    render_clip_from_frames(frames_dir, output_mov_path, fps=fps)

# ----------------------------------------------------
# TYPE 4: CALL TO ACTION (CTA)
# ----------------------------------------------------
def render_motion_type4(keyword, subtitle, output_mov_path, duration=4.0, fps=30):
    total_frames = int(duration * fps)
    frames_dir = output_mov_path.replace(".mov", "_frames")
    os.makedirs(frames_dir, exist_ok=True)

    font_prompt = get_font(36, bold=True)
    font_key = get_font(72, bold=True)
    font_sub = get_font(30, bold=True)
    font_emoji = get_font(52, bold=True)

    for f in range(total_frames):
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fade_in = min(1.0, f / 9.0)
        fade_out = max(0.0, min(1.0, (total_frames - 1 - f) / 12.0))
        global_alpha = fade_in * fade_out

        cx = 90
        cy = 560
        cw = 900
        ch = 440

        card_alpha = int(235 * global_alpha)
        if card_alpha > 0:
            # Pulsing Gold Glow behind card
            glow_pulse = 0.7 + 0.3 * math.sin(f * 0.25)
            draw.rounded_rectangle([cx-8, cy-8, cx+cw+8, cy+ch+8], radius=32, fill=(255, 215, 0, int(45 * glow_pulse * global_alpha)))

            # Semi-transparent dark card with gold border
            draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=28, fill=(14, 18, 28, card_alpha), outline=(255, 215, 0, int(220*global_alpha)), width=3)

            # Heart + Comment top icons
            draw.text((cx + 40, cy + 32), "❤️  💬  SAVE", fill=(255, 215, 0, int(240*global_alpha)), font=get_font(28, bold=True))

            # Prompt text
            draw.text((cx + 40, cy + 86), "Like this video & comment:", fill=(255, 255, 255, int(255*global_alpha)), font=font_prompt)

            # Typewriter keyword effect (reveals over 20 frames)
            typewriter_prog = min(1.0, max(0.0, (f - 10) / 20.0))
            chars_to_show = int(len(keyword) * typewriter_prog)
            visible_key = f"\"{keyword[:chars_to_show]}\""
            draw.text((cx + 40, cy + 150), visible_key, fill=(255, 215, 0, int(255*global_alpha)), font=font_key)

            # Subtitle
            draw.text((cx + 40, cy + 270), subtitle, fill=(220, 235, 255, int(220*global_alpha)), font=font_sub)

            # Bouncing down-arrow below card
            bounce_y = int(14.0 * math.sin(f * 0.4))
            draw.text((540 - 24, cy + ch + 20 + bounce_y), "⬇️", fill=(255, 215, 0, int(255*global_alpha)), font=font_emoji)

        frame_path = os.path.join(frames_dir, f"frame_{f:05d}.png")
        img.save(frame_path, "PNG")

    render_clip_from_frames(frames_dir, output_mov_path, fps=fps)

def generate_all_motion_graphics(output_dir="graphics/clips"):
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating Motion Graphic 1: Key Phrase Highlight...")
    render_motion_type1(
        headline="FIRST THING WE DO?",
        subtitle="Check Faculty Reviews on Facebook",
        output_mov_path=os.path.join(output_dir, "motion_01_highlight.mov"),
        duration=3.5
    )

    print("Generating Motion Graphic 2: Warning/Problem...")
    render_motion_type2(
        headline="65.2% FEEL STRESSED",
        subtitle="Negative Reviews Spike Anxiety Before Class",
        output_mov_path=os.path.join(output_dir, "motion_02_warning.mov"),
        duration=3.5
    )

    print("Generating Motion Graphic 3: Split Comparison...")
    render_motion_type3(
        left_text="Strict Grader\nHeavy Workload\nStressful",
        right_text="54% Matched\nStrictness was\nExaggerated!",
        output_mov_path=os.path.join(output_dir, "motion_03_compare.mov"),
        duration=3.5
    )

    print("Generating Motion Graphic 4: Call To Action...")
    render_motion_type4(
        keyword="REVIEW",
        subtitle="We'll send the full research breakdown 🚀",
        output_mov_path=os.path.join(output_dir, "motion_04_cta.mov"),
        duration=4.0
    )

if __name__ == "__main__":
    generate_all_motion_graphics()
