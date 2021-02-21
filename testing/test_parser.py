from src.parser.SimpleParser import *
# from src.parser.IParser import *


def check(s: str, expected: PipeInfo):
    tokens = Lexer.split(s)
    pipe_info = SimpleParser.parse(tokens)
    assert str(pipe_info) == str(expected)


def test_1():
    cmd = """echo 5"""
    expected = PipeInfo([
        UtilityInfo(Token(TokenType.STR, 'echo'), [Token(TokenType.STR, '5')])
    ])
    check(cmd, expected)


def test_2():
    cmd = """x=5"""
    expected = PipeInfo([
        UtilityInfo(Token(TokenType.STR, 'SetVar'),
                    [
                        Token(TokenType.STR, 'x'),
                        Token(TokenType.STR, '5')
                    ])
    ])
    check(cmd, expected)


def test_3():
    cmd = """ echo 'x' | cat """
    expected = PipeInfo([
        UtilityInfo(Token(TokenType.STR, 'echo'),
                    [Token(TokenType.SINGLE, "'x'")]),
        UtilityInfo(Token(TokenType.STR, 'cat'), [])
    ])
    check(cmd, expected)
