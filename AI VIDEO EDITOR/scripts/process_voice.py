import soundfile as sf
import numpy as np
import scipy.signal as signal

# Load snappy dialogue
data, sr = sf.read("AI VIDEO EDITOR/outputs/audio/dialogue_snappy.wav")
if len(data.shape) > 1:
    data = data.mean(axis=1)

# 1. High-pass filter at 85Hz (Butterworth 4th order)
sos_hp = signal.butter(4, 85, 'hp', fs=sr, output='sos')
filtered = signal.sosfilt(sos_hp, data)

# 2. Parametric EQ:
# - Cut 400Hz by 2.5dB (boxiness)
# - Boost 3500Hz by 2.2dB (clarity)
# - Boost 10000Hz by 1.5dB (air)
def peaking_eq(x, f0, gain_db, Q, fs):
    w0 = 2 * np.pi * f0 / fs
    A = 10**(gain_db / 40.0)
    alpha = np.sin(w0) / (2 * Q)
    b0 = 1 + alpha * A
    b1 = -2 * np.cos(w0)
    b2 = 1 - alpha * A
    a0 = 1 + alpha / A
    a1 = -2 * np.cos(w0)
    a2 = 1 - alpha / A
    b = np.array([b0, b1, b2]) / a0
    a = np.array([a0, a1, a2]) / a0
    return signal.lfilter(b, a, x)

eq1 = peaking_eq(filtered, 400, -2.5, 1.2, sr)
eq2 = peaking_eq(eq1, 3500, +2.2, 1.0, sr)
eq3 = peaking_eq(eq2, 10000, +1.5, 0.7, sr)

# 3. Transparent soft-knee compressor
def soft_compressor(x, threshold_db=-18.0, ratio=2.5, attack_ms=15.0, release_ms=120.0, fs=48000):
    attack_coeff = np.exp(-1.0 / (attack_ms * 0.001 * fs))
    release_coeff = np.exp(-1.0 / (release_ms * 0.001 * fs))
    
    env = 0.0
    out = np.zeros_like(x)
    for i in range(len(x)):
        inp = abs(x[i])
        if inp > env:
            env = attack_coeff * env + (1 - attack_coeff) * inp
        else:
            env = release_coeff * env + (1 - release_coeff) * inp
        
        env_db = 20 * np.log10(max(env, 1e-6))
        if env_db > threshold_db:
            gain_db = threshold_db + (env_db - threshold_db) / ratio - env_db
        else:
            gain_db = 0.0
        
        gain = 10**(gain_db / 20.0)
        out[i] = x[i] * gain
    return out

compressed = soft_compressor(eq3, threshold_db=-18.0, ratio=2.5, attack_ms=15.0, release_ms=120.0, fs=sr)

# 4. Make-up gain to hit -1.0 dBFS true peak
peak = np.max(np.abs(compressed))
if peak > 0:
    target_peak = 10**(-1.0 / 20.0) # -1.0 dB
    compressed = compressed * (target_peak / peak)

sf.write("AI VIDEO EDITOR/outputs/audio/dialogue_processed.wav", compressed, sr)
print("Saved processed dialogue to outputs/audio/dialogue_processed.wav")
