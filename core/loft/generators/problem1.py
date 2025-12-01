from dataclasses import dataclass
from typing import List

from .generator import Generator
from ..formulas import (
    LogicToken,
    ForAll,
    Exists,
    Not,
    Alternative,
    Implication,
    GreaterThan,
    Atom,
    Conjunction,
    BasicToken,
)


@dataclass
class Problem1(Generator):
    name = "Problem 1"
    param_spec = {"clauses": int, "lengths": list[int]}

    def generate(self) -> list[LogicToken]:
        total_clauses: int = self.params.get("clauses")  # type: ignore
        clause_lengths: list[int] = self.params.get("lengths")  # type: ignore

        # walidacja pewnych przypadków
        if not clause_lengths:
            raise ValueError("Lista długości klauzul (params['lengths']) nie może być pusta.")
        if len(clause_lengths) > total_clauses:
            raise ValueError(
                f"Liczba różnych długości klauzul ({len(clause_lengths)}) "
                f"nie może przekraczać całkowitej liczby klauzul ({total_clauses})."
            )

        num_per_length = total_clauses // len(clause_lengths)
        safety_per_length = num_per_length // 2

        # liczba atomów i ich nazwy
        num_atoms = total_clauses // 2
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # generowanie klauzul
        clauses: List[LogicToken] = []

        for length in clause_lengths:
            for i in range(num_per_length):
                is_safety = i < safety_per_length

                if is_safety:
                    clause = self._generate_safety_clause(length, atom_names, "U")
                else:
                    clause = self._generate_liveness_clause(length, atom_names, ["U", "V"])

                clauses.append(clause)

        # generowanie pozostalych brakujących klauzul jesli istnieją
        half_of_remaining_clauses = (total_clauses - len(clauses)) // 2

        for _ in range(half_of_remaining_clauses):
            length = self.random.choice(clause_lengths)
            clause = self._generate_safety_clause(length, atom_names, "U")
            clauses.append(clause)

        while len(clauses) < total_clauses:
            length = self.random.choice(clause_lengths)
            clause = self._generate_liveness_clause(length, atom_names, ["U", "V"])
            clauses.append(clause)

        return clauses

    def _generate_safety_clause(self, length: int, atom_names: list[str], parameter: str) -> LogicToken:
        """Generuje pojedynczą klauzulę bezpieczeństwa o zadanej długości i parametrze (U)."""
        chosen_atoms = self.random.sample(atom_names, k=min(length, len(atom_names)))
        literals: list[BasicToken] = []

        for name in chosen_atoms:
            atom = Atom(name, parameter)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals.append(atom)

        return ForAll(parameter, Not(Alternative(literals)))

    def _generate_liveness_clause(self, length: int, atom_names: list[str], parameters: list[str]) -> LogicToken:
        """Generuje pojedynczą klauzulę żywotnościową o zadanej długości i parametrach (U oraz V)."""

        # walidacja
        if len(parameters) != 2:
            raise ValueError("parameters powinno mieć dokładnie 2 elementy, np. ['U', 'V'].")
        if length < 2:
            raise ValueError("length musi być >= 2, żeby poprzednik i następnik nie były puste.")

        U, V = parameters[0], parameters[1]
        k_pred = self.random.randint(1, length - 1)
        k_cons = length - k_pred

        chosen_pred_atoms = self.random.sample(atom_names, k=min(k_pred, len(atom_names)))
        chosen_cons_atoms = self.random.sample(atom_names, k=min(k_cons, len(atom_names)))

        literals_predecessor: list[BasicToken] = []
        literals_consequent: list[BasicToken] = []

        # budowanie listy literałów poprzednika
        for name in chosen_pred_atoms:
            atom = Atom(name, V)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals_predecessor.append(atom)

        # budowanie listy literałów następnika
        for name in chosen_cons_atoms:
            atom = Atom(name, U)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals_consequent.append(atom)

        predecessor_or = Alternative(literals_predecessor)
        consequent_or = Alternative(literals_consequent)

        implication = Implication(predecessor_or, consequent_or)
        gte = GreaterThan(U, V)
        body = Conjunction([gte, implication])

        return ForAll(U, Exists(V, body))
