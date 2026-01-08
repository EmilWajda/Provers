from dataclasses import dataclass
from typing import List, Any
from random import Random

from .generator import Generator
from .problem1 import Problem1
from .problem2 import Problem2
from ..formulas import (
    LogicToken,
    Conjunction,
    Alternative,
    Implication,
    Exists,
    Not,
    Atom,
    BasicToken,
)


@dataclass
class Problem7(Generator):
    name = "Problem 7"
    param_spec = {"clauses": int, "poisson": bool, "conjunction": bool}

    def generate(self) -> list[LogicToken]:
        clauses_num: int = self.params.get("clauses")  # type: ignore
        poisson: bool = self.params.get("poisson")  # type: ignore
        conjunction: bool = self.params.get("conjunction")  # type: ignore

        if poisson:
            lam = self.params.get("lambda")
            if lam is None:
                raise ValueError("Parameter 'lambda' is required when 'poisson' is True.")
            params_sub = {"clauses": clauses_num, "lambda": lam}
            GenClass = Problem2
        else:
            lengths = self.params.get("lengths")
            if lengths is None:
                raise ValueError("Parameter 'lengths' is required when 'poisson' is False.")
            params_sub = {"clauses": clauses_num, "lengths": lengths}
            GenClass = Problem1

        formulas: List[LogicToken] = []

        # liczba atomów i ich nazwy
        num_atoms = clauses_num // 2
        if num_atoms < 1:
            num_atoms = 1
        atom_names = [f"var{i+1}" for i in range(num_atoms)]

        # Generowanie trzech podproblemów F1, F2, F3
        for _ in range(3):
            # Generowanie unikalnego seeda dla każdego podproblemu
            sub_seed = self.random.randint(0, 2**32 - 1)

            gen_instance = GenClass(seed=sub_seed, params=params_sub)
            clauses_list = gen_instance.generate()

            formulas.append(Conjunction(clauses_list))  # type: ignore

        # Tworzenie G
        if conjunction:
            G = Conjunction(formulas)  # type: ignore
        else:
            G = Alternative(formulas)  # type: ignore

        # generowanie R
        R = self._generate_formula_R(atom_names)

        return [Implication(G, R)]  # type: ignore

    def _generate_formula_R(self, atom_names: list[str]) -> LogicToken:
        """
        Generuje formułę R: prostą klauzulę żywotności składającą się z 4 atomów.
        Bazuje na logice klauzuli bezpieczeństwa (negacja alternatywy),
        ale z kwantyfikatorem Exists zamiast ForAll.
        """
        length = 4
        parameter = "U"

        chosen_atoms = self.random.sample(atom_names, k=min(length, len(atom_names)))
        literals: List[BasicToken] = []

        for name in chosen_atoms:
            atom = Atom(name, parameter)
            if self.random.random() < 0.5:
                atom = Not(atom)
            literals.append(atom)

        return Exists(parameter, Not(Alternative(literals)))
