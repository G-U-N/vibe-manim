from manim import *

class Flow05LayeredStack(Scene):
    """3D-like stacked rectangles with perspective and labels."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Technology Stack", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        layers_data = [
            ("Frontend", "#61DAFB", 0.7),
            ("API Gateway", "#4CAF50", 0.6),
            ("Business Logic", "#A7074B", 0.5),
            ("Data Access", "#3465A4", 0.4),
            ("Database", "#F9A825", 0.3),
        ]

        stack = VGroup()
        for i, (name, color, opacity) in enumerate(layers_data):
            # Main rectangle
            rect = RoundedRectangle(
                corner_radius=0.1,
                height=0.7,
                width=4.5 - i * 0.15,
                color=color,
                fill_opacity=opacity,
                stroke_width=2,
            )
            # 3D offset effect
            y_pos = -i * 0.85 + 1.5
            rect.move_to(np.array([i * 0.08, y_pos, 0]))

            # Side face for 3D look
            side = Polygon(
                rect.get_corner(UR),
                rect.get_corner(UR) + np.array([0.2, 0.2, 0]),
                rect.get_corner(DR) + np.array([0.2, 0.2, 0]),
                rect.get_corner(DR),
                color=color,
                fill_opacity=opacity * 0.6,
                stroke_width=1,
            )
            # Top face
            top = Polygon(
                rect.get_corner(UL),
                rect.get_corner(UL) + np.array([0.2, 0.2, 0]),
                rect.get_corner(UR) + np.array([0.2, 0.2, 0]),
                rect.get_corner(UR),
                color=color,
                fill_opacity=opacity * 0.4,
                stroke_width=1,
            )

            label = Text(name, font_size=22, color=WHITE).move_to(rect)

            layer_group = VGroup(rect, side, top, label)
            stack.add(layer_group)

        stack.move_to(DOWN * 0.3)

        # Animate from bottom to top
        for layer in reversed(list(stack)):
            self.play(FadeIn(layer, shift=DOWN * 0.3), run_time=0.5)

        self.wait(0.5)

        # Highlight middle layer
        mid = stack[2]
        box = SurroundingRectangle(mid, color=YELLOW, buff=0.1, corner_radius=0.1)
        self.play(Create(box), run_time=0.8)
        self.wait(1.5)
