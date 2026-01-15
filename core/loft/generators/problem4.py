from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem4(Generator):
    name = "4"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "length": StandardParams.LENGTH.value,
    }
    presets = {}

    def validate_extra(self) -> str | None:
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_length: int = self.params.get("length")  # type: ignore

        num_atoms = total_clauses // 2
        if num_atoms < 1:
            num_atoms = 1
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        clauses: List[LogicToken] = []

        safety_target = total_clauses // 2

        for i in range(total_clauses):
            if i < safety_target:
                clauses.append(self._generate_safety_clause(clause_length, atom_names))
            else:
                clauses.append(self._generate_liveness_clause(clause_length, atom_names))

        return clauses
