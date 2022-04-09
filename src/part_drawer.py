from src.svg_drawing import SvgDrawing


class PartDrawer:
    def __init__(self, shape_wh, unit_size, pattern_drawer, fillet_radius=5):
        self.drawing = SvgDrawing()

        self.shape_wh = shape_wh
        self.unit_size = unit_size
        self.pattern_drawer = pattern_drawer
        self.fillet_radius = fillet_radius

    def _draw_border(self):
        w, h = self.shape_wh
        w_mm = w * self.unit_size
        h_mm = h * self.unit_size
        fr = self.fillet_radius

        d = self.drawing

        # ~~~lines~~~
        # top
        d.line(
            (fr, 0),
            (w_mm - fr, 0)
        )
        # bottom
        d.line(
            (fr, h_mm),
            (w_mm - fr, h_mm)
        )
        # left
        d.line(
            (0, fr),
            (0, h_mm - fr)
        )
        # right
        d.line(
            (w_mm, fr),
            (w_mm, h_mm - fr)
        )

        # ~~~fillets~~~
        # top-left
        d.arc_csa(
            (fr, fr),
            (0, fr),
            90
        )
        # bottom-left
        d.arc_csa(
            (fr, h_mm - fr),
            (fr, h_mm),
            90
        )
        # botom-right
        d.arc_csa(
            (w_mm - fr, h_mm - fr),
            (w_mm - fr, h_mm),
            -90
        )
        # top-right
        d.arc_csa(
            (w_mm - fr, fr),
            (w_mm, fr),
            -90
        )

    def draw(self):
        self._draw_border()
        self.pattern_drawer.draw(self.drawing)

    def write(self, file):
        self.drawing.write(file)