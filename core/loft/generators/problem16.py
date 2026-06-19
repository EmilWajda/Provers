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
)


@dataclass
class Problem16(Generator):
    name = "16"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "chain_length": StandardParams.CHAIN_LENGTH.value,
        "implication_mode": StandardParams.IMPLICATION_MODE.value,
    }
    presets = {
        "K2-Short": {"clauses": 100, "lengths": [2, 3, 4, 6], "chain_length": 2, "implication_mode": "t1"},
        "K10-Medium": {"clauses": 200, "lengths": [2, 3, 4, 6], "chain_length": 10, "implication_mode": "t1"},
        "K25-Long": {"clauses": 500, "lengths": [2, 3, 4, 6], "chain_length": 25, "implication_mode": "t2"},
        "K50-Deep": {"clauses": 500, "lengths": [2, 3, 4, 6], "chain_length": 50, "implication_mode": "t2"},
    }

    def validate_extra(self) -> str | None:
        k: int = self.params.get("chain_length")  # type: ignore
        total_clauses: int = self.params.get("clauses")  # type: ignore
        mode: str = self.params.get("implication_mode")  # type: ignore
        
        if mode not in ["t1", "t2"]:
            return f"Implication mode '{mode}' is not supported in Problem 16. Allowed: 't1', 't2'."
            
        if k < 2:
            return "Chain length (k) must be at least 2."
            
        if k - 1 > total_clauses:
            return f"Chain length implies {k-1} clauses, which exceeds total clauses limit ({total_clauses})."
            
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        k: int = self.params.get("chain_length")  # type: ignore
        mode: str = self.params.get("implication_mode")  # type: ignore

        # zapewniamy odpowiednią liczbę atomów, by swobodnie pomieścić łańcuch k-elementowy
        num_atoms = max(k, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # 1. generowanie łańcucha implikacji (kręgosłupa dowodu)
        # dla uproszczenia i uniknięcia cykli bierzemy pierwsze k atomów
        chain_atoms = atom_names[:k]
        chain_clauses: List[LogicToken] = []
        
        for i in range(k - 1):
            # klauzula równoważna implikacji: ~A_i v A_{i+1}
            A_i = chain_atoms[i]
            A_next = chain_atoms[i+1]
            clause = ForAll("U", Alternative([Not(Atom(A_i, "U")), Atom(A_next, "U")]))
            chain_clauses.append(clause)

        # 2. generowanie szumu tła (pozostałe klauzule z rygorystyczną proporcją 50:50)
        noise_target = total_clauses - len(chain_clauses)
        noise_clauses: List[LogicToken] = []
        
        if noise_target > 0:
            num_per_length = noise_target // len(clause_lengths)
            safety_per_length = num_per_length // 2

            for length in clause_lengths:
                for i in range(num_per_length):
                    is_safety = i < safety_per_length
                    if is_safety:
                        noise_clauses.append(self._generate_safety_clause(length, atom_names))
                    else:
                        noise_clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

            # uzupełnianie braków z powodu reszty z dzielenia
            half_remaining = (noise_target - len(noise_clauses)) // 2
            for _ in range(half_remaining):
                length = self.random.choice(clause_lengths)
                noise_clauses.append(self._generate_safety_clause(length, atom_names))
                
            while len(noise_clauses) < noise_target:
                length = self.random.choice(clause_lengths)
                noise_clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        # 3. łączenie i tasowanie, aby mocno ukryć łańcuch zależności w szumie
        all_clauses = chain_clauses + noise_clauses
        self.random.shuffle(all_clauses)
        
        F = Conjunction(all_clauses)  # type: ignore

        # 4. testowane relacje
        A_1 = chain_atoms[0]
        A_k = chain_atoms[-1]

        if mode == "t1":
            # T1: F => (A_1 => A_k)
            # implikację docelową opakowujemy w ForAll aby utrzymać zgodność logiczną FOL
            target = ForAll("U", Implication(Atom(A_1, "U"), Atom(A_k, "U")))
            return [Implication(F, target)]  # type: ignore
            
        elif mode == "t2":
            # T2: F ^ A_1 ^ ~A_k (test niesprzeczności - UNSAT)
            # dopinamy fakty A_1 oraz ~A_k na koniec koniunkcji
            a1_fact = ForAll("U", Atom(A_1, "U"))
            ak_not_fact = ForAll("U", Not(Atom(A_k, "U")))
            return [Conjunction([F, a1_fact, ak_not_fact])]  # type: ignore

        return []