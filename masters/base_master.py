from argparse import Namespace
from utils.custom_arg_parser import CustomArgParser


class BaseMaster:
    @staticmethod
    def make_subparser(parser: CustomArgParser):
        pass

    @staticmethod
    def run(args: Namespace):
        pass
