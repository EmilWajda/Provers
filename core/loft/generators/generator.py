from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import ClassVar, Any
from random import Random

from ..formulas import LogicToken


@dataclass
class Generator(ABC):
    name: ClassVar[str]
    param_spec: ClassVar[dict[str, type]]

    seed: int
    random: Random = field(init=False)
    params: dict[str, Any]

    def __post_init__(self):
        self.random = Random(self.seed)

    @abstractmethod
    def generate(self) -> list[LogicToken]: ...
