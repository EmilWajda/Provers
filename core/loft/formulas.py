from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class LogicToken(ABC):
    @abstractmethod
    def to_tptp(self) -> str: ...


@dataclass
class BasicToken(LogicToken):
    pass


# TODO: wszystkie ponizsze: to_tptp


@dataclass
class GreaterThan(BasicToken):
    pass


@dataclass
class Atom(BasicToken):
    name: str


@dataclass
class Not(BasicToken):
    token: BasicToken


@dataclass
class Alternative(BasicToken):
    tokens: list[BasicToken]


@dataclass
class Conjunction(BasicToken):
    tokens: list[BasicToken]


@dataclass
class Implication(BasicToken):
    premise: BasicToken
    conclusion: BasicToken


@dataclass
class ForAll(LogicToken):
    formula: LogicToken


@dataclass
class Exists(LogicToken):
    formula: LogicToken
