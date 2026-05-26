from manim import *
import numpy as np

class Flow04CircularArch(Scene):
    """Components arranged in a circle with curved arrows between them."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Circular Architecture", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        components = ["API", "Auth", "Cache", "DB", "Queue", "Worker"]
        colors = [BLUE, RED, GREEN, ORANGE, PURPLE, TEAL]
        n = len(components)
        radius = 2.5

        boxes = VGroup()
        comp_labels = VGroup()
        for i, (name, color) in enumerate(zip(components, colors)):
            angle = PI / 2 - i * TAU / n
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle) - 0.5, 0])

            box = RoundedRectangle(
                corner_radius=0.15, height=0.8, width=1.4,
                color=color, fill_opacity=0.3, stroke_width=2,
            )
            box.move_to(pos)
            label = Text(name, font_size=22, color=WHITE).move_to(box)
            boxes.add(box)
            comp_labels.add(label)

        self.play(
            LaggedStart(
                *[FadeIn(VGroup(b, l), scale=0.8) for b, l in zip(boxes, comp_labels)],
                lag_ratio=0.15,
            ),
            run_time=2,
        )

        # Curved arrows: sequential flow
        arrows = VGroup()
        for i in range(n):
            j = (i + 1) % n
            start = boxes[i].get_center()
            end = boxes[j].get_center()
            mid = (start + end) / 2
            # Push midpoint outward for curve
            direction = mid - np.array([0, -0.5, 0])
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            curve_point = mid + direction * 0.4

            arrow = CurvedArrow(
                start, end,
                color=GRAY_B, stroke_width=1.5,
                angle=PI / 5,
            )
            arrows.add(arrow)

        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.15),
            run_time=2,
        )

        # Highlight one connection
        highlight_arrow = arrows[0].copy().set_color(YELLOW).set_stroke(width=3)
        self.play(Create(highlight_arrow), run_time=0.8)
        self.play(
            boxes[0].animate.set_fill(opacity=0.6),
            boxes[1].animate.set_fill(opacity=0.6),
            run_time=0.5,
        )
        self.wait(1.5)
