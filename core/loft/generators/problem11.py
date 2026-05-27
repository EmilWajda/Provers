import copy
from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import (
    LogicToken,
    Conjunction,
    Implication,
    Not,
    Alternative,
    ForAll,
    Exists,
)


@dataclass
class Problem11(Generator):
    name = "11"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "redundancy_percent": StandardParams.REDUNDANCY_PERCENT.value,
        "redundancy_mode": StandardParams.REDUNDANCY_MODE.value,
    }
    presets = {
        "R0%": {"clauses": 100, "lengths": [2, 3, 4, 6], "redundancy_percent": 0.0, "redundancy_mode": "t1"},
        "R10%": {"clauses": 200, "lengths": [2, 3, 4, 6], "redundancy_percent": 10.0, "redundancy_mode": "t2"},
        "R25%": {"clauses": 500, "lengths": [2, 3, 4, 6], "redundancy_percent": 25.0, "redundancy_mode": "t3"},
        "R50%": {"clauses": 1000, "lengths": [2, 3, 4, 6], "redundancy_percent": 50.0, "redundancy_mode": "t4"},
    }

    def validate_extra(self) -> str | None:
        return None

    def _create_redundant_clause(self, base_clause: LogicToken) -> LogicToken:
        """tworzy redundantną klauzulę na podstawie istniejącej poprzez r1, r2 lub r3."""
        op = self.random.choice(["R1", "R2", "R3"])
        
        # r1: proste skopiowanie istniejącej klauzuli
        if op == "R1":
            return copy.deepcopy(base_clause)
            
        new_c = copy.deepcopy(base_clause)
        
        # modyfikacje drzewa ast tokenów (r2 i r3)
        try:
            if isinstance(new_c, ForAll):
                # struktura safety: ForAll(U, Not(Alternative(literals)))
                if isinstance(new_c.formula, Not) and isinstance(new_c.formula.token, Alternative):
                    alts = new_c.formula.token.tokens
                    
                    if op == "R2":
                        # r2: zmiana kolejności literałów
                        self.random.shuffle(alts)
                    elif op == "R3" and len(alts) > 1:
                        # r3: podzbiór literałów (usunięcie jednego elementu wzmacnia klauzulę)
                        alts.pop(self.random.randrange(len(alts)))
                        
                # struktura liveness: ForAll(U, Exists(V, Conjunction([GreaterThan, Implication(pre, cons)])))
                elif isinstance(new_c.formula, Exists) and isinstance(new_c.formula.formula, Conjunction):
                    body = new_c.formula.formula
                    if len(body.tokens) == 2 and isinstance(body.tokens[1], Implication):
                        impl = body.tokens[1]
                        if isinstance(impl.premise, Alternative) and isinstance(impl.conclusion, Alternative):
                            pre_alts = impl.premise.tokens
                            cons_alts = impl.conclusion.tokens
                            
                            if op == "R2":
                                self.random.shuffle(pre_alts)
                                self.random.shuffle(cons_alts)
                            elif op == "R3":
                                # wybieramy czy ucinamy z poprzednika czy następnika
                                choices = []
                                if len(pre_alts) > 1: choices.append(pre_alts)
                                if len(cons_alts) > 1: choices.append(cons_alts)
                                if choices:
                                    target = self.random.choice(choices)
                                    target.pop(self.random.randrange(len(target)))
        except Exception:
            # fallback do r1 w razie jakiejkolwiek niespójności strukturalnej
            pass
            
        return new_c

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        redundancy_percent: float = self.params.get("redundancy_percent")  # type: ignore
        mode: str = self.params.get("redundancy_mode")  # type: ignore

        # wspólny zbiór atomów 
        num_atoms = max(1, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # 1. generowanie formuły bazowej f (z zachowaniem zasady 50:50 i logiki P1)
        clauses_f: List[LogicToken] = []
        num_per_length = total_clauses // len(clause_lengths)
        safety_per_length = num_per_length // 2

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length
                if is_safety:
                    clauses_f.append(self._generate_safety_clause(length, atom_names))
                else:
                    clauses_f.append(self._generate_liveness_clause(max(2, length), atom_names))

        half_of_remaining = (total_clauses - len(clauses_f)) // 2
        for _ in range(half_of_remaining):
            length = self.random.choice(clause_lengths)
            clauses_f.append(self._generate_safety_clause(length, atom_names))
            
        while len(clauses_f) < total_clauses:
            length = self.random.choice(clause_lengths)
            clauses_f.append(self._generate_liveness_clause(max(2, length), atom_names))

        # 2. tworzenie formuły f' poprzez doklejenie redundantnych klauzul
        clauses_f_prime = list(clauses_f)
        num_redundant = round(total_clauses * (redundancy_percent / 100.0))

        for _ in range(num_redundant):
            base_clause = self.random.choice(clauses_f)
            redundant_clause = self._create_redundant_clause(base_clause)
            clauses_f_prime.append(redundant_clause)

        # mieszamy f', aby redundantne klauzule nie lądowały zawsze na samym końcu
        self.random.shuffle(clauses_f_prime)

        # opakowanie w koniunkcje
        F = Conjunction(clauses_f)  # type: ignore
        F_prime = Conjunction(clauses_f_prime)  # type: ignore

        # 3. testowane relacje
        if mode == "t1":
            part1 = Implication(F, F_prime)  # type: ignore
            part2 = Implication(F_prime, F)  # type: ignore
            return [Conjunction([part1, part2])]  # type: ignore
        elif mode == "t2":
            return [Implication(F_prime, F)]  # type: ignore
        elif mode == "t3":
            return [Implication(F, F_prime)]  # type: ignore
        elif mode == "t4":
            return [Conjunction([F, F_prime])]  # type: ignore

        return []