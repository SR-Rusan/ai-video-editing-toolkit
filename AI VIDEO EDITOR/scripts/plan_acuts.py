import json

with open("AI VIDEO EDITOR/Raw video/IMG_2079.json") as f:
    data = json.load(f)

# The phonetic substitutions we agreed on:
# "vibrating" -> "web scraping"
# "interview" -> "income / breakthrough"

# Let's inspect each sentence and where the natural cuts/breaths are:
# Cut criteria:
# Keep ~0.08s padding before speech starts and ~0.08s padding after speech ends.
# Cut out all dead silences between phrases.

words = []
for s in data["segments"]:
    words.extend(s.get("words", []))

# Group words into tight speech chunks (phrases/sentences) separated by pauses > 0.25s
chunks = []
current_chunk = [words[0]]

for i in range(1, len(words)):
    w = words[i]
    prev_w = words[i-1]
    gap = w["start"] - prev_w["end"]
    if gap > 0.25:
        chunks.append(current_chunk)
        current_chunk = [w]
    else:
        current_chunk.append(w)
chunks.append(current_chunk)

print(f"Total speech chunks: {len(chunks)}")
total_speech_duration = 0.0

for idx, c in enumerate(chunks):
    start = max(0.0, c[0]["start"] - 0.06)
    end = min(96.29, c[-1]["end"] + 0.08)
    dur = end - start
    total_speech_duration += dur
    text = " ".join(w["word"].strip() for w in c)
    print(f"Chunk {idx:02d}: [{start:6.2f} -> {end:6.2f}] ({dur:5.2f}s) | \"{text}\"")

print(f"\nOriginal video duration: 96.29s")
print(f"Trimmed A-cut speech duration: {total_speech_duration:.2f}s (saved {96.29 - total_speech_duration:.2f}s of silence!)")
