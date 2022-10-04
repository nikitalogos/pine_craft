import os
import svgwrite
import numpy as np

from .base_drawing import BaseDrawing


class SvgDrawing(BaseDrawing):
    def __init__(self):
        dwg = svgwrite.Drawing()

        self.dwg = dwg

    def _color(self, color_str):
        if color_str is None:
            color_str = self.DEFAULT_COLOR

        if color_str == 'black':
            return svgwrite.rgb(0, 0, 0)
        elif color_str == 'red':
            return svgwrite.rgb(255, 0, 0)
        elif color_str == 'green':
            return svgwrite.rgb(0, 255, 0)
        else:
            raise Exception(f'Unsupported color: {color_str}!')

    def line(self, p0, p1, color=None):
        # invert y axis
        # p0 = np.array(p0)
        # p1 = np.array(p1)
        #
        # p0[1] *= -1
        # p1[1] *= -1
        # ---

        self.dwg.add(
            self.dwg.line(p0, p1, stroke=self._color(color))
        )

    def circle(self, center, diameter, color=None):
        # invert y axis
        # center = np.array(center)
        # center[1] *= -1
        # ---

        self.dwg.add(
            self.dwg.circle(
                center=center,
                r=diameter / 2,
                fill='none',
                stroke=self._color(color),
            )
        )

    def polygon_filled(self, points, color=None):
        # invert y axis
        # points = np.array(points)
        # points[:, 1] *= -1
        # ---

        self.dwg.add(
            svgwrite.shapes.Polygon(
                points=points,
                fill=self._color(color),
                stroke='none',
            )
        )

    def arc_csa(self, center, start, angle_deg, color=None):
        # invert y axis
        center = np.array(center)
        start = np.array(start)
        #
        # center[1] *= -1
        # start[1] *= -1
        # angle_deg *= -1
        # ---

        path = svgwrite.path.Path(
            d=('M', start[0], start[1]),
            fill='none',
            stroke=self._color(color),
        )

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

    def write(self, file, is_no_ext=False):
        if is_no_ext:
            file += '.svg'
        else:
            _, ext = os.path.splitext(file)
            assert ext == '.svg'

        with open(file, 'w') as outf:
            self.dwg.write(outf, pretty=True, indent=2)