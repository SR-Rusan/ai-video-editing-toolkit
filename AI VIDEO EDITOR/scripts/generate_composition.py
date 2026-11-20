import json

with open("AI VIDEO EDITOR/inputs/balanced_captions.json") as f:
    captions = json.load(f)

html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {
        font-family: "Instrument Serif";
        src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2");
        font-weight: 400;
        font-style: italic;
      }
      @font-face {
        font-family: "Instrument Serif Regular";
        src: url("assets/fonts/InstrumentSerif-Regular.woff2") format("woff2");
        font-weight: 400;
        font-style: normal;
      }
      @font-face {
        font-family: "Inter";
        src: url("assets/fonts/Inter-Variable.woff2") format("woff2");
        font-weight: 100 900;
        font-style: normal;
      }

      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      html, body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000000;
        font-family: "Inter", sans-serif;
        -webkit-font-smoothing: antialiased;
      }

      #main {
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000000;
      }

      /* ── Top B-Roll Container ── */
      #top-pane {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 960px;
        overflow: hidden;
        z-index: 10;
        background: #07090E;
      }

      .top-card {
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 960px;
        opacity: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }

      .top-video {
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 960px;
        object-fit: cover;
      }

      /* ── Speaker Pane ── */
      #speaker-pane {
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        z-index: 20;
        clip-path: inset(0px 0px 0px 0px);
      }

      #speaker-video {
        position: absolute;
        left: 0;
        top: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
      }

      /* ── Neon Split Divider ── */
      #split-divider {
        position: absolute;
        top: 958px;
        left: 0;
        width: 1080px;
        height: 4px;
        z-index: 35;
        background: linear-gradient(90deg, transparent, #FFE600 20%, #6366F1 50%, #FFE600 80%, transparent);
        box-shadow: 0 0 20px rgba(255, 230, 0, 0.8), 0 0 35px rgba(99, 102, 241, 0.6);
        opacity: 0;
      }

      /* ── HUD Badge ── */
      .hud-tag {
        position: absolute;
        top: 40px;
        left: 48px;
        background: rgba(0, 0, 0, 0.82);
        border: 1.5px solid rgba(255, 230, 0, 0.5);
        border-radius: 10px;
        padding: 10px 22px;
        font-size: 28px;
        font-weight: 800;
        color: #FFE600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 5;
        backdrop-filter: blur(10px);
      }
      .hud-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #00FF66;
        box-shadow: 0 0 12px #00FF66;
      }

      /* ── Terminal Card ── */
      .terminal-window {
        width: 980px;
        height: 780px;
        background: rgba(10, 14, 22, 0.96);
        border: 1.5px solid rgba(99, 102, 241, 0.4);
        border-radius: 24px;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(99, 102, 241, 0.25);
        padding: 40px 48px;
        display: flex;
        flex-direction: column;
        gap: 24px;
        font-family: monospace;
      }
      .term-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 22px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      }
      .dot { width: 18px; height: 18px; border-radius: 50%; }
      .dot-red { background: #FF5F56; }
      .dot-yellow { background: #FFBD2E; }
      .dot-green { background: #27C93F; }
      .term-title { margin-left: 18px; font-size: 28px; color: #8F9CAE; }
      .term-body { font-size: 30px; line-height: 1.6; color: #E2E8F0; display: flex; flex-direction: column; gap: 16px; }
      .t-cmd { color: #FFE600; font-weight: bold; }
      .t-cyan { color: #38BDF8; }
      .t-green { color: #4ADE80; font-weight: bold; }
      .t-purple { color: #A78BFA; }

      /* ── Automation Pipeline Card ── */
      .pipeline-card {
        width: 980px;
        height: 780px;
        background: rgba(12, 16, 26, 0.96);
        border: 1.5px solid rgba(255, 230, 0, 0.4);
        border-radius: 26px;
        padding: 44px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 24px 60px rgba(0,0,0,0.85);
      }
      .node-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
      }
      .pipe-node {
        flex: 1;
        background: rgba(25, 33, 50, 0.9);
        border: 1.5px solid rgba(255, 255, 255, 0.18);
        border-radius: 18px;
        padding: 26px 18px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        text-align: center;
      }
      .pipe-node-title { font-size: 28px; font-weight: 800; color: #FFFFFF; }
      .pipe-node-desc { font-size: 20px; color: #94A3B8; }
      .pipe-arrow { font-size: 36px; color: #FFE600; font-weight: 900; }

      /* ── ROI Dashboard Card ── */
      .roi-card {
        width: 980px;
        height: 780px;
        background: rgba(10, 13, 20, 0.96);
        border: 1.5px solid rgba(0, 255, 102, 0.4);
        border-radius: 26px;
        padding: 48px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 24px 60px rgba(0,0,0,0.85), 0 0 45px rgba(0, 255, 102, 0.2);
      }
      .roi-stats {
        display: flex;
        gap: 32px;
      }
      .stat-box {
        flex: 1;
        background: rgba(18, 24, 38, 0.9);
        border: 1.5px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 32px;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .stat-label { font-size: 28px; font-weight: 700; color: #94A3B8; text-transform: uppercase; }
      .stat-value { font-size: 64px; font-weight: 900; color: #00FF66; }
      .stat-sub { font-size: 22px; color: #38BDF8; font-weight: 600; }

      /* ── Stripe Proof Card ── */
      .stripe-card {
        width: 980px;
        height: 780px;
        background: rgba(11, 15, 25, 0.97);
        border: 1.5px solid rgba(99, 102, 241, 0.5);
        border-radius: 26px;
        padding: 48px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 24px 60px rgba(0,0,0,0.85), 0 0 55px rgba(99, 102, 241, 0.3);
      }
      .stripe-brand {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      .stripe-logo { font-size: 38px; font-weight: 900; color: #6366F1; letter-spacing: -0.03em; }
      .stripe-badge { background: rgba(34, 197, 94, 0.22); border: 1.5px solid #22C55E; color: #4ADE80; font-size: 22px; font-weight: 800; padding: 8px 20px; border-radius: 999px; }
      .stripe-val { font-size: 84px; font-weight: 900; color: #FFFFFF; letter-spacing: -0.02em; }
      .stripe-growth { color: #22C55E; font-size: 28px; font-weight: 800; margin-top: 8px; }

      /* ── Editorial Yellow Hook Banner ── */
      #hook-banner {
        position: absolute;
        top: 140px;
        left: 40px;
        right: 40px;
        z-index: 50;
        text-align: center;
        opacity: 0;
        pointer-events: none;
      }
      #hook-banner h1 {
        font-family: "Instrument Serif", serif;
        font-style: italic;
        font-size: 64px;
        line-height: 1.12;
        color: #FFE600;
        text-shadow: 0 4px 24px rgba(0, 0, 0, 0.9), 0 0 40px rgba(255, 230, 0, 0.35);
        letter-spacing: -0.01em;
      }
      #hook-banner h1 span {
        font-family: "Inter", sans-serif;
        font-style: normal;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-size: 54px;
        color: #FFFFFF;
        display: block;
        margin-top: 10px;
        text-shadow: 0 4px 24px rgba(0,0,0,0.9);
      }

      /* ── Captions Pill ── */
      #captions-container {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 380px;
        display: flex;
        justify-content: center;
        z-index: 60;
        pointer-events: none;
      }
      .caption-pill {
        position: absolute;
        background: rgba(0, 0, 0, 0.88);
        border: 1.5px solid rgba(255, 255, 255, 0.16);
        border-radius: 9999px;
        padding: 16px 40px;
        font-size: 40px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 0.01em;
        text-transform: uppercase;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7);
        opacity: 0;
        white-space: nowrap;
        backdrop-filter: blur(16px);
      }

      /* ── End Card ── */
      #end-card {
        position: absolute;
        inset: 0;
        z-index: 70;
        background: radial-gradient(circle at center, rgba(15, 23, 42, 0.94), rgba(0, 0, 0, 0.99));
        opacity: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 36px;
        pointer-events: none;
      }
      .end-title {
        font-family: "Instrument Serif", serif;
        font-style: italic;
        font-size: 72px;
        color: #FFE600;
        text-align: center;
        line-height: 1.15;
      }
      .end-btn {
        background: #FFE600;
        color: #000000;
        font-weight: 900;
        font-size: 34px;
        padding: 22px 56px;
        border-radius: 999px;
        box-shadow: 0 12px 36px rgba(255, 230, 0, 0.4);
      }
      .end-sub {
        font-size: 28px;
        color: #94A3B8;
        font-weight: 600;
      }
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-width="1080" data-height="1920" data-fps="30" data-duration="76.3">
      <!-- Master Audio Track -->
      <audio id="soundtrack" src="assets/audio/soundtrack.wav" data-start="0" data-duration="76.3" data-track-index="0" data-volume="1"></audio>

      <!-- Top B-Roll Container -->
      <div id="top-pane">
        <!-- Beat 2A: 3D AI Network -->
        <div id="card-network" class="top-card">
          <video id="broll-network" class="top-video" src="assets/video/broll_network.mp4" data-start="6.8" data-duration="2.9" data-track-index="2" playsinline muted></video>
          <div class="hud-tag" data-layout-ignore="true"><div class="hud-dot"></div> AI SYSTEM ARCHITECTURE // V2.4</div>
        </div>

        <!-- Beat 2B: Live Terminal Web Scraper -->
        <div id="card-terminal" class="top-card">
          <div class="hud-tag" data-layout-ignore="true"><div class="hud-dot"></div> LEAD GEN PIPELINE // LIVE</div>
          <div class="terminal-window">
            <div class="term-header">
              <div class="dot dot-red"></div>
              <div class="dot dot-yellow"></div>
              <div class="dot dot-green"></div>
              <div class="term-title" data-layout-ignore="true">bash - python scraper.py --target enterprise</div>
            </div>
            <div class="term-body" data-layout-ignore="true">
              <div><span class="t-cmd">> python -m scraper</span> <span class="t-cyan">--concurrency 16</span></div>
              <div class="t-purple">[INIT] Connecting to browser cluster...</div>
              <div>[AUTH] Bypassing Cloudflare turnstile... <span class="t-green">SOLVED</span></div>
              <div>[SCRAPE] Target: 250 Enterprise B2B Companies</div>
              <div>[PARSING] Extracting CTO & VP Engineering contacts...</div>
              <div class="t-green">> [SUCCESS] 1,420 Verified Records Extracted to DB</div>
            </div>
          </div>
        </div>

        <!-- Beat 2C: Automation Pipeline -->
        <div id="card-automation" class="top-card">
          <div class="hud-tag" data-layout-ignore="true"><div class="hud-dot"></div> WORKFLOW AUTOMATION // RUNNING</div>
          <div class="pipeline-card">
            <div style="font-size: 28px; font-weight: 800; color: #FFF; display: flex; justify-content: space-between;">
              <span>AI WORKFLOW ORCHESTRATION</span>
              <span style="color: #00FF66;">STATUS: ACTIVE</span>
            </div>
            <div class="node-row">
              <div class="pipe-node">
                <div class="pipe-node-title">Webhook</div>
                <div class="pipe-node-desc" data-layout-ignore="true">New Lead Entry</div>
              </div>
              <div class="pipe-arrow">></div>
              <div class="pipe-node" style="border-color: #FFE600;">
                <div class="pipe-node-title" style="color: #FFE600;">AI Agent</div>
                <div class="pipe-node-desc" data-layout-ignore="true">Analyze & Qualify</div>
              </div>
              <div class="pipe-arrow">></div>
              <div class="pipe-node">
                <div class="pipe-node-title">CRM Sync</div>
                <div class="pipe-node-desc" data-layout-ignore="true">Auto Proposal</div>
              </div>
            </div>
            <div style="background: rgba(0,0,0,0.5); border-radius: 14px; padding: 22px; font-family: monospace; font-size: 28px; color: #94A3B8;" data-layout-ignore="true">
              [TRIGGER] Incoming request received at 14:28:10 UTC<br/>
              [AGENT] Claude 3.7 executed evaluation in 420ms<br/>
              [ACTION] Customized pitch deck sent to client email
            </div>
          </div>
        </div>

        <!-- Beat 2D: Animated Websites Code -->
        <div id="card-code" class="top-card">
          <video id="broll-code" class="top-video" src="assets/video/broll_code.mp4" data-start="18.5" data-duration="3.3" data-track-index="3" playsinline muted></video>
          <div class="hud-tag" data-layout-ignore="true"><div class="hud-dot"></div> DYNAMIC REACT/GSAP ENGINE</div>
        </div>

        <!-- Beat 4: Consultant HUD & Client ROI Dashboard -->
        <div id="card-roi" class="top-card">
          <div class="hud-tag" data-layout-ignore="true"><div class="hud-dot"></div> FULL-TIME CONSULTANT // AUDITED</div>
          <div class="roi-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 28px; font-weight: 800; color: #FFFFFF;">CLIENT IMPACT METRICS</span>
              <span style="background: #FFE600; color: #000; font-size: 28px; font-weight: 800; padding: 6px 18px; border-radius: 999px;">TOP 1% CONSULTANT</span>
            </div>
            <div class="roi-stats">
              <div class="stat-box">
                <div class="stat-label">Hours Saved</div>
                <div class="stat-value">18.5</div>
                <div class="stat-sub" data-layout-ignore="true">per week / client</div>
              </div>
              <div class="stat-box">
                <div class="stat-label">Cost Reduced</div>
                <div class="stat-value">-$4,200</div>
                <div class="stat-sub" data-layout-ignore="true">monthly operational spend</div>
              </div>
            </div>
            <div style="background: rgba(0, 255, 102, 0.12); border: 1.5px solid rgba(0, 255, 102, 0.35); border-radius: 16px; padding: 20px 24px; font-size: 28px; color: #4ADE80; font-weight: 800; text-align: center;">
              Net ROI Generated: +480% in First 30 Days
            </div>
          </div>
        </div>

        <!-- Beat 6A: Stripe Revenue Proof -->
        <div id="card-stripe" class="top-card">
          <div class="hud-tag" data-layout-ignore="true"><div class="hud-dot"></div> REVENUE VERIFIED // STRIPE</div>
          <div class="stripe-card">
            <div class="stripe-brand">
              <div class="stripe-logo">stripe</div>
              <div class="stripe-badge">Live Payments</div>
            </div>
            <div>
              <div style="font-size: 28px; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Gross Volume (Last 30 Days)</div>
              <div class="stripe-val">$12,450.00</div>
              <div class="stripe-growth">▲ +148.2% vs previous period</div>
            </div>
            <div style="display: flex; gap: 24px; border-top: 1px solid rgba(255,255,255,0.12); padding-top: 22px;">
              <div><span style="color: #94A3B8; font-size: 28px;">Active Retainers:</span> <b style="color: #FFF; font-size: 28px;">4 Clients</b></div>
              <div><span style="color: #94A3B8; font-size: 28px;">Avg Deal Size:</span> <b style="color: #FFE600; font-size: 28px;">$3,100 / mo</b></div>
            </div>
          </div>
        </div>

        <!-- Beat 6B: Modern Office Consulting B-Roll -->
        <div id="card-office" class="top-card">
          <video id="broll-office" class="top-video" src="assets/video/broll_office.mp4" data-start="58.5" data-duration="7.9" data-track-index="4" playsinline muted></video>
          <div class="hud-tag" data-layout-ignore="true"><div class="hud-dot"></div> SCALING HIGH-VALUE AI CLIENTS</div>
        </div>
      </div>

      <!-- Speaker Pane -->
      <div id="speaker-pane">
        <video id="speaker-video" src="assets/video/rusan_speaker.mp4" data-start="0" data-duration="76.3" data-track-index="1" playsinline muted></video>
      </div>

      <!-- Neon Split Divider -->
      <div id="split-divider"></div>

      <!-- Editorial Yellow Hook Banner -->
      <div id="hook-banner">
        <h1>How to Make $5,000/mo<span>as an AI CONSULTANT</span></h1>
      </div>

      <!-- Synchronized Micro-Chunked Captions -->
      <div id="captions-container">
"""

for idx, c in enumerate(captions):
    html += f'        <div id="cap-{idx}" class="caption-pill">{c["text"]}</div>\n'

html += """      </div>

      <!-- End Card -->
      <div id="end-card">
        <div class="end-title">Full Breakdown Drops Next</div>
        <div class="end-btn">Follow @rusan.ai for Part 2</div>
        <div class="end-sub">Roadmap, Cold Outreaches & Toolstack Included</div>
      </div>
    </div>

    <!-- GSAP Seekable Timeline Construction -->
    <script>
      (function () {
        const tl = gsap.timeline({ paused: true });

        // 1. Dual Hook (0.0s - 3.8s)
        tl.fromTo("#hook-banner", { autoAlpha: 0, scale: 0.92, y: -20 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(1.5)" }, 0.0);
        tl.to("#hook-banner", { autoAlpha: 0, y: -20, duration: 0.25, ease: "power2.in" }, 3.6);

        // 2. Split Screen Transitions
        // Beat 2 (6.8s - 21.8s): AI Capabilities Split
        tl.to("#speaker-pane", { clipPath: "inset(960px 0px 0px 0px)", duration: 0.35, ease: "power2.out" }, 6.8);
        tl.to("#speaker-video", { y: 820, duration: 0.35, ease: "power2.out" }, 6.8);
        tl.to("#split-divider", { autoAlpha: 1, duration: 0.2 }, 6.8);

        // Top Beat 2A (6.8s - 9.7s): 3D AI Network
        tl.to("#card-network", { autoAlpha: 1, duration: 0.25 }, 6.8);
        tl.to("#card-network", { autoAlpha: 0, duration: 0.2 }, 9.6);

        // Top Beat 2B (9.7s - 15.0s): Terminal Web Scraper
        tl.fromTo("#card-terminal", { autoAlpha: 0, scale: 0.95 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "power2.out" }, 9.7);
        tl.to("#card-terminal", { autoAlpha: 0, duration: 0.2 }, 14.9);

        // Top Beat 2C (15.0s - 18.5s): Automation Pipeline Card
        tl.fromTo("#card-automation", { autoAlpha: 0, scale: 0.95 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "power2.out" }, 15.0);
        tl.to("#card-automation", { autoAlpha: 0, duration: 0.2 }, 18.4);

        // Top Beat 2D (18.5s - 21.8s): Animated Websites Code B-roll
        tl.to("#card-code", { autoAlpha: 1, duration: 0.25 }, 18.5);
        tl.to("#card-code", { autoAlpha: 0, duration: 0.2 }, 21.7);

        // Return to Full Screen (21.8s - 30.2s): State I was in 2 months ago
        tl.to("#speaker-pane", { clipPath: "inset(0px 0px 0px 0px)", duration: 0.35, ease: "power2.inOut" }, 21.8);
        tl.to("#speaker-video", { y: 0, duration: 0.35, ease: "power2.inOut" }, 21.8);
        tl.to("#split-divider", { autoAlpha: 0, duration: 0.2 }, 21.8);

        // Beat 4 (30.2s - 42.1s): AI Consultant Verified HUD & ROI Metrics Split
        tl.to("#speaker-pane", { clipPath: "inset(960px 0px 0px 0px)", duration: 0.35, ease: "power2.out" }, 30.2);
        tl.to("#speaker-video", { y: 820, duration: 0.35, ease: "power2.out" }, 30.2);
        tl.to("#split-divider", { autoAlpha: 1, duration: 0.2 }, 30.2);
        tl.fromTo("#card-roi", { autoAlpha: 0, scale: 0.94 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out" }, 30.2);
        
        // Return to Full Screen (42.1s - 53.2s): Motto of this video
        tl.to("#card-roi", { autoAlpha: 0, duration: 0.2 }, 42.0);
        tl.to("#speaker-pane", { clipPath: "inset(0px 0px 0px 0px)", duration: 0.35, ease: "power2.inOut" }, 42.1);
        tl.to("#speaker-video", { y: 0, duration: 0.35, ease: "power2.inOut" }, 42.1);
        tl.to("#split-divider", { autoAlpha: 0, duration: 0.2 }, 42.1);

        // Beat 6 (53.2s - 66.4s): Revenue Proof & Office B-Roll Split
        tl.to("#speaker-pane", { clipPath: "inset(960px 0px 0px 0px)", duration: 0.35, ease: "power2.out" }, 53.2);
        tl.to("#speaker-video", { y: 820, duration: 0.35, ease: "power2.out" }, 53.2);
        tl.to("#split-divider", { autoAlpha: 1, duration: 0.2 }, 53.2);

        // Top Beat 6A (53.2s - 58.5s): Stripe Dashboard
        tl.fromTo("#card-stripe", { autoAlpha: 0, scale: 0.94 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out" }, 53.2);
        tl.to("#card-stripe", { autoAlpha: 0, duration: 0.2 }, 58.4);

        // Top Beat 6B (58.5s - 66.4s): Modern Office Consulting B-Roll
        tl.to("#card-office", { autoAlpha: 1, duration: 0.25 }, 58.5);
        tl.to("#card-office", { autoAlpha: 0, duration: 0.2 }, 66.3);

        // Return to Full Screen (66.4s - 76.3s): Detailed video later & End Card
        tl.to("#speaker-pane", { clipPath: "inset(0px 0px 0px 0px)", duration: 0.35, ease: "power2.inOut" }, 66.4);
        tl.to("#speaker-video", { y: 0, duration: 0.35, ease: "power2.inOut" }, 66.4);
        tl.to("#split-divider", { autoAlpha: 0, duration: 0.2 }, 66.4);

        // End Card (71.0s - 76.3s)
        tl.fromTo("#end-card", { autoAlpha: 0, scale: 0.9 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "power2.out" }, 71.0);

        // 3. Caption Pills Synced Strictly
"""

for idx, c in enumerate(captions):
    s = c["start"]
    e = c["end"]
    html += f'        tl.fromTo("#cap-{idx}", {{ autoAlpha: 0, scale: 0.92, y: 12 }}, {{ autoAlpha: 1, scale: 1, y: 0, duration: 0.10, ease: "power2.out" }}, {s});\n'
    html += f'        tl.to("#cap-{idx}", {{ autoAlpha: 0, duration: 0.08, ease: "power1.in" }}, {e});\n'

html += """
        window.__timelines["main"] = tl;
        tl.seek(0);
      })();
    </script>
  </body>
</html>
"""

with open("videos/ai-consultant-reel/index.html", "w") as f:
    f.write(html)

print("Regenerated videos/ai-consultant-reel/index.html with GPU transforms!")
