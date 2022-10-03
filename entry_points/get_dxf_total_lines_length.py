#!/bin/sh
"exec" "`dirname $0`/../venv/bin/python" "$0" "$@"

import os

import sys
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)
from src.drawings.dxf_drawing import DxfDrawing
from src.utils.my_parser import MyParser


if __name__ =='__main__':
    parser = MyParser(description='Compute all lines length from dxf file')
    parser.add_argument(
        'file',
        type=str,
        help='input file',
    )

    args = parser.parse_args()

    dwg = DxfDrawing(file_name=args.file)
    len_m = dwg.get_total_lines_length_mm() / 1000
    print(f'Total lines length: {len_m:.3f} m', )

