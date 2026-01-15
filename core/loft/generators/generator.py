from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import ClassVar, Any, Self
from random import Random

from .param_spec import ParamSpec
from ..formulas import (
    LogicToken,
    ForAll,
    Exists,
    Not,
    Alternative,
    Implication,
    GreaterThan,
    Atom,
    Conjunction,
    BasicToken,
)


@dataclass
class Generator(ABC):
    name: ClassVar[str]
    param_spec: ClassVar[dict[str, ParamSpec]]
    presets: ClassVar[dict[str, dict[str, Any]]]

    seed: int
    random: Random = field(init=False)
    params: dict[str, Any]

    def __post_init__(self) -> None:
        self.random = Random(self.seed)
        self._validate_params()

    @classmethod
    def from_preset(cls, preset_name: str, seed: int) -> Self:
        if preset_name not in cls.presets:
            raise ValueError(f"Preset '{preset_name}' not found.")
        params = cls.presets[preset_name]
        return cls(seed=seed, params=params)

    def _validate_params(self) -> None:
        for key, expected_type in self.param_spec.items():
            if key not in self.params:
                raise ValueError(f"Missing required parameter '{key}' in params.")
            value = self.params[key]
            if not expected_type.validate(value):
                checks = expected_type.get_checks()
                checks_str = ", ".join(f"{k}={v}" for k, v in checks.items() if v is not None) if checks else "any"
                raise ValueError(
                    f"Parameter '{key}' has invalid value: {value}. Expected: {expected_type.name} ({checks_str})."
                )
        error = self.validate_extra()
        if error is not None:
            raise ValueError(error)

    @abstractmethod
    def validate_extra(self) -> str | None: ...

    @abstractmethod
    def generate(self) -> list[LogicToken]: ...

    def _generate_safety_clause(self, length: int, atom_names: list[str], parameter: str = "U") -> LogicToken:
        """Generuje pojedynczą klauzulę bezpieczeństwa o zadanej długości i parametrze (U)."""
        chosen_atoms = self.random.sample(atom_names, k=min(length, len(atom_names)))
        literals: list[BasicToken] = []

        for name in chosen_atoms:
            atom = Atom(name, parameter)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals.append(atom)

        return ForAll(parameter, Not(Alternative(literals)))

    def _generate_liveness_clause(
        self, length: int, atom_names: list[str], parameters: tuple[str, str] = ("U", "V")
    ) -> LogicToken:
        """Generuje pojedynczą klauzulę żywotnościową o zadanej długości i parametrach (U oraz V)."""
        U, V = parameters[0], parameters[1]
        k_pred = self.random.randint(1, length - 1)
        k_cons = length - k_pred

        chosen_pred_atoms = self.random.sample(atom_names, k=min(k_pred, len(atom_names)))
        chosen_cons_atoms = self.random.sample(atom_names, k=min(k_cons, len(atom_names)))

        literals_predecessor: list[BasicToken] = []
        literals_consequent: list[BasicToken] = []

        # budowanie listy literałów poprzednika
        for name in chosen_pred_atoms:
            atom = Atom(name, V)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals_predecessor.append(atom)

        # budowanie listy literałów następnika
        for name in chosen_cons_atoms:
            atom = Atom(name, U)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals_consequent.append(atom)

        predecessor_or = Alternative(literals_predecessor)
        consequent_or = Alternative(literals_consequent)

        implication = Implication(predecessor_or, consequent_or)
        gte = GreaterThan(U, V)
        body = Conjunction([gte, implication])

        return ForAll(U, Exists(V, body))
