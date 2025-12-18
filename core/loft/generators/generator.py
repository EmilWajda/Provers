from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import ClassVar, Any, Union, Tuple
from random import Random
from typing import get_origin, get_args

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
    param_spec: ClassVar[dict[str, Union[type, Tuple[type, ...]]]]

    seed: int
    random: Random = field(init=False)
    params: dict[str, Any]

    def __post_init__(self):
        self.random = Random(self.seed)
        self._validate_params()

    def _validate_params(self):
        for key, expected_type in self.param_spec.items():
            if key not in self.params:
                raise ValueError(f"Missing required parameter '{key}' in params.")

            value = self.params[key]

            # Obsługa list dodatkowo typowanych
            if get_origin(expected_type) is list:
                if not isinstance(value, list):
                    raise TypeError(f"Parameter '{key}' must be a list, got {type(value).__name__}")

                (elem_type,) = get_args(expected_type)
                for i, elem in enumerate(value):
                    if not isinstance(elem, elem_type):
                        raise TypeError(
                            f"Element params['{key}'][{i}] must be {elem_type}, " + f"got {type(elem).__name__}"
                        )

            # obsługa zwykłych typów
            else:
                if not isinstance(value, expected_type):
                    raise TypeError(f"Parameter '{key}' must be {expected_type}, got {type(value).__name__}.")

    @abstractmethod
    def generate(self) -> list[LogicToken]: ...

    def _generate_safety_clause(self, length: int, atom_names: list[str], parameter: str) -> LogicToken:
        """Generuje pojedynczą klauzulę bezpieczeństwa o zadanej długości i parametrze (U)."""
        chosen_atoms = self.random.sample(atom_names, k=min(length, len(atom_names)))
        literals: list[BasicToken] = []

        for name in chosen_atoms:
            atom = Atom(name, parameter)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals.append(atom)

        return ForAll(parameter, Not(Alternative(literals)))

    def _generate_liveness_clause(self, length: int, atom_names: list[str], parameters: list[str]) -> LogicToken:
        """Generuje pojedynczą klauzulę żywotnościową o zadanej długości i parametrach (U oraz V)."""

        # walidacja
        if len(parameters) != 2:
            raise ValueError("parameters powinno mieć dokładnie 2 elementy, np. ['U', 'V'].")
        if length < 2:
            raise ValueError("length musi być >= 2, żeby poprzednik i następnik nie były puste.")

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
