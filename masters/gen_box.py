import numpy as np
import os
import yaml
from argparse import Namespace

from drawings.base_drawing import BaseDrawing
from drawings.svg_drawing import SvgDrawing
from drawings.dxf_drawing import DxfDrawing
from masters.base_master import BaseMaster
from utils.custom_arg_parser import CustomArgParser
from constants.constants import UNIT_SIZE_MM, HOLE_DIAMETER_MM, MATERIAL_THICKNESS_MM


class GenBox(BaseMaster):
    def __init__(self):
        self.output: str = None
        self.unit_size: float = None
        self.hole_diameter: float = None
        self.material_thickness: float = None

    @classmethod
    def make_subparser(cls, parser: CustomArgParser):
        parser.add_argument(
            '-o',
            '--output',
            type=str,
            default='.',
            help='Path to output directory. Results will be placed in subdirectories of this directory',
        )

        parser.add_argument(
            '--unit-size',
            type=float,
            default=UNIT_SIZE_MM,
            help='Unit size in mm',
        )
        parser.add_argument(
            '--hole-diameter',
            type=float,
            default=HOLE_DIAMETER_MM,
            help='Diameter of hole in mm',
        )
        parser.add_argument(
            '--material-thickness',
            type=float,
            default=MATERIAL_THICKNESS_MM,
            help='Thickness of the material in mm',
        )

    def _make_holes(self, drawing: BaseDrawing):
        """Draw screw holes"""
        circles = [
            [
                self.unit_size * 0.5,
                self.unit_size * 0.25
            ],
            [
                self.unit_size * 0.5,
                self.unit_size * 0.75
            ],
        ]
        for circle in circles:
            drawing.circle(
                center=circle,
                diameter=self.hole_diameter,
                color='red',
            )

    @staticmethod
    def _make_symmetric_shape(drawing: BaseDrawing, path_rel_to_center: np.ndarray):
        """Given a path in the I-st quadrant, will mirror it horizontally and vertically and then draw"""
        for x_mirr in [-1, 1]:
            for y_mirr in [-1, 1]:
                for i in range(len(path_rel_to_center) - 1):
                    line = path_rel_to_center[i:i + 2].copy()

                    line[:, 0] *= x_mirr
                    line[:, 1] *= y_mirr
                    line += 15

                    drawing.line(
                        p0=line[0].tolist(),
                        p1=line[1].tolist()
                    )

    def _part_a(self, drawing: BaseDrawing):
        u50 = self.unit_size * 0.5
        u25 = self.unit_size * 0.25
        m = self.material_thickness
        path = np.array([
            [u50, 0],
            [u50, u50 - m],
            [u25, u50 - m],
            [u25, u50],
            [0, u50]
        ])
        self._make_symmetric_shape(
            drawing=drawing,
            path_rel_to_center=path
        )
        self._make_holes(drawing)

    def _part_b(self, drawing: BaseDrawing):
        u50 = self.unit_size * 0.5
        u25 = self.unit_size * 0.25
        m = self.material_thickness
        path = np.array([
            [u50 - m, 0],
            [u50 - m, u25],
            [u50, u25],
            [u50, u50],
            [0, u50]
        ])
        self._make_symmetric_shape(
            drawing=drawing,
            path_rel_to_center=path
        )
        self._make_holes(drawing)

        # polygon
        h50 = self.hole_diameter * 0.5
        points = np.array([
            [u50 - m, h50],
            [u50 - m, -h50],
            [m - u50, -h50],
            [m - u50, h50],
        ])
        points += u50
        drawing.polygon_filled(
            points=points.tolist(),
            color='green',
        )

    def _part(self, is_part_a: bool):
        drawings = [
            SvgDrawing(),
            DxfDrawing()
        ]
        extensions = [
            '.svg',
            '.dxf'
        ]
        for idx, zipped in enumerate(zip(drawings, extensions)):
            drawing, extension = zipped
            if is_part_a:
                self._part_a(drawing)
            else:
                self._part_b(drawing)

            name = f'box_part_{"a" if is_part_a else "b"}'
            base_dir = f'{self.output}/{name}'
            os.makedirs(base_dir, exist_ok=True)
            drawing.write(f'{base_dir}/{name}{extension}')

            # write metadata
            if idx == 0:
                data = {
                    "shape_wh": [
                        1, 1
                    ],
                    "unit_size": self.unit_size,
                }
                with open(f'{base_dir}/{name}.yaml', 'w') as outf:
                    yaml.safe_dump(data, outf)

    def run(self, args: Namespace):
        print('Generating box parts...')

        self.output = args.output
        self.unit_size = args.unit_size
        self.hole_diameter = args.hole_diameter
        self.material_thickness = args.material_thickness

        self._part(is_part_a=True)
        self._part(is_part_a=False)
