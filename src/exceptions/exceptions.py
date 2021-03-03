class InterpreterException(RuntimeError):
    pass


class CommandNotRegistered(InterpreterException):
    pass


class ParseError(InterpreterException):
    pass


class ExitInterpreter(SystemExit):
    pass
