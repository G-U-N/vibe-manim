<h1 align="center">vibe-manim</h1>

<p align="center">
  <i>Turn blogs, papers, and notes into beautiful Manim presentations — automatically, through Claude Code.</i>
</p>

<p align="center">
  <a href="https://github.com/G-U-N/vibe-manim/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://docs.manim.community/"><img alt="Manim" src="https://img.shields.io/badge/manim-community-ff6f00"></a>
  <a href="https://manim-slides.eertmans.be/"><img alt="manim-slides" src="https://img.shields.io/badge/manim--slides-supported-2ea44f"></a>
  <a href="https://claude.com/claude-code"><img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-skills-9b59b6"></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.11-3776AB">
</p>

<p align="center">
  <a href="#demos">Demos</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#visual-styles">Styles</a> ·
  <a href="#gallery">Gallery</a>
</p>

---

## Demos

End-to-end runs of `/generate-presentation` on real blog posts. Source HTMLs live in [`examples/blogs/`](examples/blogs/); full-quality MP4s in [`assets/video/`](assets/video/).

<table>
<tr>
<td width="50%" align="center">
<img src="assets/gif/demo_cm_meanflow.gif" width="100%" alt="cm-meanflow demo"/>
<br/>
<b>Equivalence of Consistency Models &amp; MeanFlow</b>
<br/>
<sub>from <code>cm-meanflow.html</code> · <a href="assets/video/demo_cm_meanflow.mp4">HD MP4</a> · <a href="https://g-u-n.github.io/blogs/cm-meanflow.html">source blog</a></sub>
</td>
<td width="50%" align="center">
<img src="assets/gif/demo_consolver_theory.gif" width="100%" alt="consolver-theory demo"/>
<br/>
<b>Theoretical Analysis of ConsistencySolver</b>
<br/>
<sub>from <code>consolver-theory.html</code> · <a href="assets/video/demo_consolver_theory.mp4">HD MP4</a> · <a href="https://g-u-n.github.io/blogs/consolver-theory.html">source blog</a></sub>
</td>
</tr>
</table>

---

## What it does

You give Claude Code a blog, a LaTeX paper, or even a verbal description. `vibe-manim` then drives the full pipeline — **understand → plan → animate → render → review** — to produce a polished MP4 video or an interactive HTML slide deck, with no manual Manim coding.

```
HTML / LaTeX / Markdown / topic        Claude Code + vibe-manim                   MP4 video
       ─────────────────────  ───────────────────────────────────────►   or
                              Read · Plan · Animate · Render · Review     HTML slides
```

The skills handle the parts that are usually painful: parsing math-heavy sources, choosing scene structure, writing positioning-correct Manim code, sanitizing LaTeX, scaling figures, picking colors that read at video resolution, and catching layout bugs through automated Codex review.

---

## Quick Start

```bash
git clone https://github.com/G-U-N/vibe-manim.git
cd vibe-manim
cp -r skills/* ~/.claude/skills/

# Then in Claude Code:
/generate-presentation "examples/blogs/cm-meanflow.html"
```

Claude Code asks you a handful of questions (format, style, voice, audience), shows you a scene outline for approval, then generates, renders, and reviews everything automatically.

---

## Installation

<details>
<summary><b>1. System dependencies</b> (Ubuntu / Debian)</summary>

```bash
sudo apt update
sudo apt install -y \
  python3 python3-pip ffmpeg \
  libcairo2-dev libpango1.0-dev \
  texlive texlive-latex-extra texlive-fonts-extra \
  poppler-utils
```

On macOS: `brew install ffmpeg cairo pango poppler` and install [MacTeX](https://tug.org/mactex/).
</details>

<details>
<summary><b>2. Python environment</b></summary>

```bash
conda create -n manim python=3.11
conda activate manim

pip install manim manim-slides
pip install "manim-voiceover[gtts]"   # optional: voice narration (video only)
pip install manim_ml                   # optional: neural network diagrams
python -m pip install --force-reinstall "setuptools<82"
```
</details>

<details>
<summary><b>3. Codex (for automatic code review)</b></summary>

```bash
npm install -g @openai/codex
codex setup                                       # follow prompts
claude mcp add codex -s user -- codex mcp-server
```

After setup, `/codex:review` is wired in automatically — `vibe-manim` calls it after every render and auto-fixes critical issues it surfaces.
</details>

<details>
<summary><b>4. Install the skills</b></summary>

```bash
git clone https://github.com/G-U-N/vibe-manim.git
cd vibe-manim
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

Verify in Claude Code: typing `/` should list `generate-presentation`, `render-presentation`, `review-presentation`.
</details>

---

## Usage

```text
/generate-presentation "path/to/blog.html"
/generate-presentation "path/to/paper.tex"
/generate-presentation "Explain how transformers work"
```

Claude Code interactively collects:

| Question | Options |
|---|---|
| Output format | Video MP4 *(default)* · Slides HTML |
| Voice narration | None · gTTS · Azure TTS · *(video only)* |
| Background music | Bundled · Custom file · URL · None |
| Visual style | Cinematic Dark · Academic White · Vibrant Explainer · Minimal Modern · Colorful Playful |
| Audience | Researchers · Students · General |
| Scope | Full generation · Quick 3-scene preview |

After generation, two follow-up skills are available:

```text
/render-presentation  "output/<project>/scenes/"   # re-render after manual edits
/review-presentation  "output/<project>/scenes/"   # static analysis + Codex review
```

---

## Skills

| Skill | What it does |
|---|---|
| **`/generate-presentation`** | Full workflow — discover → plan → write Manim code → render → review |
| **`/render-presentation`** | Render existing `scene_*.py` files to MP4 (Scene) or HTML (Slide) |
| **`/review-presentation`** | Static checks + `/codex:review` for adversarial code review |

---

## Visual Styles

Pick a style per project; each maps to a coordinated palette, font sizing, animation vocabulary, and pacing.

| Style | Look &amp; Feel |
|---|---|
| **Cinematic Dark** | Black bg, color-coded math, `LaggedStart` reveals, generous pauses. 3Blue1Brown feel. |
| **Academic White** | White bg, blue / black scheme, structured grid layout. Conference-talk feel. |
| **Vibrant Explainer** | Dark bg, saturated accents, rich flow diagrams. Educational explainer feel. |
| **Minimal Modern** | Dark-gray bg, large type, generous whitespace, two-color palette. Apple-keynote feel. |
| **Colorful Playful** | Dark bg, bold saturated colors, bouncy animations. Fun &amp; accessible. |

---

## Output Layout

```
output/<project_name>/
├── scenes/
│   ├── scene_01_title.py
│   ├── scene_02_motivation.py
│   └── ...
├── last_frames/         # review screenshots
├── assets/              # images, converted figures
├── scene_outline.md     # planned structure
└── presentation.mp4     # (or presentation.html for slides mode)
```

---

## Gallery

[`gallery/patterns/`](gallery/) ships **33 standalone Manim scenes** demonstrating reusable visual patterns across seven categories — geometric, data-flow, mathematical, physics, ML/AI, presentation elements, and charts. `vibe-manim` reads from these when planning "wow" interludes.

```bash
bash gallery/render_all.sh           # render all at 480p15 (fast)
bash gallery/render_all.sh h         # render all at 1080p60
```

See [`gallery/README.md`](gallery/README.md) for the full index.

---

## Background Music

For video mode **without** voice narration, `vibe-manim` can mix in royalty-free background music. Bundled tracks live in [`assets/music/`](assets/music/); you can also point at any local file or supply a URL from [Pixabay Music](https://pixabay.com/music/) or [Mixkit](https://mixkit.co/free-stock-music/).

```bash
# Manual usage
bash scripts/add_bgm.sh input.mp4 output.mp4 assets/music/track.mp3
```

`add_bgm.sh` loops the track to match video length, applies −20 dB, and fades the last 3 s.

---

## Defaults

| Setting | Default |
|---|---|
| Format | Video MP4 |
| Quality | 1080p60 |
| Voice | Off (asks you) |
| Style | Asks you |
| Codex review | **On**, automatic |

---

## Notes &amp; Constraints

- Voice narration is **video-only** (incompatible with `manim-slides` HTML export).
- Background music is **only added when there is no voice narration**.
- PDF figures are auto-converted to PNG via `pdftoppm` (`poppler-utils`).
- Debug mode (3-scene preview) is recommended for validating a style cheaply before committing to a full render.

---

## Repository Layout

```
vibe-manim/
├── skills/          installable Claude Code skills (copy to ~/.claude/skills/)
├── gallery/         33 reusable visual patterns + render script
├── assets/
│   ├── music/       bundled royalty-free music + sourcing guide
│   ├── video/       demo MP4s
│   └── gif/         README demo GIFs
├── examples/blogs/  HTML sources used to generate the demos above
├── scripts/         render, pdf2png, add_bgm utilities
└── output/          generated presentations land here (gitignored)
```

---

## Acknowledgments

Built on top of [Manim Community](https://www.manim.community/), [manim-slides](https://manim-slides.eertmans.be/), and [manim-voiceover](https://voiceover.manim.community/). Adversarial code review via [OpenAI Codex](https://github.com/openai/codex). Orchestrated by [Claude Code](https://claude.com/claude-code).

---

## License

MIT © 2026 [Fu-Yun Wang](https://g-u-n.github.io/)
