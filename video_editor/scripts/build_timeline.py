#!/usr/bin/env python3
"""
build_timeline.py - Generates Edit Decision List (EDL) and renders timeline specifications,
mapping source timecodes to edited master timecodes with camera zooms and overlays.
"""

import sys
import os
import json

def build_edit_decision_list(transcript_json_path, silence_json_path, analysis_json_path, output_edl_path):
    # Load inputs
    transcript = {}
    if os.path.exists(transcript_json_path):
        with open(transcript_json_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

    silences = {}
    if os.path.exists(silence_json_path):
        with open(silence_json_path, "r", encoding="utf-8") as f:
            silences = json.load(f)

    analysis = {}
    if os.path.exists(analysis_json_path):
        with open(analysis_json_path, "r", encoding="utf-8") as f:
            analysis = json.load(f)

    speech_segments = silences.get("speech_segments", [])
    if not speech_segments and transcript.get("segments"):
        # Use transcript segments as speech segments
        for seg in transcript["segments"]:
            speech_segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "duration": seg["end"] - seg["start"]
            })

    # Build edited timeline mapping
    timeline_events = []
    current_out_time = 0.0

    # Dynamic zooms from analysis
    zooms = analysis.get("dynamic_zooms", [])
    cards = analysis.get("graphic_cards", [])

    for idx, seg in enumerate(speech_segments):
        s_in = seg["start"]
        s_out = seg["end"]
        dur = round(s_out - s_in, 3)
        if dur <= 0.1:
            continue

        out_start = round(current_out_time, 3)
        out_end = round(current_out_time + dur, 3)

        # Check if zoom falls into this segment
        has_zoom = any(z["start"] <= s_in <= z["end"] or s_in <= z["start"] < s_out for z in zooms)
        scale = 1.12 if has_zoom else 1.0

        timeline_events.append({
            "index": idx + 1,
            "type": "talking_head",
            "source_start": s_in,
            "source_end": s_out,
            "timeline_start": out_start,
            "timeline_end": out_end,
            "duration": dur,
            "camera_scale": scale,
            "purpose": "Active speech delivery"
        })

        current_out_time += dur

    # Overlay events (motion graphic cards)
    overlay_events = []
    for c in cards:
        # Find corresponding timeline start/end
        c_src_start = c["start"]
        # Map src time to timeline time
        t_start = None
        for ev in timeline_events:
            if ev["source_start"] <= c_src_start <= ev["source_end"]:
                offset = c_src_start - ev["source_start"]
                t_start = ev["timeline_start"] + offset
                break
        if t_start is None:
            t_start = c_src_start

        overlay_events.append({
            "type": "motion_graphic",
            "timeline_start": round(t_start, 2),
            "timeline_end": round(t_start + 3.0, 2),
            "headline": c.get("headline", ""),
            "badge": c.get("type", "INSIGHT"),
            "asset": c.get("asset_filename", "card_01.png")
        })

    edl_data = {
        "total_source_duration": silences.get("total_duration", 0.0),
        "total_edited_duration": round(current_out_time, 3),
        "total_cuts": len(timeline_events),
        "timeline_events": timeline_events,
        "overlay_events": overlay_events
    }

    os.makedirs(os.path.dirname(output_edl_path), exist_ok=True)
    with open(output_edl_path, "w", encoding="utf-8") as f:
        json.dump(edl_data, f, indent=2)

    print(f"Generated Edit Decision List: {output_edl_path} ({len(timeline_events)} segments, duration: {current_out_time:.2f}s)")
    return edl_data

if __name__ == "__main__":
    t_p = "video_editor/captions/transcript.json"
    s_p = "video_editor/logs/silence_detection.json"
    a_p = "video_editor/logs/content_analysis.json"
    o_p = "video_editor/logs/edit_decision_list.json"
    build_edit_decision_list(t_p, s_p, a_p, o_p)
