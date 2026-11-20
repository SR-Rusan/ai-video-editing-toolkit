import json

with open("AI VIDEO EDITOR/Raw video/IMG_2079.json") as f:
    data = json.load(f)

words = []
for s in data["segments"]:
    words.extend(s.get("words", []))

for i, w in enumerate(words):
    prev_end = words[i-1]["end"] if i > 0 else 0.0
    gap = w["start"] - prev_end
    gap_str = f" [GAP: {gap:4.2f}s]" if gap > 0.2 else ""
    print(f"{i:3d}: {w['start']:6.2f} - {w['end']:6.2f} | {w['word']:<18}{gap_str}")
