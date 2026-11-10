#!/usr/bin/env bash
# Build one episode after the script, episode data and voice-over exist (animation engine: ep.json + story.js;
# clips mode: ep.json with "mode": "clips" + shots.json).
#   tools/produce.sh <channel_dir> <ep_id> check     -> control frames only (episodes/<ep>/sheet.jpg) — LOOK at them
#   tools/produce.sh <channel_dir> <ep_id> render    -> full video: episodes/<ep>/final.mp4
set -euo pipefail
CH="$1"; EP="$2"; MODE="${3:-check}"; D="$CH/episodes/$EP"; HERE="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$HERE/engine/timing.py" "$D"
MODE_EP="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('mode','engine'))" "$D/ep.json")"
FW="$(python3 -c "import json,sys;t=json.load(open(sys.argv[1]));print(t.get('cta',{}).get('followWord','follow'))" "$CH/theme.json")"
if [ "$MODE_EP" = "clips" ]; then
  # episode made from generated clips / footage / images (shots.json) instead of the animation engine
  if [ "$MODE" = "check" ]; then
    python3 "$HERE/tools/clips.py" plan "$CH" "$EP"; python3 "$HERE/tools/clips.py" review "$CH" "$EP"
  else
    python3 "$HERE/tools/assemble.py" "$CH" "$EP"; python3 "$HERE/engine/mix.py" "$D" "$CH/sfx" "$FW"
    echo "done: $D/final.mp4"
  fi
  exit 0
fi
python3 "$HERE/engine/build.py" "$D" "$CH/theme.json"
if [ "$MODE" = "check" ]; then
  node "$HERE/engine/shots.js" "$D"; echo "control sheet: $D/sheet.jpg"
else
  node "$HERE/engine/render.js" "$D"
  python3 "$HERE/engine/mix.py" "$D" "$CH/sfx" "$FW"
  SIZE=$(wc -c < "$D/final.mp4"); echo "done: $D/final.mp4 ($((SIZE/1024/1024)) MB)"
fi
