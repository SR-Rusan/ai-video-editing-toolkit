import json

with open("AI VIDEO EDITOR/outputs/audio/dialogue_snappy.json") as f:
    data = json.load(f)

words = []
for s in data.get("segments", []):
    for w in s.get("words", []):
        word_text = w["word"].strip()
        if word_text.lower() == "vibrating":
            word_text = "web scraping"
        elif word_text.lower() in ["interview.", "interview"]:
            word_text = "breakthrough"
        words.append({
            "word": word_text,
            "start": round(w["start"], 2),
            "end": round(w["end"], 2)
        })

# Target 3-5 words per caption chunk, with minimum duration 1.1s
balanced_captions = []
i = 0
while i < len(words):
    # take 4 words by default
    chunk_size = 4
    if i + chunk_size >= len(words):
        chunk_words = words[i:]
        i = len(words)
    else:
        chunk_words = words[i:i+chunk_size]
        i += chunk_size
        
    start = chunk_words[0]["start"]
    end = chunk_words[-1]["end"]
    # Ensure minimum on-screen duration of 1.1s if there's room before next
    text = " ".join(cw["word"] for cw in chunk_words).upper()
    balanced_captions.append({
        "text": text,
        "start": start,
        "end": end,
        "duration": round(end - start, 2)
    })

# Adjust ends so consecutive captions transition smoothly without micro-flash gaps
for idx in range(len(balanced_captions) - 1):
    curr = balanced_captions[idx]
    nxt = balanced_captions[idx+1]
    if curr["end"] < nxt["start"]:
        # Extend current end up to next start minus 0.05s, up to 1.8s duration
        curr["end"] = min(curr["start"] + 2.0, nxt["start"] - 0.05)
        curr["duration"] = round(curr["end"] - curr["start"], 2)

print(f"Generated {len(balanced_captions)} balanced caption pills.")
for idx in range(min(10, len(balanced_captions))):
    c = balanced_captions[idx]
    print(f"[{c['start']:5.2f}s -> {c['end']:5.2f}s] ({c['duration']:4.2f}s) {c['text']}")

with open("AI VIDEO EDITOR/inputs/balanced_captions.json", "w") as f:
    json.dump(balanced_captions, f, indent=2)
