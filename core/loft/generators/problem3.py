from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem3(Generator):
    name = "3"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "ratio": StandardParams.RATIO.value,
    }
    presets = {
        "Default": {"clauses": 50, "ratio": 2.0},
        "Medium": {"clauses": 100, "ratio": 5.0},
        "Large": {"clauses": 500, "ratio": 10.0},
    }

    def validate_extra(self) -> str | None:
        ratio: float = self.params.get("ratio")  # type: ignore
        max_length = int(ratio)
        
        if max_length < 2:
            return "Ratio must be at least 2 to generate valid liveness clauses."
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        ratio: float = self.params.get("ratio")  # type: ignore

        # liczba atomów i ich nazwy
        num_atoms = int(total_clauses * ratio)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # maksymalna długość klauzuli to liczba wszystkich zmiennych do ilości klauzul
        max_length = int(ratio)

        # generowanie klauzul
        clauses: List[LogicToken] = []

        safety_count = total_clauses // 2
        liveness_count = total_clauses - safety_count

        for _ in range(safety_count):
            length = self.random.randint(2, max_length)
            clause = self._generate_safety_clause(length, atom_names)
            clauses.append(clause)

        for _ in range(liveness_count):
            length = self.random.randint(2, max_length)
            clause = self._generate_liveness_clause(length, atom_names)
            clauses.append(clause)

        # mieszanie kolejności klauzul
        self.random.shuffle(clauses)

        return clauses