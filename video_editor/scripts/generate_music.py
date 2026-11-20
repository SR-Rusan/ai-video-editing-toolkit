#!/usr/bin/env python3
"""
generate_music.py - Synthesizes a clean, upbeat, royalty-free instrumental backing track
at 120 BPM with lush Rhodes/synth chords, smooth bassline, and subtle rhythm.
"""

import sys
import os
import wave
import struct
import numpy as np

def generate_background_music(output_path="assets/music/bg_music.wav", duration_sec=60.0):
    sample_rate = 44100
    bpm = 120.0
    beat_dur = 60.0 / bpm # 0.5s per beat, 2.0s per bar
    num_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)

    audio_l = np.zeros(num_samples)
    audio_r = np.zeros(num_samples)

    # Chord Progression: Cmaj7 (C4, E4, G4, B4), Am7 (A3, C4, E4, G4), Fmaj7 (F3, A3, C4, E4), G7 (G3, B3, D4, F4)
    # Chord frequencies
    chords = [
        [261.63, 329.63, 392.00, 493.88], # Cmaj7
        [220.00, 261.63, 329.63, 392.00], # Am7
        [174.61, 220.00, 261.63, 329.63], # Fmaj7
        [196.00, 246.94, 293.66, 349.23]  # G7
    ]
    bass_notes = [130.81, 110.00, 87.31, 98.00] # C3, A2, F2, G2

    bar_dur = beat_dur * 4 # 2.0s per chord
    total_bars = int(np.ceil(duration_sec / bar_dur))

    for bar_idx in range(total_bars):
        chord_idx = bar_idx % len(chords)
        chord_freqs = chords[chord_idx]
        bass_freq = bass_notes[chord_idx]
        
        bar_start_sample = int(bar_idx * bar_dur * sample_rate)
        bar_end_sample = min(num_samples, int((bar_idx + 1) * bar_dur * sample_rate))
        bar_len = bar_end_sample - bar_start_sample
        if bar_len <= 0:
            break

        bar_t = np.linspace(0, bar_len / sample_rate, bar_len, endpoint=False)

        # 1. Warm Synth Electric Piano / Chords with soft tremolo
        chord_signal = np.zeros(bar_len)
        env = np.exp(-0.8 * bar_t) * (1.0 - np.exp(-15.0 * bar_t)) # smooth swell and decay
        
        for f in chord_freqs:
            # Fundamental + soft 2nd harmonic + subtle detuning
            detune = 1.002
            note_sig = 0.5 * np.sin(2 * np.pi * f * bar_t) + 0.2 * np.sin(2 * np.pi * f * 2 * bar_t) + 0.3 * np.sin(2 * np.pi * (f * detune) * bar_t)
            chord_signal += note_sig

        chord_signal *= env * 0.18

        # Stereo spread on chords
        audio_l[bar_start_sample:bar_end_sample] += chord_signal * (1.0 + 0.15 * np.sin(2 * np.pi * 3.0 * bar_t))
        audio_r[bar_start_sample:bar_end_sample] += chord_signal * (1.0 - 0.15 * np.sin(2 * np.pi * 3.0 * bar_t))

        # 2. Bassline with smooth plucked envelope on beats 0 and 2
        for b in [0, 2]:
            b_start = int(b * beat_dur * sample_rate)
            b_len = min(bar_len - b_start, int(beat_dur * 1.8 * sample_rate))
            if b_len > 0:
                bt = np.linspace(0, b_len / sample_rate, b_len, endpoint=False)
                bass_env = np.exp(-3.5 * bt) * (1.0 - np.exp(-30.0 * bt))
                bass_sig = 0.6 * np.sin(2 * np.pi * bass_freq * bt) + 0.25 * np.sin(2 * np.pi * bass_freq * 2 * bt)
                audio_l[bar_start_sample + b_start:bar_start_sample + b_start + b_len] += bass_sig * bass_env * 0.22
                audio_r[bar_start_sample + b_start:bar_start_sample + b_start + b_len] += bass_sig * bass_env * 0.22

    # 3. Subtle rhythm pulse (soft kick on beats 1 & 3, soft shaker on 16th notes)
    total_16ths = int(duration_sec / (beat_dur / 4))
    for step in range(total_16ths):
        step_t = step * (beat_dur / 4)
        step_sample = int(step_t * sample_rate)
        if step_sample >= num_samples:
            break

        # Shaker / hi-hat
        shaker_len = min(num_samples - step_sample, int(0.04 * sample_rate))
        if shaker_len > 0:
            noise = np.random.uniform(-1, 1, shaker_len)
            shaker_env = np.exp(-120.0 * np.linspace(0, shaker_len / sample_rate, shaker_len))
            pan = 0.5 + 0.2 * np.sin(step * 0.7)
            vol = 0.04 if (step % 2 == 0) else 0.02
            audio_l[step_sample:step_sample + shaker_len] += noise * shaker_env * vol * pan
            audio_r[step_sample:step_sample + shaker_len] += noise * shaker_env * vol * (1.0 - pan)

    # Normalize audio cleanly
    max_val = max(np.max(np.abs(audio_l)), np.max(np.abs(audio_r)), 1e-6)
    audio_l = (audio_l / max_val) * 0.85
    audio_r = (audio_r / max_val) * 0.85

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with wave.open(output_path, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        
        interleaved = np.empty((num_samples * 2,), dtype=np.int16)
        interleaved[0::2] = (audio_l * 32767).astype(np.int16)
        interleaved[1::2] = (audio_r * 32767).astype(np.int16)
        wf.writeframes(interleaved.tobytes())

    print(f"Generated upbeat background music track: {output_path} ({duration_sec}s, 120 BPM)", flush=True)
    return output_path

if __name__ == "__main__":
    generate_background_music("assets/music/bg_music.wav", duration_sec=500.0)
