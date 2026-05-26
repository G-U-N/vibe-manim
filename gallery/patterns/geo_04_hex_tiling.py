from manim import *
import numpy as np

class Geo04HexTiling(Scene):
    """Hexagonal tiling building up progressively with color gradient."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Hexagonal Tiling", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        hex_radius = 0.45
        dx = hex_radius * 1.5
        dy = hex_radius * np.sqrt(3)

        hexagons = VGroup()
        colors = color_gradient([BLUE_E, TEAL, GREEN, YELLOW], 50)

        idx = 0
        for row in range(-3, 4):
            for col in range(-4, 5):
                x = col * dx * 1.15
                y = row * dy * 0.58
                if col % 2 != 0:
                    y += dy * 0.29

                pos = np.array([x, y - 0.5, 0])
                if np.linalg.norm(pos) > 4.5:
                    continue

                color = colors[min(idx, len(colors) - 1)]
                hexagon = RegularPolygon(
                    n=6, radius=hex_radius,
                    color=color, fill_opacity=0.3,
                    stroke_width=1.5, stroke_color=color,
                )
                hexagon.move_to(pos)
                hexagons.add(hexagon)
                idx += 1

        # Sort by distance from center for build-up effect
        hexagons.sort(lambda p: np.linalg.norm(p))

        self.play(
            LaggedStart(
                *[GrowFromCenter(h) for h in hexagons],
                lag_ratio=0.02,
            ),
            run_time=4,
        )
        self.wait(1)

        # Pulse effect
        self.play(
            *[h.animate.set_fill(opacity=0.6) for h in hexagons],
            run_time=1,
            rate_func=there_and_back,
        )
        self.wait(1)
