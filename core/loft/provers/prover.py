from dataclasses import dataclass
from typing import Callable
from .run_output import RunResult, RunStats
from ..docker import run_docker_container


@dataclass
class Prover:  # TODO: add some way to change formats
    name: str
    result_parser: Callable[[str], RunResult]

    async def run_on_problem(self, problem_file: str, timeout: int | None = None) -> tuple[RunResult, RunStats | None]:
        stdout, stderr, ret_code = await run_docker_container(self.name, problem_file, timeout)
        stats = RunStats.from_raw_stderr(stderr)
        if ret_code is None:
            return RunResult.TIMEOUT, stats
        result = self.result_parser(stdout)
        return result, stats
