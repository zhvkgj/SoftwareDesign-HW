from abc import ABC, abstractmethod
from typing import List
from src.lexer.lexer import Token

from typing import TypeVar, Generic

T = TypeVar('T')


class CommandInfo(Generic[T]):
    def __init__(self, name: T, args: List[T]):
        self._name = name
        self._args = args

    @property
    def name(self) -> T:
        return self._name

    @property
    def args(self) -> List[T]:
        return self._args

    def __str__(self):
        return f'(name={self.name}, args={[str(x) for x in self.args]})'


class PipeInfo(Generic[T]):
    def __init__(self, utils: List[CommandInfo[T]]):
        self._utils = utils

    @property
    def utils(self) -> List[CommandInfo[T]]:
        return self._utils

    def __str__(self):
        return f'{[str(x) for x in self.utils]}'


class IParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(s: List[Token]) -> PipeInfo:
        pass
