---
name: generate-presentation
description: Generate a Manim-based video or slides presentation from user-provided content (HTML, LaTeX, plain text, or verbal description). Guides the user through interactive discovery, style selection, content planning, code generation, rendering, and review.
argument-hint: '"path/to/content or topic description"'
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion]
---

# Generate Presentation — Full Workflow

Transforms text content into Manim-powered presentations:
- **Video** (default) — MP4 animation (manim `Scene`)
- **Slides** — Interactive HTML (manim-slides `Slide`)

**IMPORTANT**: Every invocation is a fresh task. Do NOT carry over context from previous runs. Always start from Phase 0.

## Configuration Defaults

```
MAX_SCENES = 20    QUALITY = h    FORMAT = video    DEBUG = false
```

Override via user answers in Phase 0. Never ask user to pass CLI parameters.

---

## Phase 0: Interactive Discovery

**Ask ALL questions via `AskUserQuestion` BEFORE generating anything.**

### Q1: Content Source
"What content should be presented?" — file path (HTML/LaTeX/txt/md), verbal description, or URL.

### Q2: Output Format
Video (MP4, default) or Slides (HTML). Note: Slides mode is incompatible with voice narration.

### Q3: Voice Narration (video only)
No / gTTS (free) / Azure TTS (needs API key, best quality).

### Q3b: Background Music (video + no-voice only)
- **A** — Bundled track from `assets/music/`
- **B** — User-provided local file
- **C** — Download from URL (recommend: Pixabay Music, Mixkit, YouTube Audio Library)
- **D** — No music

Store chosen path in `BGM_FILE` for Phase 4.

### Q4: Visual Style
Present these options:

| Style | Look & Feel | Key Settings |
|-------|-------------|-------------|
| **A — Cinematic Dark** | Black bg, color-coded math, LaggedStart reveals, generous pauses. 3Blue1Brown feel. | `bg="#1C1C1C"`, BLUE/YELLOW/RED, `Write` + `LaggedStart`, `set_backstroke(BLACK,3)` |
| **B — Academic White** | White bg, blue/black scheme, structured grid layout. Conference talk feel. | default bg, BLUE_D headings, `FadeIn` + `Write`, `.arrange()` grid |
| **C — Vibrant Explainer** | Dark bg, vibrant accents, rich diagrams & flow charts. Educational feel. | `bg="#0D1117"`, `"#A7074B"/"#3465A4"/"#4CAF50"`, `GrowFromCenter` + `Transform` |
| **D — Minimal Modern** | Dark-gray bg, large type, generous whitespace, few colors. Apple-keynote feel. | `bg="#2B2B2B"`, WHITE + one accent, `font_size=60/32`, `FadeIn`/`FadeOut` only |
| **E — Colorful Playful** | Dark bg, bold saturated colors, bouncy animations. Fun & accessible. | `bg="#1a1a2e"`, `"#e94560"/"#0f3460"/"#533483"`, `rate_func=there_and_back_with_pause` |

User may mix styles or describe their own.

### Q5: Target Audience
Researchers (more equations) / Students (step-by-step) / General (minimal jargon).

### Q6: Debug Mode
Full generation or quick preview (3 scenes: title + 1 content + references).

---

## Phase 1: Content Reading

| Source | Steps |
|--------|-------|
| **HTML blog** | Read file. Extract from `const markdownSource = \`...\`` (Markdown + `$$`/`$` math) or `.innerHTML = \`...\`` (HTML + `\[...\]`/`\(...\)` math). Extract title, author, sections, equations, figures. |
| **LaTeX paper** | Read main `.tex` + `\input{}` includes + `preamble.tex` (expand custom macros). Extract `\title`, `\author`, `\begin{abstract}`, sections, equations, figures, tables. Convert PDF figures: `pdftoppm -png -r 300 -singlefile <in.pdf> <out_base>` |
| **Plain text / MD** | Identify structure from headings, lists, code blocks. |
| **Verbal** | Outline key points with user. |

**Output**: Mental model of title, authors, sections, key equations, figures, narrative flow.

---

## Phase 2: Scene Outline

Present outline to user for approval before proceeding.

```
1. Title — title, authors, venue/date
2. Motivation — problem, why it matters
3. Background — key concepts
4-5. Method — core approach, key equations
6-7. Results — findings, figures/tables
...
N. References — key citations
```

### Planning Rules
- Title first, references last. Each major section → 1-3 scenes.
- Key equations / figures → own scene. Max per scene: 3-5 bullets OR 1-2 equations OR 1 figure.
- Blogs: 8-15 scenes. Papers: 15-25 scenes. Debug: 3 scenes only.
- **Wow scenes (MANDATORY)**: 2-4 visual interludes at section boundaries, marked with ✦. Choose from Wow Techniques table below. Prefer metaphors matching surrounding content.
- **Camera work**: 2-3 scenes use `MovingCameraScene` to zoom into key equations/diagrams, marked with 🎥.

---

## Phase 3: Code Generation

### Output structure
```
output/<project_name>/
├── scenes/          # scene_01_title.py, scene_02_motivation.py, ...
├── last_frames/     # Scene01Title.jpg, ... (review artifacts)
├── assets/
└── scene_outline.md
```

### CRITICAL: Read the Aesthetics & Coding Guide sections below before writing ANY code.

### Gallery Reference
Consult `gallery/patterns/` (33 patterns) for diagrams, flows, charts, etc. Also see https://docs.manim.community/en/stable/examples.html.
- Use as *inspiration*, NOT templates. Adapt, remix, vary across scenes.

### Wow Scenes (MANDATORY)
Before coding each ✦ scene, **read** the corresponding `gallery/patterns/*.py`. Adapt colors, labels, timing. Keep 5-10s max. Connect to content when possible (e.g., fractal tree labeled "Data → Features → Model").

### Naming
Files: `scene_01_title.py` / Classes: `Scene01Title` / One class per file.

### Base class templates

**Video:**
```python
from manim import *
class Scene01Title(Scene):
    def construct(self):
        title = Tex("Title", font_size=50)
        title.move_to(ORIGIN)
        self.play(FadeIn(title))
        self.wait(2)
```

**Slides:** Same but `from manim_slides import Slide`, inherit `Slide`, use `self.next_slide()`.

**Voiceover (video only, NOT compatible with slides):**
```python
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService  # or AzureService
class Scene01Title(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        with self.voiceover(text="Welcome") as tracker:
            self.play(FadeIn(title), run_time=tracker.duration)
```

### ⚠️ LAYOUT RULES (prevents text shifting bugs)

1. **Explicitly position every element.** Never rely on defaults. Use `to_edge`, `next_to`, `move_to`.
2. **`VGroup.arrange()` resets positions** — always call positioning AFTER arrange.
3. **`to_edge(LEFT)` is ONLY for bullet lists** (`$\bullet$` items) and reference lists. NEVER on equations, titles, narrative text, or labels — these must stay centered via `move_to(ORIGIN)` or `next_to`.

```python
# Bullets — the ONLY valid use of to_edge(LEFT)
bullets = VGroup(Tex(r"$\bullet$ Point 1"), Tex(r"$\bullet$ Point 2"))
bullets.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
bullets.to_edge(LEFT, buff=1.0)
bullets.next_to(title, DOWN, buff=0.6)

# Equations — always centered
eq = MathTex(r"E = mc^2", font_size=38).move_to(ORIGIN)

# Labels + equations — center the label, equation follows
label = Tex("Key result:", font_size=26).move_to(UP * 1.5)
eq.next_to(label, DOWN, buff=0.3)
```

### ⚠️ IMAGE HANDLING

Always scale to fit within bounds, preserving aspect ratio:
```python
img = ImageMobject(path)
img.scale_to_fit_height(min(3.5, config.frame_height * 0.5))
if img.width > config.frame_width * 0.7:
    img.scale_to_fit_width(config.frame_width * 0.7)
img.move_to(ORIGIN)
```

With Pillow available, read actual dimensions for precise scaling:
```python
from PIL import Image
with Image.open(path) as pil_img:
    aspect = pil_img.size[0] / pil_img.size[1]
if aspect > 5.5 / 3.5: img.scale_to_fit_width(5.5)
else: img.scale_to_fit_height(3.5)
```

### LaTeX sanitization
Remove: `\label{}`, `\cref{}`, `\ref{}`, `\cite{}`, `\TODO{}`, `\todo{}`, `\red{}`
Expand custom macros from preamble. Extract inner content from `\begin{figure/table/align}`.

---

## Phase 4: Rendering

### Video
```bash
cd output/<project>/scenes/
for f in scene_*.py; do
    cn=$(grep -oP 'class\s+\K\w+(?=\s*\(.*Scene)' "$f" | head -1)
    [ -n "$cn" ] && manim render -qh "$f" "$cn"
done
```

### Slides
```bash
cd output/<project>/scenes/
for f in scene_*.py; do
    cn=$(grep -oP 'class\s+\K\w+(?=\s*\(.*Slide)' "$f" | head -1)
    [ -n "$cn" ] && manim-slides render -qh "$f" "$cn"
done
classes=$(for f in scene_*.py; do grep -oP 'class\s+\K\w+(?=\s*\(.*Slide)' "$f" | head -1; done)
manim-slides convert --one-file --offline $classes ../presentation.html
```

### Error handling
Read error → fix `.py` → retry. Max 3 attempts per scene. Common fixes: simplify LaTeX, check image paths, add missing imports.

### Video Post-Processing
```bash
# Concatenate scenes
cd output/<project>/scenes/
for f in $(ls media/videos/scene_*/1080p60/Scene*.mp4 2>/dev/null | sort); do
    echo "file '$f'"
done > concat_list.txt
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy ../presentation.mp4

# Add BGM (only if BGM_FILE set)
bash scripts/add_bgm.sh ../presentation.mp4 ../presentation_bgm.mp4 <BGM_FILE>
mv ../presentation_bgm.mp4 ../presentation.mp4
```

`add_bgm.sh` auto-loops, applies -20dB, fades out last 3s.

---

## Phase 5: Visual Review (mandatory)

Do NOT skip. Run automatically after rendering.

### Step 1: Extract last frames
```bash
mkdir -p ../last_frames
for f in media/videos/scene_*/1080p60/Scene*.mp4; do
    scene=$(basename "$f" .mp4)
    ffmpeg -y -sseof -0.1 -i "$f" -frames:v 1 -q:v 2 "../last_frames/${scene}.jpg" 2>/dev/null
done
```

Save to `output/<project>/last_frames/` (persistent, NOT `/tmp/`). Use last frame (not mid-point) — it shows final state where issues are most visible.

### Step 2: Read every screenshot and check
Layout overlap, text alignment (equations centered?), image scaling, color contrast, spacing, text wrapping.

### Step 3: Invoke Codex review
Call `/codex:review` with generated `.py` files:
> Check: explicit positioning, font consistency, color accessibility, animation variety, image aspect ratio, text overflow, one-idea-per-scene. Report: file, line, severity, fix.

### Step 4: Auto-fix & re-verify
Fix critical issues → re-render affected scenes → extract & verify last frames again.

### Step 5: Report to user
Output paths, scenes rendered (X/Y), review summary, remaining issues.
- **Video**: Open `.mp4` with any player.
- **Slides**: Open `.html` in browser. `→/←` navigate, `F` fullscreen, `Esc` overview.

---

# ═══════════════════════════════════════════════════════════
# AESTHETICS GUIDE
# ═══════════════════════════════════════════════════════════

## Wow Techniques (pick 2-4 per presentation)

| Technique | Use Case | Gallery File |
|-----------|----------|-------------|
| **MovingCameraScene** zoom/follow | Section transitions, key equations | `pres_06_camera_follow.py` |
| **Fractal Tree** | Growth/complexity metaphor | `math_03_fractal_tree.py` |
| **Lorenz Attractor** | Chaos, dynamics | `math_01_lorenz.py` |
| **Spiral Galaxy** | Scale, elegance | `geo_05_spiral_galaxy.py` |
| **Particle System** | Celebration, transitions | `phys_03_particle_system.py` |
| **Fourier Epicycles** | Signal processing, math beauty | `math_02_fourier_circles.py` |
| **Wave Interference** | Physics, combining ideas | `math_04_wave_interference.py` |
| **Golden Spiral** | Nature, design | `math_05_golden_spiral.py` |
| **Polygon Morphing** | Transformation, evolution | `geo_03_polygon_morph.py` |
| **Stream Lines** | Data flow, dynamics | `phys_04_stream_lines.py` |

Insert as: transition interludes, decorative openers, visual metaphors, or closing flourishes.
`MovingCameraScene` is the single highest-impact technique — use it liberally, even on content scenes with a focal point worth zooming into.

## Core Aesthetic Principles

**Spacing**: Titles 44-50pt, body 26-30pt, labels 18-22pt. `to_edge(UP, buff=0.5)` for titles. If it looks tight, split into two scenes.

**Color**: Max 3-4 colors per presentation, one per concept. Multi-part `MathTex` for per-term coloring. `set_backstroke(BLACK, 3)` on busy backgrounds. Opacity 0.2-0.4 for background elements.

**Animation**: Vary types — never repeat 5× in a row. Quick 0.5-1s, standard 1.5-2.5s, key reveals 2-3s. `LaggedStart(lag_ratio=0.2)` for rhythm. Video: `self.wait(1-3)`. Slides: `self.next_slide()`.

**Composition**: One idea per scene. Visual center for key element. Left-to-right for processes, top-to-bottom for hierarchies.

---

# ═══════════════════════════════════════════════════════════
# MANIM REFERENCE
# ═══════════════════════════════════════════════════════════

## Docs: fetch when unsure

| Resource | URL |
|----------|-----|
| Manim Community | https://docs.manim.community/en/stable/ |
| Text & Math | https://docs.manim.community/en/stable/guides/using_text.html |
| Manim Voiceover | https://voiceover.manim.community/en/stable/ |
| Manim-Slides | https://manim-slides.eertmans.be/stable/ |
| ManimML | https://github.com/helblazer811/ManimML |

## Quick Reference

```python
# Text & Math
Tex(r"Text with \textbf{bold} and $E = mc^2$", font_size=30)
MathTex(r"\frac{d\mathbf{x}}{dt} = f(\mathbf{x})", font_size=40)
eq = MathTex(r"E", r"=", r"mc^2"); eq[0].set_color(RED); eq[2].set_color(BLUE)
Tex("The loss minimizes error", t2c={"loss": YELLOW, "error": RED})
Text("Hello", font="Sans", font_size=48)

# Layout
obj.to_edge(UP, buff=0.5)  |  obj.next_to(other, DOWN, buff=0.5)
obj.move_to(ORIGIN)  |  obj.to_corner(UL)
VGroup(a, b, c).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(ORIGIN)

# Animations
FadeIn(obj)  |  FadeIn(obj, shift=UP)  |  Write(obj)  |  Create(obj)  |  GrowFromCenter(obj)
Transform(old, new)  |  ReplacementTransform(old, new)
obj.animate.shift(RIGHT*2)  |  obj.animate.set_color(RED)
LaggedStart(*[FadeIn(b, shift=UP*0.3) for b in items], lag_ratio=0.2)

# Shapes
RoundedRectangle(corner_radius=0.3, height=1, width=2.5, color=BLUE)
Arrow(a.get_right(), b.get_left(), buff=0.1)
SurroundingRectangle(eq, color=YELLOW, buff=0.2, corner_radius=0.1)

# Camera (use MovingCameraScene as base)
self.camera.frame.save_state()
self.camera.frame.animate.scale(0.4).move_to(target)  # zoom in
Restore(self.camera.frame)  # zoom out
self.camera.frame.add_updater(lambda m: m.move_to(dot))  # follow

# Neural Networks
from manim_ml.neural_network import FeedForwardLayer, NeuralNetwork
nn = NeuralNetwork([FeedForwardLayer(3), FeedForwardLayer(5), FeedForwardLayer(2)])
self.play(nn.make_forward_pass_animation(run_time=2))

# Scene Control
self.wait(2)          # video
self.next_slide()     # slides (loop=True for looping)

# Colors: RED GREEN BLUE YELLOW WHITE GRAY ORANGE PURPLE TEAL
# Graduated: BLUE_E (dark) → BLUE_A (light)  |  Hex: "#A7074B"

# Quality: -ql (480p/15fps) | -qm (720p/30fps) | -qh (1080p/60fps) | -qk (4K/60fps)
# Render: manim render -qh file.py Class
# Slides: manim-slides render -qh file.py Class → manim-slides convert --one-file --offline ...
```
