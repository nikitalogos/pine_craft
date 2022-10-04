#!/bin/sh
"exec" "`dirname $0`/../venv/bin/python" "$0" "$@"

import os
import yaml
import json
import numpy as np


import os.path
from argparse import Namespace

from src.parts_placer import PartsPlacer, Part
from src.utils.utils import make_dir_with_user_ask
from masters.base_master import BaseMaster
from utils.custom_arg_parser import CustomArgParser


class PlaceParts(BaseMaster):
    @classmethod
    def make_subparser(cls, parser: CustomArgParser):
        parser.add_argument(
            '-i',
            '--input',
            type=str,
            required=True,
            help='Source file with instructions in YAML format',
        )
        parser.add_argument(
            '-o',
            '--output',
            type=str,
            required=True,
            help='Path to output directory. Results will be placed it that directory '
                 'and named after the last directory in the path',
        )
        parser.add_argument(
            '--hv_ratio',
            type=float,
            default=20.0,
            help='Ratio between vertical and horizontal alignment of parts',
        )

    @staticmethod
    def run(args: Namespace):
        output_name = os.path.basename(args.output)
        print(f'Generating {output_name}...')

        # validate input
        with open(args.input, 'r') as inf:
            data = yaml.safe_load(inf)

        parts = None
        work_area_wh = None
        unit_size = None
        try:
            work_area_wh_mm = np.array([
                data['work_area']['width_mm'],
                data['work_area']['height_mm'],
            ])

            parts = []
            unit_sizes = []
            for part in data['parts']:
                part_dir = part['path']
                part_name = part_dir.split('/')[-1]

                if not os.path.isabs(part_dir):
                    config_file_dir = os.path.dirname(args.input)
                    part_dir = os.path.join(
                        config_file_dir,
                        part_dir
                    )
                part_path = f'{part_dir}/{part_name}.json'

                with open(part_path, 'r') as inf:
                    part_meta = json.load(inf)

                parts.append(
                    Part(
                        name=part_name,
                        path_no_ext=os.path.splitext(part_path)[0],
                        shape_wh=part_meta['shape_wh'],
                        number=part['number'],
                    )
                )
                unit_sizes.append(part_meta['unit_size'])

            assert len(np.unique(np.array(unit_sizes))) == 1, \
                'Placing together parts with different unit sizes is not supported!'

            unit_size = unit_sizes[0]
            work_area_wh = (work_area_wh_mm // unit_size).astype(int).tolist()
        except Exception as e:
            print('Error while processing config file:', e)
            exit(1)

        # prepare output directory
        make_dir_with_user_ask(args.output)

        # place parts
        placer = PartsPlacer(
            parts=parts,
            work_area_wh=work_area_wh,
            unit_size=unit_size,
            h_to_v_coef_ratio=args.hv_ratio,
        )
        placer.place()
        placer.draw()
        placer.write(file_no_ext=f'{args.output}/{output_name}')
