import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import time
import os
import subprocess

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Color tokens
COLOR_BG = hex_to_rgb('#1A1614')
COLOR_BG_CENTER = hex_to_rgb('#2B221E')
COLOR_TERRACOTTA = hex_to_rgb('#D96B43')
COLOR_BURNT_ORANGE = hex_to_rgb('#C85A32')
COLOR_OCHRE = hex_to_rgb('#DDA15E')
COLOR_LINEN = hex_to_rgb('#F7F4EF')
COLOR_SAND = hex_to_rgb('#EFE9DF')
COLOR_DARK = hex_to_rgb('#1F1916')

W, H = 1080, 1920
FPS = 60
DURATION = 6.0
TOTAL_FRAMES = int(FPS * DURATION)

# Isometric projection parameters
COS30 = math.cos(math.radians(30))
SIN30 = math.sin(math.radians(30))
CX, CY = 540, 1080

def iso_project(x, y, z):
    # Isometric formula
    u = CX + (x - y) * COS30
    v = CY + (x + y) * SIN30 - z
    return (u, v)

def draw_block(draw, x, y, z, w, l, h, color, label=""):
    # Calculate 8 vertices of cuboid
    # x: left-right, y: depth, z: height
    v = [
        iso_project(x - w/2, y - l/2, z),      # 0: bottom-back-left
        iso_project(x + w/2, y - l/2, z),      # 1: bottom-back-right
        iso_project(x + w/2, y + l/2, z),      # 2: bottom-front-right
        iso_project(x - w/2, y + l/2, z),      # 3: bottom-front-left
        iso_project(x - w/2, y - l/2, z + h),  # 4: top-back-left
        iso_project(x + w/2, y - l/2, z + h),  # 5: top-back-right
        iso_project(x + w/2, y + l/2, z + h),  # 6: top-front-right
        iso_project(x - w/2, y + l/2, z + h),  # 7: top-front-left
    ]
    
    # 3 visible faces in isometric projection:
    # Top face: 4, 5, 6, 7
    # Left (front-left) face: 7, 6, 2, 3 (facing viewer)
    # Right (front-right) face: 6, 5, 1, 2 (facing viewer)
    
    r, g, b = color
    # Shading multipliers
    top_color = (min(255, int(r * 1.15)), min(255, int(g * 1.15)), min(255, int(b * 1.15)))
    left_color = (int(r * 0.85), int(g * 0.85), int(b * 0.85))
    right_color = (int(r * 0.65), int(g * 0.65), int(b * 0.65))
    stroke_color = (max(0, int(r * 0.5)), max(0, int(g * 0.5)), max(0, int(b * 0.5)))
    
    # Left face (front-left)
    draw.polygon([v[3], v[2], v[6], v[7]], fill=left_color, outline=stroke_color)
    # Right face (front-right)
    draw.polygon([v[2], v[1], v[5], v[6]], fill=right_color, outline=stroke_color)
    # Top face
    draw.polygon([v[4], v[5], v[6], v[7]], fill=top_color, outline=stroke_color)
    
    # Draw tactile cylindrical studs on top face
    stud_r = 14
    stud_h = 10
    stud_offsets = [
        (-w/4, -l/4),
        (w/4, -l/4),
        (-w/4, l/4),
        (w/4, l/4)
    ]
    for ox, oy in stud_offsets:
        sx, sy = x + ox, y + oy
        sz = z + h
        # top of stud
        p_base = iso_project(sx, sy, sz)
        p_top = iso_project(sx, sy, sz + stud_h)
        
        # Stud cylinder side
        draw.ellipse([p_base[0] - stud_r, p_base[1] - stud_r*0.5, p_base[0] + stud_r, p_base[1] + stud_r*0.5], fill=left_color)
        draw.rectangle([p_top[0] - stud_r, p_top[1], p_base[0] + stud_r, p_base[1]], fill=left_color)
        # Stud top cap
        stud_cap_color = (min(255, int(r * 1.3)), min(255, int(g * 1.3)), min(255, int(b * 1.3)))
        draw.ellipse([p_top[0] - stud_r, p_top[1] - stud_r*0.5, p_top[0] + stud_r, p_top[1] + stud_r*0.5], fill=stud_cap_color, outline=stroke_color)

def bounce_z(t, start_t, target_z, drop_height=1100):
    if t < start_t:
        return target_z + drop_height
    dt = t - start_t
    # Damped harmonic oscillator
    decay = math.exp(-6.5 * dt)
    bounce = math.cos(14.0 * dt)
    val = target_z + drop_height * decay * bounce
    return max(target_z, val) if dt > 0.8 else val

def render_frame(frame_idx):
    t = frame_idx / FPS
    
    # Background: Radial vignette from dark truffle to espresso
    im = Image.new('RGB', (W, H), COLOR_BG)
    draw = ImageDraw.Draw(im)
    
    # Ground grid
    for gx in range(-400, 500, 100):
        p1 = iso_project(gx, -400, 0)
        p2 = iso_project(gx, 400, 0)
        draw.line([p1, p2], fill=(45, 37, 33), width=1)
    for gy in range(-400, 500, 100):
        p1 = iso_project(-400, gy, 0)
        p2 = iso_project(400, gy, 0)
        draw.line([p1, p2], fill=(45, 37, 33), width=1)
        
    # Block definitions (x, y, target_z, w, l, h, color, start_time)
    blocks = [
        # Level 1: Foundation Bricks (Order: back to front so painter's algorithm renders correctly)
        (-140, 0, 0, 120, 120, 80, COLOR_BURNT_ORANGE, 0.15),
        (0, 0, 0, 120, 120, 80, COLOR_TERRACOTTA, 0.40),
        (140, 0, 0, 120, 120, 80, COLOR_OCHRE, 0.65),
        
        # Level 2: Interlocking Mid Layer
        (-70, 0, 80, 120, 120, 80, COLOR_LINEN, 1.25),
        (70, 0, 80, 120, 120, 80, COLOR_SAND, 1.55),
        
        # Level 3: Crown Keystone
        (0, 0, 160, 130, 130, 90, COLOR_TERRACOTTA, 2.20),
    ]
    
    # Draw blocks
    for bx, by, bz, bw, bl, bh, bcol, bstart in blocks:
        curr_z = bounce_z(t, bstart, bz)
        draw_block(draw, bx, by, curr_z, bw, bl, bh, bcol)
        
    # Energy pulse along seamlines after t > 2.8s
    if t > 2.8:
        pulse_alpha = min(1.0, (t - 2.8) / 0.6)
        # Pulse beam
        pulse_col = (255, 160, 110)
        p_mid1 = iso_project(-70, 0, 80)
        p_mid2 = iso_project(70, 0, 80)
        p_crown = iso_project(0, 0, 160)
        draw.line([p_mid1, p_crown], fill=pulse_col, width=4)
        draw.line([p_mid2, p_crown], fill=pulse_col, width=4)
        
    # HUD / Graphic badges in lower half
    # Badge: "MODULAR AI INFRASTRUCTURE"
    card_y = 1420
    draw.rounded_rectangle([120, card_y, 960, card_y + 260], radius=24, fill=(28, 22, 19), outline=(217, 107, 67), width=2)
    
    # Text in card
    # Headline
    draw.text((160, card_y + 40), "MODULAR BUSINESS ARCHITECTURE", fill=COLOR_LINEN)
    draw.text((160, card_y + 85), "// BUILDING AUTOMATION BRICK-BY-BRICK", fill=COLOR_OCHRE)
    
    # Two stat pills
    draw.rounded_rectangle([160, card_y + 140, 520, card_y + 220], radius=16, fill=(45, 34, 29))
    draw.text((180, card_y + 155), "80% TIME SAVED", fill=COLOR_TERRACOTTA)
    
    draw.rounded_rectangle([560, card_y + 140, 920, card_y + 220], radius=16, fill=(45, 34, 29))
    draw.text((580, card_y + 155), "3.4X REVENUE VELOCITY", fill=COLOR_OCHRE)
    
    return np.array(im)

def main():
    t0 = time.time()
    out_path = "/Users/rusan/Documents/Google anti-gravity projects/videos/ai-consultant-reel/assets/video/broll_bricks.mp4"
    temp_raw = "/tmp/raw_bricks.mp4"
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_raw, fourcc, float(FPS), (W, H))
    
    print(f"Rendering {TOTAL_FRAMES} frames of modular 3D bricks B-roll...")
    for f in range(TOTAL_FRAMES):
        frame = render_frame(f)
        # RGB to BGR for cv2
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
        if f % 60 == 0:
            print(f"Rendered {f}/{TOTAL_FRAMES} frames ({f/TOTAL_FRAMES*100:.1f}%)")
            
    out.release()
    
    # H.264 encode via ffmpeg
    cmd = [
        "ffmpeg", "-y", "-i", temp_raw,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18",
        out_path
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_raw):
        os.remove(temp_raw)
        
    print(f"Rendered 3D Bricks B-roll in {time.time()-t0:.2f}s to {out_path}!")

if __name__ == '__main__':
    main()
