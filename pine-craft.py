#!/bin/sh
"exec" "`dirname $0`/venv/bin/python" "$0" "$@"
# PYTHON_ARGCOMPLETE_OK


import argcomplete
from typing import NamedTuple

from masters.base_master import BaseMaster
from masters.gen_part import GenPart
from masters.cut_length import CutLength
from masters.gen_box import GenBox

from utils.custom_arg_parser import CustomArgParser


class Master(NamedTuple):
    master: BaseMaster = None
    name: str = None
    description: str = ''


MASTERS = [
    Master(GenPart(), 'gen-part', 'Part generator'),
    Master(GenBox(), 'gen-box', 'Generate box parts A and B'),
    Master(CutLength(), 'cut-length', 'Compute total curves length in a file')
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
