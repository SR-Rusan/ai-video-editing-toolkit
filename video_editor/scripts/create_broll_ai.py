#!/usr/bin/env python3
"""
create_broll_ai.py - Renders smooth 120% -> 100% ease-out cubic zoom-out B-roll video clips
from photorealistic AI images with 0.3s fade-in and 0.3s fade-out.
"""

import sys
import os
import shutil
import subprocess
from PIL import Image

def render_broll_clip(
    image_path,
    output_mp4_path,
    duration=3.0,
    fps=30,
    target_w=1080,
    target_h=1920,
    fade_d=0.3
):
    ffmpeg_exe = os.path.expanduser("~/.local/bin/ffmpeg")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"B-roll source image not found: {image_path}")

    img = Image.open(image_path).convert("RGB")
    img_w, img_h = img.size

    # Base bounding box for 9:16 target
    target_aspect = target_w / target_h # 9/16 = 0.5625
    img_aspect = img_w / img_h

    if img_aspect > target_aspect:
        base_crop_h = img_h
        base_crop_w = img_h * target_aspect
    else:
        base_crop_w = img_w
        base_crop_h = img_w / target_aspect

    center_x = img_w / 2.0
    center_y = img_h / 2.0

    total_frames = int(duration * fps)
    temp_frames_dir = os.path.join(os.path.dirname(output_mp4_path), f"temp_frames_{os.path.splitext(os.path.basename(image_path))[0]}")
    os.makedirs(temp_frames_dir, exist_ok=True)

    print(f"Rendering {total_frames} frames for B-roll: {os.path.basename(image_path)} (120% -> 100% zoom-out)...", flush=True)

    for i in range(total_frames):
        progress = i / max(1, (total_frames - 1))
        # Ease-out cubic: eased = 1 - (1 - progress)³
        eased = 1.0 - (1.0 - progress) ** 3
        # Zoom factor: 1.2 -> 1.0
        zoom = 1.2 - 0.2 * eased

        cur_w = base_crop_w / zoom
        cur_h = base_crop_h / zoom

        left = max(0, center_x - cur_w / 2.0)
        top = max(0, center_y - cur_h / 2.0)
        right = min(img_w, center_x + cur_w / 2.0)
        bottom = min(img_h, center_y + cur_h / 2.0)

        if right - left < cur_w:
            if left == 0:
                right = min(img_w, left + cur_w)
            elif right == img_w:
                left = max(0, right - cur_w)
        if bottom - top < cur_h:
            if top == 0:
                bottom = min(img_h, top + cur_h)
            elif bottom == img_h:
                top = max(0, bottom - cur_h)

        crop_box = (int(left), int(top), int(right), int(bottom))
        cropped = img.crop(crop_box)
        resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

        frame_file = os.path.join(temp_frames_dir, f"frame_{i:05d}.png")
        resized.save(frame_file, "PNG")

    os.makedirs(os.path.dirname(output_mp4_path), exist_ok=True)

    fade_out_st = max(0.0, duration - fade_d)
    vf_filter = f"fade=t=in:st=0:d={fade_d},fade=t=out:st={fade_out_st:.2f}:d={fade_d},format=yuv420p"

    cmd = [
        ffmpeg_exe, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%05d.png"),
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        output_mp4_path
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    shutil.rmtree(temp_frames_dir, ignore_errors=True)
    print(f"Successfully created B-roll clip: {output_mp4_path} ({duration}s)", flush=True)
    return output_mp4_path

def generate_all_broll_clips(images_dir="broll/images", output_dir="broll/clips", duration=3.5):
    os.makedirs(output_dir, exist_ok=True)
    image_files = sorted([
        f for f in os.listdir(images_dir) 
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ])

    clips = []
    for idx, img_file in enumerate(image_files):
        img_path = os.path.join(images_dir, img_file)
        out_clip_name = f"broll_clip_{idx+1:02d}.mp4"
        out_clip_path = os.path.join(output_dir, out_clip_name)
        render_broll_clip(img_path, out_clip_path, duration=duration)
        clips.append({
            "index": idx + 1,
            "image": img_path,
            "clip_path": out_clip_path,
            "duration": duration
        })

    return clips

if __name__ == "__main__":
    generate_all_broll_clips()
