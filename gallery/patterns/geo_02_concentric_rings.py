from manim import *

class Geo02ConcentricRings(Scene):
    """Expanding colored rings with fade pulse — compact radar effect."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        title = Text("Concentric Ring Pulse", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        center_dot = Dot(ORIGIN + DOWN * 0.3, radius=0.08, color=YELLOW)
        self.play(FadeIn(center_dot))

        colors = [BLUE_A, TEAL_A, GREEN_A, YELLOW_A, ORANGE, RED_A, PURPLE_A, BLUE_B]
        rings = VGroup()
        for i, color in enumerate(colors):
            r = 0.25 + i * 0.28  # tighter spacing, max ~2.2 radius
            ring = Annulus(
                inner_radius=r - 0.04,
                outer_radius=r + 0.04,
                color=color,
                fill_opacity=0.6,
                stroke_width=2,
            )
            ring.move_to(DOWN * 0.3)
            rings.add(ring)

        # Staggered expansion from center
        for ring in rings:
            ring_start = ring.copy().scale(0.01)
            self.play(
                ring_start.animate.become(ring),
                run_time=0.35,
                rate_func=smooth,
            )
            self.add(ring)
            self.remove(ring_start)

        self.wait(0.5)

        # Pulse: rings briefly brighten then return
        self.play(
            *[ring.animate.set_fill(opacity=0.9) for ring in rings],
            run_time=0.5,
            rate_func=there_and_back,
        )

        # Second pulse: scale up slightly and back
        self.play(
            *[ring.animate.scale(1.08) for ring in rings],
            run_time=0.8,
            rate_func=there_and_back,
        )
        self.wait(1)
