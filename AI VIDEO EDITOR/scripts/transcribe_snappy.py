import mlx_whisper
import json

result = mlx_whisper.transcribe(
    "AI VIDEO EDITOR/outputs/audio/dialogue_snappy.wav",
    path_or_hf_repo="mlx-community/whisper-tiny",
    word_timestamps=True
)

with open("AI VIDEO EDITOR/outputs/audio/dialogue_snappy.json", "w") as f:
    json.dump(result, f, indent=2)

print("Transcribed snappy dialogue successfully!")
for s in result.get("segments", []):
    print(f"[{s['start']:5.2f} -> {s['end']:5.2f}] {s['text'].strip()}")
