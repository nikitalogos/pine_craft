import argparse


class CustomArgParser(argparse.ArgumentParser):
    def add_argument(self, *args, **kwargs):
        if '-h' not in args:
            is_required = kwargs.get('required', False)
            default = kwargs.get('default', None)
            help = kwargs.get('help', '')

            default_str = ''
            if default is not None:
                default_str = f", default: {default}"

            help += f' ({"required" if is_required else "optional"}{default_str})'
            kwargs['help'] = help

        super().add_argument(*args, **kwargs)