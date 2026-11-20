import json

with open("AI VIDEO EDITOR/Raw video/IMG_2079.json") as f:
    data = json.load(f)

words = []
for s in data["segments"]:
    words.extend(s.get("words", []))

for i in range(len(words)-1):
    w1 = words[i]
    w2 = words[i+1]
    if w1["start"] >= 41.0 and w2["end"] <= 69.0:
        gap = w2["start"] - w1["end"]
        if gap > 0.15:
            print(f"[{w1['word'].strip()}] -> [{w2['word'].strip()}]: gap of {gap:.2f}s ({w1['end']:.2f} -> {w2['start']:.2f})")
