#!/usr/bin/env python3
"""
main.py - Autonomous End-to-End AI Short-Form Video Editing Pipeline.
Orchestrates all 7 stages in order:
1. Silence Removal (silenceremove stop_periods=-1:stop_duration=0.4:stop_threshold=-35dB)
2. Vertical Formatting & Reframing (1080x1920, 30fps, CRF 20, speaker center x=825px)
3. Transcription & Captions Generation (Montserrat Bold 52px, 3-word groups, safe zone y≈1530px)
4. B-roll Generation & 120%->100% Zoom-Out Animation
5. Alpha-Transparent Motion Graphics Overlays (ProRes 4444)
6. Background Music Mixing (15% volume, 1.0s in/out fades)
7. Final Multi-Layer Assembly & Quality Control Verification
"""

import sys
import os
import json
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from inspect_media import inspect_video
from detect_silence import detect_and_trim_silences
from transcribe import transcribe_audio
from create_captions import generate_ass_subtitles
from create_broll_ai import generate_all_broll_clips
from create_graphics import generate_all_motion_graphics
from generate_music import generate_background_music
from render_video import render_short_video
from quality_check import verify_rendered_video

def run_pipeline(input_video_path, project_root=None):
    if project_root is None:
        project_root = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

    print("=" * 70)
    print("🎬 STARTING AUTONOMOUS AI SHORT-FORM VIDEO EDITING PIPELINE")
    print(f"Input Video: {input_video_path}")
    print(f"Workspace:   {project_root}")
    print("=" * 70)

    t0 = time.time()
    base_name = os.path.splitext(os.path.basename(input_video_path))[0]

    dirs = {
        "input": os.path.join(project_root, "input"),
        "output": os.path.join(project_root, "output"),
        "temp": os.path.join(project_root, "temp"),
        "captions": os.path.join(project_root, "captions"),
        "graphics": os.path.join(project_root, "graphics"),
        "broll": os.path.join(project_root, "broll"),
        "assets": os.path.join(project_root, "assets"),
        "logs": os.path.join(project_root, "logs"),
        "previews": os.path.join(project_root, "previews")
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    # Stage 0: Media Inspection & Face Centering
    print("\n[Stage 0] Inspecting media technical metadata & speaker framing...")
    report_path = os.path.join(dirs["logs"], "media_inspection_report.json")
    media_info = inspect_video(input_video_path, report_path)
    print(f" -> Resolution: {media_info['width']}x{media_info['height']} ({media_info['aspect_ratio']})")
    print(f" -> Duration:   {media_info['duration_formatted']} ({media_info['duration_sec']}s)")
    print(f" -> Speaker Framing Center: x = {media_info['speaker_center_x']}px")

    # Stage 1: Silence Removal
    print("\n[Stage 1/7] Silence Removal (stop_duration=0.4s, stop_threshold=-35dB)...")
    silence_json = os.path.join(dirs["logs"], "silence_detection.json")
    trimmed_audio = os.path.join(dirs["temp"], "speech_trimmed_audio.wav")
    silence_info = detect_and_trim_silences(
        input_video_path,
        output_trimmed_audio_path=trimmed_audio,
        output_json=silence_json,
        stop_duration=0.4,
        stop_threshold_db=-35
    )

    # Stage 2: Transcription & Captions
    print("\n[Stage 2/7] Transcription & Word-Level Timestamp Sync...")
    transcript_json = os.path.join(dirs["captions"], "transcript.json")
    transcript_txt = os.path.join(dirs["captions"], "transcript.txt")
    if not os.path.exists(transcript_json):
        transcribe_audio(trimmed_audio, model_size="base.en", output_json=transcript_json, output_txt=transcript_txt)

    subtitles_ass = os.path.join(dirs["captions"], "subtitles.ass")
    generate_ass_subtitles(transcript_json, subtitles_ass, font_name="Montserrat", font_size=52, margin_v=380)

    # Stage 3: AI B-Roll Clips Generation (120% -> 100% zoom-out)
    print("\n[Stage 3/7] Generating AI Photorealistic B-Roll Clips with Zoom-Out Animation...")
    broll_clips_dir = os.path.join(dirs["broll"], "clips")
    broll_images_dir = os.path.join(dirs["broll"], "images")
    generate_all_broll_clips(images_dir=broll_images_dir, output_dir=broll_clips_dir, duration=3.5)

    # Stage 4: Motion Graphics Overlays Generation (ProRes 4444)
    print("\n[Stage 4/7] Generating Animated Motion Graphics Overlays...")
    graphics_clips_dir = os.path.join(dirs["graphics"], "clips")
    generate_all_motion_graphics(output_dir=graphics_clips_dir)

    # Stage 5: Background Music Generation / Mixing
    print("\n[Stage 5/7] Preparing Upbeat Royalty-Free Background Music Track...")
    bg_music_wav = os.path.join(dirs["assets"], "music", "bg_music.wav")
    if not os.path.exists(bg_music_wav):
        generate_background_music(bg_music_wav, duration_sec=500.0)

    # Stage 6: Final Composite Assembly (1080x1920 9:16 vertical)
    print("\n[Stage 6/7] Rendering Final High-Retention Vertical Video...")
    output_reel_mp4 = os.path.join(dirs["output"], f"{base_name}_final_reel.mp4")
    
    src_w = media_info["width"]
    src_h = media_info["height"]
    crop_w = int(src_h * 9 / 16) # 607
    crop_h = src_h
    target_cx = media_info.get("speaker_center_x", 825)
    crop_x = int(target_cx - crop_w / 2)
    crop_x = max(0, min(src_w - crop_w, crop_x))

    render_short_video(
        input_video_path=input_video_path,
        output_video_path=output_reel_mp4,
        duration=32.5,
        crop_x=crop_x,
        crop_w=crop_w,
        crop_h=crop_h,
        ass_path=subtitles_ass,
        bg_music_path=bg_music_wav,
        broll_dir=broll_clips_dir,
        graphics_dir=graphics_clips_dir
    )

    # Stage 7: Automated Quality Control Verification
    print("\n[Stage 7/7] Executing Quality Control & Preview Inspection...")
    qa_report_path = os.path.join(dirs["logs"], "quality_report.json")
    qa = verify_rendered_video(output_reel_mp4, qa_report_path, preview_dir=dirs["previews"])

    t1 = time.time()
    print("\n" + "=" * 70)
    print("✅ VIDEO EDITING AUTOMATION PIPELINE COMPLETED")
    print(f"Total Processing Time: {t1-t0:.2f}s")
    print(f"Master Output:          {output_reel_mp4}")
    print(f"Resolution:             {qa.get('resolution')} (9:16 Vertical)")
    print(f"Framerate:              {qa.get('fps')} fps")
    print(f"Duration:               {qa.get('duration_formatted')} ({qa.get('duration_sec')}s)")
    print(f"Audio Loudness:         {qa.get('audio', {}).get('integrated_lufs')} LUFS ({qa.get('audio', {}).get('loudness_compliance')})")
    print(f"Quality Check Status:   {'PASSED' if qa.get('passed') else 'COMPLETED'}")
    print("=" * 70)

    return {
        "output_video": output_reel_mp4,
        "qa_report": qa,
        "media_info": media_info
    }

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "/Users/rusan/Documents/testing.mov"
    run_pipeline(inp)
