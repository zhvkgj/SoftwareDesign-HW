from typing import IO

from termcolor import colored

from src.interpreter.bash import BashInterpreter
from src.exceptions.exceptions import InterpreterException


class Bash:
    @staticmethod
    def run(inp: IO, out: IO, err: IO):
        interpreter = BashInterpreter(inp, out, err)

        try:
            for cmd_line in inp:
                try:
                    interpreter.execute_cmd_line(cmd_line)
                except InterpreterException as e:
                    print(colored(f'Error: {e}', 'red'), file=err)
        except KeyboardInterrupt:
            print('Closing bash...', file=out)
            return 0
        return 0
