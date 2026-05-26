from manim import *
import numpy as np

class Ml01AttentionHeatmap(Scene):
    """Attention weight heatmap grid with varying opacity and labels."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Attention Heatmap", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        tokens = ["The", "cat", "sat", "on", "the", "mat"]
        n = len(tokens)

        # Generate attention-like weights (softmax-normalized random)
        np.random.seed(42)
        raw = np.random.exponential(1, (n, n))
        # Make it more interesting: tokens attend to nearby + semantically related
        for i in range(n):
            for j in range(n):
                if abs(i - j) <= 1:
                    raw[i][j] *= 3
        weights = raw / raw.sum(axis=1, keepdims=True)

        cell_size = 0.65
        grid = VGroup()
        grid_offset = np.array([-n * cell_size / 2 + cell_size / 2, -n * cell_size / 2 + cell_size / 2, 0])
        grid_offset += DOWN * 0.3

        for i in range(n):
            for j in range(n):
                w = weights[i][j]
                color = interpolate_color(BLACK, YELLOW, min(w * 2.5, 1.0))
                cell = Square(
                    side_length=cell_size * 0.95,
                    color=GRAY, stroke_width=0.5,
                    fill_color=color, fill_opacity=0.8,
                )
                cell.move_to(grid_offset + np.array([j * cell_size, (n - 1 - i) * cell_size, 0]))

                # Show weight value for strong attention
                if w > 0.2:
                    val_text = Text(f"{w:.2f}", font_size=12, color=WHITE)
                    val_text.move_to(cell)
                    grid.add(VGroup(cell, val_text))
                else:
                    grid.add(cell)

        # Row labels (query tokens) — left side
        row_labels = VGroup()
        for i, token in enumerate(tokens):
            label = Text(token, font_size=18, color=BLUE_A)
            label.next_to(grid[i * n], LEFT, buff=0.3)
            # Align with row center
            y_pos = grid_offset[1] + (n - 1 - i) * cell_size
            label.move_to(np.array([grid_offset[0] - cell_size, y_pos, 0]))
            row_labels.add(label)

        # Column labels (key tokens) — top
        col_labels = VGroup()
        for j, token in enumerate(tokens):
            label = Text(token, font_size=18, color=RED_A)
            x_pos = grid_offset[0] + j * cell_size
            y_pos = grid_offset[1] + n * cell_size
            label.move_to(np.array([x_pos, y_pos, 0]))
            col_labels.add(label)

        query_label = Text("Query →", font_size=16, color=BLUE_A)
        query_label.next_to(row_labels, LEFT, buff=0.3)
        key_label = Text("Key ↓", font_size=16, color=RED_A)
        key_label.next_to(col_labels, UP, buff=0.2)

        self.play(
            LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01),
            run_time=2,
        )
        self.play(FadeIn(row_labels), FadeIn(col_labels))
        self.play(FadeIn(query_label), FadeIn(key_label))

        # Highlight one row
        highlight = SurroundingRectangle(
            VGroup(*[grid[1 * n + j] for j in range(n)]),
            color=BLUE, buff=0.05, corner_radius=0.05,
        )
        self.play(Create(highlight))
        self.wait(1.5)
