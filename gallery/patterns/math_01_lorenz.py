from manim import *
import numpy as np

class Math01Lorenz(Scene):
    """Lorenz attractor with colorful trajectories and trailing effect."""
    def construct(self):
        self.camera.background_color = "#0a0a1a"

        title = Text("Lorenz Attractor", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Lorenz system parameters
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

        def lorenz(state, dt=0.005):
            x, y, z = state
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            return np.array([x + dx * dt, y + dy * dt, z + dz * dt])

        # Generate trajectory
        n_steps = 6000
        states = [np.array([1.0, 1.0, 1.0])]
        for _ in range(n_steps):
            states.append(lorenz(states[-1]))
        states = np.array(states)

        # Normalize to screen coordinates
        x_range = states[:, 0].max() - states[:, 0].min()
        y_range = states[:, 2].max() - states[:, 2].min()
        scale = min(5.0 / x_range, 3.0 / y_range)

        points = []
        for s in states[::3]:
            px = (s[0] - states[:, 0].mean()) * scale
            py = (s[2] - states[:, 2].mean()) * scale - 0.3
            points.append(np.array([px, py, 0]))

        # Create curve segments with color gradient
        colors = color_gradient([BLUE_E, BLUE_A, TEAL, GREEN, YELLOW, RED], len(points))
        curves = VGroup()
        segment_size = 20
        for i in range(0, len(points) - segment_size, segment_size):
            segment_points = points[i:i + segment_size + 1]
            if len(segment_points) < 2:
                continue
            curve = VMobject()
            curve.set_points_smoothly(segment_points)
            curve.set_stroke(colors[i], width=1.5, opacity=0.8)
            curves.add(curve)

        # Animated drawing
        self.play(
            LaggedStart(
                *[Create(c, run_time=0.1) for c in curves],
                lag_ratio=0.02,
            ),
            run_time=5,
        )

        # Add glowing center dots
        lobe1 = Dot(
            np.array([-1.5 * scale, 0, 0]),
            radius=0.06, color=YELLOW, fill_opacity=0.8,
        )
        lobe2 = Dot(
            np.array([1.5 * scale, 0, 0]),
            radius=0.06, color=YELLOW, fill_opacity=0.8,
        )
        self.play(FadeIn(lobe1), FadeIn(lobe2))
        self.wait(1.5)
