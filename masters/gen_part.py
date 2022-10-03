import os
from argparse import Namespace

from src.pattern_drawer import PatternDrawer
from src.part_drawer import PartDrawer
from src.utils.utils import make_dir_with_user_ask
from masters.base_master import BaseMaster
from utils.custom_arg_parser import CustomArgParser


class GenPart(BaseMaster):
    @classmethod
    def make_subparser(cls, parser: CustomArgParser):
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
            '--unit_size',
            type=float,
            default=30.0,
            help='Unit size in mm',
        )
        parser.add_argument(
            '--fillet_radius',
            type=float,
            default=5.0,
            help='Radius of fillet on corners in mm',
        )
        parser.add_argument(
            '--first_hole_angle_deg',
            type=float,
            default=0.0,
            help='Angle of first hole from zero in degrees (counterclockwise, zero is from the right)',
        )
        parser.add_argument(
            '--holes_num',
            type=int,
            default=4,
            help='Number of holes in mm',
        )
        parser.add_argument(
            '--hole_diameter',
            type=float,
            default=4.0,
            help='Diameter of hole in mm',
        )

        parser.add_argument(
            '-n',
            '--name',
            type=str,
            required=True,
            help='Part name',
        )
        parser.add_argument(
            '-d',
            '--directory',
            type=str,
            default='.',
            help='Output directory',
        )

    @staticmethod
    def run(args: Namespace):
        print(f'Generating {args.name}...')

        # prepare output directory
        base_dir = args.directory
        if base_dir == '.':
            base_dir = os.getcwd()

        part_dir = f'{base_dir}/{args.name}'
        make_dir_with_user_ask(part_dir)

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
        part_drawer.write(f'{part_dir}/{args.name}')
