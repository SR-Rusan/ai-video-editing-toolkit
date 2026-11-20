import json
import soundfile as sf
import numpy as np

with open("AI VIDEO EDITOR/Raw video/IMG_2079.json") as f:
    transcript = json.load(f)

words = []
for s in transcript["segments"]:
    words.extend(s.get("words", []))

# We want to identify the natural phrases:
# Group words into sentences/phrases:
# When gap between words > 0.28s, that is a cut point.
# Also, inside the long pauses (like 52s-56s where "So... my... motto" has huge pauses):

cuts = []
current_words = [words[0]]

for i in range(1, len(words)):
    w_prev = words[i-1]
    w_curr = words[i]
    gap = w_curr["start"] - w_prev["end"]
    if gap > 0.28:
        cuts.append(current_words)
        current_words = [w_curr]
    else:
        current_words.append(w_curr)
cuts.append(current_words)

print(f"Divided speech into {len(cuts)} tight sentence/phrase blocks:")

edit_cuts = []
t_timeline = 0.0

for idx, c in enumerate(cuts):
    # Precise boundaries with natural padding:
    src_in = max(0.0, c[0]["start"] - 0.08)
    src_out = min(96.28, c[-1]["end"] + 0.08)
    dur = src_out - src_in
    text = " ".join(w["word"].strip() for w in c)
    edit_cuts.append({
        "index": idx,
        "src_in": round(src_in, 3),
        "src_out": round(src_out, 3),
        "duration": round(dur, 3),
        "timeline_start": round(t_timeline, 3),
        "text": text,
        "words": c
    })
    print(f"[{t_timeline:6.2f} -> {t_timeline+dur:6.2f}] (src: {src_in:5.2f} - {src_out:5.2f}, dur: {dur:4.2f}s) | \"{text}\"")
    t_timeline += dur

print(f"\nFinal A-Cut Video Duration: {t_timeline:.2f} seconds.")
with open("AI VIDEO EDITOR/inputs/edit_cuts.json", "w") as f:
    json.dump(edit_cuts, f, indent=2)
