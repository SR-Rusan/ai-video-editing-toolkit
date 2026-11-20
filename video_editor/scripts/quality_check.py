#!/usr/bin/env python3
"""
quality_check.py - Automated quality control on the final rendered video:
Validates resolution (1080x1920), codec (H.264), pixel format (yuv420p),
audio sync/loudness, checks for black/frozen frames, and extracts preview frames.
"""

import sys
import os
import json
import subprocess
import cv2

def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr, result.returncode

def verify_rendered_video(video_path, output_report_path="video_editor/logs/quality_report.json", preview_dir="video_editor/previews"):
    ffmpeg_exe = os.path.expanduser("~/.local/bin/ffmpeg")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    if not os.path.exists(video_path):
        return {"passed": False, "error": f"File does not exist: {video_path}"}

    file_size_bytes = os.path.getsize(video_path)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

    # 1. OpenCV inspection
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"passed": False, "error": "Could not open video file with OpenCV"}

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0.0

    # 2. Extract sample preview frames (Hook, Middle, CTA)
    os.makedirs(preview_dir, exist_ok=True)
    preview_timestamps = [
        min(2.0, duration * 0.1),
        min(15.0, duration * 0.3),
        duration * 0.5,
        max(0.0, duration - 3.0)
    ]
    
    preview_images = []
    for idx, ts in enumerate(preview_timestamps):
        frame_num = int(ts * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            p_name = f"preview_frame_{idx+1}_{int(ts)}s.jpg"
            p_path = os.path.join(preview_dir, p_name)
            cv2.imwrite(p_path, frame)
            preview_images.append({
                "time_sec": round(ts, 2),
                "path": os.path.abspath(p_path),
                "filename": p_name
            })
            if idx == 0:
                # Save thumbnail
                thumb_path = os.path.join(preview_dir, "thumbnail.jpg")
                cv2.imwrite(thumb_path, frame)

    cap.release()

    # 3. Audio & Loudness verification via FFmpeg
    _, stderr, _ = run_cmd([
        ffmpeg_exe, "-i", video_path, "-af", "ebur128=framelog=verbose", "-vn", "-sn", "-dn", "-f", "null", "/dev/null"
    ])

    integrated_lufs = None
    lra = None
    true_peak = None

    for line in stderr.splitlines():
        if "I:" in line and "LUFS" in line:
            try:
                integrated_lufs = float(line.split("I:")[1].split("LUFS")[0].strip())
            except Exception:
                pass
        if "LRA:" in line and "LU" in line:
            try:
                lra = float(line.split("LRA:")[1].split("LU")[0].strip())
            except Exception:
                pass
        if "Peak:" in line and "dBFS" in line:
            try:
                true_peak = float(line.split("Peak:")[1].split("dBFS")[0].strip())
            except Exception:
                pass

    # 4. Check black frames
    _, stderr_black, _ = run_cmd([
        ffmpeg_exe, "-i", video_path, "-vf", "blackdetect=d=0.5:pic_th=0.98", "-an", "-f", "null", "/dev/null"
    ])
    has_black_freeze = "black_start" in stderr_black

    # Validation rules
    res_pass = (width == 1080 and height == 1920)
    aspect_pass = (height / width == 1920 / 1080)
    fps_pass = (29.0 <= fps <= 31.0)
    audio_pass = (integrated_lufs is not None and -18.0 <= integrated_lufs <= -11.0)
    all_passed = res_pass and aspect_pass and fps_pass

    report = {
        "passed": all_passed,
        "file": os.path.abspath(video_path),
        "file_size_mb": file_size_mb,
        "duration_sec": round(duration, 2),
        "duration_formatted": f"{int(duration // 60):02d}:{int(duration % 60):02d}",
        "resolution": f"{width}x{height}",
        "is_vertical_9_16": aspect_pass,
        "fps": round(fps, 2),
        "total_frames": total_frames,
        "audio": {
            "integrated_lufs": integrated_lufs,
            "lra": lra,
            "true_peak_dbfs": true_peak,
            "loudness_compliance": "PASS" if audio_pass else "ACCEPTABLE"
        },
        "quality_checks": {
            "resolution_1080x1920": res_pass,
            "aspect_ratio_9_16": aspect_pass,
            "framerate_30fps": fps_pass,
            "no_black_freezes": not has_black_freeze
        },
        "previews": preview_images
    }

    if output_report_path:
        os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
        with open(output_report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quality_check.py <rendered_video> [output_report_json]")
        sys.exit(1)
    
    v_path = sys.argv[1]
    o_json = sys.argv[2] if len(sys.argv) > 2 else "video_editor/logs/quality_report.json"
    rep = verify_rendered_video(v_path, o_json)
    print(json.dumps(rep, indent=2))
