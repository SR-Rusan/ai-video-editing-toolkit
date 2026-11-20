#!/usr/bin/env python3
"""
create_captions.py - Generates clean, modern 3-word ASS subtitle events
styled with Montserrat Bold (52px, White, 3px Black Outline, 2px Shadow)
in the Instagram/TikTok safe zone (y ≈ 1530px).
"""

import sys
import os
import json

def format_ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    centisecs = int((secs - int(secs)) * 100)
    return f"{hours:d}:{minutes:02d}:{int(secs):02d}.{centisecs:02d}"

def generate_ass_subtitles(transcript_json_path, output_ass_path, font_name="Montserrat", font_size=52, margin_v=380):
    if not os.path.exists(transcript_json_path):
        raise FileNotFoundError(f"Transcript not found: {transcript_json_path}")

    with open(transcript_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ASS Header exactly following specification
    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{font_name},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,40,40,{margin_v},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    all_words = []
    for seg in data.get("segments", []):
        if "words" in seg and seg["words"]:
            all_words.extend(seg["words"])
        else:
            words_in_seg = seg["text"].split()
            dur = seg["end"] - seg["start"]
            w_dur = dur / max(1, len(words_in_seg))
            for i, w in enumerate(words_in_seg):
                all_words.append({
                    "word": w,
                    "start": round(seg["start"] + i * w_dur, 3),
                    "end": round(seg["start"] + (i + 1) * w_dur, 3)
                })

    if not all_words:
        print("No words found in transcript.")
        return

    # Clean, 3 words grouping
    chunks = []
    current_chunk = []
    
    for w in all_words:
        clean_word = w["word"].strip()
        if not clean_word:
            continue
        current_chunk.append(w)
        if len(current_chunk) >= 3:
            chunks.append(current_chunk)
            current_chunk = []

    if current_chunk:
        chunks.append(current_chunk)

    for chunk in chunks:
        start_t = chunk[0]["start"]
        end_t = chunk[-1]["end"]
        # Ensure positive duration
        if end_t <= start_t:
            end_t = start_t + 0.5
        
        words_text = " ".join([cw["word"].strip().upper() for cw in chunk])
        start_str = format_ass_time(start_t)
        end_str = format_ass_time(end_t)
        
        ass_lines.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{words_text}")

    os.makedirs(os.path.dirname(output_ass_path), exist_ok=True)
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")

    print(f"Generated ASS captions: {output_ass_path} ({len(chunks)} 3-word subtitle events)", flush=True)

if __name__ == "__main__":
    t_json = sys.argv[1] if len(sys.argv) > 1 else "captions/transcript.json"
    o_ass = sys.argv[2] if len(sys.argv) > 2 else "captions/subtitles.ass"
    generate_ass_subtitles(t_json, o_ass)
