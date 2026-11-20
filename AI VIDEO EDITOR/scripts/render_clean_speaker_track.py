import subprocess
import json
import os
import time

def main():
    t0 = time.time()
    timeline_path = "/Users/rusan/Documents/Google anti-gravity projects/New AI Videos/analysis/tight_reel_timeline.json"
    raw_video = "/Users/rusan/Documents/Google anti-gravity projects/New AI Videos/Raw video/IMG_2079.mov"
    out_dir = "/tmp/clean_speaker_cuts"
    os.makedirs(out_dir, exist_ok=True)
    
    with open(timeline_path) as f:
        timeline = json.load(f)
        
    cuts = timeline["cuts"]
    print(f"Total cuts to render: {len(cuts)}")
    
    cut_files = []
    
    for i, cut in enumerate(cuts):
        src_start = cut["src_start"]
        src_end = cut["src_end"]
        duration = cut["duration"]
        is_punch = cut["is_punch"]
        
        # Dimensions for 9:16 vertical 1080x1920
        # Raw is 1920x1080
        if not is_punch:
            # 1.0x wide: 608x1080 centered at x=656
            crop_filter = "crop=608:1080:656:0"
        else:
            # 1.32x punch-in: 460x818 centered at x=730, y=71
            crop_filter = "crop=460:818:730:71"
            
        out_cut = os.path.join(out_dir, f"cut_{i:02d}.mp4")
        cut_files.append(out_cut)
        
        # Studio Grade Tone Mapping:
        # Input is HLG BT.2020 10-bit (arib-std-b67).
        # We tone-map cleanly to Rec.709 with standard gamma and neutral balance.
        # Zero artificial saturation boosts or channel multipliers.
        vf = (
            f"{crop_filter},"
            f"scale=1080:1920:flags=lanczos,"
            f"zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:t=bt709:p=bt709:m=bt709:r=tv,"
            f"format=yuv420p"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{src_start:.3f}",
            "-t", f"{duration:.3f}",
            "-i", raw_video,
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "17",
            "-r", "30",
            "-an",
            out_cut
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Rendered cut {i:02d} ({duration:.2f}s, punch={is_punch})")
        
    # Concatenate all cuts
    concat_list = os.path.join(out_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for p in cut_files:
            f.write(f"file '{p}'\n")
            
    final_speaker = "/Users/rusan/Documents/Google anti-gravity projects/videos/ai-consultant-reel/assets/video/rusan_speaker.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        final_speaker
    ]
    subprocess.run(cmd_concat, check=True)
    
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", final_speaker]
    final_dur = subprocess.run(probe_cmd, capture_output=True, text=True).stdout.strip()
    print(f"Successfully generated clean studio-grade speaker track in {time.time()-t0:.2f}s!")
    print(f"Path: {final_speaker}")
    print(f"Duration: {final_dur}s")

if __name__ == "__main__":
    main()
