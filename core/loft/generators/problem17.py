from dataclasses import dataclass
from typing import List

from .generator import Generator
from .std_params import StandardParams
from ..formulas import (
    LogicToken,
    BasicToken,
    Alternative,
    Conjunction,
    Implication,
    Not,
    Atom,
    ForAll,
    Exists,
    GreaterThan,
)


@dataclass
class Problem17(Generator):
    name = "17"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "lengths": StandardParams.LENGTHS.value,
        "horn_percent": StandardParams.HORN_PERCENT.value,
    }
    presets = {
        "100% Horn": {"clauses": 500, "lengths": [2, 3, 4, 6], "horn_percent": 100.0},
        "75% Horn": {"clauses": 500, "lengths": [2, 3, 4, 6], "horn_percent": 75.0},
        "50% Horn": {"clauses": 500, "lengths": [2, 3, 4, 6], "horn_percent": 50.0},
        "25% Horn": {"clauses": 500, "lengths": [2, 3, 4, 6], "horn_percent": 25.0},
        "0% Horn": {"clauses": 500, "lengths": [2, 3, 4, 6], "horn_percent": 0.0},
    }

    def validate_extra(self) -> str | None:
        return None

    def _generate_specific_safety_clause(self, length: int, atom_names: list[str], is_horn: bool) -> LogicToken:
        """generuje klauzulę safety z narzuconą kontrolą literałów pozytywnych (horn vs non-horn)"""
        # nie-hornowska musi mieć >= 2 literały pozytywne, więc długość klauzuli musi wynosić min. 2
        if not is_horn:
            length = max(2, length)

        chosen_atoms = self.random.sample(atom_names, k=min(length, len(atom_names)))
        actual_length = len(chosen_atoms)

        # logika hornowska: max 1 pozytywny (dla klauzuli pustej 0)
        if is_horn:
            pos_count = self.random.choice([0, 1]) if actual_length > 0 else 0
        else:
            pos_count = self.random.randint(2, actual_length) if actual_length >= 2 else actual_length

        polarities = [True] * pos_count + [False] * (actual_length - pos_count)
        self.random.shuffle(polarities)

        literals: List[BasicToken] = []
        for name, is_positive in zip(chosen_atoms, polarities):
            atom = Atom(name, "U")
            if not is_positive:
                atom = Not(atom)
            literals.append(atom)

        return ForAll("U", Not(Alternative(literals)))

    def _generate_specific_liveness_clause(self, length: int, atom_names: list[str], is_horn: bool) -> LogicToken:
        """generuje klauzulę liveness z narzuconą kontrolą literałów pozytywnych (horn vs non-horn)"""
        length = max(2, length)

        k_pred = self.random.randint(1, length - 1)
        k_cons = length - k_pred

        chosen_pred = self.random.sample(atom_names, k=min(k_pred, len(atom_names)))
        chosen_cons = self.random.sample(atom_names, k=min(k_cons, len(atom_names)))

        actual_len = len(chosen_pred) + len(chosen_cons)

        if is_horn:
            pos_count = self.random.choice([0, 1]) if actual_len > 0 else 0
        else:
            pos_count = self.random.randint(2, actual_len) if actual_len >= 2 else actual_len

        polarities = [True] * pos_count + [False] * (actual_len - pos_count)
        self.random.shuffle(polarities)

        pred_pols = polarities[:len(chosen_pred)]
        cons_pols = polarities[len(chosen_pred):]

        lit_pred: List[BasicToken] = []
        for name, is_positive in zip(chosen_pred, pred_pols):
            atom = Atom(name, "V")
            if not is_positive:
                atom = Not(atom)
            lit_pred.append(atom)

        lit_cons: List[BasicToken] = []
        for name, is_positive in zip(chosen_cons, cons_pols):
            atom = Atom(name, "U")
            if not is_positive:
                atom = Not(atom)
            lit_cons.append(atom)

        body = Conjunction([GreaterThan("U", "V"), Implication(Alternative(lit_pred), Alternative(lit_cons))])
        return ForAll("U", Exists("V", body))

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore
        horn_percent: float = self.params.get("horn_percent")  # type: ignore

        num_atoms = max(1, total_clauses // 2)
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # wyliczenie konkretnej liczby klauzul hornowskich do wygenerowania
        horn_count = round(total_clauses * (horn_percent / 100.0))
        non_horn_count = total_clauses - horn_count

        # tworzymy pulę atrybutów "is_horn" aby mieć idealną dystrybucję globalną
        horn_pool = [True] * horn_count + [False] * non_horn_count
        self.random.shuffle(horn_pool)

        clauses: List[LogicToken] = []
        
        num_per_length = total_clauses // len(clause_lengths)
        safety_per_length = num_per_length // 2

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length
                # bezpiecznie pobieramy atrybut z puli (w razie błędu ułamków zakładamy True jako default)
                is_horn = horn_pool.pop() if horn_pool else True
                
                if is_safety:
                    clauses.append(self._generate_specific_safety_clause(length, atom_names, is_horn))
                else:
                    clauses.append(self._generate_specific_liveness_clause(length, atom_names, is_horn))

        # uzupełnianie brakujących klauzul po reszcie z dzielenia
        half_of_remaining = (total_clauses - len(clauses)) // 2
        for _ in range(half_of_remaining):
            length = self.random.choice(clause_lengths)
            is_horn = horn_pool.pop() if horn_pool else True
            clauses.append(self._generate_specific_safety_clause(length, atom_names, is_horn))

        while len(clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            is_horn = horn_pool.pop() if horn_pool else True
            clauses.append(self._generate_specific_liveness_clause(length, atom_names, is_horn))

        # ostateczne przetasowanie 
        self.random.shuffle(clauses)

        return clauses