from manim import *

class Pres03SplitCompare(Scene):
    """Left vs Right comparison — symmetric text positioning."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Comparison", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Left panel
        left_bg = Rectangle(
            width=5.5, height=4.5,
            color=BLUE, fill_opacity=0.1, stroke_width=1,
        ).move_to(LEFT * 3.2 + DOWN * 0.3)

        left_title = Text("Method A", font_size=30, color=BLUE, weight=BOLD)
        left_title.move_to(left_bg.get_top() + DOWN * 0.4)

        left_items = VGroup(
            Tex(r"$\bullet$ Fast convergence", font_size=24, color=WHITE),
            Tex(r"$\bullet$ Low memory usage", font_size=24, color=WHITE),
            Tex(r"$\bullet$ Simple implementation", font_size=24, color=WHITE),
            Tex(r"$\bullet$ Limited accuracy", font_size=24, color=RED_A),
        )
        left_items.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        left_items.next_to(left_title, DOWN, buff=0.5)
        # Align to left panel center-left
        left_items.move_to(left_bg.get_center() + DOWN * 0.3)
        left_items.align_to(left_bg, LEFT).shift(RIGHT * 0.6)

        # Right panel
        right_bg = Rectangle(
            width=5.5, height=4.5,
            color=GREEN, fill_opacity=0.1, stroke_width=1,
        ).move_to(RIGHT * 3.2 + DOWN * 0.3)

        right_title = Text("Method B", font_size=30, color=GREEN, weight=BOLD)
        right_title.move_to(right_bg.get_top() + DOWN * 0.4)

        right_items = VGroup(
            Tex(r"$\bullet$ High accuracy", font_size=24, color=WHITE),
            Tex(r"$\bullet$ Robust to noise", font_size=24, color=WHITE),
            Tex(r"$\bullet$ Scalable", font_size=24, color=WHITE),
            Tex(r"$\bullet$ Slower training", font_size=24, color=RED_A),
        )
        right_items.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        right_items.next_to(right_title, DOWN, buff=0.5)
        # Mirror: same offset from panel edge as left side
        right_items.move_to(right_bg.get_center() + DOWN * 0.3)
        right_items.align_to(right_bg, LEFT).shift(RIGHT * 0.6)

        # Divider
        divider = Line(UP * 2.5, DOWN * 2.5, color=YELLOW, stroke_width=2)
        divider.move_to(DOWN * 0.3)

        vs_label = Text("VS", font_size=24, color=YELLOW, weight=BOLD)
        vs_bg = Circle(radius=0.3, color="#0D1117", fill_opacity=1, stroke_width=0)
        vs_bg.move_to(divider.get_center())
        vs_label.move_to(vs_bg)

        # Animate
        self.play(FadeIn(left_bg), FadeIn(right_bg))
        self.play(FadeIn(left_title), FadeIn(right_title))
        self.play(Create(divider), FadeIn(vs_bg), FadeIn(vs_label))

        self.play(
            LaggedStart(*[FadeIn(item, shift=LEFT * 0.3) for item in left_items], lag_ratio=0.2),
            run_time=1.5,
        )
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT * 0.3) for item in right_items], lag_ratio=0.2),
            run_time=1.5,
        )

        # Winner highlight
        winner_box = SurroundingRectangle(right_bg, color=GREEN, buff=0.1, corner_radius=0.1)
        winner_label = Text("Recommended", font_size=20, color=GREEN)
        winner_label.next_to(right_bg, DOWN, buff=0.2)
        self.play(Create(winner_box), FadeIn(winner_label))
        self.wait(1.5)
