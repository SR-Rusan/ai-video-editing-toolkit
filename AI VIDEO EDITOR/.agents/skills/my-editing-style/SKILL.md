---
name: my-editing-style
description: Edit high-retention vertical reels in the signature AevyTV storytelling style. Features a bold yellow serif hook banner, white-on-black pill captions, 1.3x punch-in jump cuts every 1.5-2.5s, contextual B-roll (obsidian HUD grid cards or full-screen archival media), and auto-added ducked lo-fi background music with tactile UI sound effects (-14.5 LUFS master). Use whenever the user asks to edit a video in their style, apply their template, or produce an AevyTV-style vertical reel.
---

# My Editing Style (High-Retention Storytelling Reel)

This skill codifies the signature **AevyTV** high-retention vertical reel style (9:16 format: 1080×1920). It enforces crisp rhythmic pacing, dual visual hooks, punch-in emphasis cuts, contextual B-roll, and broadcast-mastered automated audio.

---

## 🎯 The 5 Core Pillars

1. **Dual Hook (0.0s – 3.0s)**:
   * **Top Banner**: Editorial serif headline in warm yellow (`#FFE600`) with core keywords in ALL CAPS (pinned for 2.5–4.0s).
   * **Visual Punch**: Medium shot at 0.0s, followed by an immediate **1.3× punch-in jump cut** at 0.8s–1.5s on the first emphasis word.
2. **Pacing & Jump Cuts**:
   * Cut or reframe every **1.2 to 2.5 seconds**; never hold a static frame longer than 3 seconds.
   * Alternates between **Shot A** (1.0× medium shot) and **Shot B** (1.3× punch-in close-up on eyes).
   * Breath gaps and pauses trimmed tight (**5.5 to 6.5 onsets/sec**).
3. **Captions**:
   * Lower third (~75% vertical height), centered horizontally.
   * White text (`#FFFFFF`, Inter/SF Pro bold) inside a **black rounded pill** (`rgba(0,0,0,0.85)`).
   * Micro-chunked into **2 to 4 words** per line, synced strictly to spoken cadence.
4. **Context-Driven B-Roll**:
   * **Concepts / Tech / Stats / Tools**: Obsidian HUD Grid layout (dark `#0A0A0A` canvas, subtle wireframe grid lines, floating white/glass data cards, hand-drawn annotations like `this one!`).
   * **Stories / People / History**: Clean, high-impact full-screen B-roll or archival imagery.
5. **Automated Sound & Music Bed**:
   * Crisp, forward, dry dialogue with zero room echo.
   * Subtle lo-fi / ambient music bed ducked **-20 dB** below voice.
   * Tactile UI sound effects (`real-sfx`): soft whooshes on punch-ins, clicks on card reveals, scribbles on doodles.
   * Final master: **`-14.5 LUFS`** and **`-0.5 dBTP`**.

---

## 🎬 Step-by-Step Workflow

### Step 1: Ingest & Word Timings
Extract word timestamps with the local `mlx-whisper` (Apple Silicon Metal) engine:
```bash
.venv/bin/python .agents/skills/effects/scripts/words.py inputs/raw_clip.mp4
```
This generates `inputs/raw_clip.words.json` containing exact start (`s`) and end (`e`) seconds for every word.

### Step 2: Determine Hook & Cut Points
From the transcript:
1. **Hook Title**: Formulate a provocative 1-line hook with key words capitalized (e.g. `The STRANGEST website on the internet` or `Claude just did a BRAIN surgery?!`).
2. **First Punch-In**: Identify the primary punch word between 0.8s and 1.6s.
3. **Cut List**: Mark alternating 1.0× and 1.3× punch frames at natural punctuation and sentence beats.

### Step 3: Build the Effects Plan (`plan.json`)
Structure the JSON plan combining:
* `headline-box` or `backdrop-word` for the opening hook
* `lean-in` or punch cuts at emphasis points
* `broll-split` or dark HUD cards for concept explanations

```json
{
  "hook_banner": {
    "text": "The STRANGEST website on the internet",
    "font": "serif",
    "color": "#FFE600",
    "start": 0.0,
    "end": 3.2
  },
  "effects": [
    { "fx": "lean-in", "start": 0.9, "end": 2.2, "zoom": 1.32 },
    { "fx": "backdrop-word", "start": 4.1, "end": 5.8, "text": "DISCOVER", "color": "#FFE600" },
    { "fx": "glass-widgets", "start": 9.2, "end": 12.0 }
  ]
}
```

### Step 4: Add Automated Sound Design
1. **Background Music Bed**:
   Use `real-sound` / `real-sfx` to mix a lo-fi jazz or ambient bed under dialogue:
   ```bash
   .venv/bin/python .agents/skills/real-sfx/scripts/bed.py inputs/cues.json
   ```
2. **SFX Placement**:
   * Add a `whoosh` on every punch-in cut.
   * Add a `ui_click` or `tap` on card and title entries.
3. **Mastering Gate**:
   Verify with `earshot measure`:
   ```bash
   earshot measure outputs/reel.mp4 --json
   ```
   Confirm `-14.5 ± 0.5 LUFS` and peak `< -0.5 dBTP`.

### Step 5: Quick Frame Check & Render
1. Check still frames first:
   ```bash
   .venv/bin/python .agents/skills/effects/scripts/fx.py --plan plan.json inputs/raw_clip.mp4 outputs/check.png --still 1.2,4.5,10.0
   ```
2. Render final vertical video:
   ```bash
   .venv/bin/python .agents/skills/effects/scripts/fx.py --plan plan.json inputs/raw_clip.mp4 outputs/final_reel.mp4 --width 1080
   ```
