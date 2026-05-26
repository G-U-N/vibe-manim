from manim import *
import numpy as np

class Geo05SpiralGalaxy(Scene):
    """Logarithmic spiral of dots with color gradient and rotation."""
    def construct(self):
        self.camera.background_color = "#0a0a1a"

        title = Text("Spiral Galaxy", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        dots = VGroup()
        n_arms = 3
        dots_per_arm = 80
        colors = color_gradient([BLUE_E, BLUE_A, TEAL_A, WHITE], dots_per_arm)

        for arm in range(n_arms):
            offset = arm * TAU / n_arms
            for i in range(dots_per_arm):
                t = i / dots_per_arm
                r = 0.1 + 3.5 * t
                theta = offset + 3 * t * TAU / n_arms + 0.3 * np.random.randn()
                x = r * np.cos(theta) + 0.05 * np.random.randn()
                y = r * np.sin(theta) + 0.05 * np.random.randn()

                size = 0.02 + 0.04 * (1 - t)
                dot = Dot(
                    point=np.array([x, y - 0.3, 0]),
                    radius=size,
                    color=colors[i],
                    fill_opacity=0.4 + 0.6 * (1 - t),
                )
                dots.add(dot)

        # Center glow
        center = Dot(ORIGIN + DOWN * 0.3, radius=0.15, color=YELLOW, fill_opacity=0.8)
        glow = Circle(radius=0.4, color=YELLOW, fill_opacity=0.15, stroke_width=0)
        glow.move_to(center)

        self.play(FadeIn(center), FadeIn(glow))
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in dots],
                lag_ratio=0.005,
            ),
            run_time=4,
        )
        self.wait(0.5)

        # Slow rotation
        galaxy = VGroup(dots, center, glow)
        self.play(Rotate(galaxy, angle=PI / 6, about_point=DOWN * 0.3), run_time=3, rate_func=smooth)
        self.wait(1)
