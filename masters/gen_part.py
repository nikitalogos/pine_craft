import os
import argparse
from argparse import Namespace

from constants.constants import UNIT_SIZE_MM, HOLE_DIAMETER_MM, FILLET_RADIUS_MM, HOLES_NUM, HOLES_RING_RADIUS_NORM

from masters.base_master import BaseMaster
from tools.pattern_drawer import PatternDrawer
from tools.part_drawer import PartDrawer
from utils.utils import make_dir_with_user_ask
from utils.custom_arg_parser import CustomArgParser


def _ranged_type(value_type, min_value, max_value):
    """
    source: https://stackoverflow.com/questions/55324449/how-to-specify-a-minimum-or-maximum-float-value-with-argparse
    """

    def range_checker(arg: str):
        try:
            f = value_type(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f'must be a valid {value_type}')
        if f < min_value or f > max_value:
            raise argparse.ArgumentTypeError(f'must be within [{min_value}, {max_value}]')
        return f

    return range_checker


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

        # these arguments specify a pattern. They can be called multiple times
        parser.add_argument(
            '-p',
            '--pattern',
            type=str,
            default=['x:1 y:1'],
            help='String that defines units pattern. There are two ways to define pattern:\n'
                 '1. "x:2 y:3,1" - define strides per x and per y\n'
                 '2. "ooo o.. oo. o.o" - define whether to put holes in this unit or not row by row.\n'
                 '   "o" means yes, "." means no.\n'
                 '   Spaces are optional but are useful to visually split rows to not to make a mistake.',
            action='append',
        )
        parser.add_argument(
            '--first-hole-angle-deg',
            type=float,
            default=[0.0],
            help='Angle of first hole from zero in degrees (counterclockwise, zero is from the right)',
            action='append',
        )
        parser.add_argument(
            '--holes-num',
            type=int,
            default=[HOLES_NUM],
            help='Number of holes',
            action='append',
        )
        parser.add_argument(
            '--holes-ring-radius-norm',
            type=_ranged_type(float, 0.0, 2**0.5),
            default=[HOLES_RING_RADIUS_NORM],
            help='Radius of circular pattern where holes will be placed. Normalized to the "unit-size". '
                 '1.0 means half of "unit-size". Should be a float in range 0.0..1.41',
            action='append',
        )
        parser.add_argument(
            '--hole-diameter',
            type=float,
            default=[HOLE_DIAMETER_MM],
            help='Diameter of hole in mm',
            action='append',
        )

    @staticmethod
    def run(args: Namespace):
        output_name = os.path.basename(args.output)
        print(f'Generating {output_name}...')

        # prepare output directory
        make_dir_with_user_ask(args.output)

        # generate part
        shape_wh = (args.width, args.height)

        pattern_params = dict(
            pattern_str=args.pattern,
            first_hole_angle_deg=args.first_hole_angle_deg,
            holes_num=args.holes_num,
            hole_diameter=args.hole_diameter,
            holes_ring_radius_norm=args.holes_ring_radius_norm,
        )

        # if user passes at least one param - it should overwrite default param value
        for k, v in pattern_params.items():
            if len(v) > 1:
                v = v[1:]
                pattern_params[k] = v

        patterns_num = max([len(v) for v in pattern_params.values()])
        print(f'You specified {patterns_num} pattern(s)!')

        pattern_drawers = []
        for idx in range(patterns_num):
            kwargs = {
                k: v[idx] if idx < len(v) else v[-1] for k, v in pattern_params.items()
            }
            print(f'Pattern {idx + 1}: {kwargs}')

            pattern_drawer = PatternDrawer(
                shape_wh=shape_wh,
                unit_size=args.unit_size,
                **kwargs,
            )
            pattern_drawers.append(pattern_drawer)
        part_drawer = PartDrawer(
            shape_wh=shape_wh,
            unit_size=args.unit_size,
            pattern_drawers=pattern_drawers,
            fillet_radius=args.fillet_radius,
        )
        part_drawer.draw()
        part_drawer.write(f'{args.output}/{output_name}')
