from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem1(Generator):
    name = "1"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
    }
    presets = {
        "Default": {"clauses": 50, "lengths": [2, 3, 4, 6, 8, 10]},
        "Short": {"clauses": 30, "lengths": [2, 3, 4]},
        "Long": {"clauses": 100, "lengths": [6, 8, 10, 12]},
    }

    def validate_extra(self) -> str | None:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        if len(clause_lengths) > total_clauses:
            return "Number of different clause lengths cannot exceed total number of clauses."
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore

        num_per_length = total_clauses // len(clause_lengths)
        safety_per_length = num_per_length // 2

        # liczba atomów i ich nazwy
        num_atoms = total_clauses // 2
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # generowanie klauzul
        clauses: List[LogicToken] = []

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length

                if is_safety:
                    clause = self._generate_safety_clause(length, atom_names)
                else:
                    clause = self._generate_liveness_clause(length, atom_names)

                clauses.append(clause)

        # generowanie pozostalych brakujących klauzul jesli istnieją
        half_of_remaining_clauses = (total_clauses - len(clauses)) // 2

        for _ in range(half_of_remaining_clauses):
            length = self.random.choice(clause_lengths)
            clause = self._generate_safety_clause(length, atom_names)
            clauses.append(clause)

        while len(clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            clause = self._generate_liveness_clause(length, atom_names)
            clauses.append(clause)

        return clauses
