import os
from typing import List, IO

from src.commands.command_api import IBasicCommand
from src.enviroment.enviroment import Environment


class BasicCmdNames:
    Echo = 'echo'
    Cat = 'cat'
    Pwd = 'pwd'
    Wc = 'wc'


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

    def run(self, args: List[str], inp: IO, out: IO, err: IO, env: Environment) -> int:
        if len(args) == 0:
            self._count(inp, out)
        elif len(args) == 1:
            path = args[0]
            with open(path, 'r') as f:
                self._count(f, out)
        return 0
