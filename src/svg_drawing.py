import svgwrite
import numpy as np


class SvgDrawing:
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.dwg = svgwrite.Drawing()

    @staticmethod
    def _color(color_str):
        if color_str is None:
            color_str = SvgDrawing.DEFAULT_COLOR

        if color_str == 'black':
            return svgwrite.rgb(0, 0, 0)
        elif color_str == 'red':
            return svgwrite.rgb(255, 0, 0)
        elif color_str == 'green':
            return svgwrite.rgb(0, 255, 0)
        else:
            raise Exception(f'Unsupported color: {color_str}!')

    def line(self, p0, p1, color=None):
        self.dwg.add(
            self.dwg.line(p0, p1, stroke=self._color(color))
        )

    def circle(self, center, diameter, color=None):
        self.dwg.add(
            self.dwg.circle(
                center=center,
                r=diameter / 2,
                fill='none',
                stroke=self._color(color),
            )
        )

    def polygon_filled(self, points, color=None):
        self.dwg.add(
            svgwrite.shapes.Polygon(
                points=points,
                fill=self._color(color),
                stroke='none',
            )
        )

    def arc_csa(self, center, start, angle_deg, color=None):
        path = svgwrite.path.Path(
            d=('M', start[0], start[1]),
            fill='none',
            stroke=self._color(color),
        )

        center = np.array(center)
        start = np.array(start)
        fi = np.deg2rad(angle_deg)
        R = np.array([
            [np.cos(fi), -np.sin(fi)],
            [np.sin(fi), np.cos(fi)],
        ])
        end = center + np.matmul(R, (start - center))
        end = end.tolist()

        radius = np.linalg.norm(start - center)

        path.push_arc(
            target=end,
            rotation=0,
            r=radius,
            large_arc=abs(angle_deg) > 180,
            angle_dir='+' if angle_deg > 0 else '-',
            absolute=True
        )

        self.dwg.add(
            path
        )

    def write(self, file):
        with open(file, 'w') as outf:
            self.dwg.write(outf, pretty=True, indent=2)