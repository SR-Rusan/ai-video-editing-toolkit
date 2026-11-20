import soundfile as sf
import numpy as np
import json

data, sr = sf.read("AI VIDEO EDITOR/outputs/audio/dialogue_raw.wav")
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Find speech energy
frame_len = int(sr * 0.025)
hop_len = int(sr * 0.010)

rms = []
times = []
for i in range(0, len(data) - frame_len, hop_len):
    f = data[i:i+frame_len]
    r = np.sqrt(np.mean(f**2))
    rms.append(r)
    times.append(i / sr)

rms = np.array(rms)
times = np.array(times)
max_rms = np.max(rms)

# Dialogue threshold: RMS > 0.007 (approx -20dB to -22dB from peak)
is_speech = rms > 0.0075

# Fill gaps < 0.20s (speech pauses within words/syllables)
gap_frames = int(0.20 / 0.010)
s_smooth = is_speech.copy()
i = 0
while i < len(s_smooth):
    if not s_smooth[i]:
        st = i
        while i < len(s_smooth) and not s_smooth[i]:
            i += 1
        if i - st < gap_frames:
            s_smooth[st:i] = True
    else:
        i += 1

# Minimum speech burst: 0.15s
burst_frames = int(0.15 / 0.010)
i = 0
while i < len(s_smooth):
    if s_smooth[i]:
        st = i
        while i < len(s_smooth) and s_smooth[i]:
            i += 1
        if i - st < burst_frames:
            s_smooth[st:i] = False
    else:
        i += 1

# Build list of active segments with 0.05s head and 0.06s tail padding
raw_segments = []
in_seg = False
seg_start = 0.0

for t, s in zip(times, s_smooth):
    if s and not in_seg:
        in_seg = True
        seg_start = max(0.0, t - 0.05)
    elif not s and in_seg:
        in_seg = False
        seg_end = min(len(data)/sr, t + 0.06)
        raw_segments.append((seg_start, seg_end))
if in_seg:
    raw_segments.append((seg_start, len(data)/sr))

# Merge overlapping or close segments (< 0.10s)
merged = []
for s, e in raw_segments:
    if not merged:
        merged.append([s, e])
    else:
        if s <= merged[-1][1] + 0.10:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])

print(f"Total snappy speech cuts: {len(merged)}")
total_dur = sum(e - s for s, e in merged)
print(f"Trimmed duration: {total_dur:.2f}s (removed {len(data)/sr - total_dur:.2f}s of silence!)")

# Assemble the cut audio with 15ms crossfade
xfade_len = int(sr * 0.015)
window_in = np.linspace(0, 1, xfade_len)
window_out = np.linspace(1, 0, xfade_len)

assembled_audio = []
cut_metadata = []
curr_timeline = 0.0

for idx, (s, e) in enumerate(merged):
    s_idx = int(s * sr)
    e_idx = int(e * sr)
    chunk = data[s_idx:e_idx].copy()
    
    # Apply soft fades at edges
    if len(chunk) > 2 * xfade_len:
        chunk[:xfade_len] *= window_in
        chunk[-xfade_len:] *= window_out
    
    assembled_audio.append(chunk)
    dur = len(chunk) / sr
    cut_metadata.append({
        "index": idx,
        "src_start": round(s, 3),
        "src_end": round(e, 3),
        "duration": round(dur, 3),
        "timeline_start": round(curr_timeline, 3),
        "timeline_end": round(curr_timeline + dur, 3)
    })
    curr_timeline += dur

final_audio = np.concatenate(assembled_audio)
sf.write("AI VIDEO EDITOR/outputs/audio/dialogue_snappy.wav", final_audio, sr)

with open("AI VIDEO EDITOR/inputs/snappy_cuts.json", "w") as f:
    json.dump(cut_metadata, f, indent=2)

print(f"Wrote snappy dialogue to outputs/audio/dialogue_snappy.wav ({len(final_audio)/sr:.2f}s)")
