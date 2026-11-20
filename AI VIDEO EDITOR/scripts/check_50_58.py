import soundfile as sf
import numpy as np

data, sr = sf.read("AI VIDEO EDITOR/outputs/audio/dialogue_raw.wav")
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Check energy in 0.1s windows from 50.0 to 57.0
for t in np.arange(50.0, 58.0, 0.2):
    s = int(t * sr)
    e = int((t + 0.2) * sr)
    rms = np.sqrt(np.mean(data[s:e]**2))
    print(f"{t:5.1f}s - {t+0.2:5.1f}s | RMS: {rms:8.5f} | {'SPEECH' if rms > 0.008 else 'SILENCE'}")
