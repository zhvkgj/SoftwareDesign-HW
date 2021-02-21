from abc import ABC, abstractmethod
from typing import List
from src.lexer.lexer import Token

from typing import TypeVar, Generic

T = TypeVar('T')


class UtilityInfo(Generic[T]):
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
    def __init__(self, utils: List[UtilityInfo[T]]):
        self._utils = utils

    @property
    def utils(self) -> List[UtilityInfo[T]]:
        return self._utils

    def __str__(self):
        return f'{[str(x) for x in self.utils]}'


class IParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(s: List[Token]) -> PipeInfo:
        pass
