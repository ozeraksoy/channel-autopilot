#!/usr/bin/env python3
"""Create an episode folder from the starter episode:  python3 tools/new_episode.py <channel_dir> <ep_id>"""
import sys, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) != 3: sys.exit(__doc__)
dst = os.path.join(sys.argv[1], 'episodes', sys.argv[2])
if os.path.exists(dst): sys.exit(f'{dst} already exists')
shutil.copytree(os.path.join(ROOT, 'templates', 'episode'), dst); print('created', dst)
