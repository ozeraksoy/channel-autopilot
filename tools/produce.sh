#!/usr/bin/env bash
# Build one episode after script.json, ep.json, story.js and the voice-over exist.
#   tools/produce.sh <channel_dir> <ep_id> check     -> control frames only (episodes/<ep>/sheet.jpg) — LOOK at them
#   tools/produce.sh <channel_dir> <ep_id> render    -> full video: episodes/<ep>/final.mp4
set -euo pipefail
CH="$1"; EP="$2"; MODE="${3:-check}"; D="$CH/episodes/$EP"; HERE="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$HERE/engine/timing.py" "$D"
python3 "$HERE/engine/build.py" "$D" "$CH/theme.json"
if [ "$MODE" = "check" ]; then
  node "$HERE/engine/shots.js" "$D"; echo "control sheet: $D/sheet.jpg"
else
  node "$HERE/engine/render.js" "$D"
  FW="$(python3 -c "import json,sys;t=json.load(open(sys.argv[1]));print(t.get('cta',{}).get('followWord','follow'))" "$CH/theme.json")"
  python3 "$HERE/engine/mix.py" "$D" "$CH/sfx" "$FW"
  SIZE=$(wc -c < "$D/final.mp4"); echo "done: $D/final.mp4 ($((SIZE/1024/1024)) MB)"
fi
