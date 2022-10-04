import os.path
from argparse import Namespace

from drawings.dxf_drawing import DxfDrawing
from masters.base_master import BaseMaster
from utils.custom_arg_parser import CustomArgParser


class CutLength(BaseMaster):
    @classmethod
    def make_subparser(cls, parser: CustomArgParser):
        parser.add_argument(
            '-i',
            '--input',
            type=str,
            required=True,
            help='Input file in DXF format',
        )

    @staticmethod
    def run(args: Namespace):
        path = args.input

        extension = os.path.splitext(path)[-1]
        if extension.lower() != '.dxf':
            print("Only .dxf files are supported!")
            exit(1)

        dwg = DxfDrawing(file_path=path)
        len_m = dwg.get_total_lines_length_mm() / 1000
        print(f'Cut length = {len_m:.3f} m')

