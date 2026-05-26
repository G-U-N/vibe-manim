from manim import *
import numpy as np

class Ml04NeuralNet(Scene):
    """Neural network visualization with forward pass animation."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Neural Network", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        layer_sizes = [4, 6, 8, 6, 3]
        layer_colors = [BLUE, TEAL, GREEN, TEAL, RED]
        spacing_x = 2.2
        spacing_y = 0.6

        all_nodes = []
        all_node_mobs = VGroup()

        for l, (size, color) in enumerate(zip(layer_sizes, layer_colors)):
            layer_nodes = []
            for i in range(size):
                x = (l - (len(layer_sizes) - 1) / 2) * spacing_x
                y = (i - (size - 1) / 2) * spacing_y - 0.3
                node = Circle(
                    radius=0.15, color=color,
                    fill_opacity=0.6, stroke_width=1.5,
                )
                node.move_to(np.array([x, y, 0]))
                layer_nodes.append(node)
                all_node_mobs.add(node)
            all_nodes.append(layer_nodes)

        # Connections
        all_edges = VGroup()
        for l in range(len(layer_sizes) - 1):
            for node_a in all_nodes[l]:
                for node_b in all_nodes[l + 1]:
                    edge = Line(
                        node_a.get_right(), node_b.get_left(),
                        color=GRAY, stroke_width=0.5, stroke_opacity=0.3,
                    )
                    all_edges.add(edge)

        # Layer labels
        layer_labels = VGroup()
        names = ["Input", "Hidden 1", "Hidden 2", "Hidden 3", "Output"]
        for l, name in enumerate(names):
            x = (l - (len(layer_sizes) - 1) / 2) * spacing_x
            label = Text(name, font_size=16, color=GRAY_B)
            label.move_to(np.array([x, -3.2, 0]))
            layer_labels.add(label)

        self.play(FadeIn(all_edges), run_time=1)
        self.play(
            LaggedStart(*[FadeIn(n, scale=0.5) for n in all_node_mobs], lag_ratio=0.02),
            run_time=2,
        )
        self.play(FadeIn(layer_labels))

        # Forward pass animation: highlight layer by layer
        for l in range(len(layer_sizes)):
            nodes_in_layer = all_nodes[l]
            self.play(
                *[n.animate.set_fill(opacity=1.0).set_stroke(width=3) for n in nodes_in_layer],
                run_time=0.4,
            )
            if l < len(layer_sizes) - 1:
                # Highlight edges from this layer
                layer_edges = VGroup()
                for node_a in all_nodes[l]:
                    for node_b in all_nodes[l + 1]:
                        edge = Line(
                            node_a.get_right(), node_b.get_left(),
                            color=YELLOW, stroke_width=1.5, stroke_opacity=0.6,
                        )
                        layer_edges.add(edge)
                self.play(FadeIn(layer_edges), run_time=0.3)
                self.play(FadeOut(layer_edges), run_time=0.2)

            self.play(
                *[n.animate.set_fill(opacity=0.6).set_stroke(width=1.5) for n in nodes_in_layer],
                run_time=0.2,
            )

        # Output highlight
        output_nodes = all_nodes[-1]
        self.play(
            *[n.animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.8) for n in output_nodes],
            run_time=0.5,
        )
        output_label = Text("Prediction", font_size=20, color=YELLOW)
        output_label.next_to(VGroup(*output_nodes), RIGHT, buff=0.3)
        self.play(FadeIn(output_label))
        self.wait(1.5)
