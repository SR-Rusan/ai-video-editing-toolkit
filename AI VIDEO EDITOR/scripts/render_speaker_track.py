import cv2
import numpy as np
import json
import time

t0 = time.time()
with open("AI VIDEO EDITOR/inputs/snappy_cuts.json") as f:
    cuts = json.load(f)

# Jump cut schedule (alternating 1.0x wide and 1.3x punch-in)
# We want punch-in on strong emphasis beats:
# 0.0 - 0.85: 1.0x
# 0.85 - 3.4: 1.3x ("wondered in the past few days")
# 3.4 - 6.8: 1.0x ("and you are not?")
# 6.8 - 9.7: 1.0x ("You have a lot of ideas")
# 9.7 - 15.0: 1.0x (Split Screen B-Roll)
# 15.0 - 21.8: 1.0x (Split Screen B-Roll)
# 21.8 - 25.5: 1.0x ("See that was the state")
# 25.5 - 30.2: 1.3x ("probably two months ago")
# 30.2 - 34.2: 1.0x (Split Screen Consultant HUD)
# 34.2 - 42.1: 1.0x (Split Screen ROI Dashboard)
# 42.1 - 47.0: 1.0x ("motto of this video")
# 47.0 - 50.5: 1.3x ("particular Rusan who was lost")
# 50.5 - 53.2: 1.0x ("couldn't start a business")
# 53.2 - 66.4: 1.0x (Split Screen Stripe Proof & Office B-Roll)
# 66.4 - 71.0: 1.3x ("detailed video later")
# 71.0 - 76.3: 1.0x ("so that was it for today")

punch_ranges = [
    (0.85, 3.40),
    (25.50, 30.20),
    (47.00, 50.50),
    (66.40, 71.00)
]

def is_punched_in(t):
    for s, e in punch_ranges:
        if s <= t < e:
            return True
    return False

# Open raw video
cap = cv2.VideoCapture("AI VIDEO EDITOR/Raw video/IMG_2079.mov")
fps = 30.0
W, H = 1080, 1920

# Video writer
out_path = "videos/ai-consultant-reel/assets/video/rusan_speaker.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(out_path, fourcc, fps, (W, H))

cx = 960
# 1.0x crop (608 x 1080)
crop_w_1 = 608
crop_h_1 = 1080
x1_1 = cx - crop_w_1 // 2
x2_1 = x1_1 + crop_w_1

# 1.3x punch-in crop (468 x 830) centered slightly up towards eyes (cy=480)
zoom = 1.32
crop_w_z = int(608 / zoom)
crop_h_z = int(1080 / zoom)
cy = 480
x1_z = cx - crop_w_z // 2
x2_z = x1_z + crop_w_z
y1_z = max(0, cy - crop_h_z // 2)
y2_z = y1_z + crop_h_z

total_frames_rendered = 0
timeline_t = 0.0

for cut in cuts:
    src_start = cut["src_start"]
    src_end = cut["src_end"]
    duration = cut["duration"]
    
    start_frame = int(round(src_start * fps))
    end_frame = int(round(src_end * fps))
    num_frames = max(1, end_frame - start_frame)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    for f_idx in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break
        
        current_t = timeline_t + f_idx / fps
        punched = is_punched_in(current_t)
        
        # Color grade (Natural Warm Rec.709)
        g = frame.astype(np.float32)
        g[:, :, 0] = g[:, :, 0] * 0.96
        g[:, :, 1] = g[:, :, 1] * 0.96
        g[:, :, 2] = np.clip(g[:, :, 2] * 1.05, 0, 255)
        g = np.clip((g - 128) * 1.08 + 128, 0, 255).astype(np.uint8)
        
        if punched:
            cropped = g[y1_z:y2_z, x1_z:x2_z]
        else:
            cropped = g[:, x1_1:x2_1]
            
        resized = cv2.resize(cropped, (W, H), interpolation=cv2.INTER_LANCZOS4)
        out.write(resized)
        total_frames_rendered += 1
        
    timeline_t += duration

cap.release()
out.release()

# Re-encode to standard H.264 using FFmpeg for optimal browser decoding
h264_path = "videos/ai-consultant-reel/assets/video/rusan_speaker_h264.mp4"
import subprocess
cmd = [
    "ffmpeg", "-y", "-i", out_path,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18",
    h264_path
]
subprocess.run(cmd, check=True)
import os
os.replace(h264_path, out_path)

print(f"Rendered {total_frames_rendered} frames ({total_frames_rendered/fps:.2f}s) in {time.time()-t0:.2f}s to {out_path}")
