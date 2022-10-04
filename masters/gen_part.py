import os
from argparse import Namespace

from constants.constants import UNIT_SIZE_MM, HOLE_DIAMETER_MM, FILLET_RADIUS_MM, HOLES_NUM

from masters.base_master import BaseMaster
from tools.pattern_drawer import PatternDrawer
from tools.part_drawer import PartDrawer
from utils.utils import make_dir_with_user_ask
from utils.custom_arg_parser import CustomArgParser


class GenPart(BaseMaster):
    @classmethod
    def make_subparser(cls, parser: CustomArgParser):
        parser.add_argument(
            '-o',
            '--output',
            type=str,
            required=True,
            help='Path to output directory. Results will be placed it that directory '
                 'and named after the last directory in the path',
        )

        parser.add_argument(
            '-w',
            '--width',
            type=int,
            required=True,
            help='Part width in units',
        )
        parser.add_argument(
            '-t',
            '--height',
            type=int,
            required=True,
            help='Part height in units',
        )
        parser.add_argument(
            '-p',
            '--pattern',
            type=str,
            default='x:1 y:1',
            help='String that defines units pattern',
        )

        parser.add_argument(
            '--unit-size',
            type=float,
            default=UNIT_SIZE_MM,
            help='Unit size in mm',
        )
        parser.add_argument(
            '--fillet-radius',
            type=float,
            default=FILLET_RADIUS_MM,
            help='Radius of fillet on corners in mm',
        )
        parser.add_argument(
            '--first-hole-angle-deg',
            type=float,
            default=0.0,
            help='Angle of first hole from zero in degrees (counterclockwise, zero is from the right)',
        )
        parser.add_argument(
            '--holes-num',
            type=int,
            default=HOLES_NUM,
            help='Number of holes in mm',
        )
        parser.add_argument(
            '--hole-diameter',
            type=float,
            default=HOLE_DIAMETER_MM,
            help='Diameter of hole in mm',
        )

    @staticmethod
    def run(args: Namespace):
        output_name = os.path.basename(args.output)
        print(f'Generating {output_name}...')

        # prepare output directory
        make_dir_with_user_ask(args.output)

        # generate part
        shape_wh = (args.width, args.height)

        pattern_drawer = PatternDrawer(
            pattern_str=args.pattern,
            shape_wh=shape_wh,
            unit_size=args.unit_size,
            first_hole_angle_deg=args.first_hole_angle_deg,
            holes_num=args.holes_num,
            hole_diameter=args.hole_diameter
        )
        part_drawer = PartDrawer(
            shape_wh=shape_wh,
            unit_size=args.unit_size,
            pattern_drawer=pattern_drawer,
            fillet_radius=args.fillet_radius,
        )
        part_drawer.draw()
        part_drawer.write(f'{args.output}/{output_name}')
