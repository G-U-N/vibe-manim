from manim import *

class Flow02TrapezoidLayers(Scene):
    """Neural network layers as colored trapezoid polygons with data flow."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Neural Layer Flow", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        def make_trapezoid(scale_in, scale_out, color, pos):
            h = 1.5
            pts = [
                pos + np.array([-scale_in / 2, h / 2, 0]),
                pos + np.array([-scale_in / 2, -h / 2, 0]),
                pos + np.array([scale_out / 2, -h / 2 * 0.7, 0]),
                pos + np.array([scale_out / 2, h / 2 * 0.7, 0]),
            ]
            trap = Polygon(*pts, color=color, fill_opacity=0.35, stroke_width=2)
            return trap

        layers = [
            (0.8, 0.5, "#A7074B", "Encoder"),
            (0.5, 0.3, "#3465A4", "Bottleneck"),
            (0.3, 0.5, "#4CAF50", "Decoder"),
            (0.5, 0.8, "#F9A825", "Output"),
        ]

        traps = VGroup()
        layer_labels = VGroup()
        x_pos = -4.0
        for scale_in, scale_out, color, name in layers:
            trap = make_trapezoid(scale_in, scale_out, color, np.array([x_pos, -0.3, 0]))
            label = Text(name, font_size=20, color=WHITE).next_to(trap, DOWN, buff=0.3)
            traps.add(trap)
            layer_labels.add(label)
            x_pos += 2.8

        # Center the group
        all_group = VGroup(traps, layer_labels)
        all_group.move_to(DOWN * 0.3)

        # Arrows
        arrows = VGroup()
        for i in range(len(traps) - 1):
            arrow = Arrow(
                traps[i].get_right(), traps[i + 1].get_left(),
                buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.2,
            )
            arrows.add(arrow)

        self.play(
            LaggedStart(*[FadeIn(t, shift=RIGHT * 0.3) for t in traps], lag_ratio=0.2),
            run_time=2,
        )
        self.play(
            LaggedStart(*[FadeIn(l) for l in layer_labels], lag_ratio=0.15),
            run_time=1,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
            run_time=1.5,
        )

        # Forward pass glow
        for trap in traps:
            self.play(
                trap.animate.set_fill(opacity=0.7),
                run_time=0.3,
            )
            self.play(
                trap.animate.set_fill(opacity=0.35),
                run_time=0.3,
            )
        self.wait(1)
