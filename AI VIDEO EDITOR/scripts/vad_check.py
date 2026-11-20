import soundfile as sf
import numpy as np

# Load dialogue_raw.wav
data, sr = sf.read("AI VIDEO EDITOR/outputs/audio/dialogue_raw.wav")
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Check 50s to 58s
t0, t1 = 50.0, 58.0
chunk = data[int(t0*sr):int(t1*sr)]
hop = int(sr * 0.05) # 50ms frames
frame_len = int(sr * 0.1)

rms = []
times = []
for i in range(0, len(chunk) - frame_len, hop):
    f = chunk[i:i+frame_len]
    r = np.sqrt(np.mean(f**2))
    rms.append(r)
    times.append(t0 + i/sr)

max_rms = max(rms)
print(f"Max RMS: {max_rms:.4f}")
for t, r in zip(times, rms):
    db = 20 * np.log10(max(r, 1e-6) / max_rms)
    bar = "#" * int(max(0, (db + 40) / 2))
    print(f"{t:5.2f}s: {db:6.1f} dB {bar}")
