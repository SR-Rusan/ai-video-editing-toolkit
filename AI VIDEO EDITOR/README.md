# AI Video Editor (Vertical Reels & Sound Design)

This workspace is configured as an AI-assisted video editing environment optimized for **vertical reels** (9:16 format, 1080×1920 or 2160×3840 4K) and **intelligent sound design & audio analysis**.

---

## 🛠 Installed Tools & Engines

| Component | Status | Details |
|---|---|---|
| **FFmpeg & FFprobe** | ✅ Ready | `v7.0` at `/Users/rusan/.local/bin/ffmpeg` |
| **yt-dlp** | ✅ Ready | `2026.10.26` at `/Users/rusan/.local/bin/yt-dlp` |
| **Whisper (Apple Silicon)** | ✅ Ready | `mlx-whisper` (Metal GPU accelerated) at `/Users/rusan/.local/bin/mlx_whisper` + `.venv` |
| **Whisper (Fallback)** | ✅ Ready | `faster-whisper` (`v1.2.1`) installed in `.venv` |
| **HyperFrames** | ✅ Ready | `v0.9.19` at `/Users/rusan/node/bin/hyperframes` |
| **earshot CLI** | ✅ Ready | `v0.4.1` at `/Users/rusan/.local/bin/earshot` |
| **Python Environment** | ✅ Ready | Python `3.12` venv at `.venv/` (`mediapipe`, `cv2`, `PIL`, `numpy`, `mlx-whisper`, `faster-whisper`, `earshot`, `soundfile`, `scipy`, `librosa`, `torch`, `transformers`) |

---

## 🧩 Installed Skills

### 0. `my-editing-style` (Signature Preset)
*Locations: `.agents/skills/my-editing-style`, `.claude/skills/my-editing-style`*

* **AevyTV High-Retention Storytelling Reel System**:
  * Dual Visual Hook: Yellow editorial serif top banner (`#FFE600`) + 1.3× punch-in cut at 0.8s–1.5s
  * Jump-Cut Cadence: Reframing / zoom swap every 1.5–2.5s (5.5–6.5 onsets/sec)
  * Subtitle Pills: Lower-third white-on-black pills (`rgba(0,0,0,0.85)`), 2–4 words per line
  * Dynamic B-Roll: Obsidian HUD grid cards for tech/concepts; full-screen media for stories
  * Automated Sound: Ducked lo-fi bed (-20 dB) + UI clicks & zoom whooshes (-14.5 LUFS master)
* **Commands:**
  * Auto-scaffold editing plan:
    ```bash
    .venv/bin/python .agents/skills/my-editing-style/scripts/scaffold_plan.py inputs/clip.words.json --hook "YOUR HOOK TITLE" --out outputs/plan.json
    ```

### 1. `claude-video-effects` (`effects`)
*Source: `github.com/Vibha-Ramprakash/claude-video-effects`*  
*Locations: `.agents/skills/effects`, `.claude/skills/effects`*

* **51 Face-Tracking & Behind-Head Effects** designed for talking-head reels:
  * Kinetic type behind head (`backdrop-word`, `red-collage`, `crayon-write`, `huge-strike`)
  * Dynamic tracking & camera zooms (`locked-on`, `lean-in`, `slow-push`, `over-the-shoulder-zoom`)
  * Floating UI & Glass widgets (`glass-widgets`, `liquid-glass-graph`, `apple-toggles`, `messages`, `todo`, `comment-box`)
  * Media layers & Reels fan (`orbit`, `noise`, `phone-fan`, `place-in-grid`, `carousel-spin`)
* **Commands:**
  * Word timing extraction:
    ```bash
    .venv/bin/python .agents/skills/effects/scripts/words.py inputs/clip.mp4
    ```
  * Quick check still frames:
    ```bash
    .venv/bin/python .agents/skills/effects/scripts/fx.py --plan plan.json inputs/clip.mp4 outputs/check.png --still 4.5,12.0
    ```
  * Render single effect:
    ```bash
    .venv/bin/python .agents/skills/effects/scripts/fx.py orbit inputs/clip.mp4 outputs/final.mp4 --start 3 --end 6
    ```
  * Render multi-effect plan:
    ```bash
    .venv/bin/python .agents/skills/effects/scripts/fx.py --plan plan.json inputs/clip.mp4 outputs/final.mp4
    ```

### 2. `claude-video` (`watch`)
*Source: `github.com/bradautomates/claude-video`*  
*Locations: `.agents/skills/watch`, `.claude/skills/watch`*

* **Video Evidence & Understanding**:
  * Downloads YouTube, Instagram Reels, or web videos using `yt-dlp`
  * Extracts auto-scaled frames using `ffmpeg`
  * Transcribes spoken audio with Whisper or extracts native captions
* **Commands:**
  * Watch a video or local file:
    ```bash
    python3 .agents/skills/watch/scripts/watch.py <video-url-or-file>
    ```

### 3. `real-sfx`
*Source: `real-sfx.skill`*  
*Locations: `.agents/skills/real-sfx`, `.claude/skills/real-sfx`*

* **Realistic Sound Design for Motion & UI**:
  * Adds real recorded sounds (whooshes, impacts, risers, clicks, keystrokes, UI foley)
  * Shipped with full `uisfx` CC0 UI sound pack
  * Extracts event cues from animations or motion videos without synthesized artifacts
* **Commands:**
  * Verify setup:
    ```bash
    .venv/bin/python .agents/skills/real-sfx/scripts/setup.py check
    ```
  * Detect moments in video:
    ```bash
    .venv/bin/python .agents/skills/real-sfx/scripts/find_moments.py inputs/clip.mp4 --out outputs/moments
    ```

### 4. `earshot`
*Source: `github.com/Leonxlnx/earshot`*  
*Locations: `.agents/skills/earshot`, `.claude/skills/earshot`, CLI: `earshot`*

* **Ears for Coding Agents**:
  * AI-driven audio verification, realness classification, loudness matching, and soundtrack critique
  * Objective metrics: spectral analysis, CLAP similarity, AST classification, LUFS metering
  * Pre-packaged 252-sound forge sound bank
* **Commands:**
  * Check health and models:
    ```bash
    earshot doctor
    ```
  * Rank sound candidates for a prompt:
    ```bash
    earshot rank "clean mechanical keyboard click" downloads/sfx/ --top 5
    ```

### 5. `real-sound`
*Source: `github.com/Leonxlnx/earshot` (skills/real-sound)*  
*Locations: `.agents/skills/real-sound`, `.claude/skills/real-sound`*

* **Full-Length Video Soundtracks & Scoring**:
  * Automates music edits, multi-category SFX sourcing, QA sync, and audio mastering
  * Validates audio sync and mix gates (+/-0.5 LU, <= -1.5 dBTP)
* **Commands:**
  * Analyze audio asset:
    ```bash
    .venv/bin/python .agents/skills/real-sound/scripts/analyze.py --music asset.wav
    ```

---

## 📁 Workspace Layout

```
AI VIDEO EDITOR/
├── .agents/skills/
│   ├── effects/          # claude-video-effects (51 visual reel effects)
│   ├── watch/            # claude-video (/watch video parser)
│   ├── real-sfx/         # real-sfx motion sound design & uisfx bank
│   ├── earshot/          # earshot AI audio analysis skill
│   └── real-sound/       # real-sound soundtrack & scoring supervisor
├── .claude/skills/       # Claude Code skill discovery symlinks
├── .venv/                # Python 3.12 virtualenv with all AI dependencies
├── tools/
│   └── earshot/          # earshot engine source repository
├── inputs/               # Place raw talking-head and reel clips here
├── outputs/              # Exported reels, check stills, and sound exports
└── README.md             # This guide
```
