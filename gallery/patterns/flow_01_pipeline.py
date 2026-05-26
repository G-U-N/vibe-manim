from manim import *

class Flow01Pipeline(Scene):
    """Data pipeline with RoundedRectangle boxes and animated arrows."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Data Pipeline", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        stages = [
            ("Input", "#3465A4"),
            ("Process", "#A7074B"),
            ("Transform", "#4CAF50"),
            ("Output", "#F9A825"),
        ]

        boxes = VGroup()
        labels = VGroup()
        for name, color in stages:
            box = RoundedRectangle(
                corner_radius=0.2, height=1.2, width=2.2,
                color=color, fill_color=color, fill_opacity=0.25,
                stroke_width=2.5,
            )
            label = Text(name, font_size=26, color=WHITE)
            label.move_to(box)
            boxes.add(box)
            labels.add(label)

        boxes.arrange(RIGHT, buff=1.0)
        boxes.move_to(DOWN * 0.3)
        for label, box in zip(labels, boxes):
            label.move_to(box)

        # Arrows between boxes
        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i].get_right(), boxes[i + 1].get_left(),
                buff=0.15, color=WHITE, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows.add(arrow)

        # Animate: boxes appear staggered, then arrows flow
        self.play(
            LaggedStart(
                *[FadeIn(VGroup(b, l), shift=UP * 0.3) for b, l in zip(boxes, labels)],
                lag_ratio=0.25,
            ),
            run_time=2,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in arrows],
                lag_ratio=0.3,
            ),
            run_time=1.5,
        )

        # Data flow animation — dot traveling through pipeline
        dot = Dot(color=YELLOW, radius=0.1)
        dot.move_to(boxes[0].get_left() + LEFT * 0.5)
        self.play(FadeIn(dot))

        for i in range(len(boxes)):
            target = boxes[i].get_center()
            self.play(dot.animate.move_to(target), run_time=0.6)
            # Pulse effect at each stage
            pulse = boxes[i].copy().set_fill(opacity=0.6)
            self.play(
                Transform(boxes[i], pulse),
                run_time=0.3,
                rate_func=there_and_back,
            )

        self.play(dot.animate.move_to(boxes[-1].get_right() + RIGHT * 0.5), run_time=0.4)
        self.play(FadeOut(dot))
        self.wait(1)
