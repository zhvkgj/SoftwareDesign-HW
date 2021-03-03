import io
import sys
from typing import List

from src.commands.command_api import IBasicCommand
from src.commands.command_api import ICommand
from src.enviroment.enviroment import Environment
from src.exceptions.exceptions import ExitInterpreter
import subprocess


class BuiltInCmdNames:
    SetVar = 'SetVar'
    ListVars = 'printenv'
    Exit = 'exit'


class SetVarCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BuiltInCmdNames.SetVar

    def run(self, args, inp, out, err, env) -> int:
        name, value = args
        env.vars[name] = value
        return 0


class ListVarsCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BuiltInCmdNames.ListVars

    def run(self, args, inp, out, err, env) -> int:
        print('\n'.join([f'{k}={v}' for k, v in env.vars.items()]),
              file=out)
        return 0


class ExitCommand(IBasicCommand):
    @staticmethod
    def get_name() -> str:
        return BuiltInCmdNames.Exit

    def run(self, args, inp, out, err, env) -> int:
        raise ExitInterpreter('By-by!')


class PipeAggregationCommand(ICommand):
    def __init__(self, cmd_1: ICommand, args_1: List[str],
                 cmd_2: ICommand, args_2: List[str]):
        self.cmd_1 = cmd_1
        self.cmd_2 = cmd_2
        self.args_1 = args_1
        self.args_2 = args_2

    def run(self, args, inp, out, err, env):
        if len(args) != 0:
            raise RuntimeError('PipeAggregation expected 0 arguments')

        out_cmd_1 = io.StringIO()
        ret = self.cmd_1.run(self.args_1, inp, out_cmd_1, err, env)

        if ret != 0:
            return ret

        inp_cmd_2 = io.StringIO(out_cmd_1.getvalue())
        return self.cmd_2.run(self.args_2, inp_cmd_2, out, err, env)


class ExternalCommand(ICommand):
    def run(self, args, inp, out, err, env) -> int:
        proc = subprocess.Popen(args,
                                stdin=inp,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf8')

        s_out, s_err = proc.communicate()
        out.write(s_out)
        err.write(s_err)


# x = ExternalCommand()
#
# inp = io.StringIO("csdcscdcs")
# x.run(['echo', '134'], inp, sys.stdout, sys.stderr, Environment())

# print(xs.getvalue())

from contextlib import redirect_stdout

