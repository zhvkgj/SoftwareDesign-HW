from typing import IO
from src.interpreter.bash import BashInterpreter
from src.exceptions.exceptions import InterpreterException


def bash(inp: IO, out: IO, err: IO):
    interpreter = BashInterpreter(inp, out, err)

    try:
        for cmd_line in inp:
            try:
                interpreter.execute_cmd_line(cmd_line)
            except InterpreterException as e:
                print(f'Error: {e}', file=err)
    except KeyboardInterrupt:
        print('Closing bash...')
        return 0

    print('Exit from interpreter due to input closing', file=err)
    return 0

