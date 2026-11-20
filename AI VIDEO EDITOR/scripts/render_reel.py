#!/usr/bin/env python3
"""AevyTV-style vertical reel renderer for Rusan's AI Consultant Journey.
Revised with:
1. Professional Color Grade: natural healthy skin tones, rich contrast, no sickly green/yellow tint.
2. Proper A-cuts: Snappy jump cuts alternating 1.0x wide and 1.30x punch-ins with eye-line locked.
3. Distortion-Free Split Screen: Top 50% for Pop B-Roll, Bottom 50% for Rusan with 100% aspect ratio preserved.
4. Rich Pop B-Rolls: Terminal code scraping, 3D neural network, automation node graphs, financial ROI charts, Stripe dashboards.
5. Real Human-Produced Music Bed: Days Like These (authentic drums, Rhodes, bass) mastered to -14.5 LUFS / < -0.5 dBTP.
"""
import os
import sys
import json
import math
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = '/Users/rusan/Documents/Google anti-gravity projects/AI VIDEO EDITOR'
RAW_VIDEO = os.path.join(BASE_DIR, 'Raw video/IMG_2079.mov')
WORDS_JSON = os.path.join(BASE_DIR, 'Raw video/IMG_2079.json')
AUDIO_MASTER = os.path.join(BASE_DIR, 'outputs/audio/soundtrack_mastered.wav')
OUTPUT_VIDEO = os.path.join(BASE_DIR, 'outputs/final_reel.mp4')
FONTS_DIR = os.path.join(BASE_DIR, '.agents/skills/effects/fonts')
BROLL_DIR = os.path.join(BASE_DIR, 'inputs/broll')

# Load Fonts
f_hook_serif = ImageFont.truetype(f'{FONTS_DIR}/PlayfairDisplay-Italic.ttf', 52)
f_hook_sub = ImageFont.truetype(f'{FONTS_DIR}/SpaceMono-Bold.ttf', 40)
f_caption = ImageFont.truetype(f'{FONTS_DIR}/Inter.ttf', 42)
f_card_hdr = ImageFont.truetype(f'{FONTS_DIR}/SpaceMono-Bold.ttf', 32)
f_card_num = ImageFont.truetype(f'{FONTS_DIR}/SpaceMono-Bold.ttf', 30)
f_card_item = ImageFont.truetype(f'{FONTS_DIR}/Inter.ttf', 34)
f_badge = ImageFont.truetype(f'{FONTS_DIR}/SpaceMono-Bold.ttf', 30)
f_mono_sm = ImageFont.truetype(f'{FONTS_DIR}/SpaceMono-Bold.ttf', 23)
f_metric_title = ImageFont.truetype(f'{FONTS_DIR}/SpaceMono-Bold.ttf', 28)
f_metric_val = ImageFont.truetype(f'{FONTS_DIR}/Inter.ttf', 44)
f_heavy = ImageFont.truetype(f'{FONTS_DIR}/ArchivoBlack-Regular.ttf', 76)
f_follow = ImageFont.truetype(f'{FONTS_DIR}/Inter.ttf', 36)

# Load word timestamps and build micro-chunk captions
with open(WORDS_JSON, 'r', encoding='utf-8') as f:
    whisper_data = json.load(f)

words = []
corrections = {
    'vibrating': 'web scraping',
    'interview': 'income / breakthrough',
    'interview.': 'income / breakthrough.'
}

for seg in whisper_data['segments']:
    for w in seg['words']:
        clean_w = w['word'].strip()
        lower_w = clean_w.lower().rstrip('.,!?')
        if lower_w in corrections:
            clean_w = corrections[lower_w]
        words.append({
            'word': clean_w,
            'start': w['start'],
            'end': w['end']
        })

caption_chunks = []
i = 0
while i < len(words):
    chunk_words = [words[i]]
    i += 1
    while i < len(words) and len(chunk_words) < 3:
        if words[i]['start'] - chunk_words[-1]['end'] > 0.4:
            break
        chunk_words.append(words[i])
        if chunk_words[-1]['word'].endswith(('.', '?', '!', ',')):
            i += 1
            break
        i += 1
    chunk_text = ' '.join(cw['word'] for cw in chunk_words)
    caption_chunks.append({
        'start': chunk_words[0]['start'],
        'end': chunk_words[-1]['end'] + 0.15,
        'text': chunk_text
    })

def get_active_caption(t):
    for c in caption_chunks:
        if c['start'] <= t <= c['end']:
            return c['text']
    return None

def apply_pro_grade(bgr):
    """Clean Rec.709 color grade: warm natural skin, rich contrast, clean whites, vibrant pop."""
    img = bgr.astype(np.float32) / 255.0
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    # Remove greenish ceiling cast and warm skin tones
    r = r * 1.04
    g = g * 0.97
    b = b * 1.02
    img = np.clip(np.stack([b, g, r], axis=2), 0, 1)

    # Gamma and contrast S-curve
    img = np.power(img, 0.93)
    img = 0.5 + (img - 0.5) * 1.14
    img = np.clip(img, 0, 1)

    # Vibrance & Saturation boost
    hsv = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.22, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.04, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

# Open optional video B-roll clip for 3D neural net
broll_net_cap = cv2.VideoCapture(os.path.join(BROLL_DIR, 'code_typing.mp4'))

def get_framing(t):
    """Determine camera framing: zoom factor and mode ('medium', 'punch', 'split_terminal', 'split_network', 'split_roi', 'split_stripe')"""
    # Beat 1: 0.0 - 3.5 (Hook)
    if t < 1.4: return 1.0, 'medium'
    if t < 3.5: return 1.32, 'punch'
    # Beat 2: 3.5 - 8.0 (Falling behind?)
    if t < 5.5: return 1.0, 'medium'
    if t < 8.0: return 1.28, 'punch'
    # Beat 3: 8.0 - 15.5 (Web Scraping B-Roll Terminal)
    if t < 15.5: return 1.0, 'split_terminal'
    # Beat 4: 15.5 - 22.0 (Autonomous Agent & Website B-Roll Network)
    if t < 22.0: return 1.0, 'split_network'
    # Beat 5: 22.0 - 25.5 (Rejection tight punch)
    if t < 25.5: return 1.36, 'punch_warning'
    # Beat 6: 25.5 - 32.5 (60 Days Ago)
    if t < 29.0: return 1.0, 'medium'
    if t < 32.5: return 1.28, 'punch'
    # Beat 7: 32.5 - 37.6 (Consultant punch)
    if t < 35.8: return 1.32, 'punch'
    if t < 37.6: return 1.0, 'medium'
    # Beat 8: 37.6 - 41.5 (Automation architect)
    if t < 41.5: return 1.0, 'medium'
    # Beat 9: 41.5 - 51.2 (Client Impact & ROI B-Roll)
    if t < 48.0: return 1.0, 'split_roi'
    if t < 51.2: return 1.30, 'punch'
    # Beat 10: 51.2 - 65.0 (Comparison)
    if t < 58.0: return 1.0, 'medium'
    if t < 65.0: return 1.28, 'punch'
    # Beat 11: 65.0 - 75.0 (Struggle / Underline)
    if t < 70.0: return 1.0, 'medium'
    if t < 75.0: return 1.32, 'punch'
    # Beat 12: 75.0 - 85.0 (Cashflow Positive Stripe B-Roll)
    if t < 81.0: return 1.0, 'split_stripe'
    if t < 85.0: return 1.0, 'medium'
    # Beat 13: 85.0 - 96.3 (Outro & Follow)
    if t < 91.0: return 1.0, 'medium'
    if t < 94.0: return 1.28, 'punch'
    return 1.0, 'medium'

def draw_vector_check(draw, x, y, size=24, active=True):
    col = (0, 255, 136) if active else (100, 100, 100)
    draw.ellipse([x - 5, y - 5, x + size + 5, y + size + 5], outline=col, width=2)
    if active:
        draw.line([(x + 2, y + int(size * 0.5)), (x + int(size * 0.35), y + int(size * 0.8))], fill=col, width=3)
        draw.line([(x + int(size * 0.35), y + int(size * 0.8)), (x + int(size * 0.85), y + int(size * 0.2))], fill=col, width=3)

# ----------------- TOP HALF B-ROLL GENERATORS (1080x960) ----------------- #

def render_broll_terminal(t, w=1080, h=960):
    """Animated macOS terminal running Python Playwright web scraping."""
    img = Image.new('RGB', (w, h), (13, 14, 18))
    draw = ImageDraw.Draw(img, 'RGBA')

    bx0, by0, bx1, by1 = 50, 40, w - 50, h - 40
    # Terminal Window Box
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=22, fill=(18, 20, 26, 255), outline=(255, 255, 255, 38), width=2)
    # Title Bar
    draw.rounded_rectangle([bx0, by0, bx1, by0 + 64], radius=22, fill=(26, 29, 38, 255))
    draw.rectangle([bx0, by0 + 44, bx1, by0 + 64], fill=(26, 29, 38, 255))
    # Window Buttons
    draw.ellipse([bx0 + 24, by0 + 24, bx0 + 42, by0 + 42], fill=(255, 95, 86))
    draw.ellipse([bx0 + 52, by0 + 24, bx0 + 70, by0 + 42], fill=(255, 189, 46))
    draw.ellipse([bx0 + 80, by0 + 24, bx0 + 98, by0 + 42], fill=(39, 201, 63))
    draw.text((bx0 + 120, by0 + 20), 'bash - python3 scrape_pipeline.py', font=f_mono_sm, fill=(180, 180, 180))

    lines = [
        ('$ python3 -m playwright scrape --target "B2B Founders"', (255, 230, 0), 8.0),
        ('[INFO] Initializing headless Chrome cluster...', (160, 160, 160), 8.8),
        ('[STATUS] Connected to proxy pool (US-East)...', (160, 160, 160), 9.6),
        ('[EXTRACT] 2,450 verified business emails extracted', (0, 255, 136), 10.6),
        ('[PIPELINE] Enriching domain records via Apollo API...', (0, 229, 255), 11.8),
        ('[DATABASE] Exporting lead table -> postgres://prod_db', (255, 255, 255), 13.0),
        ('[SUCCESS] Web scraping workflow finished in 4.2s', (0, 255, 136), 14.0),
    ]

    y = by0 + 95
    for text, col, show_t in lines:
        if t >= show_t:
            draw.text((bx0 + 36, y), text, font=f_mono_sm, fill=col)
        y += 56

    # Bottom badge
    draw.rounded_rectangle([bx0 + 36, by1 - 90, bx0 + 470, by1 - 32], radius=14, fill=(0, 255, 136, 30), outline=(0, 255, 136, 160), width=1)
    draw.ellipse([bx0 + 56, by1 - 68, bx0 + 72, by1 - 52], fill=(0, 255, 136))
    draw.text((bx0 + 86, by1 - 74), 'LIVE WEB SCRAPING ENGINE', font=f_mono_sm, fill=(0, 255, 136))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def render_broll_network(t, w=1080, h=960):
    """3D neural network video B-roll overlaid with automation pipeline nodes."""
    ret, frame_net = broll_net_cap.read()
    if not ret:
        broll_net_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame_net = broll_net_cap.read()
    
    # Scale neural net to 1080x960
    base = cv2.resize(frame_net, (w, h), interpolation=cv2.INTER_LINEAR)
    # Darken slightly for high-contrast card overlays
    base = (base * 0.65).astype(np.uint8)

    img = Image.fromarray(cv2.cvtColor(base, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Top title tag
    draw.rounded_rectangle([60, 45, 580, 110], radius=14, fill=(12, 14, 18, 220), outline=(255, 230, 0, 140), width=1)
    draw.text((85, 60), '// AUTONOMOUS AI AGENTS', font=f_card_hdr, fill=(255, 230, 0))

    # Pipeline Cards
    nodes = [
        ('01', 'WEBHOOK TRIGGER', 'Incoming Client Lead', 15.5, (0, 229, 255)),
        ('02', 'AUTONOMOUS AGENT', 'Claude 3.7 Reasoning', 17.0, (255, 230, 0)),
        ('03', 'MOTION ENGINE', 'GSAP / React Render', 18.5, (0, 255, 136)),
        ('04', 'ACTIVE DELIVERABLE', 'Revenue Deal Closed', 20.0, (0, 255, 136)),
    ]

    ny = 140
    for num, title, desc, show_t, col in nodes:
        act = (t >= show_t)
        bg_col = (15, 18, 24, 235) if act else (15, 18, 24, 160)
        border_col = col if act else (255, 255, 255, 30)
        draw.rounded_rectangle([60, ny, w - 60, ny + 115], radius=18, fill=bg_col, outline=border_col, width=2)
        draw_vector_check(draw, 96, ny + 28, 22, active=act)
        draw.text((140, ny + 20), num, font=f_card_num, fill=col if act else (120, 120, 120))
        draw.text((200, ny + 18), title, font=f_card_hdr, fill=(255, 255, 255) if act else (140, 140, 140))
        draw.text((200, ny + 64), desc, font=f_mono_sm, fill=(180, 180, 180) if act else (100, 100, 100))
        ny += 135

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def render_broll_roi(t, w=1080, h=960):
    """Financial & Time Efficiency Dashboard with animated progress."""
    img = Image.new('RGB', (w, h), (13, 14, 18))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Grid lines
    for gx in range(60, w, 120):
        draw.line([(gx, 40), (gx, h - 40)], fill=(255, 255, 255, 12), width=1)
    for gy in range(60, h, 120):
        draw.line([(40, gy), (w - 40, gy)], fill=(255, 255, 255, 12), width=1)

    # Header Card
    draw.rounded_rectangle([60, 45, 520, 110], radius=14, fill=(255, 230, 0, 30), outline=(255, 230, 0, 180), width=1)
    draw.text((85, 60), '// CLIENT ROI & IMPACT', font=f_card_hdr, fill=(255, 230, 0))

    metrics = [
        ('[TIME EFFICIENCY]', '80% TIME SAVED', (0, 229, 255), 41.5, 0.80),
        ('[REVENUE MULTIPLIER]', '3.2X REVENUE ACCELERATION', (255, 230, 0), 43.5, 0.95),
        ('[COST REDUCTION]', '$15,000+ SAVED / MONTH', (0, 255, 136), 45.5, 0.88),
    ]

    my = 145
    for tag, val, col, show_t, bar_pct in metrics:
        act = (t >= show_t)
        draw.rounded_rectangle([60, my, w - 60, my + 175], radius=20, fill=(18, 20, 26, 245), outline=(255, 255, 255, 38), width=1)
        draw_vector_check(draw, 96, my + 30, 22, active=act)
        draw.text((140, my + 24), tag, font=f_metric_title, fill=(180, 180, 180) if act else (110, 110, 110))
        draw.text((140, my + 68), val, font=f_metric_val, fill=col if act else (120, 120, 120))

        # Animated progress bar
        bar_w = int((w - 200) * bar_pct) if act else 40
        draw.rounded_rectangle([140, my + 130, w - 100, my + 144], radius=7, fill=(35, 38, 48))
        if act:
            draw.rounded_rectangle([140, my + 130, 140 + bar_w, my + 144], radius=7, fill=col)
        my += 205

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def render_broll_stripe(t, w=1080, h=960):
    """Sleek Stripe / Revenue Dashboard B-Roll."""
    img = Image.new('RGB', (w, h), (13, 14, 18))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Card container
    draw.rounded_rectangle([50, 45, w - 50, h - 45], radius=24, fill=(18, 20, 26, 250), outline=(0, 255, 136, 120), width=2)
    # Header
    draw.text((90, 75), '// PROFITABLE AI CONSULTANCY', font=f_card_hdr, fill=(0, 255, 136))
    draw.text((90, 125), 'Monthly Gross Volume', font=f_mono_sm, fill=(160, 160, 160))
    # Big Number
    draw.text((90, 165), '$18,450.00', font=ImageFont.truetype(f'{FONTS_DIR}/Inter.ttf', 64), fill=(255, 255, 255))

    # Metric pills
    draw.rounded_rectangle([90, 260, 420, 315], radius=14, fill=(0, 255, 136, 30), outline=(0, 255, 136, 180), width=1)
    draw.text((115, 275), '+340% vs DAY 0', font=f_mono_sm, fill=(0, 255, 136))

    draw.rounded_rectangle([440, 260, 780, 315], radius=14, fill=(255, 230, 0, 30), outline=(255, 230, 0, 180), width=1)
    draw.text((465, 275), '92.5% NET MARGIN', font=f_mono_sm, fill=(255, 230, 0))

    # Graph line simulation
    pts = [(90, 680), (220, 620), (360, 640), (520, 520), (680, 480), (840, 410), (990, 360)]
    for idx in range(len(pts) - 1):
        draw.line([pts[idx], pts[idx+1]], fill=(0, 255, 136, 230), width=6)
        draw.ellipse([pts[idx][0]-8, pts[idx][1]-8, pts[idx][0]+8, pts[idx][1]+8], fill=(0, 255, 136))
    draw.ellipse([pts[-1][0]-10, pts[-1][1]-10, pts[-1][0]+10, pts[-1][1]+10], fill=(255, 255, 255))

    # Status badge
    draw.rounded_rectangle([90, 740, w - 90, 830], radius=18, fill=(0, 255, 136, 240))
    draw.text((140, 765), '>> STATUS: CASH FLOW POSITIVE FOUNDER', font=f_card_hdr, fill=(10, 15, 12))

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# ----------------- MAIN COMPOSITOR ----------------- #

def render_frame(raw_bgr, t, w_out=1080, h_out=1920):
    raw_h, raw_w, _ = raw_bgr.shape
    zoom, mode = get_framing(t)

    # Apply professional color grade to Rusan's footage
    graded_raw = apply_pro_grade(raw_bgr)

    canvas = np.zeros((h_out, w_out, 3), dtype=np.uint8)

    if mode.startswith('split'):
        # SPLIT SCREEN MODE:
        # Top 50% (0:960, 0:1080) -> Pop B-Roll
        # Bottom 50% (960:1920, 0:1080) -> Rusan's Video (Distortion-Free)

        # 1. Rusan Bottom Tile (Aspect Ratio 1080x960 = 1.125 preserved)
        crop_w = int(raw_h * 1080 / 960) # 1215
        crop_x = int((raw_w - crop_w) / 2) # 352
        cropped_speaker = graded_raw[0:raw_h, crop_x:crop_x+crop_w]
        speaker_tile = cv2.resize(cropped_speaker, (1080, 960), interpolation=cv2.INTER_LANCZOS4)
        canvas[960:1920, :] = speaker_tile

        # 2. Render Matching Pop B-Roll on Top
        if mode == 'split_terminal':
            top_broll = render_broll_terminal(t, w=1080, h=960)
        elif mode == 'split_network':
            top_broll = render_broll_network(t, w=1080, h=960)
        elif mode == 'split_roi':
            top_broll = render_broll_roi(t, w=1080, h=960)
        elif mode == 'split_stripe':
            top_broll = render_broll_stripe(t, w=1080, h=960)
        else:
            top_broll = render_broll_terminal(t, w=1080, h=960)

        canvas[0:960, :] = top_broll

        # Divider Hairline with glow
        cv2.line(canvas, (0, 959), (w_out, 959), (255, 230, 0), 2)

    else:
        # FULL SCREEN A-ROLL JUMP CUTS (9:16 vertical)
        base_crop_w = int(raw_h * 9 / 16) # 608
        cw = int(base_crop_w / zoom)
        ch = int(raw_h / zoom)
        cx = int((raw_w - cw) / 2)
        cy = int((raw_h - ch) * 0.35) if zoom > 1.0 else 0
        cropped = graded_raw[cy:cy+ch, cx:cx+cw]
        canvas[:] = cv2.resize(cropped, (w_out, h_out), interpolation=cv2.INTER_LANCZOS4)

    # Typographic Overlays via PIL
    pil_img = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img, 'RGBA')

    # Beat 1 (0.0s - 3.5s): Yellow Hook Banner
    if 0.0 <= t < 3.5:
        hook_main = "How are people doing so much with AI..."
        hook_sub = "AND YOU ARE NOT?!"
        draw.rectangle([0, 0, w_out, 240], fill=(0, 0, 0, 160))
        bbox1 = draw.textbbox((0, 0), hook_main, font=f_hook_serif)
        tw1 = bbox1[2] - bbox1[0]
        draw.text(((w_out - tw1) // 2 + 3, 63), hook_main, font=f_hook_serif, fill=(0, 0, 0, 220))
        draw.text(((w_out - tw1) // 2, 60), hook_main, font=f_hook_serif, fill=(255, 230, 0, 255))
        bbox2 = draw.textbbox((0, 0), hook_sub, font=f_hook_sub)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((w_out - tw2) // 2 + 2, 137), hook_sub, font=f_hook_sub, fill=(0, 0, 0, 200))
        draw.text(((w_out - tw2) // 2, 135), hook_sub, font=f_hook_sub, fill=(255, 255, 255, 255))

    # Beat 2 (3.5s - 8.0s): Backdrop text
    elif 3.5 <= t < 8.0:
        word = "FALLING BEHIND?"
        bbox = draw.textbbox((0, 0), word, font=f_heavy)
        tw = bbox[2] - bbox[0]
        draw.rounded_rectangle([(w_out - tw)//2 - 24, 180, (w_out + tw)//2 + 24, 280], radius=16, fill=(0, 0, 0, 180))
        draw.text(((w_out - tw) // 2, 190), word, font=f_heavy, fill=(255, 255, 255, 245))

    # Beat 5 (22.0s - 25.5s): Warning Box
    elif 22.0 <= t < 25.5:
        stamp_text = "BLOCKED: ZERO REVENUE"
        bbox = draw.textbbox((0, 0), stamp_text, font=f_card_hdr)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        bx0 = (w_out - tw) // 2 - 32
        by0 = 360
        draw.rounded_rectangle([bx0, by0, bx0 + tw + 64, by0 + th + 40], radius=16, fill=(255, 30, 50, 45), outline=(255, 40, 60, 240), width=4)
        draw.text(((w_out - tw)//2, by0 + 20), stamp_text, font=f_card_hdr, fill=(255, 60, 80, 255))

    # Beat 6 (25.5s - 32.5s): 60 Days Ago pill
    elif 25.5 <= t < 32.5:
        pill_text = "[60 DAYS AGO]"
        draw.rounded_rectangle([70, 120, 360, 184], radius=16, fill=(0, 0, 0, 210), outline=(255, 255, 255, 40), width=1)
        draw.text((95, 136), pill_text, font=f_badge, fill=(240, 240, 240))

    # Beat 7 (32.5s - 37.6s): Consultant Golden Badge
    elif 32.5 <= t < 37.6:
        badge_text = "// FULL-TIME AI CONSULTANT"
        bbox = draw.textbbox((0, 0), badge_text, font=f_card_hdr)
        tw = bbox[2] - bbox[0]
        bx0 = (w_out - tw)//2 - 36
        draw.rounded_rectangle([bx0, 150, bx0 + tw + 72, 226], radius=18, fill=(255, 230, 0, 245))
        draw.text(((w_out - tw)//2, 168), badge_text, font=f_card_hdr, fill=(10, 10, 10))

    # Beat 8 (37.6s - 41.5s): Active Automations Tag
    elif 37.6 <= t < 41.5:
        draw.rounded_rectangle([70, 130, 520, 200], radius=18, fill=(15, 16, 20, 230), outline=(0, 255, 136, 120), width=2)
        draw.ellipse([96, 155, 114, 173], fill=(0, 255, 136))
        draw.text((130, 146), "AI AUTOMATIONS ACTIVE", font=f_badge, fill=(255, 255, 255))

    # Beat 10 (51.2s - 65.0s): Comparison Banner
    elif 51.2 <= t < 65.0:
        draw.rounded_rectangle([70, 130, 460, 198], radius=16, fill=(0, 0, 0, 210), outline=(255, 255, 255, 40), width=1)
        draw.text((95, 146), "[DAY 0: LOST & STUCK]", font=f_badge, fill=(200, 200, 200))

    # Beat 11 (65.0s - 75.0s): Underline struggle
    elif 65.0 <= t < 75.0:
        if 70.0 <= t <= 75.0:
            draw.line([(240, 1530), (840, 1535)], fill=(255, 45, 65, 240), width=8)

    # Beat 13 (85.0s - 96.3s): Follow CTA Button
    elif 85.0 <= t < 96.3:
        is_followed = (t >= 89.0)
        btn_text = "FOLLOWING @RUSAN" if is_followed else "+ FOLLOW @RUSAN"
        btn_bg = (255, 255, 255, 245) if is_followed else (255, 230, 0, 245)
        btn_txt_col = (10, 10, 10)
        bbox = draw.textbbox((0, 0), btn_text, font=f_follow)
        tw = bbox[2] - bbox[0]
        bx0 = (w_out - tw)//2 - 36
        by0 = 980
        draw.rounded_rectangle([bx0, by0, bx0 + tw + 72, by0 + 78], radius=22, fill=btn_bg)
        if is_followed:
            draw_vector_check(draw, bx0 + 24, by0 + 26, 22, active=True)
            draw.text((bx0 + 64, by0 + 20), btn_text, font=f_follow, fill=btn_txt_col)
        else:
            draw.text(((w_out - tw)//2, by0 + 20), btn_text, font=f_follow, fill=btn_txt_col)

    # Synchronized Micro-Chunked Pill Captions
    active_cap = get_active_caption(t)
    if active_cap:
        bbox = draw.textbbox((0, 0), active_cap, font=f_caption)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        pad_x, pad_y = 28, 14
        # Position caption in lower third of speaker tile
        cap_y = 1520 if mode.startswith('split') else 1460
        x0 = int((w_out - tw) / 2) - pad_x
        y0 = cap_y - pad_y
        x1 = int((w_out + tw) / 2) + pad_x
        y1 = cap_y + th + pad_y
        draw.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=(0, 0, 0, 225))
        draw.text((int((w_out - tw) / 2), cap_y), active_cap, font=f_caption, fill=(255, 255, 255))

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def main():
    print(f"Opening raw video: {RAW_VIDEO}")
    cap = cv2.VideoCapture(RAW_VIDEO)
    if not cap.isOpened():
        print(f"Error: Could not open {RAW_VIDEO}", file=sys.stderr)
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = total_frames / fps
    print(f"Video metadata: {total_frames} frames, {fps:.2f} fps, {dur:.2f}s")

    os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)

    ffmpeg_cmd = [
        'ffmpeg', '-v', 'warning', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1080x1920', '-r', str(fps),
        '-i', '-',
        '-i', AUDIO_MASTER,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'h264_videotoolbox', '-b:v', '12M',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest',
        '-movflags', '+faststart',
        OUTPUT_VIDEO
    ]
    print(f"Starting ffmpeg hardware-accelerated pipeline -> {OUTPUT_VIDEO}")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    frame_idx = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            t = frame_idx / fps
            out_bgr = render_frame(frame, t)
            proc.stdin.write(out_bgr.tobytes())
            frame_idx += 1
            if frame_idx % 200 == 0 or frame_idx == total_frames:
                pct = (frame_idx / total_frames) * 100
                print(f"  Rendered {frame_idx}/{total_frames} frames ({pct:.1f}%) - {t:.1f}s / {dur:.1f}s", flush=True)
    finally:
        cap.release()
        broll_net_cap.release()
        proc.stdin.close()
        proc.wait()

    if proc.returncode == 0:
        file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f"SUCCESS: Rendered revised vertical reel to {OUTPUT_VIDEO} ({file_size_mb:.2f} MB)")
    else:
        print(f"ERROR: ffmpeg exited with code {proc.returncode}", file=sys.stderr)
        sys.exit(proc.returncode)

if __name__ == '__main__':
    main()
