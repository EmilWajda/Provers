from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import LogicToken


@dataclass
class Problem18(Generator):
    name = "18"
    param_spec = {
        "atoms": StandardParams.ATOMS.value,
        "alpha": StandardParams.ALPHA.value,
        "lengths": StandardParams.LENGTHS.value,
    }
    presets = {
        "Low Density": {"atoms": 100, "alpha": 2.0, "lengths": [2, 3, 4, 6]},
        "Phase Transition": {"atoms": 100, "alpha": 4.26, "lengths": [2, 3, 4, 6]},
        "High Density": {"atoms": 100, "alpha": 8.0, "lengths": [2, 3, 4, 6]},
    }

    def validate_extra(self) -> str | None:
        atoms: int = self.params.get("atoms")  # type: ignore
        alpha: float = self.params.get("alpha")  # type: ignore
        
        # kod defensywny: upewniamy się, że wyliczona liczba klauzul ma matematyczny sens
        m = round(atoms * alpha)
        if m < 2:
            return f"The combination of atoms ({atoms}) and alpha ({alpha}) results in {m} clauses. Minimum required is 2."
            
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        if not clause_lengths:
            return "Clause lengths list cannot be empty."
            
        return None

    def generate(self) -> list[LogicToken]:
        num_atoms: int = self.params.get("atoms")  # type: ignore
        alpha: float = self.params.get("alpha")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore

        # obliczamy m (całkowitą liczbę klauzul)
        total_clauses = max(2, round(num_atoms * alpha))

        # budujemy zbiór n atomów
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # generowanie klauzul (klasyczne podejście P1/P2 z rygorem 50:50)
        clauses: List[LogicToken] = []
        
        num_per_length = total_clauses // len(clause_lengths)
        safety_per_length = num_per_length // 2

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length
                if is_safety:
                    clauses.append(self._generate_safety_clause(length, atom_names))
                else:
                    clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        # uzupełnianie brakujących klauzul z powodu reszty z dzielenia
        half_of_remaining = (total_clauses - len(clauses)) // 2
        for _ in range(half_of_remaining):
            length = self.random.choice(clause_lengths)
            clauses.append(self._generate_safety_clause(length, atom_names))
            
        while len(clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        # ostateczne przetasowanie
        self.random.shuffle(clauses)

        return clauses