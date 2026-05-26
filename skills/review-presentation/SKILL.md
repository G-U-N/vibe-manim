---
name: review-presentation
description: Review generated Manim presentation code for correctness, quality, and rendering issues. Uses Codex for adversarial review when available.
argument-hint: '"path/to/slides/dir" — codex_review: true'
allowed-tools: [Read, Glob, Grep, Bash, Agent, Skill]
---

# Review Presentation

## Configuration

```
CODEX_REVIEW = true      # Use /codex:review for adversarial code review
```

## Workflow

### Step 1: Collect Files & Detect Mode

List all `.py` files in the directory (typically `scene_*.py`), sorted by name.

Detect mode from imports in the first file:
- **slides mode** — contains `from manim_slides import Slide`
- **video mode** — only `from manim import *` (may also have `from manim_voiceover import VoiceoverScene`)

Subsequent checks adapt to the detected mode.

### Step 2: Static Analysis

For each file, check:

1. **Syntax**: `python3 -c "import py_compile; py_compile.compile('<file>', doraise=True)"`
2. **Required imports**: Must have `from manim import *`. Slides mode additionally requires `from manim_slides import Slide`.
3. **Class structure**: Class inheriting from `Slide` (slides mode) or `Scene`/`MovingCameraScene`/`VoiceoverScene` (video mode), with `def construct(self)`.
4. **Boundary calls (slides mode only)**: At least one `self.next_slide()` call. (Video mode uses `self.wait()` instead — no requirement.)
5. **Asset paths**: Verify all `ImageMobject("...")` referenced files exist.
6. **LaTeX safety**: Flag `\label{`, `\cref{`, `\cite{`, `\ref{` — these should be removed.
7. **Unbalanced braces**: Check `{` and `}` counts match in Tex/MathTex strings.

### Step 3: Quality Review

1. **Density**: Flag slides with >10 Tex/MathTex/ImageMobject objects
2. **Font consistency**: Titles should be ~font_size=50, body ~30
3. **Animation variety**: Flag slides with only FadeIn — suggest Write, Transform, etc.
4. **Pacing**: Slides mode — each logical group should end with `self.next_slide()`. Video mode — `self.wait()` between segments, no run of identical durations.

### Step 4: Codex Review (if `CODEX_REVIEW = true`)

Invoke `/codex:review` with prompt:

> Review these Manim-Slides Python files for:
> 1. Python syntax and runtime errors
> 2. Manim API correctness
> 3. LaTeX compatibility (Manim supports a LaTeX subset)
> 4. Presentation quality (layout, readability, animation flow)
> 5. Missing assets or broken paths
>
> For each issue: file, line, severity (critical/minor), suggested fix.

### Step 5: Report

```markdown
# Presentation Review Report

## Summary
- Files: N | Issues: X (Y critical, Z minor)

## Critical Issues
- file:line — Description — Fix suggestion

## Minor Issues
- file:line — Description — Fix suggestion

## Codex Feedback
[If enabled]
```

Offer to auto-fix critical issues.
