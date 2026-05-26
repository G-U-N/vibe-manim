# Visual Pattern Gallery

33 standalone Manim scenes demonstrating beautiful visual patterns for presentations. Render all, review the outputs, and pick which patterns to keep as references in the generate-presentation skill.

## Quick Start

```bash
# Render all at low quality (fast preview)
bash gallery/render_all.sh

# Render at high quality
bash gallery/render_all.sh h

# Extract last-frame screenshots for review
mkdir -p gallery/screenshots
for f in gallery/patterns/media/videos/*/480p15/*.mp4; do
  name=$(basename "$f" .mp4)
  ffmpeg -y -sseof -0.1 -i "$f" -frames:v 1 -q:v 2 "gallery/screenshots/${name}.jpg" 2>/dev/null
done
```

## Pattern Index

### A: Geometric & Shape
| # | File | Description |
|---|------|-------------|
| 1 | `geo_01_boolean_shapes.py` | Intersection/Union/Difference of circles with color fills |
| 2 | `geo_02_concentric_rings.py` | Expanding colored rings — radar pulse effect |
| 3 | `geo_03_polygon_morph.py` | Triangle→Square→Pentagon→Circle smooth morphing |
| 4 | `geo_04_hex_tiling.py` | Hexagonal tiling building progressively with gradient |
| 5 | `geo_05_spiral_galaxy.py` | Logarithmic spiral of dots with color gradient + rotation |

### B: Data Flow & Architecture
| # | File | Description |
|---|------|-------------|
| 6 | `flow_01_pipeline.py` | RoundedRectangle boxes + arrows, animated data dot flow |
| 7 | `flow_02_trapezoid_layers.py` | Neural network layers as colored trapezoid polygons |
| 8 | `flow_03_binary_tree.py` | Recursive binary tree growing level by level |
| 9 | `flow_04_circular_arch.py` | Components in circle with curved arrows |
| 10 | `flow_05_layered_stack.py` | 3D-like technology stack with perspective |

### C: Mathematical Beauty
| # | File | Description |
|---|------|-------------|
| 11 | `math_01_lorenz.py` | Lorenz attractor with colorful trajectory segments |
| 12 | `math_02_fourier_circles.py` | Fourier series approximation of square wave |
| 13 | `math_03_fractal_tree.py` | Recursive branching fractal tree with depth colors |
| 14 | `math_04_wave_interference.py` | Two waves combining — beats and envelope |
| 15 | `math_05_golden_spiral.py` | Fibonacci rectangles + golden spiral overlay |

### D: Physics & Dynamics
| # | File | Description |
|---|------|-------------|
| 16 | `phys_01_pendulum.py` | Pendulum + phase space diagram side by side |
| 17 | `phys_02_em_wave.py` | EM wave with perpendicular E/B field vectors |
| 18 | `phys_03_particle_system.py` | Particles emitting from center with gravity |
| 19 | `phys_04_stream_lines.py` | Stream lines through a swirling vector field |

### E: ML/AI Visualization
| # | File | Description |
|---|------|-------------|
| 20 | `ml_01_attention_heatmap.py` | Attention weight grid with varying opacity |
| 21 | `ml_02_embedding_space.py` | 2D dot clusters with labels and boundaries |
| 22 | `ml_03_loss_curve.py` | Animated loss graph with tracker dot and legend |
| 23 | `ml_04_neural_net.py` | Neural network nodes + forward pass animation |

### F: Presentation Elements
| # | File | Description |
|---|------|-------------|
| 24 | `pres_01_title_card.py` | Cinematic title with floating particle background |
| 25 | `pres_02_section_divider.py` | Stylish section transition with morphing shapes |
| 26 | `pres_03_split_compare.py` | Left vs Right comparison with divider |
| 27 | `pres_04_timeline.py` | Horizontal timeline with animated milestones |
| 28 | `pres_05_quote_card.py` | Elegant quote display with decorative elements |
| 33 | `pres_06_camera_follow.py` | Camera follows dot along curve, then zooms out |

### G: Charts & Data
| # | File | Description |
|---|------|-------------|
| 29 | `chart_01_bar_race.py` | Animated bar chart with growing and re-ranking |
| 30 | `chart_02_pie_explode.py` | Pie chart with exploding sectors |
| 31 | `chart_03_radar.py` | Multi-axis radar chart with two overlapping series |
| 32 | `chart_04_scatter_cluster.py` | Scatter plot → K-Means clustering animation |
