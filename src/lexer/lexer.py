from typing import List

from src.lexer.rules import *


class Lexer:
    @staticmethod
    def split(s: str) -> List[Token]:
        lexer.input(s)
        return [x.value for x in lexer]
