from .prover import Prover
from .run_output import basic_result_parser

KNOWN_PROVERS: dict[str, Prover] = {  # TODO: verify result parsers
    "vampire": Prover("vampire", basic_result_parser("satisfiable", "unsatisfiable")),
    "spass": Prover("spass", basic_result_parser("completion found", "proof found")),
    "e": Prover("e", basic_result_parser("satisfiable", "unsatisfiable")),
}
