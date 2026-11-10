#!/usr/bin/env python3
"""Create an episode folder from the starter episode:  python3 tools/new_episode.py <channel_dir> <ep_id> [short|long|clips]
short = vertical animated short (default) · long = 16:9 animated explainer · clips = generated clips / own footage / images"""
import sys, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) not in (3, 4): sys.exit(__doc__)
dst = os.path.join(sys.argv[1], 'episodes', sys.argv[2])
if os.path.exists(dst): sys.exit(f'{dst} already exists')
kind = sys.argv[3] if len(sys.argv) > 3 else "short"
src = {"short": "episode", "long": "episode-long", "clips": "episode-clips"}.get(kind) or sys.exit("kind must be short, long or clips")
shutil.copytree(os.path.join(ROOT, "templates", src), dst); shutil.copy(os.path.join(ROOT, "templates", "quality.md"), os.path.join(dst, "quality.md"))
q = os.path.join(dst, "quality.md"); open(q, "w").write(open(q).read().replace("{{EP}}", sys.argv[2]))
print("created", dst, "from", src)
