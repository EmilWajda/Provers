from dataclasses import dataclass, field
from typing import List

from .formulas import LogicToken

@dataclass
class TPTPBuilder:
    """ Generuje pełny string w formacie TPTP z podanej listy klauzul. """
    counter: int = 1
    role: str = "axiom"
    prefix: str = "ax"

    def build_single_fof(self, name: str, role: str, clause_str: str) -> str:
        """ Buduje pojedynczy wpis FOF w formacie TPTP. """
        return f"fof({name},{role},(\n{clause_str}\n)). \n"

    def build_tptp_str(self, clauses: list[LogicToken]) -> str:
        """ Tworzy pełny string w formacie TPTP z podanej listy klauzul. """
        lines = []

        for clause in clauses:
            clause_str = clause.to_tptp()

            name = f"{self.prefix}{self.counter}"
            self.counter += 1

            fof_entry = self.build_single_fof(name, self.role, clause_str)
            lines.append(fof_entry)

        return "\n".join(lines)
