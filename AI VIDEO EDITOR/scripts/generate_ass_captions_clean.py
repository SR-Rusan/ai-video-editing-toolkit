import json

with open('/Users/rusan/Documents/Google anti-gravity projects/New AI Videos/analysis/caption_chunks_v3.json') as f:
    chunks = json.load(f)

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ass_content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Plus Jakarta Sans,64,&H00FAF7F2,&H00436BD9,&H0014161A,&H80000000,-1,0,0,0,100,100,1,0,1,4,2,2,60,60,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

for c in chunks:
    st = format_ass_time(c['start'])
    et = format_ass_time(c['end'])
    words = c['text'].split()
    if len(words) > 1:
        # Highlight first word in terracotta BGR &H00436BD9&
        styled = f"{{\\c&H00436BD9&}}{words[0]}{{\\c&H00FAF7F2&}} " + " ".join(words[1:])
    else:
        styled = f"{{\\c&H00436BD9&}}{c['text']}{{\\c&H00FAF7F2&}}"
    ass_content += f"Dialogue: 0,{st},{et},Default,,0,0,180,,{styled}\n"

with open('/Users/rusan/Documents/Google anti-gravity projects/New AI Videos/analysis/clean_reels_captions.ass', 'w') as f:
    f.write(ass_content)

print('Generated clean_reels_captions.ass successfully!')
