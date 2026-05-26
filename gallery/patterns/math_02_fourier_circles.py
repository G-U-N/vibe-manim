from manim import *
import numpy as np

class Math02FourierCircles(Scene):
    """Fourier epicycles drawing a square wave approximation."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Fourier Epicycles", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Fourier coefficients for a square-ish shape
        n_terms = 7
        coefficients = []
        for k in range(n_terms):
            n = 2 * k + 1  # Odd harmonics
            amp = 1.0 / n
            coefficients.append((n, amp))

        # Build epicycle visualization
        base_radius = 1.2
        circles = VGroup()
        radii_lines = VGroup()
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW], n_terms)

        center = LEFT * 3 + DOWN * 0.5

        for i, (n, amp) in enumerate(coefficients):
            r = amp * base_radius
            circle = Circle(
                radius=r, color=colors[i],
                stroke_width=1.5, stroke_opacity=0.5,
            )
            circles.add(circle)
            line = Line(ORIGIN, RIGHT * r, color=colors[i], stroke_width=2)
            radii_lines.add(line)

        # Static display of circles stacked
        info = VGroup()
        for i, (n, amp) in enumerate(coefficients):
            row = Tex(
                f"$n={n}$, $A={amp:.3f}$",
                font_size=22, color=colors[i],
            )
            info.add(row)
        info.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        info.to_edge(RIGHT, buff=1.0).shift(DOWN * 0.5)
        self.play(FadeIn(info))

        # Draw the approximate waveform on the right
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5, y_length=2.5,
            axis_config={"color": GRAY, "stroke_width": 1},
        )
        axes.move_to(RIGHT * 2 + DOWN * 0.5)

        def fourier_sum(t):
            s = 0
            for n, amp in coefficients:
                s += amp * np.sin(n * t)
            return s

        graph = axes.plot(fourier_sum, x_range=[0, 2 * PI], color=YELLOW, stroke_width=2)

        self.play(FadeIn(axes))
        self.play(Create(graph), run_time=3)

        # Show ideal square wave for comparison
        def square_wave(t):
            return 1.0 if np.sin(t) > 0 else -1.0

        square = axes.plot(
            square_wave, x_range=[0.01, 2 * PI - 0.01],
            color=RED, stroke_width=1.5, stroke_opacity=0.5,
            discontinuities=[PI],
        )
        self.play(Create(square), run_time=1)

        label = Text("7 harmonics", font_size=24, color=YELLOW)
        label.next_to(axes, DOWN, buff=0.3)
        self.play(FadeIn(label))
        self.wait(1.5)
