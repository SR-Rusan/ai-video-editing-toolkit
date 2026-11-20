#!/usr/bin/env python3
"""
render_video.py - Assembles the full multi-layer video editing pipeline via FFmpeg:
1. Vertical 9:16 crop & speaker centering (1080x1920, 30fps, CRF 20)
2. Dynamic 15% punch-in zoom moments in gap intervals
3. Burned-in ASS captions (Montserrat Bold 52px, safe zone y≈1530px)
4. AI B-roll clips (120%->100% cubic zoom-out + 0.3s fades)
5. ProRes 4444 RGBA Motion Graphics overlays
6. Background music mixed at 15% volume (-20dB) with 1.0s in/out fades
"""

import sys
import os
import json
import subprocess

def render_short_video(
    input_video_path,
    output_video_path,
    duration=32.5,
    crop_x=521,
    crop_w=607,
    crop_h=1080,
    ass_path="captions/subtitles.ass",
    bg_music_path="assets/music/bg_music.wav",
    broll_dir="broll/clips",
    graphics_dir="graphics/clips"
):
    ffmpeg_exe = os.path.expanduser("~/.local/bin/ffmpeg")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    # Timeline schedule (32.5s Short/Reel)
    # Motion 1: 0.5 - 3.5s (dur 3.0s)
    # Zoom 1:   3.5 - 4.5s
    # B-roll 1: 4.5 - 7.5s (dur 3.0s)
    # Gap:      7.5 - 8.2s
    # B-roll 2: 8.2 - 11.5s (dur 3.3s)
    # Zoom 2:   11.5 - 12.2s
    # Motion 2: 12.2 - 15.5s (dur 3.3s)
    # Zoom 3:   15.5 - 16.5s
    # Motion 3: 16.5 - 20.0s (dur 3.5s)
    # B-roll 3: 20.0 - 23.5s (dur 3.5s)
    # Zoom 4:   23.5 - 24.2s
    # B-roll 4: 24.2 - 27.5s (dur 3.3s)
    # Zoom 5:   27.5 - 28.2s
    # Motion 4: 28.2 - 32.2s (dur 4.0s)

    broll1 = os.path.join(broll_dir, "broll_clip_01.mp4")
    broll2 = os.path.join(broll_dir, "broll_clip_02.mp4")
    broll3 = os.path.join(broll_dir, "broll_clip_03.mp4")
    broll4 = os.path.join(broll_dir, "broll_clip_04.mp4")

    m1 = os.path.join(graphics_dir, "motion_01_highlight.mov")
    m2 = os.path.join(graphics_dir, "motion_02_warning.mov")
    m3 = os.path.join(graphics_dir, "motion_03_compare.mov")
    m4 = os.path.join(graphics_dir, "motion_04_cta.mov")

    inputs = [
        "-ss", "0.0", "-t", str(duration), "-i", input_video_path, # 0
        "-itsoffset", "4.5", "-i", broll1,                         # 1
        "-itsoffset", "8.2", "-i", broll2,                         # 2
        "-itsoffset", "20.0", "-i", broll3,                        # 3
        "-itsoffset", "24.2", "-i", broll4,                        # 4
        "-itsoffset", "0.5", "-i", m1,                             # 5
        "-itsoffset", "12.2", "-i", m2,                            # 6
        "-itsoffset", "16.5", "-i", m3,                            # 7
        "-itsoffset", "28.2", "-i", m4,                            # 8
        "-i", bg_music_path                                        # 9
    ]

    # Zoom crop parameters (15% punch-in)
    zoom_w = int(crop_w / 1.15) # 527
    zoom_h = int(crop_h / 1.15) # 939
    zoom_x = crop_x + int((crop_w - zoom_w) / 2) # 561
    zoom_y = int((crop_h - zoom_h) / 2)          # 70

    escaped_ass = ass_path.replace(":", "\\:").replace("'", "\\'")

    # Zoom intervals
    zoom_expr = "between(t,3.5,4.5)+between(t,11.5,12.2)+between(t,15.5,16.5)+between(t,23.5,24.2)+between(t,27.5,28.2)"

    fade_out_start = max(0.0, duration - 1.0)

    filter_complex = [
        # 1. Base Normal & Zoom
        f"[0:v]crop={crop_w}:{crop_h}:{crop_x}:0,scale=1080:1920:flags=lanczos,format=yuv420p[base_norm]",
        f"[0:v]crop={zoom_w}:{zoom_h}:{zoom_x}:{zoom_y},scale=1080:1920:flags=lanczos,format=yuv420p[base_zoom]",
        f"[base_norm][base_zoom]overlay=enable='{zoom_expr}'[v_zoomed]",
        
        # 2. Burn ASS Subtitles
        f"[v_zoomed]ass='{escaped_ass}'[v_caps]",

        # 3. Chain B-Roll Overlays
        f"[v_caps][1:v]overlay=enable='between(t,4.5,7.5)'[v_b1]",
        f"[v_b1][2:v]overlay=enable='between(t,8.2,11.5)'[v_b2]",
        f"[v_b2][3:v]overlay=enable='between(t,20.0,23.5)'[v_b3]",
        f"[v_b3][4:v]overlay=enable='between(t,24.2,27.5)'[v_b4]",

        # 4. Chain Motion Graphics Overlays
        f"[v_b4][5:v]overlay=enable='between(t,0.5,3.5)'[v_m1]",
        f"[v_m1][6:v]overlay=enable='between(t,12.2,15.5)'[v_m2]",
        f"[v_m2][7:v]overlay=enable='between(t,16.5,20.0)'[v_m3]",
        f"[v_m3][8:v]overlay=enable='between(t,28.2,32.2)'[v_final]",

        # 5. Audio: speech filter + bg music mixed at 15% (-20dB)
        f"[0:a]highpass=f=80,lowpass=f=12000,loudnorm=I=-14:LRA=7:TP=-1.0[a_voice]",
        f"[9:a]volume=0.15,afade=t=in:st=0:d=1.0,afade=t=out:st={fade_out_start:.2f}:d=1.0[a_music]",
        f"[a_voice][a_music]amix=inputs=2:duration=first:dropout_transition=2[a_final]"
    ]

    filter_complex_str = ";".join(filter_complex)

    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

    cmd = [
        ffmpeg_exe, "-y",
        *inputs,
        "-filter_complex", filter_complex_str,
        "-map", "[v_final]",
        "-map", "[a_final]",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-movflags", "+faststart",
        "-t", str(duration),
        output_video_path
    ]

    print(f"Rendering high-retention vertical Reel ({duration}s): {output_video_path}...")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if proc.returncode != 0:
        print("FFmpeg stderr:", proc.stderr)
        raise RuntimeError(f"FFmpeg render failed with exit code {proc.returncode}")

    print(f"Render completed successfully: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "/Users/rusan/Documents/testing.mov"
    out = sys.argv[2] if len(sys.argv) > 2 else "output/testing_final_reel.mp4"
    render_short_video(inp, out)
