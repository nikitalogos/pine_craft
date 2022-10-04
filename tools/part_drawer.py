import json
from collections.abc import Sequence

from drawings.base_drawing import BaseDrawing
from drawings.svg_drawing import SvgDrawing
from drawings.dxf_drawing import DxfDrawing


class PartDrawer:
    def __init__(self, shape_wh, unit_size, pattern_drawer, fillet_radius=5, drawings: Sequence[BaseDrawing] = None):
        if drawings is None:
            drawings = [
                SvgDrawing(),
                DxfDrawing(),
            ]

        self.drawings = drawings

        self.shape_wh = shape_wh
        self.unit_size = unit_size
        self.pattern_drawer = pattern_drawer
        self.fillet_radius = fillet_radius

    def _draw_border(self, drawing):
        w, h = self.shape_wh
        w_mm = w * self.unit_size
        h_mm = h * self.unit_size
        fr = self.fillet_radius

        d = drawing

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
        for drawing in self.drawings:
            self._draw_border(drawing)
            self.pattern_drawer.draw(drawing)

    def get_meta_dict(self):
        return {
            'shape_wh': self.shape_wh,
            'unit_size': self.unit_size,
            'pattern_drawer': self.pattern_drawer.get_meta_dict(),
            'fillet_radius': self.fillet_radius,
        }

    def write(self, file):
        for drawing in self.drawings:
            drawing.write(file, is_no_ext=True)

        with open(f'{file}.json', 'w') as outf:
            json.dump(
                self.get_meta_dict(),
                outf,
                indent=4,
            )
