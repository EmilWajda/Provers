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
class Problem9b(Generator):
    name = "9b"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "mode": StandardParams.MODE.value,
        "semantic_case": StandardParams.SEMANTIC_CASE.value,
    }
    presets = {
        "Contradictory Case1": {"clauses": 100, "lengths": [2, 3, 4, 6], "mode": "contradictory", "semantic_case": "case1"},
        "Subalternated Case1": {"clauses": 100, "lengths": [2, 3, 4, 6], "mode": "subalternated", "semantic_case": "case1"},
        "Subalternated Case2": {"clauses": 100, "lengths": [2, 3, 4, 6], "mode": "subalternated", "semantic_case": "case2"},
    }

    def validate_extra(self) -> str | None:
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
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        mode: str = self.params.get("mode")  # type: ignore
        semantic_case: str = self.params.get("semantic_case")  # type: ignore

        # generujemy wspólną pulę atomów
        num_atoms = max(1, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        if semantic_case == "case1":
            F1 = self._generate_formula(total_clauses, 80.0, atom_names, clause_lengths)
            F2 = self._generate_formula(total_clauses, 20.0, atom_names, clause_lengths)
        else:
            F1 = self._generate_formula(total_clauses, 20.0, atom_names, clause_lengths)
            F2 = self._generate_formula(total_clauses, 80.0, atom_names, clause_lengths)

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