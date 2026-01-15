from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem5(Generator):
    name = "5"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "distribution": StandardParams.DISTRIBUTION.value,
    }
    presets = {}

    def validate_extra(self) -> str | None:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        if len(clause_lengths) > total_clauses:
            return "Number of different clause lengths cannot exceed total number of clauses."
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        distribution: str = self.params.get("distribution")  # type: ignore
        safety_coeff: float = 0.5
        num_atoms = max(1, total_clauses // 2)
        m = len(clause_lengths)

        counts: List[int] = [0]

        if distribution == "even":
            base = total_clauses // m
            rem = total_clauses - base * m
            for i in range(m):
                counts[i] = base + (1 if i < rem else 0)

        elif distribution == "tiny_short":
            tiny = max(1, round(total_clauses * 0.01))
            remaining = total_clauses - tiny
            base = remaining // (m - 1)
            rem = remaining - base * (m - 1)
            counts[0] = tiny
            idx = 1
            for i in range(m - 1):
                counts[idx] = base + (1 if i < rem else 0)
                idx += 1

        elif distribution == "tiny_long":
            tiny = max(1, round(total_clauses * 0.01))
            remaining = total_clauses - tiny
            base = remaining // (m - 1)
            rem = remaining - base * (m - 1)
            for i in range(m - 1):
                counts[i] = base + (1 if i < rem else 0)
            counts[-1] = tiny

        # generowanie
        clauses: List[LogicToken] = []

        for idx, length in enumerate(clause_lengths):
            want = counts[idx]
            want_safety = round(want * safety_coeff)
            safety_generated = 0

            for i in range(want):
                if len(clauses) >= total_clauses:
                    break
                if safety_generated < want_safety:
                    clauses.append(
                        self._generate_safety_clause(max(1, length), [f"var{i+1}" for i in range(num_atoms)])
                    )
                    safety_generated += 1
                else:
                    clauses.append(
                        self._generate_liveness_clause(max(2, length), [f"var{i+1}" for i in range(num_atoms)])
                    )

        # uzupelnianie braków co zostały
        while len(clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            if self.random.random() < safety_coeff:
                clauses.append(self._generate_safety_clause(max(1, length), [f"var{i+1}" for i in range(num_atoms)]))
            else:
                clauses.append(self._generate_liveness_clause(max(2, length), [f"var{i+1}" for i in range(num_atoms)]))

        return clauses
