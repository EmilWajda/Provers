from dataclasses import dataclass
from typing import List

from .generator import Generator
from ..formulas import LogicToken


@dataclass
class Problem5(Generator):
    name = "Problem 5"
    # dlugości 1,5,10,20
    param_spec = {"clauses": int, "lengths": list[int], "distribution": str}

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        distribution: str = self.params.get("distribution")  # type: ignore
        safety_coeff: float = 0.5
        num_atoms = max(1, total_clauses // 2)

        if not clause_lengths or len(clause_lengths) < 1:
            raise ValueError("params['lengths'] must be a non-empty list of clause lengths.")

        m = len(clause_lengths)
        if total_clauses < m:
            raise ValueError("Number of clauses must be at least the number of different lengths.")

        counts: List[int] = [0] * m

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

        else:
            raise ValueError("Invalid distribution; choose 'even', 'tiny_short' or 'tiny_long'.")

        #generowanie
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
                        self._generate_safety_clause(max(1, length), [f"var{i+1}" for i in range(num_atoms)], "U")
                    )
                    safety_generated += 1
                else:
                    clauses.append(
                        self._generate_liveness_clause(max(2, length), [f"var{i+1}" for i in range(num_atoms)], ["U", "V"])
                    )

        #uzupelnianie braków co zostały
        while len(clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            if self.random.random() < safety_coeff:
                clauses.append(self._generate_safety_clause(max(1, length), [f"var{i+1}" for i in range(num_atoms)], "U"))
            else:
                clauses.append(
                    self._generate_liveness_clause(max(2, length), [f"var{i+1}" for i in range(num_atoms)], ["U", "V"])
                )

        return clauses

