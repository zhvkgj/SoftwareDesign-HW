from enum import Enum
import ply.lex as lex


class TokenType(Enum):
    STR = 'STR'
    SINGLE = 'SINGLE'
    DOUBLE = 'DOUBLE'
    PIPE = 'PIPE'
    VAR_DEF = 'VAR_DEF'


class Token:
    def __init__(self, kind: TokenType, token: str):
        self._kind = kind
        self._token = token

    @property
    def kind(self) -> TokenType:
        return self._kind

    @property
    def string(self) -> str:
        return self._token

    def __str__(self):
        return f'({self._kind}, {self._token})'

    def __eq__(self, other):
        return isinstance(other, Token) and self.kind == other.kind and self.string == other.string

tokens = (
    'VAR_DEF',
    'STR',
    'SINGLE',
    'DOUBLE',
    'PIPE',
)


def tokenize(t: lex.LexToken, tp: TokenType):
    t.value = Token(tp, t.value)
    return t


def t_VAR_DEF(t):
    r'\w+\=\w+'
    return tokenize(t, TokenType.VAR_DEF)


def t_STR(t):
    r'\w+'
    return tokenize(t, TokenType.STR)


def t_SINGLE(t):
    r'\'(\s|\w)*\''
    return tokenize(t, TokenType.SINGLE)


def t_DOUBLE(t):
    r'\"(\s|\w)*\"'
    return tokenize(t, TokenType.DOUBLE)


def t_PIPE(t):
    r'\|'
    return tokenize(t, TokenType.PIPE)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
