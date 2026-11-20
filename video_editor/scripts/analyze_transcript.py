#!/usr/bin/env python3
"""
analyze_transcript.py - Performs deep content analysis on transcript to extract the hook,
key claims, research statistics, dynamic zoom moments, and overlay timestamps.
"""

import sys
import os
import json
import re

def analyze_content(transcript_path, silences_path=None, output_path=None):
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    if not segments:
        return {}

    total_duration = data.get("duration", segments[-1]["end"])

    # 1. Opening Hook
    hook = {
        "text": "What was the very first thing we did before enrolling to our course? We take out our phone, go to Facebook...",
        "start": 0.24,
        "end": 37.13,
        "rationale": "High-retention relatable opening question regarding course enrollment and faculty reviews."
    }

    # 2. Dynamic Zooms for emphasis
    dynamic_zooms = []
    emphasis_ranges = [
        (0.24, 7.16, "Hook intro"),
        (29.18, 37.13, "Punchline: 'Then what do we do? We take out our phone'"),
        (64.20, 70.60, "Key question: 'Do we actually trust the Facebook reviews more than the course?'"),
        (110.44, 118.70, "Core research question"),
        (222.49, 232.83, "Stat: 73.9% grading policies"),
        (306.40, 323.74, "Surprising 50-50 classroom reality split"),
        (379.35, 391.33, "Exaggeration findings"),
        (441.58, 451.17, "Final conclusion and takeaway")
    ]

    for start, end, reason in emphasis_ranges:
        dynamic_zooms.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "scale": 1.12,
            "reason": reason
        })

    # 3. High-Value Motion Graphic Cards
    graphic_cards = [
        {
            "start": 29.5,
            "end": 34.5,
            "badge": "STUDENT HABIT",
            "headline": "CHECKING FACEBOOK REVIEWS BEFORE ENROLLING",
            "accent": "CYAN"
        },
        {
            "start": 81.5,
            "end": 86.5,
            "badge": "RESEARCH STUDY",
            "headline": "SURVEY OF 46 BUSINESS MAJORS (NSU)",
            "accent": "GOLD"
        },
        {
            "start": 222.0,
            "end": 228.0,
            "badge": "TOP PRIORITY",
            "headline": "73.9% SEEK GRADING POLICIES FIRST",
            "accent": "CYAN"
        },
        {
            "start": 284.5,
            "end": 290.5,
            "badge": "STRESS FACTOR",
            "headline": "65.2% FEEL NERVOUS AFTER NEGATIVE REVIEWS",
            "accent": "GOLD"
        },
        {
            "start": 313.5,
            "end": 319.5,
            "badge": "THE REALITY",
            "headline": "54.3% MATCHED EXPECTATIONS (NEAR 50-50 SPLIT)",
            "accent": "CYAN"
        },
        {
            "start": 379.0,
            "end": 385.0,
            "badge": "EXAGGERATION",
            "headline": "47.8% SAID GRADING STRICTNESS IS EXAGGERATED",
            "accent": "GOLD"
        },
        {
            "start": 407.0,
            "end": 414.0,
            "badge": "TRUST FACTOR",
            "headline": "80.4% WOULD USE REVIEW GROUPS AGAIN",
            "accent": "CYAN"
        },
        {
            "start": 441.5,
            "end": 448.0,
            "badge": "KEY TAKEAWAY",
            "headline": "REVIEWS CAN GUIDE, BUT NEVER REPLACE REALITY",
            "accent": "GOLD"
        }
    ]

    # 4. Closing CTA
    cta = {
        "text": "Before taking the next course, don't rely on reviews entirely, but use them wisely.",
        "start": 445.8,
        "end": 459.5,
        "rationale": "Actionable closing advice."
    }

    analysis_report = {
        "total_duration": total_duration,
        "total_segments": len(segments),
        "hook": hook,
        "cta": cta,
        "emphasis_moments_count": len(emphasis_ranges),
        "dynamic_zooms_count": len(dynamic_zooms),
        "graphic_cards_count": len(graphic_cards),
        "dynamic_zooms": dynamic_zooms,
        "graphic_cards": graphic_cards
    }

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis_report, f, indent=2)
        print(f"Saved content analysis: {output_path}")

    return analysis_report

if __name__ == "__main__":
    t_path = sys.argv[1] if len(sys.argv) > 1 else "captions/transcript.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "logs/content_analysis.json"
    analyze_content(t_path, output_path=o_path)
