from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import (
    LogicToken,
    Conjunction,
    Implication,
    Alternative,
    Not,
    Atom,
    ForAll,
    Exists,
    GreaterThan,
)


@dataclass
class Problem15(Generator):
    name = "15"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "conflict_percent": StandardParams.CONFLICT_PERCENT.value,
        "conflict_type": StandardParams.CONFLICT_TYPE.value,
        "conflict_depth": StandardParams.CONFLICT_DEPTH.value,
    }
    presets = {
        "Base (0%)": {"clauses": 100, "lengths": [2, 3, 4, 6], "conflict_percent": 0.0, "conflict_type": "c1", "conflict_depth": "v1"},
        "C1-Direct-Local (5%)": {"clauses": 200, "lengths": [2, 3, 4, 6], "conflict_percent": 5.0, "conflict_type": "c1", "conflict_depth": "v1"},
        "C2-Cond-Near (10%)": {"clauses": 500, "lengths": [2, 3, 4, 6], "conflict_percent": 10.0, "conflict_type": "c2", "conflict_depth": "v2"},
        "C3-Behav-Dist (1%)": {"clauses": 1000, "lengths": [2, 3, 4, 6], "conflict_percent": 1.0, "conflict_type": "c3", "conflict_depth": "v3"},
    }

    def validate_extra(self) -> str | None:
        c_type: str = self.params.get("conflict_type")  # type: ignore
        c_depth: str = self.params.get("conflict_depth")  # type: ignore
        
        if c_type not in ["c1", "c2", "c3"]:
            return f"Conflict type '{c_type}' is not supported. Allowed: 'c1', 'c2', 'c3'."
        if c_depth not in ["v1", "v2", "v3"]:
            return f"Conflict depth '{c_depth}' is not supported. Allowed: 'v1', 'v2', 'v3'."
            
        return None

    def _create_conflict_chain(self, c_type: str, c_depth: str, atom_names: list[str]) -> List[LogicToken]:
        """generuje niezależny łańcuch klauzul o zadanym profilu gwarantujący sprzeczność (unsat)."""
        # pobieramy 4 unikalne atomy do budowy łańcucha wnioskowania
        A, B, C, D = self.random.sample(atom_names, 4)
        
        # helpery do precyzyjnego budowania tokenów
        def atom(name): return Atom(name, "U")
        def not_atom(name): return Not(Atom(name, "U"))
        def impl(p, c): return Implication(p, c)
        def forall(token): return ForAll("U", token)

        if c_type == "c1":
            # C1: bezposrednie (A oraz ~A)
            if c_depth == "v1":
                return [forall(atom(A)), forall(not_atom(A))]
            elif c_depth == "v2":
                return [forall(atom(A)), forall(impl(atom(A), atom(B))), forall(not_atom(B))]
            else: # v3
                return [forall(atom(A)), forall(impl(atom(A), atom(B))), forall(impl(atom(B), atom(C))), forall(not_atom(C))]
                
        elif c_type == "c2":
            # C2: warunkowe (A => B oraz A => ~B)
            if c_depth == "v1":
                return [forall(atom(A)), forall(impl(atom(A), atom(B))), forall(impl(atom(A), not_atom(B)))]
            elif c_depth == "v2":
                return [forall(atom(A)), forall(impl(atom(A), atom(B))), forall(impl(atom(B), atom(C))), forall(impl(atom(A), not_atom(C)))]
            else: # v3
                return [forall(atom(A)), forall(impl(atom(A), atom(B))), forall(impl(atom(B), atom(C))), forall(impl(atom(C), atom(D))), forall(impl(atom(A), not_atom(D)))]
                
        elif c_type == "c3":
            # C3: behawioralne (safety vs liveness)
            def liveness(pre, cons):
                return ForAll("U", Exists("V", Conjunction([
                    GreaterThan("U", "V"),
                    Implication(Atom(pre, "V"), Atom(cons, "U"))
                ])))
                
            if c_depth == "v1":
                return [forall(atom(A)), liveness(A, B), forall(not_atom(B))]
            elif c_depth == "v2":
                return [forall(atom(A)), liveness(A, B), forall(impl(atom(B), atom(C))), forall(not_atom(C))]
            else: # v3
                return [forall(atom(A)), liveness(A, B), forall(impl(atom(B), atom(C))), forall(impl(atom(C), atom(D))), forall(not_atom(D))]
        
        return []

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        percent: float = self.params.get("conflict_percent")  # type: ignore
        c_type: str = self.params.get("conflict_type")  # type: ignore
        c_depth: str = self.params.get("conflict_depth")  # type: ignore

        # min 4 atomy do zbudowania najdłuższego łańcucha v3
        num_atoms = max(4, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # 1. budowanie klauzul konfliktowych
        conflict_clauses: List[LogicToken] = []
        target_conflict_count = round(total_clauses * (percent / 100.0))

        while len(conflict_clauses) < target_conflict_count:
            chain = self._create_conflict_chain(c_type, c_depth, atom_names)
            conflict_clauses.extend(chain)

        # 2. generowanie pozostałych standardowych klauzul (50:50)
        normal_target = max(0, total_clauses - len(conflict_clauses))
        normal_clauses: List[LogicToken] = []
        
        if normal_target > 0:
            num_per_length = normal_target // len(clause_lengths)
            safety_per_length = num_per_length // 2

            for length in clause_lengths:
                for i in range(num_per_length):
                    is_safety = i < safety_per_length
                    if is_safety:
                        normal_clauses.append(self._generate_safety_clause(length, atom_names))
                    else:
                        normal_clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

            half_remaining = (normal_target - len(normal_clauses)) // 2
            for _ in range(half_remaining):
                length = self.random.choice(clause_lengths)
                normal_clauses.append(self._generate_safety_clause(length, atom_names))
                
            while len(normal_clauses) < normal_target:
                length = self.random.choice(clause_lengths)
                normal_clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        # 3. łączenie i przemieszanie (aby złośliwie rozrzucić konfliktowe po całym pliku)
        all_clauses = conflict_clauses + normal_clauses
        self.random.shuffle(all_clauses)

        return all_clauses