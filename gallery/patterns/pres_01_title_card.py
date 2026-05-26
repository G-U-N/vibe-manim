from manim import *
import numpy as np

class Pres01TitleCard(Scene):
    """Cinematic title card with gradient line accents and subtle particles."""
    def construct(self):
        self.camera.background_color = "#0a0a1a"

        # Subtle background particles
        np.random.seed(42)
        particles = VGroup()
        for _ in range(40):
            x = np.random.uniform(-7, 7)
            y = np.random.uniform(-4, 4)
            size = np.random.uniform(0.015, 0.035)
            opacity = np.random.uniform(0.15, 0.35)
            dot = Dot(np.array([x, y, 0]), radius=size, color=BLUE_A, fill_opacity=opacity)
            particles.add(dot)

        self.play(LaggedStart(*[FadeIn(p) for p in particles], lag_ratio=0.01), run_time=0.8)

        # Accent lines with gradient
        line_top = Line(LEFT * 4, RIGHT * 4, color=TEAL, stroke_width=1.5)
        line_top.move_to(UP * 0.6)
        line_bot = line_top.copy().move_to(DOWN * 1.2)

        # Main title — bold, large
        main_title = Text(
            "Your Presentation Title",
            font_size=50, color=WHITE, weight=BOLD,
        )
        main_title.move_to(UP * 0.05)

        # Subtitle
        subtitle = Text("Subtitle or Key Message", font_size=26, color=GRAY_B)
        subtitle.next_to(main_title, DOWN, buff=0.35)

        # Author line
        author = Text("Author  ·  Conference  ·  2025", font_size=20, color=GRAY)
        author.to_edge(DOWN, buff=0.8)

        # Small logo placeholder
        logo = RoundedRectangle(
            corner_radius=0.1, width=0.8, height=0.8,
            color=TEAL, fill_opacity=0.15, stroke_width=1,
        )
        logo_text = Text("LOGO", font_size=12, color=TEAL).move_to(logo)
        logo_group = VGroup(logo, logo_text).to_corner(DR, buff=0.5)

        # Animate
        self.play(Create(line_top), Create(line_bot), run_time=0.8)
        self.play(Write(main_title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(author), FadeIn(logo_group), run_time=0.6)

        # Gentle particle drift
        self.play(
            *[p.animate.shift(UP * np.random.uniform(0.05, 0.15)) for p in particles],
            run_time=2, rate_func=smooth,
        )
        self.wait(1)
