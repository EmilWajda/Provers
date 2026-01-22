from dataclasses import dataclass
from typing import List
from random import Random

from .generator import Generator
from .problem1 import Problem1
from .problem2 import Problem2
from .std_params import StandardParams
from ..formulas import (
    LogicToken,
    Conjunction,
    Implication,
    Not,
)


@dataclass
class Problem8(Generator):
    name = "8"
    param_spec = {
        "clauses": StandardParams.CLAUSES.value,
        "poisson": StandardParams.POISSON.value,
        "mode": StandardParams.MODE.value,
        "lambda": StandardParams.LAMBDA_OR_NONE.value,
        "lengths": StandardParams.LENGTHS_OR_NONE.value,
    }
    presets = {
        "Contradictory": {"clauses": 50, "poisson": True, "mode": "contradictory", "lambda": 3.0, "lengths": []},
        "Subcontrary": {"clauses": 50, "poisson": True, "mode": "subcontrary", "lambda": 3.0, "lengths": []},
        "Subalternated": {"clauses": 50, "poisson": True, "mode": "subalternated", "lambda": 3.0, "lengths": []},
    }

    def validate_extra(self) -> str | None:
        poisson: bool = bool(self.params.get("poisson"))  # type: ignore
        lam: float = self.params.get("lambda")  # type: ignore
        lengths: list[int] = self.params.get("lengths")  # type: ignore

        if poisson:
            if lam == 0:
                return "Lambda must be greater than 0 when poisson is enabled."
        else:
            if not lengths:
                return "Clause lengths list cannot be empty when poisson is disabled."
        return None

    def generate(self) -> list[LogicToken]:
        clauses_num: int = self.params.get("clauses")  # type: ignore
        poisson: bool = self.params.get("poisson")  # type: ignore
        mode: str = self.params.get("mode")  # type: ignore

        if poisson:
            lam = self.params.get("lambda")
            params_sub = {"clauses": clauses_num, "lambda": lam}
            GenClass = Problem2
        else:
            lengths = self.params.get("lengths")
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
