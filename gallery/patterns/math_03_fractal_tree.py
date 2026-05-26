from manim import *
import numpy as np

class Math03FractalTree(Scene):
    """Recursive branching fractal tree with color gradient by depth."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Fractal Tree", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        max_depth = 9
        colors = color_gradient(["#8B4513", "#6B8E23", "#32CD32", "#90EE90"], max_depth + 1)

        branches = VGroup()

        def make_branch(start, angle, length, depth):
            if depth > max_depth or length < 0.05:
                return
            end = start + np.array([
                length * np.cos(angle),
                length * np.sin(angle),
                0,
            ])
            width = max(0.5, 3.0 * (1 - depth / max_depth))
            line = Line(
                start, end,
                color=colors[depth],
                stroke_width=width,
            )
            branches.add(line)

            # Branch left and right
            spread = PI / 6 * (1 + 0.3 * np.random.random())
            shrink = 0.68 + 0.1 * np.random.random()
            make_branch(end, angle + spread, length * shrink, depth + 1)
            make_branch(end, angle - spread, length * shrink, depth + 1)

        np.random.seed(42)
        trunk_start = np.array([0, -3.5, 0])
        make_branch(trunk_start, PI / 2, 1.8, 0)

        # Sort by depth (thicker first)
        branches.sort(lambda p: -p[1])  # top to bottom

        tree = branches.copy()
        tree.move_to(DOWN * 0.5)

        # Animate growth
        self.play(
            LaggedStart(
                *[Create(b) for b in tree],
                lag_ratio=0.002,
            ),
            run_time=5,
        )
        self.wait(1.5)
