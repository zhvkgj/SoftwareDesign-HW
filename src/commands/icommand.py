from enum import Enum
from typing import List, IO
from abc import ABC, abstractmethod


class ExitCode(Enum):
    OK = 0
    FAIL = 1


class Command(ABC):
    @abstractmethod
    def run(self, args: List[str], inp: IO,
            out: IO, err: IO) -> ExitCode:
        pass
