#!/usr/bin/env python3
"""Create the folder for a new channel from the templates:  python3 tools/new_channel.py <slug>"""
import sys, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) != 2: sys.exit(__doc__)
dst = os.path.join(ROOT, 'channels', sys.argv[1])
if os.path.exists(dst): sys.exit(f'{dst} already exists — edit it instead (see the channel-setup skill, "Editing").')
shutil.copytree(os.path.join(ROOT, 'templates', 'channel'), dst)
for d in ['episodes', 'sfx', 'brand']: os.makedirs(os.path.join(dst, d), exist_ok=True)
print('created', os.path.relpath(dst, ROOT))
