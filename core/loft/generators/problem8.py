from dataclasses import dataclass
from typing import List
from random import Random

from .generator import Generator
from .problem1 import Problem1
from .problem2 import Problem2
from ..formulas import (
    LogicToken,
    Conjunction,
    Implication,
    Not,
)


@dataclass
class Problem8(Generator):
    name = "Problem 8"
    param_spec = {"clauses": int, "poisson": bool, "mode": str}

    def generate(self) -> list[LogicToken]:
        clauses_num: int = self.params.get("clauses")  # type: ignore
        poisson: bool = self.params.get("poisson")  # type: ignore
        mode: str = self.params.get("mode")  # type: ignore

        if mode not in ["contradictory", "subcontrary", "subalternated"]:
            raise ValueError(f"Unknown mode: {mode}. Expected 'contradictory', 'subcontrary', or 'subalternated'.")

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

        # generowanie F1 i F2
        for _ in range(2):
            sub_seed = self.random.randint(0, 2**32 - 1)

            gen_instance = GenClass(seed=sub_seed, params=params_sub)
            clauses_list = gen_instance.generate()

            formulas.append(Conjunction(clauses_list))  # type: ignore

        F1 = formulas[0]
        F2 = formulas[1]

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
