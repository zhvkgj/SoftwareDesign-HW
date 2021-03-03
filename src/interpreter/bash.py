from typing import IO

from src.commands.basic_commands import *
from src.interpreter.base_interpreter import BaseInterpreter


class BashInterpreter(BaseInterpreter):
    _registered_commands = [
        EchoCommand,
        CatCommand,
        PwdCommand,
        WcCommand,
        GrepCommand
    ]

    def __init__(self, inp: IO, out: IO, err: IO):
        super().__init__(inp, out, err)

        for cmd in BashInterpreter._registered_commands:
            self.register_cmd(cmd())
