#!/bin/sh
"exec" "`dirname $0`/../venv/bin/python" "$0" "$@"

import numpy as np
import os

import sys
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)
from src.drawings.svg_drawing import SvgDrawing
from src.drawings.dxf_drawing import DxfDrawing


def make_holes(d):
    d.circle(
        center=(15, 1 / 4 * 30),
        diameter=4,
        color='red',
    )
    d.circle(
        center=(15, 3 / 4 * 30),
        diameter=4,
        color='red',
    )


def make_symmetric_shape(d, path_rel_to_center):
    for x_mirr in [-1, 1]:
        for y_mirr in [-1, 1]:
            for i in range(len(path_rel_to_center) - 1):
                line = path_rel_to_center[i:i + 2].copy()

                line[:, 0] *= x_mirr
                line[:, 1] *= y_mirr
                line += 15

                d.line(
                    p0=line[0].tolist(),
                    p1=line[1].tolist()
                )


def part_a(d):
    # ~~~lines~~~
    make_symmetric_shape(
        d=d,
        path_rel_to_center=np.array([
            [15, 0],
            [15, 15 - 6],
            [15 - 8, 15 - 6],
            [15 - 8, 15],
            [0, 15]
        ])
    )

    # ~~~holes~~~
    make_holes(d)


def part_b(d):
    # ~~~lines~~~
    make_symmetric_shape(
        d=d,
        path_rel_to_center=np.array([
            [9, 0],
            [9, 7],
            [15, 7],
            [15, 15],
            [0, 15]
        ])
    )

    # ~~~holes~~~
    make_holes(d)

    # polygon
    points = np.array([
        [9, 2],
        [9, -2],
        [-9, -2],
        [-9, 2],
    ])
    points += 15
    d.polygon_filled(
        points=points.tolist(),
        color='green',
    )


def part(is_part_a: bool):
    drawings = [
        SvgDrawing(),
        DxfDrawing()
    ]
    extensions = [
        '.svg',
        '.dxf'
    ]
    for d, ext in zip(drawings, extensions):
        if is_part_a:
            part_a(d)
        else:
            part_b(d)

        name = f'box_part_{"a" if is_part_a else "b"}'
        os.makedirs(name, exist_ok=True)
        d.write(f'{name}/{name}{ext}')


if __name__ =='__main__':
    part(is_part_a=True)
    part(is_part_a=False)
