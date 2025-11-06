from dataclasses import dataclass

from .generator import Generator
from ..formulas import LogicToken


@dataclass
class Problem1(Generator):
    name = "Problem 1"
    param_spec = {"clauses": int}

    def generate(self) -> list[LogicToken]:
        ...  # TODO
