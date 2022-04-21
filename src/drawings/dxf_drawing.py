import os
import numpy as np
import ezdxf

from .base_drawing import BaseDrawing


class DxfDrawing(BaseDrawing):
    def __init__(self):
        dxf = ezdxf.new()
        dxf.units = ezdxf.units.MM

        msp = dxf.modelspace()

        self.dxf = dxf
        self.msp = msp

    def _color(self, color_str):
        if color_str is None:
            color_str = self.DEFAULT_COLOR

        if color_str == 'black':
            return ezdxf.enums.ACI.BLACK
        elif color_str == 'red':
            return ezdxf.enums.ACI.RED
        elif color_str == 'green':
            return ezdxf.enums.ACI.GREEN
        else:
            raise Exception(f'Unsupported color: {color_str}!')

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
        if is_no_ext:
            subdrawing_file_no_ext = subdrawing_file
            subdrawing_file += '.dxf'
        else:
            subdrawing_file_no_ext = os.path.splitext(subdrawing_file)[0]

        subdrawing_name = subdrawing_file_no_ext.split('/')[-1]

        if subdrawing_name not in self.dxf.blocks:
            block = self.dxf.blocks.new(
                subdrawing_name
            )
            sub_dwg = ezdxf.readfile(subdrawing_file)
            sub_msp = sub_dwg.modelspace()
            for entity in sub_msp:
                block.add_foreign_entity(
                    entity,
                    copy=True,
                )

        self.msp.add_blockref(
            name=subdrawing_name,
            insert=translate_xy,
            dxfattribs={
                'rotation': rotate_deg
            }
        )

    def write(self, file, is_no_ext=False):
        if is_no_ext:
            file += '.dxf'
        else:
            _, ext = os.path.splitext(file)
            assert ext == '.dxf'

        self.dxf.saveas(file)
