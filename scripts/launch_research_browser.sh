#!/usr/bin/env bash
set -euo pipefail

# A dedicated, persistent profile keeps Xiaohongshu login separate from daily Chrome.
PROFILE_DIR="${XHS_RESEARCH_PROFILE:-$HOME/.codex/browser-profiles/xiaohongshu-research}"
DEBUG_PORT="${XHS_RESEARCH_DEBUG_PORT:-9227}"
EXTENSION_DIR="${XHS_BRIDGE_EXTENSION_DIR:-$(cd "$(dirname "$0")/../extension" && pwd)}"

mkdir -p "$PROFILE_DIR"

if [[ "$(uname)" == "Darwin" ]]; then
  open -na "Google Chrome" --args \
    --user-data-dir="$PROFILE_DIR" \
    --remote-debugging-port="$DEBUG_PORT" \
    --load-extension="$EXTENSION_DIR" \
    --no-first-run \
    --no-default-browser-check \
    "https://www.xiaohongshu.com/"
else
  CHROME_BIN="${CHROME_BIN:-google-chrome}"
  "$CHROME_BIN" \
    --user-data-dir="$PROFILE_DIR" \
    --remote-debugging-port="$DEBUG_PORT" \
    --load-extension="$EXTENSION_DIR" \
    --no-first-run \
    --no-default-browser-check \
    "https://www.xiaohongshu.com/" >/dev/null 2>&1 &
fi

echo "Research browser started."
echo "Profile: $PROFILE_DIR"
echo "Debug port: $DEBUG_PORT"
echo "Complete any login or verification yourself in this browser window."
