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
class Problem14(Generator):
    name = "14"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,  # traktowane jako liczba klauzul na JEDEN moduł
        "lengths": StandardParams.LENGTHS.value,
        "modules_count": StandardParams.MODULES_COUNT.value,
        "coupling_variant": StandardParams.COUPLING_VARIANT.value,
        "modular_mode": StandardParams.MODULAR_MODE.value,
    }
    presets = {
        "C1-Independent": {
            "clauses": 100,
            "lengths": [2, 3, 4, 6],
            "modules_count": 3,
            "coupling_variant": "c1",
            "modular_mode": "locality",
        },
        "C2-Weakly": {
            "clauses": 100,
            "lengths": [2, 3, 4, 6],
            "modules_count": 3,
            "coupling_variant": "c2",
            "modular_mode": "globality",
        },
        "C3-Medium": {
            "clauses": 200,
            "lengths": [2, 3, 4, 6],
            "modules_count": 5,
            "coupling_variant": "c3",
            "modular_mode": "co-sat",
        },
        "C4-Strongly": {
            "clauses": 50,
            "lengths": [2, 3, 4, 6],
            "modules_count": 2,
            "coupling_variant": "c4",
            "modular_mode": "globality",
        },
    }

    def validate_extra(self) -> str | None:
        mode: str = self.params.get("modular_mode")  # type: ignore
        allowed_modes = ["locality", "globality", "co-sat"]
        if mode not in allowed_modes:
            return f"Modular mode '{mode}' is not supported in Problem 14. Allowed modes are 'locality', 'globality', 'co-sat'."

        variant: str = self.params.get("coupling_variant")  # type: ignore
        if variant not in ["c1", "c2", "c3", "c4"]:
            return f"Coupling variant '{variant}' is not supported. Use 'c1', 'c2', 'c3', or 'c4'."

        return None

    def _generate_module(self, num_clauses: int, atom_names: list[str], clause_lengths: list[int]) -> LogicToken:
        """generuje pojedynczy moduł gwarantując 50:50 liveness/safety oraz użycie wszystkich atomów."""
        safety_coeff = 0.5
        num_per_length = num_clauses // len(clause_lengths)
        safety_per_length = round(num_per_length * safety_coeff)

        clauses: List[LogicToken] = []

        # lista nieużytych atomów, by zagwarantować 100% pokrycia dla każdego modułu
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
        clauses_per_module: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        modules_count: int = self.params.get("modules_count")  # type: ignore
        variant: str = self.params.get("coupling_variant")  # type: ignore
        mode: str = self.params.get("modular_mode")  # type: ignore

        # 1. ustalanie proporcji współdzielonych atomów (interfejsów)
        if variant == "c1":
            shared_ratio = 0.0
        elif variant == "c2":
            shared_ratio = 0.10  # górna granica 5-10% dla wyraźnego efektu
        elif variant == "c3":
            shared_ratio = 0.25
        elif variant == "c4":
            shared_ratio = 0.50
        else:
            shared_ratio = 0.0

        # całkowita pula atomów na JEDEN moduł
        num_atoms_per_module = max(1, clauses_per_module // 2)
        num_shared = round(num_atoms_per_module * shared_ratio)
        num_unique = num_atoms_per_module - num_shared

        # wspólny zbiór atomów dla wszystkich modułów
        shared_atoms = [f"shared_var{i+1}" for i in range(num_shared)]

        modules: List[LogicToken] = []
        module_atoms_list: List[List[str]] = []

        # 2. generowanie niezależnych modułów
        for m in range(modules_count):
            # lokalne atomy specyficzne tylko dla tego modułu
            unique_atoms = [f"m{m+1}_var{i+1}" for i in range(num_unique)]
            current_atoms = shared_atoms + unique_atoms
            module_atoms_list.append(current_atoms)

            mod_token = self._generate_module(clauses_per_module, current_atoms, clause_lengths)
            modules.append(mod_token)

        # 3. utworzenie klauzuli testowej r na bazie modułu nr 1 (M_i)
        target_module_idx = 0
        target_atoms = module_atoms_list[target_module_idx]
        M_i = modules[target_module_idx]

        r_length = self.random.choice(clause_lengths)
        if self.random.random() < 0.5:
            R = self._generate_safety_clause(r_length, target_atoms)
        else:
            R = self._generate_liveness_clause(max(2, r_length), target_atoms)

        # 4. model globalny g
        G = Conjunction(modules)  # type: ignore

        # 5. testowane relacje modularne
        if mode == "locality":
            return [Implication(M_i, R)]  # type: ignore
        elif mode == "globality":
            return [Implication(G, R)]  # type: ignore
        elif mode == "co-sat":
            return [Conjunction([G, R])]  # type: ignore

        return []
