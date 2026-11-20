import soundfile as sf
import numpy as np

data, sr = sf.read("AI VIDEO EDITOR/outputs/audio/dialogue_raw.wav")
if len(data.shape) > 1:
    data = data.mean(axis=1)

duration = len(data) / sr
print(f"Audio duration: {duration:.2f}s, sample rate: {sr} Hz")

# Compute short-time energy (RMS) in 30ms windows with 10ms hop
frame_len = int(sr * 0.030)
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

# Speech threshold: anything > -22 dB relative to max RMS, with hysteresis
db = 20 * np.log10(np.maximum(rms, 1e-6) / max_rms)

is_speech = db > -22.0

# Morphological closing to bridge micro-pauses (< 180ms)
min_pause_frames = int(0.20 / 0.010) # 200ms
# Fill small dips in speech
speech_smoothed = is_speech.copy()
i = 0
while i < len(speech_smoothed):
    if not speech_smoothed[i]:
        start = i
        while i < len(speech_smoothed) and not speech_smoothed[i]:
            i += 1
        gap_len = i - start
        if gap_len < min_pause_frames:
            speech_smoothed[start:i] = True
    else:
        i += 1

# Extract speech intervals
intervals = []
in_speech = False
seg_start = 0.0

for t, s in zip(times, speech_smoothed):
    if s and not in_speech:
        in_speech = True
        seg_start = max(0.0, t - 0.04) # 40ms head padding
    elif not s and in_speech:
        in_speech = False
        seg_end = min(duration, t + 0.06) # 60ms tail padding
        if seg_end - seg_start >= 0.25: # minimum speech length 250ms
            intervals.append((seg_start, seg_end))

if in_speech:
    intervals.append((seg_start, duration))

print(f"Extracted {len(intervals)} speech segments after silence removal:")
total_cut_duration = sum(e - s for s, e in intervals)
for idx, (s, e) in enumerate(intervals):
    print(f"  Segment {idx:02d}: {s:6.2f}s -> {e:6.2f}s ({e-s:5.2f}s)")

print(f"\nOriginal: {duration:.2f}s -> Trimmed: {total_cut_duration:.2f}s (removed {duration - total_cut_duration:.2f}s of silence)")
