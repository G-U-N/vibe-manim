from manim import *

class Geo01BooleanShapes(Scene):
    """Intersection, Union, Difference of circles — no overlap, two rows."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Boolean Shape Operations", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Source circles (shown at top)
        c1 = Circle(radius=0.9, color=BLUE, fill_opacity=0.4, stroke_width=3)
        c2 = Circle(radius=0.9, color=RED, fill_opacity=0.4, stroke_width=3)
        c1.shift(LEFT * 0.45)
        c2.shift(RIGHT * 0.45)

        l1 = Text("A", font_size=28, color=BLUE).next_to(c1, UP, buff=0.15)
        l2 = Text("B", font_size=28, color=RED).next_to(c2, UP, buff=0.15)

        source = VGroup(c1, c2, l1, l2)
        source.move_to(UP * 1.2)

        self.play(Create(c1), Create(c2), FadeIn(l1), FadeIn(l2))
        self.wait(0.5)

        # Results in a row below, well-spaced
        results_data = [
            (Intersection(c1, c2, color=YELLOW, fill_opacity=0.7), "A ∩ B", YELLOW),
            (Union(c1, c2, color=GREEN, fill_opacity=0.7), "A ∪ B", GREEN),
            (Difference(c1, c2, color=BLUE_C, fill_opacity=0.7), "A \\ B", BLUE_C),
            (Exclusion(c1, c2, color=PURPLE, fill_opacity=0.7), "A △ B", PURPLE),
        ]

        result_groups = VGroup()
        for shape, label_text, color in results_data:
            label = Text(label_text, font_size=22, color=color)
            group = VGroup(shape, label)
            # Scale each result to uniform size
            shape.scale_to_fit_height(1.2)
            label.next_to(shape, DOWN, buff=0.2)
            result_groups.add(group)

        result_groups.arrange(RIGHT, buff=1.0)
        result_groups.move_to(DOWN * 1.5)

        self.play(
            LaggedStart(
                *[FadeIn(g, shift=UP * 0.3) for g in result_groups],
                lag_ratio=0.25,
            ),
            run_time=2.5,
        )
        self.wait(2)
