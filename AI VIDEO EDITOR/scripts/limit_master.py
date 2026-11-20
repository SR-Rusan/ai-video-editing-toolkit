import soundfile as sf
import numpy as np

mix, sr = sf.read("AI VIDEO EDITOR/outputs/audio/soundtrack_snappy_mastered.wav")

# Boost gain by +3.2 dB
gain_linear = 10**(3.2 / 20.0)
boosted = mix * gain_linear

# Soft-clip / limiter curve to preserve dynamics while capping at -0.6 dBTP (0.933)
ceiling = 10**(-0.6 / 20.0) # 0.933
# Tanh soft limiter for values exceeding 0.75 * ceiling
knee = 0.75 * ceiling
mask = np.abs(boosted) > knee
diff = np.abs(boosted)[mask] - knee
range_val = ceiling - knee
limited_val = knee + range_val * np.tanh(diff / range_val)
boosted[mask] = np.sign(boosted[mask]) * limited_val

# Final hard safety ceiling
boosted = np.clip(boosted, -ceiling, ceiling)

sf.write("AI VIDEO EDITOR/outputs/audio/soundtrack_snappy_mastered.wav", boosted, sr)
print(f"Limited master written. Peak: {np.max(np.abs(boosted)):.4f}")
