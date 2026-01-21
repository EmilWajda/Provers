import asyncio
from os import path, makedirs
from random import randint
from .docker import run_tptp_checker
from .provers import KNOWN_PROVERS
from .generators import KNOWN_PROBLEMS
from .tptp_builder import TPTPBuilder


def _check_problem_path(workspace: str, problem: str) -> tuple[str | None, str | None]:
    w = path.join("workspaces", workspace)
    p = path.join(w, problem)
    if not path.exists(p):
        print(f"Problem file '{problem}' does not exist in workspace '{workspace}'.")
        return None, None
    return w, p


def check(workspace: str, problem: str) -> None:
    print("Checking TPTP problem syntax...")
    problem_path = _check_problem_path(workspace, problem)[1]
    if problem_path is None:
        return
    is_valid = asyncio.run(run_tptp_checker(problem_path))
    if is_valid:
        print("Check successful.")
    else:
        print("Warning: TPTP problem syntax is invalid! Please report this issue to the developers.")


def benchmark(workspace: str, problem: str, prover_name: str, timeout: int | None) -> None:
    print("Running benchmark...")
    prover = KNOWN_PROVERS[prover_name.lower()]
    workspace_path = _check_problem_path(workspace, problem)[0]
    if workspace_path is None:
        return
    result, stats = asyncio.run(prover.run_on_problem(workspace_path, problem, timeout))
    print(f"Result: {result.value}")
    if stats:
        print(f"System Time: {stats.system_time:.2f} s")
        print(f"Real Time: {stats.real_time:.2f} s")
        print(f"Peak Memory: {stats.peak_memory} KB")


def generate(workspace: str, seed: int | None, problem_name: str, params: dict) -> str | None:
    seed = seed or randint(0, 2**32 - 1)
    print(f"Using seed: {seed}")

    generator_class = KNOWN_PROBLEMS[problem_name]
    params = {k: v for k, v in params.items() if k in generator_class.param_spec}
    try:
        generator = generator_class(seed, params)
    except ValueError as e:
        print("Error in parameter conditions!")
        print(e)
        return
    tptp_output = TPTPBuilder().build_annotated_tptp_str(generator)

    problem_dir, suggested = generator.get_suggested_path()
    suggested += ".tptp"
    directory = path.join("workspaces", workspace, problem_dir)
    makedirs(directory, exist_ok=True)
    file = path.join(directory, suggested)
    with open(file, "w") as f:
        f.write(tptp_output)
    rel_path = path.join(problem_dir, suggested)
    print(f"Generated problem saved to {rel_path} in workspace '{workspace}'.")
    return rel_path
