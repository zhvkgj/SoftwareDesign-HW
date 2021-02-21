import io
from typing import List

from src.commands.basic_commands import EchoCommand, CatCommand
from src.commands.pipe import PipeAggregation
from src.commands.icommand import Command
from testing.common import *

def check(cmd: Command, args: List[str], inp: str, expected: str):
    inp_stream = io.StringIO(inp)
    output_stream = io.StringIO()
    err_stream = io.StringIO()
    cmd.run(args, inp_stream, output_stream, err_stream)
    assert output_stream.getvalue() == expected


def test_1():
    echo = EchoCommand()
    check(echo, ['123', '456'], '', '123 456')


def test_2():
    echo = EchoCommand()
    check(echo, [], '', '')


def test_3():
    path = test_input / 'file_1.txt'
    cat = CatCommand()
    with open(path, 'r') as f:
        expected = f.read()
    check(cat, [str(path)], '', expected)


def test_4():
    echo = EchoCommand()
    cat = CatCommand()
    pipe = PipeAggregation(echo, ['hello'], cat, [])

    check(pipe, [], '', 'hello')


