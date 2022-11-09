#!/bin/sh
# PYTHON_ARGCOMPLETE_OK


import argcomplete
from typing import NamedTuple

from masters.base_master import BaseMaster
from masters.cut_length import CutLength
from masters.gen_box import GenBox
from masters.gen_part import GenPart
from masters.place_parts import PlaceParts

from utils.custom_arg_parser import CustomArgParser


class Master(NamedTuple):
    master: BaseMaster = None
    name: str = None
    description: str = ''


MASTERS = [
    Master(CutLength(), 'cut-length', 'Compute total curves length in a file'),
    Master(GenBox(), 'gen-box', 'Generate box parts A and B'),
    Master(GenPart(), 'gen-part', 'Part generator'),
    Master(PlaceParts(), 'place-parts', 'Parts placer. Arranges parts in efficient way for manufacturing on CNC.'),
]


if __name__ == '__main__':
    parser = CustomArgParser(description='Pine Craft SW library')
    subparsers = parser.add_subparsers(dest="master")

    for master in MASTERS:
        subparser = subparsers.add_parser(master.name, description=master.description)
        master.master.make_subparser(subparser)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    for master in MASTERS:
        if master.name == args.master:
            master.master.run(args)
            exit(0)

    print(parser.format_help())
    exit(1)
