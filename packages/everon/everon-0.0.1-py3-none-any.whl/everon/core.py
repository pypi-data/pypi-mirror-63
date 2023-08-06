import argparse
import sys

import colorama


class MixinFontColor:
    def __init__(self):
        colorama.init(autoreset=True)
        self.color = colorama.Fore

    def print_ok(self, content):
        print(self.color.GREEN + '[+] ' + str(content))

    def print_err(self, content):
        print(self.color.RED + '[-] ' + str(content))

    def text_as_link(self, content):
        return self.color.LIGHTBLUE_EX + content


class StoreDictKeyPair(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        bf = {}
        for kv in values.split(","):
            k, v = kv.split("=")
            bf[k] = v
        setattr(namespace, self.dest, bf)


class BaseCommand:
    help = ''

    def create_parser(self, prog_name):
        parser = argparse.ArgumentParser(
            prog=prog_name,
            description=self.help or None
        )
        self.add_args(parser)
        return parser

    def add_args(self, parser):
        pass

    def handle(self, *args, **kwargs):
        raise NotImplementedError('Subclasses of BaseCommand must provide a handle() method')

    def run(self):
        parser = self.create_parser(sys.argv[0])
        options = parser.parse_args(sys.argv[1:])
        kwargs = vars(options)
        args = kwargs.pop('args', ())
        self.handle(*args, **kwargs)
