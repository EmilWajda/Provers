from argparse import ArgumentParser
from .web_api import app as quart_app
from .generators import KNOWN_PROBLEMS
from .provers import KNOWN_PROVERS
from .cli import check, benchmark, generate


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="loft", description="LOFT, the prover benchmarking tool")
    parser.add_argument("-w", "--workspace", type=str, default="default", help="Workspace subdirectory.")
    sub = parser.add_subparsers(dest="command", help="Subcommand to run. If none is provided, behaves as if 'dev' was given.")
    sub.add_parser("dev", help="Run the LOFT web server in development mode.")

    generate = sub.add_parser("generate", help="Generate benchmark problems.")
    generate.add_argument("-s", "--seed", type=int, default=None, help="Random seed for generation.")
    generate.add_argument("-c", "--no-check", action="store_true", help="Skip automatic TPTP syntax checking.")
    problem = generate.add_subparsers(dest="problem", help="Problem number/name to generate.")
    for problem_name, problem_class in KNOWN_PROBLEMS.items():
        p = problem.add_parser(problem_name, help=f"Generate problem {problem_name}.")
        for field, spec in problem_class.param_spec.items():
            spec.add_cli_argument(field, p)

    benchmark = sub.add_parser("benchmark", help="Run benchmarks on generated problems.")
    benchmark.add_argument("prover", type=str, choices=KNOWN_PROVERS, help="The prover to benchmark.")
    benchmark.add_argument("problem_file", type=str, help="Path to the problem file, relative to the selected workspace.")
    benchmark.add_argument("-t", "--timeout", type=int, help="Timeout in seconds.")

    check = sub.add_parser("check", help="Check TPTP problem syntax.")
    check.add_argument("problem_file", type=str, help="Path to the problem file, relative to the selected workspace.")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not args.command or args.command == "dev":
        quart_app.run(debug=True, port=8000, host="0.0.0.0")
        return
    
    match args.command:
        case "generate":
            generated = generate(args.workspace, args.seed, args.problem, vars(args))
            if not args.no_check and generated is not None:
                check(args.workspace, generated)
        case "benchmark":
            benchmark(args.workspace, args.problem_file, args.prover, args.timeout)
        case "check":
            check(args.workspace, args.problem_file)
