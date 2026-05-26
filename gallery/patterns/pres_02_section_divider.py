from manim import *

class Pres02SectionDivider(Scene):
    """Stylish section transition with morphing geometric shapes."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        # Opening shape: expanding circle that morphs
        circle = Circle(radius=0.1, color=TEAL, fill_opacity=0.5, stroke_width=2)
        self.play(GrowFromCenter(circle))
        self.play(circle.animate.scale(15), run_time=1, rate_func=rush_into)

        # Background is now teal-ish, transition to section
        self.camera.background_color = "#0D3B4F"
        self.remove(circle)

        # Section number
        number = Text("02", font_size=100, color=WHITE, weight=BOLD, font="Monospace")
        number.set_opacity(0.15)
        number.to_corner(UL, buff=0.8)

        # Section title
        section_title = Text("Methodology", font_size=52, color=WHITE, weight=BOLD)
        section_title.move_to(ORIGIN)

        # Decorative elements
        line_left = Line(LEFT * 2.5, LEFT * 0.5, color=TEAL, stroke_width=3)
        line_right = Line(RIGHT * 0.5, RIGHT * 2.5, color=TEAL, stroke_width=3)
        line_left.next_to(section_title, LEFT, buff=0.3)
        line_right.next_to(section_title, RIGHT, buff=0.3)

        subtitle = Text(
            "How we approach the problem",
            font_size=24, color=GRAY_B,
        )
        subtitle.next_to(section_title, DOWN, buff=0.5)

        self.play(FadeIn(number, scale=1.5))
        self.play(
            FadeIn(section_title, shift=UP * 0.3),
            Create(line_left),
            Create(line_right),
            run_time=1.5,
        )
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        # Small decorative dots
        dots = VGroup()
        for i in range(3):
            dot = Dot(radius=0.04, color=TEAL)
            dots.add(dot)
        dots.arrange(RIGHT, buff=0.15)
        dots.next_to(subtitle, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2))

        self.wait(2)
