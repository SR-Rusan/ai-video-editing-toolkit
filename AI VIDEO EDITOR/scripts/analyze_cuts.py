import json

with open("AI VIDEO EDITOR/Raw video/IMG_2079.json") as f:
    data = json.load(f)

segments = data.get("segments", [])
words = []
for s in segments:
    words.extend(s.get("words", []))

print(f"Total segments: {len(segments)}, Total words: {len(words)}")

# Look for pauses between words > 0.3s
pauses = []
for i in range(len(words) - 1):
    w1 = words[i]
    w2 = words[i+1]
    gap = w2["start"] - w1["end"]
    if gap > 0.25:
        pauses.append((w1["word"].strip(), w2["word"].strip(), w1["end"], w2["start"], gap))

print(f"\nFound {len(pauses)} pauses > 0.25s:")
for p in pauses:
    print(f"  '{p[0]}' -> '{p[1]}': gap of {p[4]:.2f}s (from {p[2]:.2f}s to {p[3]:.2f}s)")

# Print full transcript with sentences
print("\nSegments:")
for i, s in enumerate(segments):
    print(f"[{s['start']:6.2f} -> {s['end']:6.2f}] {s['text'].strip()}")
