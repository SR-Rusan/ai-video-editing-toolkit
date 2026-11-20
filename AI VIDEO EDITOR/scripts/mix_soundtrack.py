import soundfile as sf
import numpy as np
import scipy.ndimage as ndimage
import time

t0 = time.time()
# Load dialogue
voice, sr = sf.read("AI VIDEO EDITOR/outputs/audio/dialogue_processed.wav")
if len(voice.shape) > 1:
    voice = voice.mean(axis=1)

total_samples = len(voice)
duration = total_samples / sr
print(f"Dialogue length: {duration:.2f}s ({total_samples} samples at {sr} Hz)")

# Load pre-resampled 48k beat
beat, sr_b = sf.read("AI VIDEO EDITOR/inputs/real_beat_48k.wav")
if len(beat) < total_samples:
    reps = int(np.ceil(total_samples / len(beat)))
    beat = np.tile(beat, (reps, 1))
beat = beat[:total_samples]

# Voice RMS envelope computed at 50Hz (every 20ms = 960 samples)
hop = int(sr * 0.02)
num_frames = int(np.ceil(total_samples / hop))
rms_downsampled = np.zeros(num_frames)

for i in range(num_frames):
    chunk = voice[i*hop : (i+1)*hop]
    if len(chunk) > 0:
        rms_downsampled[i] = np.sqrt(np.mean(chunk**2))

# Smooth the downsampled RMS (sigma=7.5 frames = 150ms)
rms_smooth = ndimage.gaussian_filter1d(rms_downsampled, sigma=7.5)

# Ducking gain at 50Hz:
duck_down = np.where(rms_smooth > 0.005, 0.08, 0.20)
duck_down = ndimage.gaussian_filter1d(duck_down, sigma=5.0)

# Upsample ducking gain to full sample rate
duck_gain = np.repeat(duck_down, hop)[:total_samples]

music_ducked = beat * duck_gain[:, np.newaxis]
voice_stereo = np.column_stack([voice, voice])

# SFX cues
sfx_cues = [
    (0.00, "whoosh_punch.wav", 0.50),
    (0.00, "sub_drop.wav", 0.55),
    (0.85, "whoosh_punch.wav", 0.45),
    (6.88, "click_double.wav", 0.45),
    (9.74, "whoosh_whip.wav", 0.50),
    (15.10, "ui_pop.wav", 0.40),
    (21.80, "whoosh_punch.wav", 0.45),
    (25.50, "click_soft.wav", 0.35),
    (30.16, "sub_drop.wav", 0.55),
    (30.16, "click_double.wav", 0.45),
    (34.20, "whoosh_punch.wav", 0.45),
    (42.14, "click_soft.wav", 0.40),
    (53.16, "shutter.wav", 0.45),
    (61.60, "whoosh_whip.wav", 0.50),
    (70.60, "ui_pop.wav", 0.40),
]

sfx_bed = np.zeros((total_samples, 2))

for t_sfx, fname, vol in sfx_cues:
    sfx_path = f"AI VIDEO EDITOR/outputs/audio/sfx/{fname}"
    try:
        sfx_data, sfx_sr = sf.read(sfx_path)
        if len(sfx_data.shape) == 1:
            sfx_data = np.column_stack([sfx_data, sfx_data])
        idx = int(t_sfx * sr)
        l = min(len(sfx_data), total_samples - idx)
        if l > 0:
            sfx_bed[idx:idx+l] += sfx_data[:l] * vol
    except Exception as e:
        print(f"Warning: {fname}: {e}")

# Master sum
mix = voice_stereo + music_ducked + sfx_bed

# Fade out last 0.8s
fade_len = int(sr * 0.8)
mix[-fade_len:] *= np.linspace(1, 0, fade_len)[:, np.newaxis]

peak = np.max(np.abs(mix))
print(f"Raw mix peak: {peak:.4f} ({20*np.log10(peak):.2f} dBFS)")
if peak > 0.89: # limit to -1.0 dBFS
    mix = mix * (0.89 / peak)

sf.write("AI VIDEO EDITOR/outputs/audio/soundtrack_snappy_mastered.wav", mix, sr)
print(f"Exported master in {time.time()-t0:.2f}s to outputs/audio/soundtrack_snappy_mastered.wav ({len(mix)/sr:.2f}s)")
