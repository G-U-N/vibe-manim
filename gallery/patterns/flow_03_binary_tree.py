from manim import *
import numpy as np

class Flow03BinaryTree(Scene):
    """Recursive binary tree that grows with animation."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Binary Tree Growth", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        nodes = VGroup()
        edges = VGroup()
        depth = 4
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW], depth + 1)

        def build_tree(x, y, level, dx):
            if level > depth:
                return
            node = Dot(
                point=np.array([x, y, 0]),
                radius=0.12 - level * 0.015,
                color=colors[level],
                fill_opacity=0.9,
            )
            nodes.add(node)

            if level < depth:
                # Left child
                lx, ly = x - dx, y - 0.9
                edge_l = Line(
                    np.array([x, y, 0]), np.array([lx, ly, 0]),
                    color=GRAY, stroke_width=1.5,
                )
                edges.add(edge_l)
                build_tree(lx, ly, level + 1, dx * 0.5)

                # Right child
                rx, ry = x + dx, y - 0.9
                edge_r = Line(
                    np.array([x, y, 0]), np.array([rx, ry, 0]),
                    color=GRAY, stroke_width=1.5,
                )
                edges.add(edge_r)
                build_tree(rx, ry, level + 1, dx * 0.5)

        build_tree(0, 2.0, 0, 3.0)

        # Animate level by level
        levels = {}
        for node in nodes:
            y_approx = round(node.get_center()[1], 1)
            levels.setdefault(y_approx, []).append(node)

        edge_idx = 0
        sorted_levels = sorted(levels.keys(), reverse=True)
        for i, y_val in enumerate(sorted_levels):
            level_nodes = levels[y_val]
            if i == 0:
                self.play(
                    LaggedStart(*[GrowFromCenter(n) for n in level_nodes], lag_ratio=0.1),
                    run_time=0.5,
                )
            else:
                # Get edges leading to this level
                level_edges = []
                for n in level_nodes:
                    for e in edges:
                        end = e.get_end()
                        if np.allclose(end, n.get_center(), atol=0.15):
                            level_edges.append(e)

                if level_edges:
                    self.play(
                        LaggedStart(*[Create(e) for e in level_edges], lag_ratio=0.05),
                        run_time=0.5,
                    )
                self.play(
                    LaggedStart(*[GrowFromCenter(n) for n in level_nodes], lag_ratio=0.05),
                    run_time=0.5,
                )

        self.wait(1.5)
