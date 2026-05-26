from manim import *

class Pres04Timeline(Scene):
    """Horizontal timeline with animated milestones."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Project Timeline", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        milestones = [
            ("2023 Q1", "Research", BLUE),
            ("2023 Q2", "Design", TEAL),
            ("2023 Q3", "Prototype", GREEN),
            ("2023 Q4", "Testing", ORANGE),
            ("2024 Q1", "Launch", RED),
        ]

        # Main timeline line
        line = Line(LEFT * 5.5, RIGHT * 5.5, color=GRAY, stroke_width=2)
        line.move_to(DOWN * 0.3)
        self.play(Create(line), run_time=1)

        n = len(milestones)
        spacing = 10 / (n - 1)

        for i, (date, label_text, color) in enumerate(milestones):
            x = -5 + i * spacing

            # Milestone dot
            dot = Dot(np.array([x, -0.3, 0]), radius=0.12, color=color, fill_opacity=0.9)

            # Date label (below)
            date_label = Text(date, font_size=16, color=GRAY_B)
            date_label.next_to(dot, DOWN, buff=0.3)

            # Milestone label (above, in colored box)
            label = Text(label_text, font_size=20, color=WHITE)
            box = RoundedRectangle(
                corner_radius=0.1,
                width=label.width + 0.4,
                height=label.height + 0.3,
                color=color,
                fill_opacity=0.3,
                stroke_width=1.5,
            )

            # Alternate above/below for visual variety
            if i % 2 == 0:
                box.next_to(dot, UP, buff=0.5)
            else:
                box.next_to(dot, UP, buff=1.2)
            label.move_to(box)

            # Connecting line
            conn = Line(
                dot.get_top(), box.get_bottom(),
                color=color, stroke_width=1, stroke_opacity=0.5,
            )

            self.play(
                GrowFromCenter(dot),
                FadeIn(date_label),
                Create(conn),
                FadeIn(box),
                FadeIn(label),
                run_time=0.8,
            )

        # Progress indicator (filled portion of line)
        progress = Line(
            LEFT * 5.5, RIGHT * 0.0,
            color=GREEN, stroke_width=4,
        )
        progress.move_to(line.get_center())
        progress.align_to(line, LEFT)

        progress_label = Text("Current", font_size=16, color=GREEN)
        progress_label.next_to(progress.get_right(), UP, buff=0.2)

        self.play(Create(progress), FadeIn(progress_label), run_time=1.5)
        self.wait(1.5)
