import json
import os

def generate():
    with open('/Users/rusan/Documents/Google anti-gravity projects/New AI Videos/analysis/caption_chunks_v3.json') as f:
        caption_chunks = json.load(f)

    html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      :root {
        --bg-dark: #1A1614;
        --bg-espresso: #221C18;
        --bg-card: #2D2520;
        --color-linen: #F7F4EF;
        --color-sand: #EFE9DF;
        --color-terracotta: #D96B43;
        --color-burnt-orange: #C85A32;
        --color-ochre: #DDA15E;
        --color-border: rgba(226, 217, 204, 0.15);
      }

      html, body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: var(--bg-dark);
        font-family: 'Plus Jakarta Sans', sans-serif;
        -webkit-font-smoothing: antialiased;
      }

      #main {
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: var(--bg-dark);
      }

      /* ── Video Layers ── */
      #speaker-pane {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        z-index: 2;
        overflow: hidden;
      }

      #speaker-video {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
      }

      /* Full Screen B-Roll Videos */
      #broll-vertical-code {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
        z-index: 5;
        opacity: 0;
      }

      #broll-bricks {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
        z-index: 5;
        opacity: 0;
      }

      /* ── Half-Screen Split Top Container ── */
      #top-pane {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 960px;
        overflow: hidden;
        z-index: 10;
        background: var(--bg-espresso);
        opacity: 0;
      }

      #split-divider {
        position: absolute;
        top: 958px;
        left: 0;
        width: 1080px;
        height: 4px;
        background: linear-gradient(90deg, transparent, var(--color-terracotta) 20%, var(--color-ochre) 50%, var(--color-terracotta) 80%, transparent);
        z-index: 25;
        opacity: 0;
      }

      /* ── Half-Screen Cards ── */
      .top-card {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 960px;
        padding: 60px 48px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        opacity: 0;
      }

      /* Terminal Card (Scene 04) */
      .terminal-frame {
        background: #14110F;
        border: 1.5px solid rgba(217, 107, 67, 0.4);
        border-radius: 24px;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
        overflow: hidden;
        width: 100%;
      }
      .terminal-header {
        background: #1E1916;
        padding: 18px 24px;
        display: flex;
        align-items: center;
        border-bottom: 1.5px solid rgba(217, 107, 67, 0.25);
      }
      .terminal-dots { display: flex; gap: 10px; }
      .t-dot { width: 14px; height: 14px; border-radius: 50%; }
      .t-dot-1 { background: #D96B43; }
      .t-dot-2 { background: #DDA15E; }
      .t-dot-3 { background: #EFE9DF; }
      .t-title { margin-left: 20px; font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--color-sand); }
      .terminal-body {
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        line-height: 1.7;
        color: var(--color-linen);
        padding: 32px 30px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .tc-terra { color: var(--color-terracotta); font-weight: 700; }
      .tc-ochre { color: var(--color-ochre); }
      .tc-linen { color: var(--color-linen); }

      /* UI Architecture Card (Scene 06) */
      .bento-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        width: 100%;
      }
      .bento-card {
        background: #1C1714;
        border: 1.5px solid rgba(217, 107, 67, 0.35);
        border-radius: 20px;
        padding: 28px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .bento-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: var(--color-ochre);
        font-weight: 700;
      }
      .bento-title {
        font-family: 'Fraunces', serif;
        font-size: 32px;
        color: var(--color-linen);
        font-weight: 700;
      }
      .bento-desc {
        font-size: 22px;
        color: #B5A89E;
        line-height: 1.4;
      }

      /* Stripe Proof Card (Scene 12) */
      .stripe-card {
        background: #1C1714;
        border: 2px solid rgba(217, 107, 67, 0.45);
        border-radius: 28px;
        padding: 40px;
        box-shadow: 0 30px 70px rgba(0,0,0,0.8);
      }
      .stripe-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
      }
      .stripe-logo { font-size: 36px; font-weight: 800; color: var(--color-linen); font-family: 'Fraunces', serif; }
      .stripe-pill {
        background: rgba(217, 107, 67, 0.2);
        border: 1.5px solid var(--color-terracotta);
        color: var(--color-terracotta);
        font-size: 22px;
        font-weight: 700;
        padding: 8px 18px;
        border-radius: 999px;
      }
      .stripe-val { font-family: 'Fraunces', serif; font-size: 78px; font-weight: 800; color: var(--color-linen); }
      .stripe-growth { color: var(--color-ochre); font-size: 26px; font-weight: 700; margin-top: 10px; }

      /* ── Overlay B-Rolls ── */
      #overlay-ideas {
        position: absolute;
        top: 360px;
        right: 48px;
        width: 480px;
        z-index: 15;
        display: flex;
        flex-direction: column;
        gap: 16px;
        opacity: 0;
      }
      .idea-pill {
        background: rgba(247, 244, 239, 0.95);
        border: 1.5px solid var(--color-terracotta);
        border-radius: 16px;
        padding: 16px 22px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .idea-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--color-terracotta); }
      .idea-text { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 800; color: #1A1614; }

      #overlay-automation {
        position: absolute;
        top: 480px;
        right: 48px;
        width: 500px;
        z-index: 15;
        display: flex;
        flex-direction: column;
        gap: 16px;
        opacity: 0;
      }
      .auto-badge {
        background: rgba(26, 22, 20, 0.9);
        border: 1.5px solid var(--color-terracotta);
        border-radius: 18px;
        padding: 20px 24px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.6);
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .auto-tag { font-family: 'JetBrains Mono', monospace; font-size: 18px; color: var(--color-ochre); font-weight: 700; }
      .auto-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 800; color: var(--color-linen); }

      /* ── Full Screen B-Roll Overlays ── */
      .fs-broll-tag {
        position: absolute;
        bottom: 460px;
        left: 60px;
        background: rgba(26, 22, 20, 0.92);
        border: 2px solid var(--color-terracotta);
        border-radius: 20px;
        padding: 24px 36px;
        z-index: 20;
        box-shadow: 0 20px 50px rgba(0,0,0,0.7);
        opacity: 0;
      }
      .fs-tag-title { font-family: 'Fraunces', serif; font-size: 38px; font-weight: 800; color: var(--color-linen); }
      .fs-tag-sub { font-family: 'JetBrains Mono', monospace; font-size: 28px; color: var(--color-ochre); margin-top: 6px; }

      /* ── Overlays & Badges ── */
      #hook-banner {
        position: absolute;
        top: 140px;
        left: 48px;
        right: 48px;
        background: rgba(247, 244, 239, 0.96);
        border: 2.5px solid var(--color-terracotta);
        border-radius: 28px;
        padding: 32px 40px;
        z-index: 30;
        box-shadow: 0 24px 60px rgba(0,0,0,0.5);
        opacity: 0;
      }
      .hook-pill {
        display: inline-block;
        background: var(--color-terracotta);
        color: var(--color-linen);
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 8px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
      }
      .hook-title {
        font-family: 'Fraunces', serif;
        font-size: 46px;
        font-weight: 800;
        color: #1A1614;
        line-height: 1.25;
      }

      #badge-contrast {
        position: absolute;
        top: 240px;
        left: 60px;
        right: 60px;
        background: var(--color-terracotta);
        border-radius: 24px;
        padding: 28px 36px;
        z-index: 30;
        box-shadow: 0 24px 60px rgba(0,0,0,0.6);
        text-align: center;
        opacity: 0;
      }
      .contrast-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 40px;
        font-weight: 800;
        color: var(--color-linen);
        letter-spacing: -0.01em;
      }

      #badge-warning {
        position: absolute;
        top: 860px;
        left: 60px;
        right: 60px;
        background: var(--color-burnt-orange);
        border: 4px solid var(--color-linen);
        border-radius: 28px;
        padding: 40px;
        text-align: center;
        z-index: 30;
        box-shadow: 0 30px 80px rgba(0,0,0,0.8);
        transform: rotate(-2deg);
        opacity: 0;
      }
      .warning-title {
        font-family: 'Fraunces', serif;
        font-size: 58px;
        font-weight: 900;
        color: var(--color-linen);
        letter-spacing: 0.02em;
      }
      .warning-sub {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: var(--color-sand);
        margin-top: 10px;
      }

      #badge-past {
        position: absolute;
        top: 200px;
        left: 80px;
        right: 80px;
        background: rgba(247, 244, 239, 0.95);
        border: 1.5px solid var(--color-sand);
        border-radius: 999px;
        padding: 18px 36px;
        text-align: center;
        z-index: 30;
        box-shadow: 0 16px 40px rgba(0,0,0,0.4);
        opacity: 0;
      }
      .past-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 28px;
        font-weight: 800;
        color: #1A1614;
      }

      #badge-consultant {
        position: absolute;
        bottom: 460px;
        left: 60px;
        right: 60px;
        background: var(--color-terracotta);
        border: 2px solid var(--color-linen);
        border-radius: 28px;
        padding: 36px 40px;
        z-index: 30;
        box-shadow: 0 24px 70px rgba(0,0,0,0.7);
        opacity: 0;
      }
      .c-tag { font-family: 'JetBrains Mono', monospace; font-size: 28px; color: var(--color-ochre); font-weight: 700; }
      .c-title { font-family: 'Fraunces', serif; font-size: 54px; font-weight: 900; color: var(--color-linen); margin-top: 6px; }

      #badge-cta {
        position: absolute;
        bottom: 460px;
        left: 60px;
        right: 60px;
        background: rgba(247, 244, 239, 0.96);
        border: 2.5px solid var(--color-terracotta);
        border-radius: 28px;
        padding: 36px 40px;
        z-index: 30;
        box-shadow: 0 30px 70px rgba(0,0,0,0.6);
        text-align: center;
        opacity: 0;
      }
      .cta-pill {
        display: inline-block;
        background: var(--color-burnt-orange);
        color: var(--color-linen);
        font-size: 28px;
        font-weight: 800;
        padding: 8px 24px;
        border-radius: 999px;
        margin-bottom: 12px;
      }
      .cta-title { font-family: 'Fraunces', serif; font-size: 38px; font-weight: 800; color: #1A1614; }

      #end-card {
        position: absolute;
        top: 860px;
        left: 120px;
        right: 120px;
        background: #1C1714;
        border: 2px solid var(--color-terracotta);
        border-radius: 999px;
        padding: 26px 40px;
        text-align: center;
        z-index: 35;
        box-shadow: 0 24px 60px rgba(0,0,0,0.8);
        opacity: 0;
      }
      .end-text { font-family: 'Fraunces', serif; font-size: 36px; font-weight: 800; color: var(--color-linen); }

      /* ── Captions ── */
      #captions-container {
        position: absolute;
        top: 1640px;
        left: 0;
        width: 1080px;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 40;
        pointer-events: none;
      }

      .caption-box {
        position: absolute;
        background: rgba(26, 22, 20, 0.95);
        border: 2px solid rgba(217, 107, 67, 0.5);
        border-radius: 20px;
        padding: 16px 36px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: var(--color-linen);
        letter-spacing: -0.01em;
        text-transform: uppercase;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
        text-align: center;
        white-space: nowrap;
        opacity: 0;
      }
      .cap-terra { color: var(--color-terracotta); }
      .cap-ochre { color: var(--color-ochre); }
    </style>
  </head>
  <body>
    <div id="main" class="clip" data-composition-id="main" data-width="1080" data-height="1920">
      <!-- Audio Soundtrack -->
      <audio id="soundtrack" src="assets/audio/soundtrack.wav" data-start="0" data-duration="54.44" data-track-index="0"></audio>

      <!-- Speaker Video Track (Clean Studio Rec.709 Grade) -->
      <div id="speaker-pane">
        <video id="speaker-video" src="assets/video/rusan_speaker.mp4" data-start="0" data-duration="54.44" data-track-index="1" playsinline muted></video>
      </div>

      <!-- Full-Screen B-Roll 1: Developer / Code Workflow (Scene 05) -->
      <video id="broll-vertical-code" src="assets/video/broll_vertical_code.mp4" data-start="15.04" data-duration="3.40" data-track-index="2" playsinline muted></video>
      <div id="tag-code-broll" class="fs-broll-tag">
        <div class="fs-tag-title">// AUTOMATION PIPELINE</div>
        <div class="fs-tag-sub">ENTERPRISE SCRIPTING & EXTRACTION</div>
      </div>

      <!-- Full-Screen B-Roll 2: Modular 3D Bricks & Blocks (Scene 11) -->
      <video id="broll-bricks" src="assets/video/broll_bricks.mp4" data-start="36.42" data-duration="5.60" data-track-index="2" playsinline muted></video>
      <div id="tag-bricks-broll" class="fs-broll-tag">
        <div class="fs-tag-title">MODULAR SYSTEM ARCHITECTURE</div>
        <div class="fs-tag-sub">BUILDING AUTOMATION BRICK-BY-BRICK</div>
      </div>

      <!-- Half-Screen Split Layer (Top Pane 1080x960) -->
      <div id="top-pane">
        <!-- Scene 04: Terminal Card -->
        <div id="card-terminal" class="top-card">
          <div class="terminal-frame">
            <div class="terminal-header">
              <div class="terminal-dots">
                <div class="t-dot t-dot-1"></div>
                <div class="t-dot t-dot-2"></div>
                <div class="t-dot t-dot-3"></div>
              </div>
              <div class="t-title">bash — enterprise-scrape.sh</div>
            </div>
            <div class="terminal-body">
              <div><span class="tc-terra">$</span> curl -s https://api.axiom.ai/v1/extract \\</div>
              <div>&nbsp;&nbsp;-H "Auth: Bearer sk-live-prod" | jq '.payload'</div>
              <div><span class="tc-ochre">✓ 200 OK</span> [1,420 records parsed in 240ms]</div>
              <div><span class="tc-terra">STATUS:</span> Pipeline running autonomously.</div>
            </div>
          </div>
        </div>

        <!-- Scene 06: UI Architecture Bento Grid -->
        <div id="card-bento" class="top-card">
          <div class="bento-grid">
            <div class="bento-card">
              <div class="bento-tag">MODULE 01</div>
              <div class="bento-title">Motion Canvas</div>
              <div class="bento-desc">Hardware-accelerated 60 FPS keyframe physics</div>
            </div>
            <div class="bento-card">
              <div class="bento-tag">MODULE 02</div>
              <div class="bento-title">Agent Router</div>
              <div class="bento-desc">Autonomous multi-model prompt orchestration</div>
            </div>
          </div>
        </div>

        <!-- Scene 12: Stripe Analytics Proof Dashboard -->
        <div id="card-stripe" class="top-card">
          <div class="stripe-card">
            <div class="stripe-header">
              <div class="stripe-logo">Axiom Growth</div>
              <div class="stripe-pill">VERIFIED RETINERS</div>
            </div>
            <div class="stripe-val">$18,450.00</div>
            <div class="stripe-growth">▲ +314% vs Previous Quarter</div>
          </div>
        </div>
      </div>

      <!-- 3px Terracotta Split Divider -->
      <div id="split-divider"></div>

      <!-- Overlay B-Roll 1: Floating Idea Stack (Scene 03) -->
      <div id="overlay-ideas">
        <div class="idea-pill"><div class="idea-dot"></div><div class="idea-text">01 MULTI-AGENT SYSTEMS</div></div>
        <div class="idea-pill"><div class="idea-dot"></div><div class="idea-text">02 AUTOMATED WORKFLOWS</div></div>
        <div class="idea-pill"><div class="idea-dot"></div><div class="idea-text">03 ENTERPRISE INTEGRATION</div></div>
      </div>

      <!-- Overlay B-Roll 2: Floating Automation Badges (Scene 10) -->
      <div id="overlay-automation">
        <div class="auto-badge">
          <div class="auto-tag">// LIVE INFRASTRUCTURE</div>
          <div class="auto-title">⚡ CUSTOM ENTERPRISE AGENTS</div>
        </div>
        <div class="auto-badge">
          <div class="auto-tag">// MEASURED IMPACT</div>
          <div class="auto-title">⚡ -85% WORKFLOW EXECUTION TIME</div>
        </div>
      </div>

      <!-- Badges & Graphic Overlays -->
      <!-- Scene 01: Hook Banner -->
      <div id="hook-banner">
        <div class="hook-pill">THE AI PARADOX</div>
        <div class="hook-title">Have you ever wondered in the past few days...</div>
      </div>

      <!-- Scene 02: Contrast Punch -->
      <div id="badge-contrast">
        <div class="contrast-text">EARNING WITH AI vs. ZERO RESULTS</div>
      </div>

      <!-- Scene 07: Warning Stamp -->
      <div id="badge-warning">
        <div class="warning-title">CAN'T MAKE ANY INCOME</div>
        <div class="warning-sub">The Knowledge-Monetization Bottleneck</div>
      </div>

      <!-- Scene 08: Relatability Pill -->
      <div id="badge-past">
        <div class="past-text">⏳ 60 DAYS AGO — IN THE SAME POSITION</div>
      </div>

      <!-- Scene 09: Identity Badge -->
      <div id="badge-consultant">
        <div class="c-tag">// CAREER PIVOT</div>
        <div class="c-title">FULL-TIME AI CONSULTANT</div>
      </div>

      <!-- Scene 13: CTA Teaser -->
      <div id="badge-cta">
        <div class="cta-pill">UPCOMING MASTERCLASS</div>
        <div class="cta-title">SUBSCRIBE / FOLLOW FOR PART 2</div>
      </div>

      <!-- Scene 14: End Card -->
      <div id="end-card">
        <div class="end-text">@rusan • AI Strategy & Systems</div>
      </div>

      <!-- Captions Container -->
      <div id="captions-container" data-layout-allow-overlap="true">
"""
    # Insert caption divs
    for i, c in enumerate(caption_chunks):
        words = c['text'].split()
        if len(words) > 1:
            # Highlight first word in terracotta
            styled_text = f"<span class='cap-terra'>{words[0]}</span> " + " ".join(words[1:])
        else:
            styled_text = f"<span class='cap-terra'>{c['text']}</span>"
        html += f'        <div id="cap-{i}" class="caption-box">{styled_text}</div>\n'

    html += """      </div>
    </div>

    <script>
      (function() {
        window.__timelines = window.__timelines || {};
        const tl = gsap.timeline({ paused: true });

        // ── Scene 01: Hook (0.00s - 4.48s) ──
        tl.fromTo("#hook-banner", { autoAlpha: 0, y: -30, scale: 0.95 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: "power2.out" }, 0.2);
        tl.to("#hook-banner", { autoAlpha: 0, y: -20, duration: 0.3, ease: "power2.in" }, 4.1);

        // ── Scene 02: Contrast Punch (4.48s - 7.80s) ──
        tl.fromTo("#badge-contrast", { autoAlpha: 0, scale: 0.85, y: 20 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(1.4)" }, 4.48);
        tl.to("#badge-contrast", { autoAlpha: 0, duration: 0.25 }, 7.55);

        // ── Scene 03: Overlay B-Roll (7.80s - 11.60s) ──
        tl.fromTo("#overlay-ideas", { autoAlpha: 0, x: 40 }, { autoAlpha: 1, x: 0, duration: 0.35, ease: "power2.out" }, 7.9);
        tl.to("#overlay-ideas", { autoAlpha: 0, x: 30, duration: 0.25 }, 11.35);

        // ── Scene 04: Half-Screen Terminal (11.60s - 15.04s) ──
        tl.to("#top-pane", { autoAlpha: 1, duration: 0.25 }, 11.60);
        tl.to("#split-divider", { autoAlpha: 1, duration: 0.2 }, 11.60);
        tl.to("#speaker-video", { y: 520, duration: 0.28, ease: "power2.out" }, 11.60);
        tl.fromTo("#card-terminal", { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: "power2.out" }, 11.65);
        tl.to("#card-terminal", { autoAlpha: 0, duration: 0.2 }, 14.85);

        // ── Scene 05: Full-Screen Code B-Roll (15.04s - 18.44s) ──
        tl.to("#top-pane", { autoAlpha: 0, duration: 0.1 }, 15.04);
        tl.to("#split-divider", { autoAlpha: 0, duration: 0.1 }, 15.04);
        tl.to("#speaker-video", { y: 0, duration: 0.1 }, 15.04);
        tl.to("#broll-vertical-code", { autoAlpha: 1, duration: 0.25 }, 15.04);
        tl.fromTo("#tag-code-broll", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.3, ease: "power2.out" }, 15.2);
        tl.to("#broll-vertical-code", { autoAlpha: 0, duration: 0.2 }, 18.24);
        tl.to("#tag-code-broll", { autoAlpha: 0, duration: 0.2 }, 18.24);

        // ── Scene 06: Half-Screen UI Architecture (18.44s - 21.24s) ──
        tl.to("#top-pane", { autoAlpha: 1, duration: 0.2 }, 18.44);
        tl.to("#split-divider", { autoAlpha: 1, duration: 0.2 }, 18.44);
        tl.to("#speaker-video", { y: 520, duration: 0.25, ease: "power2.out" }, 18.44);
        tl.fromTo("#card-bento", { autoAlpha: 0, scale: 0.95 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "power2.out" }, 18.5);
        tl.to("#card-bento", { autoAlpha: 0, duration: 0.2 }, 21.05);

        // ── Scene 07: Warning Stamp (21.24s - 23.74s) ──
        tl.to("#top-pane", { autoAlpha: 0, duration: 0.1 }, 21.24);
        tl.to("#split-divider", { autoAlpha: 0, duration: 0.1 }, 21.24);
        tl.to("#speaker-video", { y: 0, duration: 0.1 }, 21.24);
        tl.fromTo("#badge-warning", { autoAlpha: 0, scale: 0.75, rotation: -8 }, { autoAlpha: 1, scale: 1, rotation: -2, duration: 0.35, ease: "back.out(1.6)" }, 21.24);
        tl.to("#badge-warning", { autoAlpha: 0, scale: 0.9, duration: 0.2 }, 23.54);

        // ── Scene 08: Relatability Pill (23.74s - 28.64s) ──
        tl.fromTo("#badge-past", { autoAlpha: 0, y: -20 }, { autoAlpha: 1, y: 0, duration: 0.3, ease: "power2.out" }, 23.9);
        tl.to("#badge-past", { autoAlpha: 0, duration: 0.25 }, 28.3);

        // ── Scene 09: Identity Badge (28.64s - 33.26s) ──
        tl.fromTo("#badge-consultant", { autoAlpha: 0, scale: 0.9, y: 30 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(1.4)" }, 28.64);
        tl.to("#badge-consultant", { autoAlpha: 0, duration: 0.25 }, 33.0);

        // ── Scene 10: Overlay Automation Badges (33.26s - 36.42s) ──
        tl.fromTo("#overlay-automation", { autoAlpha: 0, x: 40 }, { autoAlpha: 1, x: 0, duration: 0.3, ease: "power2.out" }, 33.35);
        tl.to("#overlay-automation", { autoAlpha: 0, x: 30, duration: 0.2 }, 36.2);

        // ── Scene 11: Full-Screen Modular 3D Bricks B-Roll (36.42s - 42.02s) ──
        tl.to("#broll-bricks", { autoAlpha: 1, duration: 0.25 }, 36.42);
        tl.fromTo("#tag-bricks-broll", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: "power2.out" }, 36.6);
        tl.to("#broll-bricks", { autoAlpha: 0, duration: 0.2 }, 41.82);
        tl.to("#tag-bricks-broll", { autoAlpha: 0, duration: 0.2 }, 41.82);

        // ── Scene 12: Half-Screen Stripe Proof (42.02s - 45.80s) ──
        tl.to("#top-pane", { autoAlpha: 1, duration: 0.2 }, 42.02);
        tl.to("#split-divider", { autoAlpha: 1, duration: 0.2 }, 42.02);
        tl.to("#speaker-video", { y: 520, duration: 0.25, ease: "power2.out" }, 42.02);
        tl.fromTo("#card-stripe", { autoAlpha: 0, scale: 0.95 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "power2.out" }, 42.1);
        tl.to("#card-stripe", { autoAlpha: 0, duration: 0.2 }, 45.6);

        // ── Return to Full Speaker (45.80s - 54.44s) ──
        tl.to("#top-pane", { autoAlpha: 0, duration: 0.1 }, 45.80);
        tl.to("#split-divider", { autoAlpha: 0, duration: 0.1 }, 45.80);
        tl.to("#speaker-video", { y: 0, duration: 0.1 }, 45.80);

        // ── Scene 13: CTA Card (45.80s - 52.52s) ──
        tl.fromTo("#badge-cta", { autoAlpha: 0, y: 40, scale: 0.92 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: "power2.out" }, 46.0);
        tl.to("#badge-cta", { autoAlpha: 0, duration: 0.25 }, 52.2);

        // ── Scene 14: Clean End Card (52.52s - 54.44s) ──
        tl.fromTo("#end-card", { autoAlpha: 0, scale: 0.9 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out" }, 52.52);

        // ── Synchronized Captions (42 Chunks) ──
"""
    for i, c in enumerate(caption_chunks):
        st = c['start']
        et = c['end']
        html += f'        tl.fromTo("#cap-{i}", {{ autoAlpha: 0, scale: 0.92, y: 12 }}, {{ autoAlpha: 1, scale: 1, y: 0, duration: 0.10, ease: "power2.out" }}, {st:.2f});\n'
        html += f'        tl.to("#cap-{i}", {{ autoAlpha: 0, duration: 0.08, ease: "power1.in" }}, {et:.2f});\n'

    html += """
        window.__timelines["main"] = tl;
        tl.seek(0);
      })();
    </script>
  </body>
</html>
"""
    with open('/Users/rusan/Documents/Google anti-gravity projects/videos/ai-consultant-reel/index.html', 'w') as f:
        f.write(html)
    print("Successfully generated studio-grade earthy HyperFrames index.html!")

if __name__ == '__main__':
    generate()
