from dataclasses import dataclass
from typing import List
import math

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem2(Generator):
    name = "2"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lambda": StandardParams.LAMBDA.value,
    }
    presets = {}

    def validate_extra(self) -> str | None:
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        lam: float = self.params.get("lambda")  # type: ignore

        # atomy i ich nazwy
        num_atoms = total_clauses // 2
        if num_atoms < 1:
            num_atoms = 1
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        clauses: List[LogicToken] = []

        # długości i ich liczba klauzyul według rozkładu Poissona
        planned_lengths = []
        planned_counts = []

        # Iterujemy po długościach od 1 w górę
        length = 1
        while True:
            prob = self._poisson(length, lam)
            count = round(prob * total_clauses)

            # gdy licznik to 0 i przekroczyliśmy lambda
            if count == 0 and length > lam:
                break

            if count > 0:
                planned_lengths.append(length)
                planned_counts.append(count)

            length += 1

        # gdyby lista była pusta (bardzo małe lambda)
        if not planned_lengths:
            planned_lengths = [max(1, int(lam))]
            planned_counts = [total_clauses]

        # Generowanie klauzul
        for length_val, count in zip(planned_lengths, planned_counts):
            # dla danej długości połowa to safety
            target_safety_local = round(count * 0.5)

            for i in range(count):
                # Zabezpieczenie przed przekroczeniem limitu
                if len(clauses) >= total_clauses:
                    break

                # Decyzja lokalna: czy safety?
                is_safety = i < target_safety_local

                if is_safety:
                    clauses.append(self._generate_safety_clause(length_val, atom_names))
                else:
                    # Liveness musi mieć min długość 2
                    final_len = max(2, length_val)
                    clauses.append(self._generate_liveness_clause(final_len, atom_names))
        # uzupełnianie brakujących klauzul
        while len(clauses) < total_clauses:
            # Losujemy długość z zaplanowanych
            chosen_length = self.random.choice(planned_lengths)

            # Losujemy typ
            is_safety = self.random.choice([True, False])

            if is_safety:
                clauses.append(self._generate_safety_clause(chosen_length, atom_names))
            else:
                final_len = max(2, chosen_length)
                clauses.append(self._generate_liveness_clause(final_len, atom_names))

        return clauses

    def _poisson(self, k: int, lam: float) -> float:
        """Oblicza prawdopodobieństwo P(k) dla rozkładu Poissona (PMF)."""
        return (lam**k * math.exp(-lam)) / math.factorial(k)
