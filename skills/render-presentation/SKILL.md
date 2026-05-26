---
name: render-presentation
description: Render existing Manim .py slide files into a standalone HTML presentation or MP4 video. Use after editing generated code.
argument-hint: '"path/to/slides/dir" — output: presentation.html, quality: l, format: slides'
allowed-tools: [Bash, Read, Glob, Grep, Edit]
---

# Render Presentation

## Configuration

```
QUALITY = l                    # l (480p), m (720p), h (1080p), k (4K)
FORMAT = slides                # slides (HTML) or video (MP4)
OUTPUT = presentation.html     # Output filename
```

## Workflow

### Step 1: Validate

1. Verify the slides directory exists and contains `.py` files.
2. For each file, confirm it contains a class inheriting from `Slide` (or `Scene` for video).
3. List files in sorted order — this determines slide sequence.

### Step 2: Render

**For slides (HTML):**
```bash
cd <slides_dir>

# Render each slide (files are named scene_*.py by generate-presentation)
for f in scene_*.py; do
    class_name=$(grep -oP 'class\s+\K\w+(?=\s*\(.*Slide)' "$f" | head -1)
    [ -n "$class_name" ] && manim-slides render -q<QUALITY> "$f" "$class_name"
done

# Collect class names in file order
classes=""
for f in scene_*.py; do
    cn=$(grep -oP 'class\s+\K\w+(?=\s*\(.*Slide)' "$f" | head -1)
    [ -n "$cn" ] && classes="$classes $cn"
done

# Convert to standalone HTML
manim-slides convert --one-file --offline $classes <OUTPUT>
```

**For video (MP4):**
```bash
cd <slides_dir>
for f in scene_*.py; do
    class_name=$(grep -oP 'class\s+\K\w+(?=\s*\(.*Scene)' "$f" | head -1)
    [ -n "$class_name" ] && manim render -q<QUALITY> "$f" "$class_name"
done
```

### Step 2.5: Add Background Music (video mode, optional)

After rendering all scene videos, if the user wants background music:

1. Concatenate scene videos:
```bash
cd <slides_dir>
for f in $(ls media/videos/scene_*/*/Scene*.mp4 2>/dev/null | sort); do
    echo "file '$f'"
done > concat_list.txt
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy ../presentation.mp4
```

2. Add music:
```bash
bash scripts/add_bgm.sh ../presentation.mp4 ../presentation_bgm.mp4 <music_file>
mv ../presentation_bgm.mp4 ../presentation.mp4
```

Music file can be from `assets/music/`, a user-provided path, or downloaded from a URL.
See `assets/music/README.md` for recommended free music sources.

### Step 3: Handle Errors

For each render failure:
1. Read the error message.
2. Common fixes:
   - **LaTeX error** → Simplify `Tex()` / `MathTex()` content, remove unsupported commands.
   - **Missing image** → Check asset path, ensure file exists.
   - **Import error** → Add missing imports.
3. Fix the `.py` file and retry (max 3 attempts per file).
4. If unfixable, skip and note the failure.

### Step 4: Report

- Output file path
- Slides rendered: X / Y total
- Failures (if any) with error details
- Viewing instructions:
  - **HTML**: Open in browser. `→/←` navigate, `F` fullscreen, `Esc` overview.
  - **MP4**: Open with any video player.
