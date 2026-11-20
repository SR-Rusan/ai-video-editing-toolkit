import cv2
import numpy as np

cap = cv2.VideoCapture("AI VIDEO EDITOR/Raw video/IMG_2079.mov")
cap.set(cv2.CAP_PROP_POS_MSEC, 4000) # at 4 seconds
ret, frame = cap.read()
cap.release()

if ret:
    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/raw_4s.jpg", frame)
    
    # Grade 1: Clean Rec709 Natural Warm (subtle green reduction, gentle warm lift)
    g1 = frame.astype(np.float32)
    # BGR channels:
    # Reduce green cast slightly, lift red slightly
    g1[:, :, 0] = g1[:, :, 0] * 0.96 # Blue
    g1[:, :, 1] = g1[:, :, 1] * 0.96 # Green
    g1[:, :, 2] = np.clip(g1[:, :, 2] * 1.05, 0, 255) # Red
    # Contrast S-curve
    g1 = np.clip((g1 - 128) * 1.08 + 128, 0, 255)
    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/grade_1_natural_warm.jpg", g1.astype(np.uint8))
    
    # Grade 2: Cinema Clean Studio (Punchy, rich contrast, healthy skin tones)
    # Convert to YCrCb or Lab to boost skin chroma cleanly
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
    # L channel contrast S-curve
    L = lab[:, :, 0]
    L = np.clip(128.0 + 1.15 * (L - 128.0), 0, 255)
    lab[:, :, 0] = L
    # A (green-red): shift +3 towards red/magenta to cancel fluorescent green
    lab[:, :, 1] = np.clip(lab[:, :, 1] + 3.0, 0, 255)
    # B (blue-yellow): shift +4 towards yellow for golden skin tone
    lab[:, :, 2] = np.clip(lab[:, :, 2] + 4.0, 0, 255)
    g2 = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/grade_2_cinema_clean.jpg", g2)

    # Grade 3: Vibrant Modern Creator (AevyTV reference match)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    # Boost saturation moderately
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.18, 0, 255)
    # Value contrast
    hsv[:, :, 2] = np.clip(128.0 + 1.10 * (hsv[:, :, 2] - 128.0) + 4.0, 0, 255)
    g3 = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    # slight warm tint
    g3 = g3.astype(np.float32)
    g3[:, :, 2] = np.clip(g3[:, :, 2] * 1.06, 0, 255)
    g3[:, :, 1] = np.clip(g3[:, :, 1] * 0.98, 0, 255)
    cv2.imwrite("AI VIDEO EDITOR/outputs/check_frames/grade_3_creator_vibrant.jpg", np.clip(g3, 0, 255).astype(np.uint8))

    print("Saved test grades to AI VIDEO EDITOR/outputs/check_frames/")
