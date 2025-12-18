from dataclasses import dataclass
from typing import List

from .generator import Generator
from ..formulas import LogicToken


@dataclass
class Problem3(Generator):
    name = "Problem 3"
    param_spec = {"clauses": int, "lengths": list[int], "ratio": int}

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        ratio: int = self.params.get("ratio")  # type: ignore

        # walidacja
        if not clause_lengths:
            raise ValueError("Lista długości klauzul (params['lengths']) nie może być pusta.")
        if ratio < 1:
            raise ValueError("Parametr 'ratio' musi być >= 1.")

        # liczba atomów zależna od współczynnika ratio
        num_atoms = total_clauses * ratio
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # filtrujemy długości do tych, które są <= ratio
        allowed_lengths = [l for l in clause_lengths if l <= ratio]
        if not allowed_lengths:
            raise ValueError("Brak dopuszczalnych długości po filtrze 'ratio'. Zmniejsz 'lengths' lub zwiększ 'ratio'.")

        # rozdzielamy klauzule równomiernie po dozwolonych długościach
        num_per_length = total_clauses // len(allowed_lengths)
        safety_per_length = num_per_length // 2

        clauses: List[LogicToken] = []

        for length in allowed_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length
                if is_safety:
                    clauses.append(self._generate_safety_clause(length, atom_names, "U"))
                else:
                    clauses.append(self._generate_liveness_clause(max(2, length), atom_names, ["U", "V"]))

        # uzupełnianie brakujących klauzul
        half_of_remaining_clauses = (total_clauses - len(clauses)) // 2

        for _ in range(half_of_remaining_clauses):
            length = self.random.choice(allowed_lengths)
            clauses.append(self._generate_safety_clause(length, atom_names, "U"))

        while len(clauses) < total_clauses:
            length = self.random.choice(allowed_lengths)
            clauses.append(self._generate_liveness_clause(max(2, length), atom_names, ["U", "V"]))

        return clauses
