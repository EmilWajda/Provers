from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import (
    LogicToken,
    Conjunction,
    Implication,
    Not,
)


@dataclass
class Problem10(Generator):
    name = "10"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "modification_percent": StandardParams.MODIFICATION_PERCENT.value,
        "evolution_mode": StandardParams.EVOLUTION_MODE.value,
    }
    presets = {
        "P5%": {"clauses": 100, "lengths": [2, 3, 4, 6], "modification_percent": 5.0, "evolution_mode": "r1"},
        "P10%": {"clauses": 200, "lengths": [2, 3, 4, 6], "modification_percent": 10.0, "evolution_mode": "r2"},
        "P20%": {"clauses": 500, "lengths": [2, 3, 4, 6], "modification_percent": 20.0, "evolution_mode": "r3"},
        "P50%": {"clauses": 100, "lengths": [2, 3, 4, 6], "modification_percent": 50.0, "evolution_mode": "r4"},
    }

    def validate_extra(self) -> str | None:
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        p: float = self.params.get("modification_percent")  # type: ignore
        mode: str = self.params.get("evolution_mode")  # type: ignore

        # liczba atomów i ich nazwy (wspólny zbiór dla obu formuł)
        num_atoms = max(1, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # generowanie formuły bazowej f1
        clauses_f1: List[LogicToken] = []
        num_per_length = total_clauses // len(clause_lengths)
        safety_per_length = num_per_length // 2

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length
                if is_safety:
                    clauses_f1.append(self._generate_safety_clause(length, atom_names))
                else:
                    clauses_f1.append(self._generate_liveness_clause(max(2, length), atom_names))

        # uzupełnianie brakujących klauzul dla f1
        half_of_remaining = (total_clauses - len(clauses_f1)) // 2
        for _ in range(half_of_remaining):
            length = self.random.choice(clause_lengths)
            clauses_f1.append(self._generate_safety_clause(length, atom_names))
            
        while len(clauses_f1) < total_clauses:
            length = self.random.choice(clause_lengths)
            clauses_f1.append(self._generate_liveness_clause(max(2, length), atom_names))

        # kopiujemy strukturę dla f2 przed mutacjami
        clauses_f2 = list(clauses_f1)

        # wyliczamy fizyczną liczbę mutacji na podstawie parametru p%
        num_changes = round(total_clauses * (p / 100.0))

        # symulacja ewolucji modelu (modyfikacja M1, M2 lub M3)
        for _ in range(num_changes):
            op = self.random.choice(["M1", "M2", "M3"])
            
            if op == "M1" and clauses_f2:
                # m1: usunięcie losowej klauzuli
                idx = self.random.randrange(len(clauses_f2))
                clauses_f2.pop(idx)
                
            elif op == "M2":
                # m2: dodanie nowej klauzuli
                length = self.random.choice(clause_lengths)
                if self.random.random() < 0.5:
                    clauses_f2.append(self._generate_safety_clause(length, atom_names))
                else:
                    clauses_f2.append(self._generate_liveness_clause(max(2, length), atom_names))
                    
            elif op == "M3" and clauses_f2:
                # m3: zamiana klauzuli na nową
                idx = self.random.randrange(len(clauses_f2))
                clauses_f2.pop(idx)
                
                length = self.random.choice(clause_lengths)
                if self.random.random() < 0.5:
                    clauses_f2.append(self._generate_safety_clause(length, atom_names))
                else:
                    clauses_f2.append(self._generate_liveness_clause(max(2, length), atom_names))

        # opakowanie w finalne struktury f1 i f2
        F1 = Conjunction(clauses_f1) # type: ignore
        F2 = Conjunction(clauses_f2) if clauses_f2 else Conjunction(clauses_f1[:1]) # type: ignore

        # testowane relacje ewolucyjne
        if mode == "r1":
            return [Implication(F1, F2)]  # type: ignore
        elif mode == "r2":
            return [Implication(F2, F1)]  # type: ignore
        elif mode == "r3":
            return [Conjunction([F1, Not(F2)])]  # type: ignore
        elif mode == "r4":
            return [Conjunction([F1, F2])]  # type: ignore

        return []