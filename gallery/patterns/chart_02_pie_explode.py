from manim import *
import numpy as np

class Chart02PieExplode(Scene):
    """Pie chart with sectors that separate (explode) with labels."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Market Share", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        data = [
            ("Product A", 35, BLUE),
            ("Product B", 25, RED),
            ("Product C", 20, GREEN),
            ("Product D", 12, ORANGE),
            ("Other", 8, GRAY),
        ]

        total = sum(d[1] for d in data)
        radius = 2.0
        center = DOWN * 0.3

        sectors = VGroup()
        labels = VGroup()
        start_angle = PI / 2

        for name, value, color in data:
            angle = (value / total) * TAU
            sector = AnnularSector(
                inner_radius=0,
                outer_radius=radius,
                angle=angle,
                start_angle=start_angle,
                color=color,
                fill_opacity=0.7,
                stroke_width=2,
                stroke_color=WHITE,
            )
            sector.move_arc_center_to(center)

            # Label position: midpoint of arc
            mid_angle = start_angle + angle / 2
            label_r = radius + 0.5
            label_pos = center + np.array([
                label_r * np.cos(mid_angle),
                label_r * np.sin(mid_angle),
                0,
            ])
            label = Text(f"{name}\n{value}%", font_size=18, color=WHITE)
            label.move_to(label_pos)

            sectors.add(sector)
            labels.add(label)
            start_angle += angle

        # Animate: draw sectors
        self.play(
            LaggedStart(
                *[Create(s) for s in sectors],
                lag_ratio=0.2,
            ),
            run_time=2.5,
        )
        self.play(
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.15),
            run_time=1.5,
        )

        # Explode: move each sector outward from center
        start_angle = PI / 2
        explode_anims = []
        for i, (name, value, color) in enumerate(data):
            angle = (value / total) * TAU
            mid_angle = start_angle + angle / 2
            offset = np.array([
                0.3 * np.cos(mid_angle),
                0.3 * np.sin(mid_angle),
                0,
            ])
            explode_anims.append(sectors[i].animate.shift(offset))
            explode_anims.append(labels[i].animate.shift(offset * 1.5))
            start_angle += angle

        self.play(*explode_anims, run_time=1.5)

        # Highlight largest
        highlight = sectors[0].copy().set_stroke(YELLOW, 3)
        self.play(Create(highlight))
        self.wait(1.5)
