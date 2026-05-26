from manim import *
import numpy as np

class Phys03ParticleSystem(Scene):
    """Particles emitting from center with gravity and color fading."""
    def construct(self):
        self.camera.background_color = "#0a0a1a"

        title = Text("Particle System", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Emitter
        emitter = Dot(ORIGIN + DOWN * 0.5, radius=0.1, color=YELLOW)
        glow = Circle(radius=0.3, color=YELLOW, fill_opacity=0.15, stroke_width=0)
        glow.move_to(emitter)
        self.play(FadeIn(emitter), FadeIn(glow))

        np.random.seed(123)
        n_waves = 5
        particles_per_wave = 20

        for wave in range(n_waves):
            particles = VGroup()
            targets = VGroup()
            for _ in range(particles_per_wave):
                angle = np.random.uniform(PI / 6, 5 * PI / 6)
                speed = np.random.uniform(1.5, 4.0)
                vx = speed * np.cos(angle)
                vy = speed * np.sin(angle)
                # Simulate ~1 second of flight with gravity
                t = np.random.uniform(0.5, 1.2)
                px = vx * t
                py = vy * t - 0.5 * 4.9 * t ** 2

                color = random_color()
                size = np.random.uniform(0.03, 0.08)
                particle = Dot(
                    emitter.get_center(),
                    radius=size,
                    color=color,
                    fill_opacity=0.9,
                )
                target = Dot(
                    emitter.get_center() + np.array([px, py, 0]),
                    radius=size * 0.3,
                    color=color,
                    fill_opacity=0.1,
                )
                particles.add(particle)
                targets.add(target)

            self.play(
                *[
                    p.animate.move_to(t.get_center()).set_opacity(0.1).scale(0.3)
                    for p, t in zip(particles, targets)
                ],
                run_time=1.2,
                rate_func=rush_from,
            )
            self.remove(*particles)

        # Final burst
        burst = VGroup()
        for _ in range(40):
            angle = np.random.uniform(0, TAU)
            dist = np.random.uniform(1, 3.5)
            color = interpolate_color(YELLOW, RED, np.random.random())
            dot = Dot(
                emitter.get_center(),
                radius=np.random.uniform(0.04, 0.1),
                color=color,
                fill_opacity=0.9,
            )
            burst.add(dot)

        targets = [
            emitter.get_center() + np.array([
                np.random.uniform(1, 3.5) * np.cos(np.random.uniform(0, TAU)),
                np.random.uniform(1, 3.5) * np.sin(np.random.uniform(0, TAU)),
                0,
            ])
            for _ in burst
        ]

        self.play(
            *[d.animate.move_to(t).set_opacity(0) for d, t in zip(burst, targets)],
            run_time=1.5,
            rate_func=rush_from,
        )
        self.wait(1)
