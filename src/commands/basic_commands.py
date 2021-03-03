import argparse
import os
from typing import Match, Optional

from termcolor import colored
from src.commands.command_api import IBasicCommand
import re


class BasicCmdNames:
    Echo = 'echo'
    Cat = 'cat'
    Pwd = 'pwd'
    Wc = 'wc'
    Grep = 'grep'


class EchoCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BasicCmdNames.Echo

    def run(self, args, inp, out, err, env) -> int:
        print(' '.join(args), file=out)
        return 0


class CatCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BasicCmdNames.Cat

    def run(self, args, inp, out, err, env) -> int:
        if len(args) == 0:
            s = inp.read()
            print(s, file=out, end='')
        elif len(args) == 1:
            path = args[0]
            with open(path, 'r') as f:
                print(f.read(), file=out, end='')
        else:
            err.write(f'Cat command expected 0 or 1 arguments, '
                      f'but given {len(args)}.')
        return 0


class PwdCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BasicCmdNames.Pwd

    def run(self, args, inp, out, err, env) -> int:
        cwd = os.getcwd()
        print(cwd, file=out)
        return 0


class WcCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BasicCmdNames.Wc

    @staticmethod
    def _count(inp, out):
        n_lines, n_words, n_bytes = 0, 0, 0
        for line in inp:
            n_lines += line.count("\n")
            n_words += len(line.split())
            n_bytes += len(str.encode(line))

        print(f'{n_lines} {n_words} {n_bytes}', file=out)

    def run(self, args, inp, out, err, env) -> int:
        if len(args) == 0:
            self._count(inp, out)
        elif len(args) == 1:
            path = args[0]
            with open(path, 'r') as f:
                self._count(f, out)
        return 0


class GrepCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BasicCmdNames.Grep

    @staticmethod
    def get_args_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', required=False, action='store_true')
        parser.add_argument('-w', required=False, action='store_true')
        parser.add_argument('-A', required=False, default=0, type=int)
        parser.add_argument('pattern')
        return parser

    @staticmethod
    def _grep_line(s: str, sub: str,
                   ignore_case=False, whole_word=False) -> Optional[str]:
        pattern = sub
        params = {}
        if whole_word:
            pattern = r'\b' + pattern + r'\b'
        if ignore_case:
            params = {
                'flags': re.IGNORECASE
            }

        if not re.search(pattern, s, **params):
            return None

        def replace(x: Match[str]) -> str:
            s = x.group(0)
            return colored(s, color='red')

        return re.sub(pattern, replace, s, **params)

    def run(self, args, inp, out, err, env) -> int:
        parser = GrepCommand.get_args_parser()
        namespace = parser.parse_args(args)

        window = namespace.A
        pattern = namespace.pattern
        ignore_case = namespace.i
        whole_word = namespace.w

        last = -1
        for i, line in enumerate(inp):
            s = GrepCommand._grep_line(line, pattern, ignore_case, whole_word)
            if s:
                if last != -1 and window > 0 and i > last:
                    print(colored('--', 'blue'), file=out)
                last = i + window
            else:
                s = line
            if i <= last:
                print(s, file=out, end='')
        return 0


# print(GrepCommand._grep_line('I can color it', 'color', whole_word=False, ignore_case=True))
