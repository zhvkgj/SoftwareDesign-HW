from abc import abstractmethod
from typing import List, IO

from src.commands.icommand import Command, ExitCode


class BasicCommand(Command):
    @staticmethod
    @abstractmethod
    def get_name():
        pass


class EchoCommand(BasicCommand):
    @staticmethod
    def get_name() -> str:
        return 'echo'

    def run(self, args: List[str], inp: IO, out: IO, err: IO) -> ExitCode:
        out.write(' '.join(args))
        return ExitCode.OK


class CatCommand(BasicCommand):
    @staticmethod
    def get_name() -> str:
        return 'cat'

    def run(self, args: List[str], inp: IO, out: IO, err: IO) -> ExitCode:
        if len(args) == 0:
            s = inp.read()
            out.write(s)
        elif len(args) == 1:
            path = args[0]
            with open(path, 'r') as f:
                out.write(f.read())
        else:
            err.write(f'Cat command expected 0 or 1 arguments, '
                      f'but given {len(args)}.')
        return ExitCode.OK
