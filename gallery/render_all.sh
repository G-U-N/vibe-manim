#!/bin/bash
# render_all.sh — Render all gallery pattern scenes at low quality for preview.
#
# Usage:
#   bash gallery/render_all.sh [quality]
#
# Arguments:
#   quality   l (low/480p, default), m (medium/720p), h (high/1080p)
#
# After rendering, extract last frames for visual review:
#   for f in gallery/patterns/media/videos/*/480p15/*.mp4; do
#     name=$(basename "$f" .mp4)
#     ffmpeg -y -sseof -0.1 -i "$f" -frames:v 1 -q:v 2 "gallery/screenshots/${name}.jpg" 2>/dev/null
#   done

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PATTERNS_DIR="$SCRIPT_DIR/patterns"
QUALITY="${1:-l}"

if [ ! -d "$PATTERNS_DIR" ]; then
    echo "Error: patterns/ directory not found at $PATTERNS_DIR" >&2
    exit 1
fi

mapfile -t PY_FILES < <(find "$PATTERNS_DIR" -maxdepth 1 -name '*.py' | sort)

if [ ${#PY_FILES[@]} -eq 0 ]; then
    echo "Error: No .py files found in $PATTERNS_DIR" >&2
    exit 1
fi

echo "=== Gallery Renderer ==="
echo "Found ${#PY_FILES[@]} pattern files"
echo "Quality: -q$QUALITY"
echo ""

SUCCESS=0
FAILED=0
FAILED_LIST=()

for py_file in "${PY_FILES[@]}"; do
    class_name=$(grep -oP 'class\s+\K\w+(?=\s*\(.*Scene)' "$py_file" | head -1)
    if [ -z "$class_name" ]; then
        echo "⚠ No Scene class in $(basename "$py_file"), skipping"
        continue
    fi

    echo -n "Rendering $(basename "$py_file") → $class_name ... "
    if manim render -q"$QUALITY" "$py_file" "$class_name" >/dev/null 2>&1; then
        echo "✓"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "✗"
        FAILED=$((FAILED + 1))
        FAILED_LIST+=("$(basename "$py_file")")
    fi
done

echo ""
echo "=== Done ==="
echo "Success: $SUCCESS / $((SUCCESS + FAILED))"
if [ $FAILED -gt 0 ]; then
    echo "Failed: ${FAILED_LIST[*]}"
fi
echo ""
echo "Videos in: $PATTERNS_DIR/media/videos/"
echo ""
echo "To extract last-frame screenshots:"
echo "  mkdir -p gallery/screenshots"
echo "  for f in $PATTERNS_DIR/media/videos/*/480p15/*.mp4; do"
echo "    name=\$(basename \"\$f\" .mp4)"
echo "    ffmpeg -y -sseof -0.1 -i \"\$f\" -frames:v 1 -q:v 2 \"gallery/screenshots/\${name}.jpg\" 2>/dev/null"
echo "  done"
