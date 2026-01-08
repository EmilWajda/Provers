from dataclasses import dataclass
from typing import List
import math

from .generator import Generator
from ..formulas import LogicToken


@dataclass
class Problem6(Generator):
    name = "Problem 6"
    # lengths wymagane tylko gdy poisson jest False, a lambda gdy True
    param_spec = {"clauses": int, "safety_percentage": (int, float), "poisson": bool}

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        safety_percentage = float(self.params.get("safety_percentage"))  # type: ignore
        poisson: bool = bool(self.params.get("poisson"))  # type: ignore
        lam: float | None = None

        if safety_percentage < 0 or safety_percentage > 100:
            raise ValueError("Parametr 'safety_percentage' musi być w przedziale [0,100].")

        safety_coeff = safety_percentage / 100.0

        # liczba atomów i ich nazwy
        num_atoms = max(1, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        clauses: List[LogicToken] = []

        if poisson:
            if "lambda" not in self.params:
                raise ValueError("Parametr 'lambda' jest wymagany gdy 'poisson' jest True.")
            lam = float(self.params.get("lambda"))  # type: ignore
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
                        clauses.append(self._generate_safety_clause(length_val, atom_names, "U"))
                    else:
                        clauses.append(self._generate_liveness_clause(max(2, length_val), atom_names, ["U", "V"]))

            # uzupełnianie brakujących klauzul losowo zgodnie z zaplanowanymi długościami
            while len(clauses) < total_clauses:
                chosen_length = self.random.choice(planned_lengths)
                is_safety = self.random.random() < safety_coeff

                if is_safety:
                    clauses.append(self._generate_safety_clause(chosen_length, atom_names, "U"))
                else:
                    clauses.append(self._generate_liveness_clause(max(2, chosen_length), atom_names, ["U", "V"]))

        else:
            clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
            if not clause_lengths:
                raise ValueError("Lista długości klauzul (params['lengths']) nie może być pusta w trybie non-Poisson.")

            if len(clause_lengths) > total_clauses:
                raise ValueError(
                    f"Liczba różnych długości klauzul ({len(clause_lengths)}) nie może przekraczać całkowitej liczby klauzul ({total_clauses})."
                )

            num_per_length = total_clauses // len(clause_lengths)
            safety_per_length = round(num_per_length * safety_coeff)

            for length in clause_lengths:
                for i in range(num_per_length):
                    is_safety = i < safety_per_length
                    if is_safety:
                        clauses.append(self._generate_safety_clause(length, atom_names, "U"))
                    else:
                        clauses.append(self._generate_liveness_clause(max(2, length), atom_names, ["U", "V"]))

            # uzupełnianie brakujących klauzul
            half_of_remaining_clauses = round((total_clauses - len(clauses)) * safety_coeff)

            for _ in range(half_of_remaining_clauses):
                length = self.random.choice(clause_lengths)
                clauses.append(self._generate_safety_clause(length, atom_names, "U"))

            while len(clauses) < total_clauses:
                length = self.random.choice(clause_lengths)
                clauses.append(self._generate_liveness_clause(max(2, length), atom_names, ["U", "V"]))

        #przyciecie jesli jest za duzo klauzul
        if len(clauses) > total_clauses:
            clauses = clauses[:total_clauses]

        return clauses

    def _poisson(self, k: int, lam: float) -> float:
        return (lam**k * math.exp(-lam)) / math.factorial(k)
