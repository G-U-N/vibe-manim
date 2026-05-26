#!/bin/bash
# render.sh — Render Manim-Slides .py files into a standalone HTML presentation.
#
# Usage:
#   bash scripts/render.sh <slides_dir> [output.html] [quality]
#
# Arguments:
#   slides_dir   Directory containing .py slide files (sorted by filename)
#   output.html  Output HTML file path (default: <slides_dir>/../presentation.html)
#   quality      Manim quality: l (low/480p), m (medium/720p), h (high/1080p) (default: l)
#
# Each .py file must contain exactly one class that inherits from Slide.
# Files are processed in alphabetical order.

set -euo pipefail

SLIDES_DIR="${1:?Usage: bash scripts/render.sh <slides_dir> [output.html] [quality]}"
OUTPUT="${2:-$(dirname "$SLIDES_DIR")/presentation.html}"
QUALITY="${3:-l}"

# Validate
if [ ! -d "$SLIDES_DIR" ]; then
    echo "Error: Directory '$SLIDES_DIR' not found." >&2
    exit 1
fi

# Collect .py files sorted by name
mapfile -t PY_FILES < <(find "$SLIDES_DIR" -maxdepth 1 -name '*.py' | sort)

if [ ${#PY_FILES[@]} -eq 0 ]; then
    echo "Error: No .py files found in '$SLIDES_DIR'." >&2
    exit 1
fi

echo "Found ${#PY_FILES[@]} slide files in $SLIDES_DIR"
echo "Quality: -q$QUALITY"
echo "Output: $OUTPUT"
echo ""

# Extract class names and render each slide
CLASS_NAMES=()
FAILED=()

for py_file in "${PY_FILES[@]}"; do
    # Extract class name (class Xxx(Slide):)
    class_name=$(grep -oP 'class\s+\K\w+(?=\s*\(.*Slide)' "$py_file" | head -1)
    if [ -z "$class_name" ]; then
        echo "Warning: No Slide class found in $py_file, skipping."
        continue
    fi

    echo "Rendering: $(basename "$py_file") → $class_name"
    if manim-slides render -q"$QUALITY" "$py_file" "$class_name" 2>&1; then
        CLASS_NAMES+=("$class_name")
        echo "  ✓ Success"
    else
        echo "  ✗ Failed"
        FAILED+=("$(basename "$py_file")")
    fi
    echo ""
done

if [ ${#CLASS_NAMES[@]} -eq 0 ]; then
    echo "Error: No slides rendered successfully." >&2
    exit 1
fi

# Convert to HTML
echo "Converting ${#CLASS_NAMES[@]} slides to HTML..."
manim-slides convert --one-file --offline "${CLASS_NAMES[@]}" "$OUTPUT"

echo ""
echo "=== Done ==="
echo "Output: $OUTPUT"
echo "Slides rendered: ${#CLASS_NAMES[@]}"
if [ ${#FAILED[@]} -gt 0 ]; then
    echo "Failed: ${FAILED[*]}"
fi
