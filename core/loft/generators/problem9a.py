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
class Problem9a(Generator):
    name = "9a"
    param_spec = {
        "clauses_f1": StandardParams.CLAUSES_F1.value,
        "clauses_f2": StandardParams.CLAUSES_F2.value,
        "lengths": StandardParams.LENGTHS.value,
        "mode": StandardParams.MODE.value,
    }
    presets = {
        "Default": {"clauses_f1": 50, "clauses_f2": 500, "lengths": [2, 3, 4, 6], "mode": "subalternated"},
        "Medium": {"clauses_f1": 100, "clauses_f2": 1000, "lengths": [2, 3, 4, 6], "mode": "subalternated"},
        "Large": {"clauses_f1": 200, "clauses_f2": 2000, "lengths": [2, 3, 4, 6], "mode": "subalternated"},
    }

    def validate_extra(self) -> str | None:
        clauses_f1: int = self.params.get("clauses_f1")  # type: ignore
        if clauses_f1 < 2:
            return "CLAUSES_F1 must be at least 2 for structural asymmetry."
        return None

    def _generate_formula(self, num_clauses: int, safety_percentage: float, atom_names: list[str], clause_lengths: list[int]) -> LogicToken:
        """generuje pojedynczą formułę gwarantując zadany procent liveness/safety oraz użycie wszystkich atomów."""
        safety_coeff = safety_percentage / 100.0
        num_per_length = num_clauses // len(clause_lengths)
        safety_per_length = round(num_per_length * safety_coeff)

        clauses: List[LogicToken] = []
        
        # lista nieużytych atomów, by zagwarantować, że każdy wystąpi co najmniej raz
        unused_atoms = list(atom_names)
        self.random.shuffle(unused_atoms)

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length
                
                chosen_atoms = []
                while unused_atoms and len(chosen_atoms) < length:
                    chosen_atoms.append(unused_atoms.pop())
                
                if len(chosen_atoms) < length:
                    needed = length - len(chosen_atoms)
                    remaining_pool = [a for a in atom_names if a not in chosen_atoms]
                    if len(remaining_pool) >= needed:
                        chosen_atoms.extend(self.random.sample(remaining_pool, needed))
                    else:
                        chosen_atoms.extend(remaining_pool)
                        while len(chosen_atoms) < length:
                            chosen_atoms.append(self.random.choice(atom_names))
                
                if is_safety:
                    clauses.append(self._generate_safety_clause(length, chosen_atoms))
                else:
                    clauses.append(self._generate_liveness_clause(max(2, length), chosen_atoms))

        half_of_remaining = round((num_clauses - len(clauses)) * safety_coeff)
        for _ in range(half_of_remaining):
            length = self.random.choice(clause_lengths)
            clauses.append(self._generate_safety_clause(length, atom_names))
            
        while len(clauses) < num_clauses:
            length = self.random.choice(clause_lengths)
            clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        self.random.shuffle(clauses)
        return Conjunction(clauses)  # type: ignore

    def generate(self) -> list[LogicToken]:
        clauses_f1: int = self.params.get("clauses_f1")  # type: ignore
        clauses_f2: int = self.params.get("clauses_f2")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        mode: str = self.params.get("mode")  # type: ignore

        # ustalenie wspólnego zbioru atomów opartego o F1, aby pokrycie było matematycznie możliwe
        num_atoms = max(1, clauses_f1 // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # asymetria strukturalna narzuca rozkład 50:50 dla obu formuł
        F1 = self._generate_formula(clauses_f1, 50.0, atom_names, clause_lengths)
        F2 = self._generate_formula(clauses_f2, 50.0, atom_names, clause_lengths)

        if mode == "contradictory":
            part1 = Implication(F1, Not(F2))  # type: ignore
            part2 = Implication(Not(F1), F2)  # type: ignore
            return [Conjunction([part1, part2])]  # type: ignore
            
        elif mode == "subcontrary":
            inner = Conjunction([Not(F1), Not(F2)])  # type: ignore
            return [Not(inner)]  # type: ignore
            
        elif mode == "subalternated":
            part1 = Implication(F1, F2)  # type: ignore
            part2 = Not(Implication(F2, F1))  # type: ignore
            return [Conjunction([part1, part2])]  # type: ignore

        return []