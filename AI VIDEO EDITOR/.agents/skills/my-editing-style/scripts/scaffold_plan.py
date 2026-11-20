#!/usr/bin/env python3
"""Scaffold an AevyTV-style editing plan from whisper word timestamps.

Usage:
  python scaffold_plan.py clip.words.json --hook "The STRANGEST website on the internet" --out plan.json
"""
import argparse
import json
import os
import sys

def build_plan(words_file, hook_text, out_file=None):
    with open(words_file, 'r', encoding='utf-8') as f:
        words = json.load(f)

    if not words:
        print("Error: No words found in timestamp file.", file=sys.stderr)
        sys.exit(1)

    duration = words[-1]['e']
    effects = []

    # 1. First 3 seconds Hook Plan
    hook_end = min(3.2, duration)
    
    # Find the primary emphasis word in the first 2 seconds (usually between 0.8s and 1.8s)
    first_punch_word = None
    for w in words:
        if 0.7 <= w['s'] <= 1.8 and len(w['w']) > 3:
            first_punch_word = w
            break

    if first_punch_word:
        effects.append({
            "fx": "lean-in",
            "start": round(first_punch_word['s'], 2),
            "end": round(min(first_punch_word['s'] + 1.2, hook_end), 2),
            "zoom": 1.32
        })

    # 2. Pacing Cuts / Zooms across the rest of the clip
    last_cut = hook_end
    is_zoomed = False

    for i, w in enumerate(words):
        t = w['s']
        # Every 2.0 to 3.5 seconds, trigger a cut or visual reframing
        if t - last_cut >= 2.5 and t < duration - 1.5:
            if not is_zoomed:
                # Add punch-in or backdrop word
                if len(w['w']) >= 5 and i % 3 == 0:
                    effects.append({
                        "fx": "backdrop-word",
                        "start": round(t, 2),
                        "end": round(min(t + 1.8, duration), 2),
                        "text": w['w'].upper().strip(".,!?\"'"),
                        "color": "#FFE600",
                        "font": "serif"
                    })
                else:
                    effects.append({
                        "fx": "lean-in",
                        "start": round(t, 2),
                        "end": round(min(t + 1.6, duration), 2),
                        "zoom": 1.28
                    })
                is_zoomed = True
            else:
                is_zoomed = False

            last_cut = t

    plan = {
        "style": "aevytv-storytelling",
        "hook_banner": {
            "text": hook_text,
            "font": "serif",
            "color": "#FFE600",
            "start": 0.0,
            "end": hook_end
        },
        "captions": {
            "style": "pill",
            "bg_color": "rgba(0, 0, 0, 0.85)",
            "text_color": "#FFFFFF",
            "font": "sans-serif",
            "max_words_per_line": 3,
            "y_pos": 0.76
        },
        "audio": {
            "target_lufs": -14.5,
            "true_peak": -0.5,
            "bgm_duck_db": -20.0
        },
        "effects": effects
    }

    out_path = out_file or (os.path.splitext(words_file)[0] + ".plan.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2)

    print(f"Generated editing plan with {len(effects)} visual beats -> {out_path}")
    return plan

def main():
    parser = argparse.ArgumentParser(description="Generate AevyTV-style editing plan from word timestamps")
    parser.add_argument("words_file", help="Path to input.words.json")
    parser.add_argument("--hook", required=True, help="Header hook banner text")
    parser.add_argument("--out", help="Output plan JSON file path")
    args = parser.parse_args()

    build_plan(args.words_file, args.hook, args.out)

if __name__ == "__main__":
    main()
