"""
Модуль лексера. Пока просто один класс
со статическим методом.
"""

from typing import List

from src.lexer.rules import Token, lexer


class Lexer:
    """
    Класс лексера, нужен для разделения
    исходной строки на разные токены.
    """
    @staticmethod
    def split(s: str) -> List[Token]:
        """
        Разделяет строку и преобразует её
        в список токенов.
        :param s: входная строка
        :return: список токенов
        """
        lexer.input(s)
        return [x.value for x in lexer]
