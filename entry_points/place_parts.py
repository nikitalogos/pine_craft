#!/bin/sh
"exec" "`dirname $0`/../venv/bin/python" "$0" "$@"

import os
import yaml
import json
import numpy as np

import sys
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)
from src.parts_placer import PartsPlacer, Part
from src.utils.my_parser import MyParser
from src.utils.utils import make_dir_with_user_ask


if __name__ =='__main__':
    parser = MyParser(description='Parts placer. Arranges parts in efficient way for manufacturing on CNC.')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        required=True,
        help='Config file in yaml format',
    )
    parser.add_argument(
        '-n',
        '--name',
        type=str,
        required=True,
        help='Parts layout name',
    )
    parser.add_argument(
        '-d',
        '--directory',
        type=str,
        default='.',
        help='Output directory',
    )

    args = parser.parse_args()
    print(f'Generating {args.name}...')

    # validate input
    with open(args.config, 'r') as inf:
        data = yaml.safe_load(inf)

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
                config_file_dir = os.path.dirname(args.config)
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
        work_area_wh = (work_area_wh_mm // unit_size).astype(int)
    except Exception as e:
        print('Error while processing config file:', e)
        exit(1)

    # prepare output directory
    base_dir = args.directory
    if base_dir == '.':
        base_dir = os.getcwd()

    part_dir = f'{base_dir}/{args.name}'
    make_dir_with_user_ask(part_dir)

    # place parts
    placer = PartsPlacer(parts, work_area_wh, unit_size)
    placed_parts = placer.place()
    placer.draw(placed_parts)
    placer.write(f'{part_dir}/{args.name}.dxf')
