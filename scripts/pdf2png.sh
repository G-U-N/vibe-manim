#!/bin/bash
# pdf2png.sh — Convert PDF figures to PNG for use in Manim slides.
#
# Usage:
#   bash scripts/pdf2png.sh <input.pdf> [output.png] [dpi]
#   bash scripts/pdf2png.sh <input_dir> [output_dir] [dpi]
#
# Single file mode: converts one PDF to PNG.
# Directory mode: converts all PDFs in input_dir to PNGs in output_dir.
#
# Requires: poppler-utils (pdftoppm)

set -euo pipefail

INPUT="${1:?Usage: bash scripts/pdf2png.sh <input.pdf|input_dir> [output] [dpi]}"
DPI="${3:-300}"

if [ -f "$INPUT" ]; then
    # Single file mode
    OUTPUT="${2:-${INPUT%.pdf}.png}"
    OUTPUT_BASE="${OUTPUT%.png}"
    echo "Converting: $INPUT → $OUTPUT (${DPI} dpi)"
    pdftoppm -png -r "$DPI" -singlefile "$INPUT" "$OUTPUT_BASE"
    echo "Done: $OUTPUT"

elif [ -d "$INPUT" ]; then
    # Directory mode
    OUTPUT_DIR="${2:-$INPUT/png}"
    mkdir -p "$OUTPUT_DIR"

    count=0
    for pdf in "$INPUT"/*.pdf; do
        [ -f "$pdf" ] || continue
        base=$(basename "$pdf" .pdf)
        out="$OUTPUT_DIR/$base"
        echo "Converting: $(basename "$pdf") → $base.png"
        pdftoppm -png -r "$DPI" -singlefile "$pdf" "$out"
        count=$((count + 1))
    done

    echo "Done: $count files converted to $OUTPUT_DIR"
else
    echo "Error: '$INPUT' is not a file or directory." >&2
    exit 1
fi
