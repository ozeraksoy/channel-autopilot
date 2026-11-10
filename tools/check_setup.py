#!/usr/bin/env python3
"""Check that this machine can produce episodes. Prints what is present and what is missing with the
install hint. Never prints secret values, only whether a key is set."""
import shutil, subprocess, sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_env, ROOT
load_env(); ok = True
def line(good, name, hint=''):
    print(('  OK      ' if good else '  MISSING ') + name + ('' if good or not hint else '   ->  ' + hint))
print('Required for producing videos')
for b, hint in [('python3', ''), ('ffmpeg', 'macOS: brew install ffmpeg · Ubuntu: sudo apt install ffmpeg · Windows: winget install ffmpeg'), ('ffprobe', 'comes with ffmpeg'), ('node', 'https://nodejs.org (v18+)')]:
    g = shutil.which(b) is not None; ok &= g; line(g, b, hint)
g = importlib.util.find_spec('PIL') is not None; ok &= g; line(g, 'python package Pillow', 'pip install pillow')
pw = subprocess.run(['node', '-e', "require('playwright')"], capture_output=True, cwd=ROOT).returncode == 0 if shutil.which('node') else False
ok &= pw; line(pw, 'node package playwright (+ Chromium)', 'npm install playwright && npx playwright install chromium   (run inside this folder)')
print('\nVoice-over (choose one; see .env.example)')
line(bool(os.environ.get('ELEVENLABS_API_KEY')), 'ELEVENLABS_API_KEY set in .env (best quality)', 'optional — add your own key to .env')
line(importlib.util.find_spec('edge_tts') is not None, 'edge-tts package (free voices, no key)', 'pip install edge-tts')
print('  (or the "manual" provider: record the lines yourself, no setup needed)')
print('\n' + ('Ready to produce.' if ok else 'Install the MISSING required items above, then run this again.'))
sys.exit(0 if ok else 1)
