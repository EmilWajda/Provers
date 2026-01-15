from .prover import Prover
from .run_output import basic_result_parser

KNOWN_PROVERS: dict[str, Prover] = {  # TODO: verify result parsers
    "vampire": Prover("vampire", basic_result_parser("satisfiable", "unsatisfiable")),
    "spass": Prover("spass", basic_result_parser("completion found", "proof found")),
    "e": Prover("e", basic_result_parser("satisfiable", "unsatisfiable")),
    "iprover": Prover("iprover", basic_result_parser("satisfiable", "unsatisfiable"), "cnf"),
    "prover9": Prover("prover9", basic_result_parser("theorem proved", "search failed"), "ladr"),
    "z3": Prover("z3", basic_result_parser("sat", "unsat"), "smt2"),
    "cvc4": Prover("cvc4", basic_result_parser("satisfiable", "unsatisfiable")),
    "cvc5": Prover("cvc5", basic_result_parser("sat", "unsat"), "smt2"),
}
