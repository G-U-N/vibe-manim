from manim import *

class Geo03PolygonMorph(Scene):
    """Triangle → Square → Pentagon → Hexagon → Circle smooth morphing."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Shape Morphing", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        shapes = [
            (RegularPolygon(n=3, color=RED, fill_opacity=0.5, stroke_width=3), "Triangle"),
            (RegularPolygon(n=4, color=ORANGE, fill_opacity=0.5, stroke_width=3), "Square"),
            (RegularPolygon(n=5, color=YELLOW, fill_opacity=0.5, stroke_width=3), "Pentagon"),
            (RegularPolygon(n=6, color=GREEN, fill_opacity=0.5, stroke_width=3), "Hexagon"),
            (RegularPolygon(n=8, color=TEAL, fill_opacity=0.5, stroke_width=3), "Octagon"),
            (Circle(radius=1, color=BLUE, fill_opacity=0.5, stroke_width=3), "Circle"),
        ]

        for s, _ in shapes:
            s.scale(1.5).move_to(DOWN * 0.5)

        current_shape = shapes[0][0].copy()
        label = Text(shapes[0][1], font_size=30, color=shapes[0][0].get_color())
        label.next_to(current_shape, DOWN, buff=0.5)

        self.play(Create(current_shape), FadeIn(label))
        self.wait(0.5)

        for i in range(1, len(shapes)):
            new_shape = shapes[i][0]
            new_label = Text(shapes[i][1], font_size=30, color=new_shape.get_color())
            new_label.next_to(new_shape, DOWN, buff=0.5)

            self.play(
                Transform(current_shape, new_shape),
                Transform(label, new_label),
                run_time=1.5,
                rate_func=smooth,
            )
            self.wait(0.5)

        self.wait(1)
