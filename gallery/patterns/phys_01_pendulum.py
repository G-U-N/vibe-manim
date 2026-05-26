from manim import *
import numpy as np

class Phys01Pendulum(Scene):
    """Swinging pendulum with phase space diagram side by side."""
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text("Pendulum & Phase Space", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title))

        # Left: pendulum visualization
        pivot = np.array([-3.5, 1.5, 0])
        length = 2.5
        g = 9.8
        theta0 = PI / 4
        omega0 = 0.0
        dt = 0.02
        n_steps = 500

        # Simulate pendulum
        thetas = [theta0]
        omegas = [omega0]
        for _ in range(n_steps):
            alpha = -(g / length) * np.sin(thetas[-1]) - 0.05 * omegas[-1]
            new_omega = omegas[-1] + alpha * dt
            new_theta = thetas[-1] + new_omega * dt
            omegas.append(new_omega)
            thetas.append(new_theta)

        # Draw pendulum at initial state
        bob_pos = pivot + length * np.array([np.sin(theta0), -np.cos(theta0), 0])
        rod = Line(pivot, bob_pos, color=GRAY, stroke_width=3)
        bob = Dot(bob_pos, radius=0.15, color=BLUE, fill_opacity=0.9)
        pivot_dot = Dot(pivot, radius=0.06, color=WHITE)

        self.play(FadeIn(pivot_dot), Create(rod), FadeIn(bob))

        # Right: phase space axes
        phase_ax = Axes(
            x_range=[-PI / 3, PI / 3, PI / 6],
            y_range=[-4, 4, 2],
            x_length=4.5, y_length=3.5,
            axis_config={"color": GRAY, "stroke_width": 1},
        )
        phase_ax.move_to(RIGHT * 2.5 + DOWN * 0.3)

        x_label = Tex(r"$\theta$", font_size=24, color=GRAY).next_to(phase_ax, DOWN, buff=0.2)
        y_label = Tex(r"$\dot{\theta}$", font_size=24, color=GRAY).next_to(phase_ax, LEFT, buff=0.2)
        self.play(FadeIn(phase_ax), FadeIn(x_label), FadeIn(y_label))

        # Animate pendulum + trace phase space
        trace_points = []
        phase_trace = VMobject(color=YELLOW, stroke_width=2)

        for i in range(0, n_steps, 3):
            theta = thetas[i]
            omega = omegas[i]
            new_bob = pivot + length * np.array([np.sin(theta), -np.cos(theta), 0])

            rod.put_start_and_end_on(pivot, new_bob)
            bob.move_to(new_bob)

            # Phase point
            pp = phase_ax.c2p(theta, omega)
            trace_points.append(pp)
            if len(trace_points) > 2:
                phase_trace.set_points_smoothly(trace_points)

            self.add(rod, bob, phase_trace)
            self.wait(0.02)

        # Phase dot at current position
        phase_dot = Dot(trace_points[-1], radius=0.06, color=RED)
        self.play(FadeIn(phase_dot))
        self.wait(1.5)
