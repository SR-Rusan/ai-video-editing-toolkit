import json
with open("AI VIDEO EDITOR/Raw video/IMG_2079.json") as f:
    data = json.load(f)

for s in data["segments"]:
    for w in s.get("words", []):
        if 48.0 <= w["start"] <= 58.0:
            print(f"{w['start']:6.2f} - {w['end']:6.2f} | {w['word']}")
