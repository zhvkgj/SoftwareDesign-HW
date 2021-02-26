import io
from typing import List

from src.commands.basic_commands import *
from src.commands.builtin_commands import *
from src.commands.command_api import ICommand
from src.enviroment.enviroment import Environment
from testing.common import *


def check(cmd: ICommand, args: List[str], inp: str, expected: str):
    inp_stream = io.StringIO(inp)
    output_stream = io.StringIO()
    err_stream = io.StringIO()
    env = Environment()
    cmd.run(args, inp_stream, output_stream, err_stream, env)
    assert output_stream.getvalue() == expected


def test_1():
    echo = EchoCommand()
    check(echo, ['123', '456'], '', '123 456\n')


def test_2():
    echo = EchoCommand()
    check(echo, [], '', '\n')


def test_3():
    path = test_input / 'file_1.txt'
    cat = CatCommand()
    with open(path, 'r') as f:
        expected = f.read()
    check(cat, [str(path)], '', expected)


def test_4():
    echo = EchoCommand()
    cat = CatCommand()
    pipe = PipeAggregationCommand(echo, ['hello'], cat, [])

    check(pipe, [], '', 'hello\n')


