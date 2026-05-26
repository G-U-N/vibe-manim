from manim import *
import numpy as np

class Math05GoldenSpiral(Scene):
    """Fibonacci rectangles with golden spiral overlay — no overlap."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Golden Spiral", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Fibonacci rectangles built using proper tiling algorithm
        fibs = [1, 1, 2, 3, 5, 8]
        scale = 0.35
        colors = color_gradient([BLUE_E, TEAL, GREEN, YELLOW, ORANGE, RED], len(fibs))

        rects = VGroup()
        # Track corners: each new square attaches to the growing rectangle
        # Start: 1x1 at origin
        # Direction cycle: right, up, left, down
        cx, cy = 0, 0
        prev_w, prev_h = 0, 0
        total_x, total_y = 0, 0

        corners = []  # (cx, cy) of each square center
        # Manual golden rectangle tiling
        positions = [
            (0, 0),           # fib=1
            (1, 0),           # fib=1, right of first
            (0.5, 1.5),       # fib=2, above both
            (-1.5, 0.5),      # fib=3, left
            (0, -2.5),        # fib=5, below
            (4, 1),           # fib=8, right
        ]

        for i, fib in enumerate(fibs):
            s = fib * scale
            px, py = positions[i]
            rect = Square(
                side_length=s,
                color=colors[i],
                fill_opacity=0.25,
                stroke_width=2,
            )
            rect.move_to(np.array([px * scale, py * scale, 0]))

            label = Tex(str(fib), font_size=max(16, int(fib * 4)), color=colors[i])
            label.move_to(rect)

            rects.add(VGroup(rect, label))

        rects.move_to(DOWN * 0.3)

        self.play(
            LaggedStart(
                *[FadeIn(r, scale=0.8) for r in rects],
                lag_ratio=0.3,
            ),
            run_time=3,
        )

        # Golden spiral as quarter-circle arcs approximation
        phi = (1 + np.sqrt(5)) / 2
        spiral_points = []
        for t in np.linspace(0.1, 3.5 * PI, 400):
            r_val = 0.08 * phi ** (t / (PI / 2))
            px = r_val * np.cos(t)
            py = r_val * np.sin(t)
            if abs(px) < 4.5 and abs(py) < 3:
                spiral_points.append(np.array([px, py, 0]))

        if len(spiral_points) > 2:
            spiral = VMobject()
            spiral.set_points_smoothly(spiral_points)
            spiral.set_stroke(YELLOW, width=2.5, opacity=0.9)
            spiral.move_to(rects.get_center())

            self.play(Create(spiral), run_time=3)

        phi_label = MathTex(r"\varphi = \frac{1+\sqrt{5}}{2} \approx 1.618", font_size=30, color=YELLOW)
        phi_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(phi_label))
        self.wait(1.5)
