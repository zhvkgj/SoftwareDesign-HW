import io
from typing import List, IO

from src.commands.icommand import Command, ExitCode


class PipeAggregation(Command):
    def __init__(self, cmd_1: Command, args_1: List[str],
                 cmd_2: Command, args_2: List[str]):
        self.cmd_1 = cmd_1
        self.cmd_2 = cmd_2
        self.args_1 = args_1
        self.args_2 = args_2

    def run(self, args: List[str], inp: IO, out: IO, err: IO) -> ExitCode:
        if len(args) != 0:
            raise RuntimeError("PipeAggregation expected 0 arguments")

        out_cmd_1 = io.StringIO()
        ret = self.cmd_1.run(self.args_1, inp, out_cmd_1, err)

        if ret == ExitCode.FAIL:
            return ExitCode.FAIL

        inp_cmd_2 = io.StringIO(out_cmd_1.getvalue())
        return self.cmd_2.run(self.args_2, inp_cmd_2, out, err)

