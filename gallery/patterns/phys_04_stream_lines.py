from manim import *
import numpy as np

class Phys04StreamLines(Scene):
    """Stream lines through a vector field — keeps lines visible at end."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Vector Field Stream Lines", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        def field_func(pos):
            x, y = pos[0], pos[1]
            return np.array([
                np.sin(y) + 0.5 * np.cos(x),
                np.cos(x) - 0.5 * np.sin(y),
                0,
            ])

        # Static stream lines (these stay visible)
        stream_lines = StreamLines(
            field_func,
            x_range=[-6, 6, 0.5],
            y_range=[-3.5, 3, 0.5],
            stroke_width=1.5,
            max_anchors_per_line=30,
            padding=0.5,
            colors=[BLUE_E, BLUE_A, TEAL, GREEN_A],
        )

        self.play(stream_lines.create(), run_time=4)

        # Add field equation label
        eq = MathTex(
            r"\vec{F}(x,y) = \begin{pmatrix} \sin y + \tfrac{1}{2}\cos x \\ \cos x - \tfrac{1}{2}\sin y \end{pmatrix}",
            font_size=26, color=WHITE,
        )
        eq.to_edge(DOWN, buff=0.4)
        box = SurroundingRectangle(eq, color=GRAY, buff=0.15, corner_radius=0.1)
        self.play(FadeIn(box), FadeIn(eq))

        # Brief animated flow ON TOP of the static lines
        anim_lines = StreamLines(
            field_func,
            x_range=[-6, 6, 0.8],
            y_range=[-3.5, 3, 0.8],
            stroke_width=2,
            max_anchors_per_line=20,
            colors=[YELLOW_A, ORANGE],
            stroke_opacity=0.6,
        )
        anim_lines.start_animation(warm_up=True, flow_speed=1.5)
        self.wait(3)
        anim_lines.end_animation()
        self.remove(anim_lines)

        # Static lines remain
        self.wait(1.5)
