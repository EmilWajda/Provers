from dataclasses import dataclass
from typing import List
import math

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem6(Generator):
    name = "6"
    # lengths wymagane tylko gdy poisson jest False, a lambda gdy True
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "safety_percentage": StandardParams.SAFETY_PERCENTAGE.value,
        "poisson": StandardParams.POISSON.value,
        "lambda": StandardParams.LAMBDA_OR_NONE.value,
        "lengths": StandardParams.LENGTHS_OR_NONE.value,
    }
    presets = {
        "Default": {"clauses": 50, "safety_percentage": 50, "poisson": True, "lambda": 3.0, "lengths": []},
        "Fixed Lengths": {"clauses": 50, "safety_percentage": 50, "poisson": False, "lambda": 0, "lengths": [2, 3, 5]},
    }

    def validate_extra(self) -> str | None:
        poisson: bool = bool(self.params.get("poisson"))  # type: ignore
        lam: float = self.params.get("lambda")  # type: ignore
        lengths: list[int] = self.params.get("lengths")  # type: ignore

        if poisson:
            if lam == 0:
                return "Lambda must be greater than 0 when poisson is enabled."
        else:
            if not lengths:
                return "Clause lengths list cannot be empty when poisson is disabled."
            total_clauses: int = self.params.get("clauses")  # type: ignore
            if len(lengths) > total_clauses:
                return "Number of different clause lengths cannot exceed total number of clauses."
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        safety_percentage = float(self.params.get("safety_percentage"))  # type: ignore
        poisson: bool = bool(self.params.get("poisson"))  # type: ignore

        safety_coeff = safety_percentage / 100.0

        # liczba atomów i ich nazwy
        num_atoms = max(1, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        clauses: List[LogicToken] = []

        if poisson:
            lam: float = self.params.get("lambda")  # type: ignore
            planned_lengths: List[int] = []
            planned_counts: List[int] = []

            length = 1
            while True:
                prob = self._poisson(length, lam)
                count = round(prob * total_clauses)

                if count == 0 and length > lam:
                    break

                if count > 0:
                    planned_lengths.append(length)
                    planned_counts.append(count)

                length += 1

            if not planned_lengths:
                planned_lengths = [max(1, int(lam))]
                planned_counts = [total_clauses]

            for length_val, count in zip(planned_lengths, planned_counts):
                target_safety_local = round(count * safety_coeff)

                for i in range(count):
                    if len(clauses) >= total_clauses:
                        break

                    is_safety = i < target_safety_local

                    if is_safety:
                        clauses.append(self._generate_safety_clause(length_val, atom_names))
                    else:
                        clauses.append(self._generate_liveness_clause(max(2, length_val), atom_names))

            # uzupełnianie brakujących klauzul losowo zgodnie z zaplanowanymi długościami
            while len(clauses) < total_clauses:
                chosen_length = self.random.choice(planned_lengths)
                is_safety = self.random.random() < safety_coeff

                if is_safety:
                    clauses.append(self._generate_safety_clause(chosen_length, atom_names))
                else:
                    clauses.append(self._generate_liveness_clause(max(2, chosen_length), atom_names))

        else:
            clause_lengths: list[int] = self.params.get("lengths")  # type: ignore

            num_per_length = total_clauses // len(clause_lengths)
            safety_per_length = round(num_per_length * safety_coeff)

            for length in clause_lengths:
                for i in range(num_per_length):
                    is_safety = i < safety_per_length
                    if is_safety:
                        clauses.append(self._generate_safety_clause(length, atom_names))
                    else:
                        clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

            # uzupełnianie brakujących klauzul
            half_of_remaining_clauses = round((total_clauses - len(clauses)) * safety_coeff)

            for _ in range(half_of_remaining_clauses):
                length = self.random.choice(clause_lengths)
                clauses.append(self._generate_safety_clause(length, atom_names))

            while len(clauses) < total_clauses:
                length = self.random.choice(clause_lengths)
                clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        # przyciecie jesli jest za duzo klauzul
        if len(clauses) > total_clauses:
            clauses = clauses[:total_clauses]

        return clauses

    def _poisson(self, k: int, lam: float) -> float:
        return (lam**k * math.exp(-lam)) / math.factorial(k)
