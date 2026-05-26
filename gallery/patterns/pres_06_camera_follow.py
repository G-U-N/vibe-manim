from manim import *
import numpy as np

class Pres06CameraFollow(MovingCameraScene):
    """Camera follows a dot along a curve, then zooms back out."""
    def construct(self):
        self.camera.background_color = "#0D1117"
        self.camera.frame.save_state()

        # Create axes and curve
        ax = Axes(
            x_range=[-1, 10, 1], y_range=[-2, 2, 1],
            x_length=10, y_length=4,
            axis_config={"color": GRAY, "stroke_width": 1},
        )
        ax.move_to(ORIGIN)

        graph = ax.plot(lambda x: 1.5 * np.sin(x), color=BLUE, x_range=[0, 3 * PI])
        graph_label = ax.get_graph_label(graph, label="f(x) = \\sin(x)", x_val=2, color=BLUE)

        # Dots at start and end
        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE, radius=0.08)
        start_dot = Dot(ax.i2gp(graph.t_min, graph), color=GREEN, radius=0.06)
        end_dot = Dot(ax.i2gp(graph.t_max, graph), color=RED, radius=0.06)

        start_label = Text("Start", font_size=16, color=GREEN).next_to(start_dot, DOWN, buff=0.2)
        end_label = Text("End", font_size=16, color=RED).next_to(end_dot, DOWN, buff=0.2)

        self.add(ax, graph, graph_label, start_dot, end_dot, start_label, end_label, moving_dot)

        # Zoom into the moving dot
        self.play(self.camera.frame.animate.scale(0.4).move_to(moving_dot))

        # Camera follows dot along graph
        def update_camera(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_camera)
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear), run_time=5)
        self.camera.frame.remove_updater(update_camera)

        # Zoom back out
        self.play(Restore(self.camera.frame), run_time=1.5)

        # Highlight the full path
        traced = graph.copy().set_stroke(YELLOW, width=3, opacity=0.6)
        self.play(Create(traced), run_time=1)
        self.wait(1.5)
