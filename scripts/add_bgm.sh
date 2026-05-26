#!/bin/bash
# add_bgm.sh — Add background music to a video using ffmpeg.
#
# Usage:
#   bash scripts/add_bgm.sh <input.mp4> <output.mp4> <music_file> [volume_db]
#
# Arguments:
#   input.mp4    Input video file
#   output.mp4   Output video file with music
#   music_file   Music file (MP3, WAV, OGG, etc.)
#   volume_db    Music volume in dB (default: -20, lower = quieter)
#
# Features:
#   - Loops music if shorter than video
#   - Trims music to match video duration
#   - Fades out music in the last 3 seconds
#   - Handles video-only input (no existing audio stream)
#   - Preserves original video codec (no re-encoding)

set -euo pipefail

INPUT="${1:?Usage: bash scripts/add_bgm.sh <input.mp4> <output.mp4> <music_file> [volume_db]}"
OUTPUT="${2:?Provide output file path}"
MUSIC="${3:?Provide music file path}"
VOLUME="${4:--20}"

# Validate inputs
if [ ! -f "$INPUT" ]; then
    echo "Error: Input video not found: $INPUT" >&2
    exit 1
fi
if [ ! -f "$MUSIC" ]; then
    echo "Error: Music file not found: $MUSIC" >&2
    exit 1
fi

# Get video duration
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT" 2>/dev/null)
if [ -z "$DURATION" ]; then
    echo "Error: Could not determine video duration" >&2
    exit 1
fi

echo "Video duration: ${DURATION}s"
echo "Music file: $MUSIC"
echo "Volume: ${VOLUME}dB"

# Calculate fade-out start (3 seconds before end, or half duration if very short)
FADE_START=$(python3 -c "print(max(0, float('$DURATION') - 3))")

# Check if input video has an audio stream
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$INPUT" 2>/dev/null | head -1)

if [ -n "$HAS_AUDIO" ]; then
    echo "Input has existing audio — mixing with background music"
    # Mix: keep original audio + add background music at low volume
    ffmpeg -y \
        -i "$INPUT" \
        -stream_loop -1 -i "$MUSIC" \
        -filter_complex \
        "[1:a]volume=${VOLUME}dB,afade=t=out:st=${FADE_START}:d=3,atrim=0:${DURATION}[music]; \
         [0:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
        -map 0:v -map "[aout]" \
        -c:v copy -c:a aac -b:a 192k \
        "$OUTPUT" 2>/dev/null

else
    echo "Input is video-only — adding background music as audio track"
    # No existing audio: just add the music
    ffmpeg -y \
        -i "$INPUT" \
        -stream_loop -1 -i "$MUSIC" \
        -filter_complex \
        "[1:a]volume=${VOLUME}dB,afade=t=out:st=${FADE_START}:d=3,atrim=0:${DURATION}[music]" \
        -map 0:v -map "[music]" \
        -c:v copy -c:a aac -b:a 192k \
        -shortest \
        "$OUTPUT" 2>/dev/null
fi

if [ -f "$OUTPUT" ]; then
    OUTPUT_SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo "✓ Output: $OUTPUT ($OUTPUT_SIZE)"
else
    echo "✗ Failed to create output file" >&2
    exit 1
fi
