from .prover import Prover
from .run_output import basic_result_parser

_ALL_PROVERS: list[Prover] = [
    Prover("vampire", basic_result_parser("satisfiable", "unsatisfiable")),
    Prover("spass", basic_result_parser("completion found", "proof found")),
    Prover("e", basic_result_parser("satisfiable", "unsatisfiable")),
    Prover("iprover", basic_result_parser("satisfiable", "unsatisfiable"), "cnf"),
    Prover("prover9", basic_result_parser("theorem proved", "search failed"), "ladr"),  # TODO: verify
    Prover("z3", basic_result_parser("sat", "unsat"), "smt2"),
    Prover("cvc4", basic_result_parser("satisfiable", "unsatisfiable")),
    Prover("cvc5", basic_result_parser("sat", "unsat"), "smt2"),
    Prover("drodi", basic_result_parser("satisfiable", "unsatisfiable")),
]

KNOWN_PROVERS: dict[str, Prover] = {prover.name: prover for prover in _ALL_PROVERS}
