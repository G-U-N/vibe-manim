from manim import *
import numpy as np

class Chart03Radar(Scene):
    """Multi-axis radar/spider chart with two overlapping data series."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Skill Radar", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        axes_labels = ["Speed", "Accuracy", "Scalability", "Cost", "Ease of Use", "Reliability"]
        n = len(axes_labels)
        max_val = 10
        radius = 2.2
        center = DOWN * 0.3

        # Draw radar grid
        grid = VGroup()
        for level in [0.25, 0.5, 0.75, 1.0]:
            r = radius * level
            points = []
            for i in range(n):
                angle = PI / 2 - i * TAU / n
                points.append(center + r * np.array([np.cos(angle), np.sin(angle), 0]))
            polygon = Polygon(
                *points,
                color=GRAY, stroke_width=0.5, stroke_opacity=0.3,
            )
            grid.add(polygon)

        # Axis lines
        axis_lines = VGroup()
        for i in range(n):
            angle = PI / 2 - i * TAU / n
            end = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
            line = Line(center, end, color=GRAY, stroke_width=0.5, stroke_opacity=0.5)
            axis_lines.add(line)

        # Axis labels
        ax_labels = VGroup()
        for i, label in enumerate(axes_labels):
            angle = PI / 2 - i * TAU / n
            pos = center + (radius + 0.5) * np.array([np.cos(angle), np.sin(angle), 0])
            text = Text(label, font_size=16, color=WHITE)
            text.move_to(pos)
            ax_labels.add(text)

        self.play(FadeIn(grid), FadeIn(axis_lines), FadeIn(ax_labels))

        # Data series
        def make_radar_polygon(values, color, opacity=0.3):
            points = []
            for i, val in enumerate(values):
                r = (val / max_val) * radius
                angle = PI / 2 - i * TAU / n
                points.append(center + r * np.array([np.cos(angle), np.sin(angle), 0]))
            poly = Polygon(
                *points,
                color=color,
                fill_opacity=opacity,
                stroke_width=2.5,
            )
            return poly

        series_a = [8, 7, 6, 5, 9, 8]
        series_b = [6, 9, 8, 7, 5, 7]

        poly_a = make_radar_polygon(series_a, BLUE)
        poly_b = make_radar_polygon(series_b, RED)

        # Legend
        legend = VGroup(
            VGroup(
                Square(side_length=0.2, color=BLUE, fill_opacity=0.5),
                Text("System A", font_size=16, color=BLUE),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Square(side_length=0.2, color=RED, fill_opacity=0.5),
                Text("System B", font_size=16, color=RED),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        legend.to_corner(DR, buff=0.8)

        self.play(Create(poly_a), run_time=1.5)
        self.play(Create(poly_b), run_time=1.5)
        self.play(FadeIn(legend))

        # Dots on vertices
        for vals, color in [(series_a, BLUE), (series_b, RED)]:
            for i, val in enumerate(vals):
                r = (val / max_val) * radius
                angle = PI / 2 - i * TAU / n
                dot = Dot(
                    center + r * np.array([np.cos(angle), np.sin(angle), 0]),
                    radius=0.05, color=color,
                )
                self.add(dot)

        self.wait(1.5)
