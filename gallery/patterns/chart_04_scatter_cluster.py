from manim import *
import numpy as np

class Chart04ScatterCluster(Scene):
    """Scatter plot with dots appearing randomly then clustering by color."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Clustering Analysis", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-3.5, 3.5, 1],
            x_length=9, y_length=5.5,
            axis_config={"color": GRAY_B, "stroke_width": 1},
        )
        axes.move_to(DOWN * 0.2)
        self.play(FadeIn(axes))

        np.random.seed(42)

        # Initial random positions (unclustered)
        n_points = 60
        init_positions = [
            np.array([np.random.uniform(-4, 4), np.random.uniform(-2.5, 2.5)])
            for _ in range(n_points)
        ]

        # Cluster assignments and final positions
        cluster_centers = [(-2.5, 1.5), (2, 1), (0, -1.5)]
        cluster_colors = [BLUE, RED, GREEN]
        cluster_labels_text = ["Cluster A", "Cluster B", "Cluster C"]

        assignments = np.random.choice(3, n_points)
        final_positions = []
        for i in range(n_points):
            c = assignments[i]
            cx, cy = cluster_centers[c]
            fx = cx + np.random.randn() * 0.6
            fy = cy + np.random.randn() * 0.5
            final_positions.append(np.array([fx, fy]))

        # Create dots at initial positions (all gray)
        dots = VGroup()
        for pos in init_positions:
            dot = Dot(axes.c2p(pos[0], pos[1]), radius=0.06, color=GRAY, fill_opacity=0.6)
            dots.add(dot)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02),
            run_time=2,
        )

        phase_label = Text("Unclustered", font_size=22, color=GRAY)
        phase_label.to_corner(UL, buff=0.8)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Clustering animation: move + color
        cluster_label = Text("K-Means Clustering", font_size=22, color=YELLOW)
        cluster_label.move_to(phase_label)

        anims = []
        for i, dot in enumerate(dots):
            c = assignments[i]
            target_pos = axes.c2p(final_positions[i][0], final_positions[i][1])
            anims.append(
                dot.animate.move_to(target_pos).set_color(cluster_colors[c]).set_fill(opacity=0.8)
            )

        self.play(Transform(phase_label, cluster_label))
        self.play(*anims, run_time=2.5, rate_func=smooth)

        # Draw cluster boundaries (ellipses)
        for (cx, cy), color, label_text in zip(cluster_centers, cluster_colors, cluster_labels_text):
            ellipse = Ellipse(
                width=3.0, height=2.2,
                color=color, stroke_width=1.5, stroke_opacity=0.4,
                fill_opacity=0.05, fill_color=color,
            )
            ellipse.move_to(axes.c2p(cx, cy))
            self.play(Create(ellipse), run_time=0.5)

            label = Text(label_text, font_size=16, color=color)
            label.next_to(ellipse, UP, buff=0.1)
            self.play(FadeIn(label), run_time=0.3)

        self.wait(1.5)
