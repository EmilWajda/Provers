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
    parameter_left: str
    parameter_right: str

    def to_tptp(self) -> str:
        return f"ssGTE({self.parameter_left},{self.parameter_right})"


@dataclass
class Atom(BasicToken):
    name: str
    parameter: str

    def to_tptp(self) -> str:
        return f"{self.name}({self.parameter})"


@dataclass
class Not(BasicToken):
    token: BasicToken

    def to_tptp(self) -> str:
        return f"~({self.token.to_tptp()})"


@dataclass
class Alternative(BasicToken):
    tokens: list[BasicToken]

    def to_tptp(self) -> str:
        inner = " | ".join(token.to_tptp() for token in self.tokens)
        return f"({inner})"


@dataclass
class Conjunction(BasicToken):
    tokens: list[BasicToken]

    def to_tptp(self) -> str:
        inner = " & ".join(token.to_tptp() for token in self.tokens)
        return f"({inner})"


@dataclass
class Implication(BasicToken):
    premise: BasicToken
    conclusion: BasicToken

    def to_tptp(self) -> str:
        return f"({self.premise.to_tptp()} => {self.conclusion.to_tptp()})"


@dataclass
class ForAll(LogicToken):
    parameter: str
    formula: LogicToken
    

    def to_tptp(self) -> str:
        return f"! [{self.parameter}] : ({self.formula.to_tptp()})"



@dataclass
class Exists(LogicToken):
    parameter: str
    formula: LogicToken
    

    def to_tptp(self) -> str:
        return f"? [{self.parameter}] : ({self.formula.to_tptp()})"
    

p = ForAll("U", Exists("V", Conjunction([GreaterThan("U", "V"), Implication(Not(Atom("var14", "V")), Atom("var5", "U"))])))

print(p.to_tptp())
