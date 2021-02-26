from typing import List, IO
from abc import ABC, abstractmethod
from src.enviroment.enviroment import Environment


class ICommand(ABC):
    @abstractmethod
    def run(self, args: List[str], inp: IO, out: IO, err: IO, env: Environment) -> int:
        pass


class IBasicCommand(ICommand):
    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass
