import cv2
import numpy as np

cap = cv2.VideoCapture("AI VIDEO EDITOR/Raw video/IMG_2079.mov")
cap.set(cv2.CAP_PROP_POS_MSEC, 12000) # 12s in raw
ret, raw_frame = cap.read()
cap.release()

if ret:
    # 1. Apply Natural Warm Rec.709 Color Grade
    # BGR channels: B * 0.96, G * 0.96, R * 1.05
    g = raw_frame.astype(np.float32)
    g[:, :, 0] = g[:, :, 0] * 0.96
    g[:, :, 1] = g[:, :, 1] * 0.96
    g[:, :, 2] = np.clip(g[:, :, 2] * 1.05, 0, 255)
    # S-curve contrast
    g = np.clip((g - 128) * 1.08 + 128, 0, 255).astype(np.uint8)

    # 2. Test Full-Screen 9:16 Crop (1080x1920)
    # Source is 1920x1080. 9:16 crop is 608x1080 centered at cx=960.
    cx = 960
    x1, x2 = cx - 304, cx + 304
    crop_fs = g[:, x1:x2]
    fs_1080x1920 = cv2.resize(crop_fs, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/test_fullscreen_9_16.jpg", fs_1080x1920)

    # 3. Test Bottom-Half Split Framing (1080x960)
    # Method A: Inside 1080x1920, take y from 260 to 1220 (height=960)
    bottom_half_A = fs_1080x1920[260:1220, 0:1080]
    
    # Method B: Direct 9:8 source crop (1215 x 1080) centered at cx=960
    # 1215/1080 = 1.125 = 1080/960.
    x1_b = int(cx - 1215/2)
    x2_b = int(cx + 1215/2)
    crop_b = g[:, x1_b:x2_b]
    bottom_half_B = cv2.resize(crop_b, (1080, 960), interpolation=cv2.INTER_LANCZOS4)

    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/test_bottom_half_A.jpg", bottom_half_A)
    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/test_bottom_half_B.jpg", bottom_half_B)

    # Compose test canvas: top B-roll (1080x960), bottom Rusan (1080x960)
    canvas = np.zeros((1920, 1080, 3), dtype=np.uint8)
    
    # Load broll frame
    broll_frame = cv2.imread("AI VIDEO EDITOR/outputs/check_frames/frame_code_1.jpg")
    if broll_frame is not None:
        # crop broll to 1080x960
        bx1 = int((1920 - 1215)/2)
        b_crop = broll_frame[:, bx1:bx1+1215]
        b_res = cv2.resize(b_crop, (1080, 960), interpolation=cv2.INTER_LANCZOS4)
        canvas[0:960, 0:1080] = b_res
    
    canvas[960:1920, 0:1080] = bottom_half_B
    # draw clean glowing divider line at y=960
    cv2.line(canvas, (0, 960), (1080, 960), (0, 230, 255), 4) # yellow neon accent
    
    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/test_split_composite.jpg", canvas)
    print("Saved test split frames to AI VIDEO EDITOR/outputs/check_frames/")
