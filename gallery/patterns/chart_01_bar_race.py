from manim import *
import numpy as np

class Chart01BarRace(Scene):
    """Animated bar chart with bars growing and re-sorting."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Performance Comparison", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        categories = ["GPT-4", "Claude", "Gemini", "Llama", "Mistral"]
        colors = [GREEN, BLUE, RED, PURPLE, ORANGE]

        # Phase 1 values
        values_1 = [82, 78, 75, 65, 60]
        # Phase 2 values (re-ranked)
        values_2 = [85, 92, 88, 78, 82]

        max_val = 100
        bar_width = 0.6
        max_height = 3.5

        def make_bars(values, animate=True):
            bars = VGroup()
            labels = VGroup()
            val_labels = VGroup()

            for i, (cat, val, color) in enumerate(zip(categories, values, colors)):
                height = (val / max_val) * max_height
                bar = Rectangle(
                    width=bar_width, height=height,
                    color=color, fill_opacity=0.7, stroke_width=1.5,
                )
                x = (i - (len(categories) - 1) / 2) * 1.4
                bar.move_to(np.array([x, -2.0 + height / 2, 0]))

                cat_label = Text(cat, font_size=16, color=WHITE)
                cat_label.next_to(bar, DOWN, buff=0.15)

                val_label = Text(str(val), font_size=16, color=color)
                val_label.next_to(bar, UP, buff=0.1)

                bars.add(bar)
                labels.add(cat_label)
                val_labels.add(val_label)

            return bars, labels, val_labels

        bars_1, labels_1, vals_1 = make_bars(values_1)

        # Grow bars from bottom
        zero_bars = VGroup()
        for bar in bars_1:
            zb = bar.copy()
            zb.stretch(0.01, 1, about_edge=DOWN)
            zero_bars.add(zb)

        self.add(zero_bars)
        self.play(
            *[Transform(zb, b) for zb, b in zip(zero_bars, bars_1)],
            run_time=1.5,
        )
        self.play(FadeIn(labels_1), FadeIn(vals_1))

        phase_label = Text("Round 1", font_size=24, color=GRAY_B)
        phase_label.to_edge(LEFT, buff=0.8).shift(UP * 1)
        self.play(FadeIn(phase_label))
        self.wait(1)

        # Transition to phase 2
        bars_2, labels_2, vals_2 = make_bars(values_2)
        phase_label_2 = Text("Round 2", font_size=24, color=YELLOW)
        phase_label_2.move_to(phase_label)

        self.play(
            *[Transform(zb, b) for zb, b in zip(zero_bars, bars_2)],
            *[Transform(v1, v2) for v1, v2 in zip(vals_1, vals_2)],
            Transform(phase_label, phase_label_2),
            run_time=2,
        )

        # Highlight winner
        winner_idx = np.argmax(values_2)
        winner_box = SurroundingRectangle(
            VGroup(zero_bars[winner_idx], vals_1[winner_idx]),
            color=YELLOW, buff=0.1, corner_radius=0.1,
        )
        self.play(Create(winner_box))
        self.wait(1.5)
