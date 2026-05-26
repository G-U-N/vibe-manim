# auto-pre — Automated Presentation Generation for Claude Code

Claude Code skills for transforming text content (blogs, papers, notes) into Manim-powered presentations — animated videos (MP4) or interactive slides (HTML).

## Demos

Sample presentations generated end-to-end with this toolkit (sources under `examples/blogs/`):

- [`assets/video/demo_cm_meanflow.mp4`](assets/video/demo_cm_meanflow.mp4) — from `cm-meanflow.html` (Consistency / MeanFlow theory)
- [`assets/video/demo_consolver_theory.mp4`](assets/video/demo_consolver_theory.mp4) — from `consolver-theory.html` (ConSolver theory)

## What This Does

Install these skills, then tell Claude Code what content you want to present. It will:

1. **Ask your preferences** — format, style, voice, audience, debug mode
2. **Read and understand** your content (HTML, LaTeX, Markdown, or a topic description)
3. **Plan the scene structure** — and show you for approval
4. **Write Manim code** — one `.py` file per scene with animations
5. **Render** — MP4 video (default) or standalone HTML slides
6. **Review via Codex** — automatic visual quality review and auto-fix

## Installation

### 1. System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg libcairo2-dev \
  libpango1.0-dev texlive texlive-latex-extra texlive-fonts-extra poppler-utils
```

### 2. Python Dependencies

```bash
conda create -n manim python=3.11
conda activate manim
pip install manim manim-slides
# Optional: for voice narration (video mode only)
pip install "manim-voiceover[gtts]"
# Optional: for neural network diagrams
pip install manim_ml
python -m pip install --force-reinstall "setuptools<82"
```

### 3. Codex Plugin (for automatic code review)

```bash
npm install -g @openai/codex
codex setup              # Follow prompts, pick your preferred model
claude mcp add codex -s user -- codex mcp-server
```

After setup, `/codex:review` will be available in Claude Code and used automatically during generation.

### 4. Install Skills

```bash
git clone <repo-url> auto-pre
cd auto-pre

mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

## Usage

Simply invoke the skill — Claude Code will **ask you all the questions interactively** (format, style, voice, audience, etc.). No need to pass parameters on the command line.

### Generate a presentation
```
/generate-presentation "path/to/blog.html"
```

```
/generate-presentation "path/to/paper.tex"
```

```
/generate-presentation "Explain how transformers work"
```

Claude Code will then ask:
- Output format? (Video MP4 / Slides HTML)
- Voice narration? (No / gTTS / Azure — video only)
- Background music? (Default / Custom file / Download URL / None — when no voice)
- Visual style? (Cinematic Dark / Academic White / Vibrant Explainer / Minimal Modern / Colorful Playful)
- Target audience? (Researchers / Students / General)
- Full generation or quick 3-scene preview?

### Re-render after editing
```
/render-presentation "output/project/scenes/"
```

### Review code quality
```
/review-presentation "output/project/scenes/"
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `/generate-presentation` | Full workflow: discover → style → plan → generate → render → Codex review |
| `/render-presentation` | Render existing `.py` scene files to MP4 or HTML |
| `/review-presentation` | Code review with static analysis + Codex |

## Output Structure

```
output/<project_name>/
├── scenes/
│   ├── scene_01_title.py
│   ├── scene_02_background.py
│   └── ...
├── assets/              # Images, converted figures
├── scene_outline.md     # Planned structure
└── presentation.html    # (slides mode) or media/videos/... (video mode)
```

## Visual Styles

| Style | Description |
|-------|-------------|
| **Cinematic Dark** | 3Blue1Brown inspired. Dark bg, color-coded math, smooth pacing |
| **Academic White** | Clean white bg, blue/black, structured. Conference-ready |
| **Vibrant Explainer** | Dark bg, vibrant accents, rich animations. Educational |
| **Minimal Modern** | Dark gray, large type, few colors. Apple keynote feel |
| **Colorful Playful** | Gradients, bold colors, bouncy animations. Fun & accessible |

## Defaults

| Setting | Default |
|---------|---------|
| Format | **Video (MP4)** |
| Quality | **High (1080p60)** |
| Voice | Off (ask user) |
| Codex review | **On (automatic)** |
| Style | Ask user |

## Examples Directory

`examples/` contains test content for validating the skills:
- `examples/blogs/` — HTML blog posts with KaTeX math (3 samples)

Try: `/generate-presentation "examples/blogs/cm-meanflow.html"`

## Visual Pattern Gallery

`gallery/patterns/` contains 33 standalone Manim scenes demonstrating beautiful visual patterns across 7 categories: geometric shapes, data flows, mathematical beauty, physics, ML/AI, presentation elements, and charts.

```bash
# Preview all patterns
bash gallery/render_all.sh

# Extract last-frame screenshots
mkdir -p gallery/screenshots
for f in media/videos/*/480p15/*.mp4; do
  name=$(basename "$f" .mp4)
  ffmpeg -y -sseof -0.1 -i "$f" -frames:v 1 -q:v 2 "gallery/screenshots/${name}.jpg" 2>/dev/null
done
```

## Background Music

For video mode without voice narration, Claude Code can add royalty-free background music:

- **Bundled tracks**: Place MP3s in `assets/music/`
- **Download on the fly**: Provide a URL from Pixabay Music, Mixkit, etc.
- **Custom file**: Point to any local audio file

See `assets/music/README.md` for recommended free music sources.

```bash
# Manual usage
bash scripts/add_bgm.sh input.mp4 output.mp4 assets/music/track.mp3
```

## Notes

- Voice narration is **only available in video mode** (incompatible with manim-slides HTML export)
- Background music is **only available in video mode without voice**
- PDF figures are automatically converted to PNG via `pdftoppm`
- Codex review runs automatically after rendering — critical issues are auto-fixed
- Use debug mode (3-scene preview) to quickly validate style before full generation

## License

MIT
