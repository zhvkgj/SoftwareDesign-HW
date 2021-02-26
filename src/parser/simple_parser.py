from src.commands.builtin_commands import BuiltInCmdNames
from src.parser.parser_api import *
from src.lexer.lexer import *
from itertools import groupby


class SimpleParser(IParser):
    @staticmethod
    def _is_set_var_cmd(tokens: List[Token]):
        pass

    @staticmethod
    def parse(tokens: List[Token]) -> PipeInfo[Token]:
        if len(tokens) == 1 and tokens[0].kind == TokenType.VAR_DEF:
            token = tokens[0]
            var_name, value = [arg.strip() for arg in token.string.split("=")]
            cmd_name = Token(TokenType.STR, BuiltInCmdNames.SetVar)
            arg1 = Token(TokenType.STR, var_name)
            arg2 = Token(TokenType.STR, value.strip('\"').strip('\''))
            return PipeInfo([CommandInfo(cmd_name, [arg1, arg2])])
        else:
            if TokenType.VAR_DEF in [t.kind for t in tokens]:
                raise ParseError("Var definition must be the only command")

            split_tokens = [list(y) for x, y in groupby(tokens, lambda z: z.kind == TokenType.PIPE)
                            if not x]
            cmds = [CommandInfo(tokens[0], tokens[1:]) for tokens in split_tokens]
            return PipeInfo(cmds)

