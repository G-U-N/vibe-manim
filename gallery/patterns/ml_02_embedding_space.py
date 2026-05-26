from manim import *
import numpy as np

class Ml02EmbeddingSpace(Scene):
    """2D embedding space with colored clusters and labels."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Embedding Space", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        axes = Axes(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=8, y_length=5,
            axis_config={"color": GRAY_B, "stroke_width": 1},
        )
        axes.move_to(DOWN * 0.3)
        self.play(FadeIn(axes))

        np.random.seed(42)
        clusters = [
            {"center": (-2, 1.5), "color": BLUE, "label": "Animals", "n": 15},
            {"center": (2, 1), "color": RED, "label": "Vehicles", "n": 15},
            {"center": (0, -1.5), "color": GREEN, "label": "Food", "n": 15},
            {"center": (-2.5, -1), "color": PURPLE, "label": "Science", "n": 10},
        ]

        all_dots = VGroup()
        all_labels = VGroup()

        for cluster in clusters:
            cx, cy = cluster["center"]
            dots = VGroup()
            for _ in range(cluster["n"]):
                x = cx + np.random.randn() * 0.5
                y = cy + np.random.randn() * 0.4
                dot = Dot(
                    axes.c2p(x, y),
                    radius=0.06,
                    color=cluster["color"],
                    fill_opacity=0.7,
                )
                dots.add(dot)
            all_dots.add(dots)

            # Cluster label
            label = Text(cluster["label"], font_size=20, color=cluster["color"])
            label.move_to(axes.c2p(cx, cy + 0.9))
            all_labels.add(label)

        # Animate clusters appearing one by one
        for dots, label in zip(all_dots, all_labels):
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05),
                run_time=1,
            )
            self.play(FadeIn(label))

        # Draw dashed boundary circles
        boundaries = VGroup()
        for cluster in clusters:
            cx, cy = cluster["center"]
            ellipse = Ellipse(
                width=2.5, height=2.0,
                color=cluster["color"],
                stroke_width=1.5,
                stroke_opacity=0.4,
            )
            ellipse.set_fill(cluster["color"], opacity=0.05)
            ellipse.move_to(axes.c2p(cx, cy))
            boundaries.add(ellipse)

        self.play(
            *[Create(b) for b in boundaries],
            run_time=1.5,
        )

        # Similarity arrow
        arrow = Arrow(
            axes.c2p(-1.5, 1.3), axes.c2p(1.5, 0.8),
            color=YELLOW, stroke_width=2,
        )
        sim_label = Text("semantic distance", font_size=16, color=YELLOW)
        sim_label.next_to(arrow, UP, buff=0.1)
        self.play(GrowArrow(arrow), FadeIn(sim_label))
        self.wait(1.5)
