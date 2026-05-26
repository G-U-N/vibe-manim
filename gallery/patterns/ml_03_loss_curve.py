from manim import *
import numpy as np

class Ml03LossCurve(Scene):
    """Animated training loss curve with real-time tracker dot."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Training Progress", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 3, 0.5],
            x_length=9, y_length=4,
            axis_config={"color": GRAY, "stroke_width": 1.5},
            x_axis_config={"numbers_to_include": [0, 20, 40, 60, 80, 100]},
            y_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2, 2.5, 3]},
        )
        axes.move_to(DOWN * 0.3)

        x_label = Text("Epoch", font_size=20, color=GRAY).next_to(axes, DOWN, buff=0.3)
        y_label = Text("Loss", font_size=20, color=GRAY).next_to(axes, LEFT, buff=0.3)
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))

        # Training loss: exponential decay with noise
        np.random.seed(42)
        def train_loss(x):
            return 2.5 * np.exp(-0.03 * x) + 0.15 + 0.1 * np.sin(x * 0.5) * np.exp(-0.02 * x)

        def val_loss(x):
            base = 2.5 * np.exp(-0.025 * x) + 0.25
            # Slight overfitting after epoch 70
            if x > 70:
                base += 0.005 * (x - 70)
            return base

        # Draw training loss
        train_curve = axes.plot(train_loss, x_range=[0, 100], color=BLUE, stroke_width=2.5)
        val_curve = axes.plot(val_loss, x_range=[0, 100], color=RED, stroke_width=2.5)

        # Animated tracker dot
        tracker = ValueTracker(0)
        dot_train = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), train_loss(tracker.get_value())),
                color=BLUE, radius=0.08,
            )
        )
        dot_val = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), val_loss(tracker.get_value())),
                color=RED, radius=0.08,
            )
        )

        # Epoch counter
        epoch_text = always_redraw(
            lambda: Text(
                f"Epoch: {int(tracker.get_value())}",
                font_size=22, color=WHITE,
            ).to_corner(UR, buff=0.5)
        )

        self.add(dot_train, dot_val, epoch_text)

        self.play(
            Create(train_curve),
            Create(val_curve),
            tracker.animate.set_value(100),
            run_time=5,
            rate_func=linear,
        )

        # Legend
        legend = VGroup(
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=BLUE, stroke_width=3), Text("Train", font_size=18, color=BLUE)).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=RED, stroke_width=3), Text("Val", font_size=18, color=RED)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        legend.to_corner(DR, buff=0.8)
        self.play(FadeIn(legend))

        # Mark best epoch
        best_epoch = 68
        best_line = DashedLine(
            axes.c2p(best_epoch, 0), axes.c2p(best_epoch, val_loss(best_epoch)),
            color=GREEN, stroke_width=1.5,
        )
        best_label = Text("Best", font_size=16, color=GREEN)
        best_label.next_to(best_line, UP, buff=0.1)
        self.play(Create(best_line), FadeIn(best_label))
        self.wait(1.5)
