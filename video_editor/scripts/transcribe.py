#!/usr/bin/env python3
"""
transcribe.py - Transcribes audio with word-level timestamps using Faster-Whisper,
with real-time progress logging and multi-threaded CPU acceleration.
"""

import sys
import os
import json
from faster_whisper import WhisperModel

def transcribe_audio(audio_path, model_size="base.en", output_json=None, output_txt=None):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Loading Whisper model: {model_size} with 4 threads...", flush=True)
    model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=4)

    print(f"Transcribing {audio_path}...", flush=True)
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    print(f"Detected language: {info.language} (p={info.language_probability:.2f}), duration: {info.duration:.2f}s", flush=True)

    structured_segments = []
    full_text_list = []

    for seg in segments:
        words = []
        if seg.words:
            for w in seg.words:
                words.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3)
                })
        
        seg_dict = {
            "id": seg.id,
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "text": seg.text.strip(),
            "words": words
        }
        structured_segments.append(seg_dict)
        full_text_list.append(seg.text.strip())
        print(f"[{seg.start:06.2f}s -> {seg.end:06.2f}s] {seg.text.strip()}", flush=True)

    full_text = " ".join(full_text_list)

    transcript_data = {
        "language": info.language,
        "language_probability": round(info.language_probability, 3),
        "duration": round(info.duration, 2),
        "full_text": full_text,
        "segments": structured_segments
    }

    if output_json:
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(transcript_data, f, indent=2)
        print(f"Saved structured transcript to {output_json}", flush=True)

    if output_txt:
        os.makedirs(os.path.dirname(output_txt), exist_ok=True)
        with open(output_txt, "w", encoding="utf-8") as f:
            for s in structured_segments:
                f.write(f"[{s['start']:06.2f} - {s['end']:06.2f}] {s['text']}\n")
        print(f"Saved text transcript to {output_txt}", flush=True)

    return transcript_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_path> [output_json] [output_txt] [model_size]")
        sys.exit(1)
    
    aud = sys.argv[1]
    out_j = sys.argv[2] if len(sys.argv) > 2 else "video_editor/captions/transcript.json"
    out_t = sys.argv[3] if len(sys.argv) > 3 else "video_editor/captions/transcript.txt"
    mod = sys.argv[4] if len(sys.argv) > 4 else "base.en"

    transcribe_audio(aud, model_size=mod, output_json=out_j, output_txt=out_t)
