from manim import *

class Pres05QuoteCard(Scene):
    """Elegant quote display with decorative elements."""
    def construct(self):
        self.camera.background_color = "#0D1117"

        # Large decorative quote mark
        open_quote = Text('"', font_size=200, color=TEAL, font="Serif")
        open_quote.set_opacity(0.15)
        open_quote.to_corner(UL, buff=0.8)

        close_quote = Text('"', font_size=200, color=TEAL, font="Serif")
        close_quote.set_opacity(0.15)
        close_quote.to_corner(DR, buff=0.8)

        self.play(FadeIn(open_quote), FadeIn(close_quote), run_time=0.8)

        # Quote text
        quote = Text(
            "The only way to do great work\nis to love what you do.",
            font_size=36,
            color=WHITE,
            line_spacing=1.5,
        )
        quote.move_to(UP * 0.3)

        # Decorative line under quote
        line = Line(LEFT * 2, RIGHT * 2, color=TEAL, stroke_width=2)
        line.next_to(quote, DOWN, buff=0.6)

        # Attribution
        author = Text("— Steve Jobs", font_size=24, color=GRAY_B)
        author.next_to(line, DOWN, buff=0.4)

        # Context
        context = Text("Stanford Commencement, 2005", font_size=18, color=GRAY)
        context.next_to(author, DOWN, buff=0.2)

        # Animate
        self.play(Write(quote), run_time=3)
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(author, shift=UP * 0.2))
        self.play(FadeIn(context))

        # Subtle highlight on key phrase
        # "love what you do" is approximately the last part
        highlight_box = RoundedRectangle(
            corner_radius=0.1,
            width=4.5, height=0.6,
            color=TEAL, fill_opacity=0.1,
            stroke_width=1,
        )
        highlight_box.move_to(quote.get_bottom() + UP * 0.15)
        self.play(FadeIn(highlight_box), run_time=0.8)
        self.wait(2)
