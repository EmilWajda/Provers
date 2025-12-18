from dataclasses import dataclass
from typing import List

from .generator import Generator
from ..formulas import LogicToken


@dataclass
class Problem1(Generator):
    name = "Problem 1"
    param_spec = {"clauses": int, "lengths": list[int]}

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore

        # walidacja pewnych przypadków
        if not clause_lengths:
            raise ValueError("Lista długości klauzul (params['lengths']) nie może być pusta.")
        if len(clause_lengths) > total_clauses:
            raise ValueError(
                f"Liczba różnych długości klauzul ({len(clause_lengths)}) "
                f"nie może przekraczać całkowitej liczby klauzul ({total_clauses})."
            )

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
                    clause = self._generate_safety_clause(length, atom_names, "U")
                else:
                    clause = self._generate_liveness_clause(length, atom_names, ["U", "V"])

                clauses.append(clause)

        # generowanie pozostalych brakujących klauzul jesli istnieją
        half_of_remaining_clauses = (total_clauses - len(clauses)) // 2

        for _ in range(half_of_remaining_clauses):
            length = self.random.choice(clause_lengths)
            clause = self._generate_safety_clause(length, atom_names, "U")
            clauses.append(clause)

        while len(clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            clause = self._generate_liveness_clause(length, atom_names, ["U", "V"])
            clauses.append(clause)

        return clauses
