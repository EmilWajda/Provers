import json
import asyncio
from argparse import ArgumentParser
from random import randint
from os import path, makedirs
from .tptp_builder import TPTPBuilder
from .generators.problem1 import Problem1
from .provers.known_provers import KNOWN_PROVERS


def build_parser():
    parser = ArgumentParser(prog="loft", description="LOFT, the prover benchmarking tool")
    parser.add_argument("-w", "--workspace", type=str, default="default", help="Workspace subdirectory.")
    sub = parser.add_subparsers(dest="command", help="Subcommand to run.")

    generate = sub.add_parser("generate", help="Generate benchmark problems.")
    generate.add_argument("problem_num", type=int, help="Problem number/name to generate.")
    generate.add_argument("params", type=str, help="JSON string of parameters for the generator.")
    generate.add_argument("-s", "--seed", type=int, default=None, help="Random seed for generation.")

    benchmark = sub.add_parser("benchmark", help="Run benchmarks on generated problems.")
    benchmark.add_argument("prover", type=str, help="The prover to benchmark.")
    benchmark.add_argument("problem_file", type=str, help="Path to the problem file.")
    benchmark.add_argument("-t", "--timeout", type=int, help="Timeout in seconds.")

    return parser


def main():
    args = build_parser().parse_args()
    if not args.command:
        print("No command provided. Currently, server mode is not functional. Use -h for help.")
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
