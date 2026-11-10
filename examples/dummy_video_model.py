#!/usr/bin/env python3
"""Stand-in for a real video model, used to test the clips pipeline and to show the adapter contract.
It only draws a moving test pattern with the prompt on it — replace it with a script that calls YOUR model
(a local model, or a hosted API with your own key read from .env) and writes an mp4 to --out.

  python3 examples/dummy_video_model.py --prompt "…" --seconds 6 --width 1920 --height 1080 --out clip.mp4
"""
import argparse, subprocess, textwrap
a = argparse.ArgumentParser()
for k in ['prompt', 'out']: a.add_argument('--' + k, required=True)
for k in ['seconds', 'width', 'height']: a.add_argument('--' + k, type=float, required=True)
a.add_argument('--image', default=''); x = a.parse_args()
txt = '\n'.join(textwrap.wrap('TEST PATTERN - ' + x.prompt, 48)).replace(':', ' ').replace("'", '')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'testsrc2=size={int(x.width)}x{int(x.height)}:rate=30:duration={x.seconds}',
                '-vf', f"drawtext=text='{txt}':fontcolor=white:fontsize={int(x.height/22)}:box=1:boxcolor=black@0.6:boxborderw=20:x=(w-text_w)/2:y=(h-text_h)/2",
                '-pix_fmt', 'yuv420p', x.out], check=True)
