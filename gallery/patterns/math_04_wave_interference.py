from manim import *
import numpy as np

class Math04WaveInterference(Scene):
    """Two sine waves combining — constructive and destructive interference."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Wave Interference", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Three rows of axes
        ax_params = dict(
            x_range=[0, 4 * PI, PI],
            y_range=[-2.2, 2.2, 1],
            x_length=10, y_length=1.5,
            axis_config={"color": GRAY, "stroke_width": 1},
        )

        ax1 = Axes(**ax_params).move_to(UP * 1.8)
        ax2 = Axes(**ax_params).move_to(ORIGIN)
        ax3 = Axes(**ax_params).move_to(DOWN * 1.8)

        l1 = Text("Wave A", font_size=20, color=BLUE).next_to(ax1, LEFT, buff=0.2)
        l2 = Text("Wave B", font_size=20, color=RED).next_to(ax2, LEFT, buff=0.2)
        l3 = Text("A + B", font_size=20, color=YELLOW).next_to(ax3, LEFT, buff=0.2)

        freq_a, freq_b = 1.0, 1.2

        wave_a = ax1.plot(lambda x: np.sin(freq_a * x), color=BLUE, stroke_width=2.5)
        wave_b = ax2.plot(lambda x: np.sin(freq_b * x), color=RED, stroke_width=2.5)
        wave_sum = ax3.plot(
            lambda x: np.sin(freq_a * x) + np.sin(freq_b * x),
            color=YELLOW, stroke_width=2.5,
        )

        # Envelope
        envelope_top = ax3.plot(
            lambda x: 2 * np.abs(np.cos((freq_a - freq_b) * x / 2)),
            color=GREEN, stroke_width=1, stroke_opacity=0.5,
        )
        envelope_bot = ax3.plot(
            lambda x: -2 * np.abs(np.cos((freq_a - freq_b) * x / 2)),
            color=GREEN, stroke_width=1, stroke_opacity=0.5,
        )

        self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(ax3))
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(l3))

        self.play(Create(wave_a), run_time=2)
        self.play(Create(wave_b), run_time=2)

        # Plus sign
        plus = Text("+", font_size=30, color=WHITE).move_to((ax1.get_bottom() + ax2.get_top()) / 2)
        equals = Text("=", font_size=30, color=WHITE).move_to((ax2.get_bottom() + ax3.get_top()) / 2)
        self.play(FadeIn(plus), FadeIn(equals))

        self.play(Create(wave_sum), run_time=2)
        self.play(Create(envelope_top), Create(envelope_bot), run_time=1)

        # Label beats
        beat_label = Text("Beat frequency", font_size=20, color=GREEN)
        beat_label.next_to(ax3, DOWN, buff=0.2)
        self.play(FadeIn(beat_label))
        self.wait(1.5)
