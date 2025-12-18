from dataclasses import dataclass
from typing import List

from .generator import Generator
from ..formulas import LogicToken


@dataclass
class Problem4(Generator):
    name = "Problem 4"
    param_spec = {"clauses": int, "length": int}

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_length: int = self.params.get("length")  # type: ignore

        if clause_length < 2:
            raise ValueError("Param 'length' must be >= 2 for liveness clauses.")

        num_atoms = total_clauses // 2
        if num_atoms < 1:
            num_atoms = 1
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        clauses: List[LogicToken] = []

        safety_target = total_clauses // 2

        for i in range(total_clauses):
            if i < safety_target:
                clauses.append(self._generate_safety_clause(clause_length, atom_names, "U"))
            else:
                clauses.append(self._generate_liveness_clause(clause_length, atom_names, ["U", "V"]))

        return clauses
