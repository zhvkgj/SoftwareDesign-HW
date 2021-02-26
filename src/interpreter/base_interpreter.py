from functools import reduce
from typing import Dict, IO

from src.commands.builtin_commands import *
from src.commands.command_api import ICommand
from src.enviroment.enviroment import Environment
from src.expander.expander import Expander
from src.exeptions.exeptions import CommandNotRegistered
from src.lexer.lexer import Lexer
from src.parser.parser_api import CommandInfo
from src.parser.simple_parser import SimpleParser
from src.commands.basic_commands import IBasicCommand


class BaseInterpreter:
    _registered_cmds = [
        SetVarCommand,
        ListVarsCommand,
        ExitCommand
    ]

    def __init__(self, inp: IO, out: IO, err: IO):
        self.inp = inp
        self.out = out
        self.err = err

        self._cmds: Dict[str, IBasicCommand] = {
            cmd.get_name(): cmd()
            for cmd in BaseInterpreter._registered_cmds
        }
        self._env = Environment()

    def register_cmd(self, cmd: IBasicCommand):
        name = cmd.get_name()
        self._cmds[name] = cmd

    def _run_cmd(self, cmd: ICommand, args: List[str]) -> int:
        return cmd.run(args, self.inp, self.out, self.err, self._env)

    def _get_cmd(self, name: str) -> IBasicCommand:
        if name not in self._cmds:
            raise CommandNotRegistered(f'Command {name} not registered')
        return self._cmds[name]

    def _make_pipe(self, acc: PipeAggregationCommand, cmd_info: CommandInfo[str]):
        cmd = self._get_cmd(cmd_info.name)
        return PipeAggregationCommand(acc, [], cmd, cmd_info.args)

    def execute_cmd_line(self, cmd_line: str) -> int:
        tokens = Lexer.split(cmd_line)
        pipe_token_info = SimpleParser.parse(tokens)
        pipe_str_info = Expander.substitute_pipe(pipe_token_info, self._env.vars)
        cmd_infos = pipe_str_info.utils

        if len(cmd_infos) > 1:
            ini = PipeAggregationCommand(
                    self._get_cmd(cmd_infos[0].name),
                    cmd_infos[0].args,
                    self._get_cmd(cmd_infos[1].name),
                    cmd_infos[1].args
                  )
            cmd = reduce(self._make_pipe, cmd_infos[2:], ini)
            return self._run_cmd(cmd, [])
        elif len(cmd_infos) == 1:
            cmd_info = cmd_infos[0]
            cmd = self._get_cmd(cmd_info.name)
            return self._run_cmd(cmd, cmd_info.args)
