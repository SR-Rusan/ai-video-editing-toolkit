#!/usr/bin/env python3
"""
detect_silence.py - Analyzes silences and applies FFmpeg silenceremove filter:
silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-35dB
Parameters:
- stop_duration: 0.4s (remove silences longer than 400ms)
- stop_threshold: -35dB (conservative — don't cut breath pauses)
Preserves original audio track for later mixing.
"""

import sys
import os
import json
import re
import subprocess

def detect_and_trim_silences(
    input_video_path,
    output_trimmed_audio_path="temp/speech_trimmed_audio.wav",
    output_json="logs/silence_detection.json",
    stop_duration=0.4,
    stop_threshold_db=-35
):
    ffmpeg_exe = os.path.expanduser("~/.local/bin/ffmpeg")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    os.makedirs(os.path.dirname(output_trimmed_audio_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_json), exist_ok=True)

    # 1. Apply silenceremove filter to audio
    filter_str = f"silenceremove=stop_periods=-1:stop_duration={stop_duration}:stop_threshold={stop_threshold_db}dB"
    cmd_trim = [
        ffmpeg_exe, "-y",
        "-i", input_video_path,
        "-af", filter_str,
        "-vn",
        "-c:a", "pcm_s16le",
        "-ar", "44100",
        output_trimmed_audio_path
    ]
    subprocess.run(cmd_trim, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # 2. Run silencedetect to parse timestamps
    cmd_detect = [
        ffmpeg_exe, "-i", input_video_path,
        "-af", f"silencedetect=noise={stop_threshold_db}dB:d={stop_duration}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd_detect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stderr = res.stderr

    # Parse total duration
    dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", stderr)
    total_duration = 0.0
    if dur_match:
        h, m, s = dur_match.groups()
        total_duration = int(h) * 3600 + int(m) * 60 + float(s)

    silences = []
    current_start = None
    
    for line in stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([0-9.]+)", line)
            if m:
                current_start = float(m.group(1))
        elif "silence_end:" in line:
            m_end = re.search(r"silence_end:\s*([0-9.]+)", line)
            m_dur = re.search(r"silence_duration:\s*([0-9.]+)", line)
            if m_end and current_start is not None:
                end_time = float(m_end.group(1))
                dur = float(m_dur.group(1)) if m_dur else (end_time - current_start)
                silences.append({
                    "start": round(current_start, 3),
                    "end": round(end_time, 3),
                    "duration": round(dur, 3)
                })
                current_start = None

    total_silence_time = sum(s["duration"] for s in silences)
    trimmed_duration = max(0.0, total_duration - total_silence_time)

    data = {
        "source": os.path.abspath(input_video_path),
        "total_raw_duration": round(total_duration, 2),
        "total_silence_duration": round(total_silence_time, 2),
        "trimmed_speech_duration": round(trimmed_duration, 2),
        "silences_count": len(silences),
        "stop_duration": stop_duration,
        "stop_threshold_db": stop_threshold_db,
        "silences": silences,
        "trimmed_audio_path": os.path.abspath(output_trimmed_audio_path)
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Silence Removal Complete: Raw {total_duration:.2f}s -> Trimmed {trimmed_duration:.2f}s ({len(silences)} silences removed)")
    return data

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "/Users/rusan/Documents/testing.mov"
    detect_and_trim_silences(inp)
