import os
import numpy as np
import ezdxf
import math
from typing import NamedTuple

from .base_drawing import BaseDrawing


class DxfDrawing(BaseDrawing):
    EPSILON = 1e-5

    def __init__(self, file_path=None):
        if file_path is None:
            dxf = ezdxf.new()
            dxf.units = ezdxf.units.MM
        else:
            dxf = ezdxf.readfile(file_path)

        msp = dxf.modelspace()

        self.dxf = dxf
        self.msp = msp

    def _color(self, color: str or int):
        if type(color) == int:
            return color

        if color is None:
            color = self.DEFAULT_COLOR

        if color == 'black':
            return ezdxf.enums.ACI.BLACK
        elif color == 'red':
            return ezdxf.enums.ACI.RED
        elif color == 'green':
            return ezdxf.enums.ACI.GREEN
        else:
            raise Exception(f'Unsupported color: {color}!')

    def line(self, p0, p1, color=None):
        self.msp.add_line(
            p0,
            p1,
            dxfattribs={
                "color": self._color(color)
            }
        )

    def circle(self, center, diameter, color=None):
        self.msp.add_circle(
            center=center,
            radius=diameter / 2,
            dxfattribs={
                "color": self._color(color)
            }
        )

    def polygon_filled(self, points, color=None):
        hatch = self.msp.add_hatch(
            color=self._color(color)
        )
        hatch.paths.add_polyline_path(
            points,
            is_closed=True
        )

    def arc_csa(self, center, start, angle_deg, color=None):
        center = np.array(center)
        start = np.array(start)
        start_vector = start - center

        x, y = start_vector
        start_angle = np.rad2deg(np.arctan2(y, x))

        radius = np.linalg.norm(start_vector)

        end_angle = start_angle + angle_deg

        self.msp.add_arc(
            center=center,
            radius=radius,
            start_angle=start_angle,
            end_angle=end_angle,
            is_counter_clockwise=(angle_deg > 0),
            dxfattribs={
                "color": self._color(color)
            }
        )

    def subdrawing(self, subdrawing_file, translate_xy, rotate_deg, is_no_ext=False):
        """Attention: not all elements are supported.
        Supported elements: LINE, CIRCLE, ARC, SPLINE."""

        if is_no_ext:
            subdrawing_file += '.dxf'
        sub_dwg = DxfDrawing(file_path=subdrawing_file)

        fi = np.deg2rad(rotate_deg)
        rot_matrix = np.array([
            [np.cos(fi), -np.sin(fi)],
            [np.sin(fi), np.cos(fi)],
        ])

        def transform_point(p):
            p = (p[0], p[1])
            p = np.matmul(rot_matrix, p) + translate_xy
            return p

        for e in sub_dwg.msp:
            dxf_type = e.dxftype()
            if dxf_type == 'LINE':
                p0 = transform_point(e.dxf.start)
                p1 = transform_point(e.dxf.end)
                self.line(p0, p1, color=e.dxf.color)
            elif dxf_type == 'CIRCLE':
                center = transform_point(e.dxf.center)
                diameter = e.dxf.radius * 2
                self.circle(center, diameter, color=e.dxf.color)
            elif dxf_type == 'ARC':
                center = transform_point(e.dxf.center)
                self.msp.add_arc(
                    center=center,
                    radius=e.dxf.radius,
                    start_angle=e.dxf.start_angle + rotate_deg,
                    end_angle=e.dxf.end_angle + rotate_deg,
                    dxfattribs={'color': e.dxf.color}
                )
            elif dxf_type == 'HATCH':
                points = e.paths.paths[0].vertices
                points_t = []
                for point in points:
                    points_t.append(transform_point(point))
                self.polygon_filled(points_t, color=e.dxf.color)
            else:
                raise Exception(f'Unsupported element type: {dxf_type}')

    def deduplicate(self):
        class Line(NamedTuple):
            x0: float
            y0: float
            x1: float
            y1: float

        vlines = []
        hlines = []

        for e in self.msp:
            dxf_type = e.dxftype()
            if dxf_type != 'LINE':
                continue

            line = Line(
                x0=e.dxf.start[0],
                y0=e.dxf.start[1],
                x1=e.dxf.end[0],
                y1=e.dxf.end[1],
            )
            if abs(line.x0 - line.x1) < self.EPSILON:
                vlines.append(line)
                e.destroy()
            if abs(line.y0 - line.y1) < self.EPSILON:
                hlines.append(line)
                e.destroy()
        self.msp.purge()

        def get_non_empty_groups_with_same_value(lines, idx):
            lines.sort(key=lambda line: line[idx])
            batch = []
            value = lines[0][idx]
            for line in lines:
                if abs(line[idx] - value) > self.EPSILON:
                    if len(batch) > 0:  # this case is redundant, but still
                        yield batch
                    batch = []

                value = line[idx]
                batch.append(line)
            if len(batch) > 0:
                yield batch

        def draw_lines(batch, is_vlines):
            class Point(NamedTuple):
                value: float
                is_min: bool

            x0 = batch[0].x0
            y0 = batch[0].y0

            points = []
            for line in batch:
                if is_vlines:
                    p_min = min(line.y0, line.y1)
                    p_max = max(line.y0, line.y1)
                else:
                    p_min = min(line.x0, line.x1)
                    p_max = max(line.x0, line.x1)
                points.append(Point(value=p_min, is_min=True))
                points.append(Point(value=p_max, is_min=False))
            points.sort(key=lambda point: point.value)

            counter = 0
            for i in range(len(points) - 1):
                point = points[i]
                point2 = points[i + 1]

                counter += 1 if point.is_min else -1

                if abs(point.value - point2.value) < self.EPSILON:
                    continue

                if counter > 0:
                    if is_vlines:
                        p0 = (x0, point.value)
                        p1 = (x0, point2.value)
                    else:
                        p0 = (point.value, y0)
                        p1 = (point2.value, y0)
                    self.line(p0, p1)

        x0_idx = 0
        for batch in get_non_empty_groups_with_same_value(vlines, x0_idx):
            draw_lines(batch, is_vlines=True)
        y0_idx = 1
        for batch in get_non_empty_groups_with_same_value(hlines, y0_idx):
            draw_lines(batch, is_vlines=False)

    def write(self, file, is_no_ext=False):
        if is_no_ext:
            file += '.dxf'
        else:
            _, ext = os.path.splitext(file)
            assert ext == '.dxf'

        self.dxf.saveas(file)

    def get_total_lines_length_mm(self, layout=None) -> float:
        """Attention: not all elements are supported.
        Supported elements: INSERT, LINE, CIRCLE, ARC, SPLINE."""

        if layout is None:
            layout = self.msp

        total_length_mm = 0
        for e in layout:
            dxf_type = e.dxftype()

            if dxf_type == 'INSERT':
                block_name = e.dxf.name
                block = self.dxf.blocks[block_name]
                length = self.get_total_lines_length_mm(layout=block)
            elif dxf_type == 'LINE':
                length = (
                    (e.dxf.start[0] - e.dxf.end[0]) ** 2 +
                    (e.dxf.start[1] - e.dxf.end[1]) ** 2
                ) ** 0.5
            elif dxf_type == 'CIRCLE':
                length = 2. * math.pi * e.dxf.radius
            elif dxf_type == 'ARC':
                total_angle = e.dxf.end_angle - e.dxf.start_angle
                assert total_angle >= 0, 'This should never happen...'
                length = np.deg2rad(total_angle) * e.dxf.radius
            elif dxf_type == 'HATCH':
                pass  # we do not take polygons into account, because they are meant to be engraved, not cut
            # elif e.dxftype() == 'SPLINE':
            #     points = e._control_points
            #     length = 0
            #     for i in range(len(points) - 1):
            #         length += (
            #             (points[i][0] - points[i + 1][0]) ** 2 +
            #             (points[i][1] - points[i + 1][1]) ** 2
            #         ) ** 0.5
            else:
                raise Exception(f'Unsupported element type: {dxf_type}')

            total_length_mm += length

        return float(total_length_mm)
