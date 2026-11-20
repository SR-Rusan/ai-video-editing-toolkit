import json

with open("AI VIDEO EDITOR/outputs/audio/dialogue_snappy.json") as f:
    data = json.load(f)

# Extract word array
words = []
for s in data.get("segments", []):
    for w in s.get("words", []):
        word_text = w["word"].strip()
        # Phonetic substitutions:
        if word_text.lower() == "vibrating":
            word_text = "web scraping"
        elif word_text.lower() == "interview.":
            word_text = "breakthrough."
        elif word_text.lower() == "interview":
            word_text = "breakthrough"
        words.append({
            "word": word_text,
            "start": round(w["start"], 2),
            "end": round(w["end"], 2)
        })

print(f"Total words: {len(words)}")

# Chunk words into 2-4 words per caption pill (AevyTV micro-chunks)
caption_chunks = []
i = 0
while i < len(words):
    # Take 2 to 3 words
    chunk_size = 3
    if i + chunk_size > len(words):
        chunk_size = len(words) - i
    elif i + chunk_size + 1 == len(words):
        chunk_size = 2 # balance remaining
        
    chunk_words = words[i:i+chunk_size]
    text = " ".join(cw["word"] for cw in chunk_words).upper()
    start = chunk_words[0]["start"]
    end = chunk_words[-1]["end"]
    caption_chunks.append({
        "text": text,
        "start": start,
        "end": end,
        "duration": round(end - start, 2)
    })
    i += chunk_size

print(f"Generated {len(caption_chunks)} micro-caption pills.")
for idx in range(min(12, len(caption_chunks))):
    c = caption_chunks[idx]
    print(f"[{c['start']:5.2f}s -> {c['end']:5.2f}s] {c['text']}")

with open("AI VIDEO EDITOR/inputs/caption_chunks.json", "w") as f:
    json.dump(caption_chunks, f, indent=2)
