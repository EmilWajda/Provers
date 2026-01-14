import json
import asyncio
from argparse import ArgumentParser
from random import randint
from os import path, makedirs
from .docker import run_tptp_checker
from .tptp_builder import TPTPBuilder
from .web_api import app as quart_app
from .generators.problem1 import Problem1
from .provers.known_provers import KNOWN_PROVERS


def build_parser():
    parser = ArgumentParser(prog="loft", description="LOFT, the prover benchmarking tool")
    parser.add_argument("-w", "--workspace", type=str, default="default", help="Workspace subdirectory.")
    sub = parser.add_subparsers(dest="command", help="Subcommand to run. If none is provided, behaves as if 'dev' was given.")
    sub.add_parser("dev", help="Run the LOFT web server in development mode.")

    generate = sub.add_parser("generate", help="Generate benchmark problems.")
    generate.add_argument("problem_num", type=int, help="Problem number/name to generate.")
    generate.add_argument("params", type=str, help="JSON string of parameters for the generator.")
    generate.add_argument("-s", "--seed", type=int, default=None, help="Random seed for generation.")
    generate.add_argument("-c", "--no-check", action="store_true", help="Skip automatic TPTP syntax checking.")

    benchmark = sub.add_parser("benchmark", help="Run benchmarks on generated problems.")
    benchmark.add_argument("prover", type=str, help="The prover to benchmark.")
    benchmark.add_argument("problem_file", type=str, help="Path to the problem file.")
    benchmark.add_argument("-t", "--timeout", type=int, help="Timeout in seconds.")

    check = sub.add_parser("check", help="Check TPTP problem syntax.")
    check.add_argument("problem_file", type=str, help="Path to the problem file.")

    return parser


def main():
    args = build_parser().parse_args()
    if not args.command or args.command == "dev":
        quart_app.run(debug=True, port=8000, host="0.0.0.0")
        return
    workspace = args.workspace

    if args.command == "generate":
        seed = args.seed or randint(0, 2**32 - 1)
        print(f"Using seed: {seed}")
        params = json.loads(args.params)
        if args.problem_num != 1:
            print(f"Problem number {args.problem_num} is not implemented.")
            return

        generator = Problem1(seed, params)
        problem = generator.generate()
        tptp_output = TPTPBuilder().build_tptp_str(problem)

        problem_dir = generator.name.replace(" ", "").lower()
        problem_name = f"clauses_{params["clauses"]}_lengths_{'_'.join(map(str, params["lengths"]))}.tptp"
        directory = path.join("workspaces", workspace, problem_dir)
        makedirs(directory, exist_ok=True)
        file = path.join(directory, problem_name)
        with open(file, "w") as f:
            f.write(tptp_output)
        print(f"Generated problem saved to {file}")
        if args.no_check:
            return
        args.problem_file = file
    elif args.command == "benchmark":
        print("Running benchmark...")
        prover = KNOWN_PROVERS.get(args.prover.lower())
        if not prover:
            print(f"Prover '{args.prover}' is not known.")
            return
        result, stats = asyncio.run(prover.run_on_problem(args.problem_file, args.timeout))
        print(f"Result: {result.value}")
        if stats:
            print(f"System Time: {stats.system_time:.2f} s")
            print(f"Real Time: {stats.real_time:.2f} s")
            print(f"Peak Memory: {stats.peak_memory} KB")
        return
    print("Checking TPTP problem syntax...")
    is_valid = asyncio.run(run_tptp_checker(args.problem_file))
    if is_valid:
        print("Check successful.")
    else:
        print("Warning: TPTP problem syntax is invalid! Please report this issue to the developers.")
