# Background Music Assets

Place royalty-free music files here for use as presentation background music.

## Recommended Free Music Sources

### Pixabay Music (Recommended)
- **URL**: https://pixabay.com/music/
- **License**: Royalty-free, no attribution required, commercial use OK
- **Tips**: Search by mood (calm, upbeat, cinematic) or genre (ambient, electronic, acoustic)
- **Quality**: High — curated library with 230k+ tracks

### Mixkit
- **URL**: https://mixkit.co/free-stock-music/
- **License**: Free, no attribution, commercial use OK
- **Tips**: Browse categories: Gentle, Dreamy, Motivational, Technology
- **Download**: Direct MP3 download, no login required

### YouTube Audio Library
- **Access**: YouTube Studio → Audio Library (or search "YouTube Audio Library")
- **License**: Most tracks free for any use, some require attribution
- **Tips**: Filter by mood, genre, duration. Download as MP3.

### Freesound
- **URL**: https://freesound.org/
- **License**: Varies per track (check CC license). Many are CC0.
- **Tips**: Good for ambient textures and sound effects

## Suggested Moods by Presentation Style

| Visual Style | Suggested Music Mood | Search Terms |
|---|---|---|
| Cinematic Dark | Deep ambient, slow | "cinematic ambient", "dark atmospheric" |
| Academic White | Light piano, calm | "soft piano", "minimal acoustic" |
| Vibrant Explainer | Upbeat electronic | "upbeat technology", "positive electronic" |
| Minimal Modern | Lo-fi, subtle | "lo-fi ambient", "minimal electronic" |
| Colorful Playful | Bouncy, bright | "happy upbeat", "fun electronic" |

## How to Add Music

1. Download an MP3 from any source above
2. Place it in this directory: `assets/music/`
3. During presentation generation, Claude Code will ask if you want BGM
4. You can provide the file path, or give a URL for Claude Code to download

## Usage with add_bgm.sh

```bash
# Add background music to a video
bash scripts/add_bgm.sh input.mp4 output.mp4 assets/music/your_track.mp3

# Adjust volume (default: -20dB, lower = quieter)
bash scripts/add_bgm.sh input.mp4 output.mp4 assets/music/your_track.mp3 -25
```

## File Format

ffmpeg supports: MP3, WAV, OGG, AAC, FLAC, M4A. MP3 is recommended for smaller file size.
