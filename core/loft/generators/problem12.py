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
class Problem12(Generator):
    name = "12"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "degradation_percent": StandardParams.DEGRADATION_PERCENT.value,
        "degradation_variant": StandardParams.DEGRADATION_VARIANT.value,
        "missing_info_mode": StandardParams.MISSING_INFO_MODE.value,
    }
    presets = {
        "D1-Random 5%": {"clauses": 200, "lengths": [2, 3, 4, 6], "degradation_percent": 5.0, "degradation_variant": "d1", "missing_info_mode": "r1"},
        "D2-SafetyPref 10%": {"clauses": 500, "lengths": [2, 3, 4, 6], "degradation_percent": 10.0, "degradation_variant": "d2", "missing_info_mode": "r2"},
        "D3-LivenessPref 25%": {"clauses": 1000, "lengths": [2, 3, 4, 6], "degradation_percent": 25.0, "degradation_variant": "d3", "missing_info_mode": "r3"},
        "D1-Random 50%": {"clauses": 200, "lengths": [2, 3, 4, 6], "degradation_percent": 50.0, "degradation_variant": "d1", "missing_info_mode": "r4"},
    }

    def validate_extra(self) -> str | None:
        return None

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        percent: float = self.params.get("degradation_percent")  # type: ignore
        variant: str = self.params.get("degradation_variant")  # type: ignore
        mode: str = self.params.get("missing_info_mode")  # type: ignore

        # zbiór atomów
        num_atoms = max(1, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # 1. generowanie formuły f z podziałem 50:50 na osobne pule (ułatwi to usuwanie d2/d3)
        safety_clauses: List[LogicToken] = []
        liveness_clauses: List[LogicToken] = []
        
        num_per_length = total_clauses // len(clause_lengths)
        safety_per_length = num_per_length // 2

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length
                if is_safety:
                    safety_clauses.append(self._generate_safety_clause(length, atom_names))
                else:
                    liveness_clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        # uzupełnianie brakujących
        half_of_remaining = (total_clauses - (len(safety_clauses) + len(liveness_clauses))) // 2
        for _ in range(half_of_remaining):
            length = self.random.choice(clause_lengths)
            safety_clauses.append(self._generate_safety_clause(length, atom_names))
            
        while len(safety_clauses) + len(liveness_clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            liveness_clauses.append(self._generate_liveness_clause(max(2, length), atom_names))

        # pełna formuła bazowa f
        all_clauses = safety_clauses + liveness_clauses
        self.random.shuffle(all_clauses)
        F = Conjunction(all_clauses)  # type: ignore

        # 2. utworzenie klauzuli testowej r (prosta klauzula liveness)
        r_length = self.random.choice([2, 3])
        R = self._generate_liveness_clause(r_length, atom_names)

        # 3. tworzenie formuły f' (degradacja)
        num_to_remove = round(total_clauses * (percent / 100.0))
        
        # kopiujemy i mieszamy pule robocze
        s_pool = list(safety_clauses)
        l_pool = list(liveness_clauses)
        self.random.shuffle(s_pool)
        self.random.shuffle(l_pool)
        
        clauses_f_prime: List[LogicToken] = []

        if variant == "d1":
            # d1: usunięcie całkowicie losowe
            combined_pool = s_pool + l_pool
            self.random.shuffle(combined_pool)
            clauses_f_prime = combined_pool[num_to_remove:]
            
        elif variant == "d2":
            # d2: preferencja safety
            removed = 0
            while removed < num_to_remove and s_pool:
                s_pool.pop()
                removed += 1
            while removed < num_to_remove and l_pool:
                l_pool.pop()
                removed += 1
            clauses_f_prime = s_pool + l_pool
            
        elif variant == "d3":
            # d3: preferencja liveness
            removed = 0
            while removed < num_to_remove and l_pool:
                l_pool.pop()
                removed += 1
            while removed < num_to_remove and s_pool:
                s_pool.pop()
                removed += 1
            clauses_f_prime = s_pool + l_pool

        self.random.shuffle(clauses_f_prime)
        
        # fallback na pierwszą klauzulę bazową, gdyby percent wynosił 100%
        F_prime = Conjunction(clauses_f_prime) if clauses_f_prime else Conjunction(all_clauses[:1])  # type: ignore

        # 4. testowane relacje
        if mode == "r1":
            return [Implication(F, R)]  # type: ignore
        elif mode == "r2":
            return [Implication(F_prime, R)]  # type: ignore
        elif mode == "r3":
            return [Conjunction([F, Not(R)])]  # type: ignore
        elif mode == "r4":
            return [Conjunction([F_prime, Not(R)])]  # type: ignore

        return []