import aiofiles
import hashlib
import os
from aiofiles import os as aos
from dataclasses import dataclass
from typing import Callable
from .run_output import RunResult, RunStats
from ..docker import run_docker_container

_CONVERTED_PROBLEMS_DIR = "convertion_cache"


async def _hash_file(path: str) -> str:
    hasher = hashlib.sha256()
    async with aiofiles.open(path, "rb") as f:
        hasher.update(await f.read())
    return hasher.hexdigest()


@dataclass
class Prover:
    name: str
    result_parser: Callable[[str], RunResult]
    converter: str | None = None

    async def run_on_problem_direct(
        self, problem_file: str, timeout: int | None = None
    ) -> tuple[RunResult, RunStats | None]:
        stdout, stderr, ret_code = await run_docker_container(self.name, problem_file, timeout)
        stats = RunStats.from_raw_stderr(stderr)
        if ret_code is None:
            return RunResult.TIMEOUT, stats
        result = self.result_parser(stdout)
        return result, stats

    async def ensure_converted(self, workspace: str, problem_file: str) -> str:
        problem_file = os.path.join(workspace, problem_file)
        if self.converter is None:
            return problem_file
        file_hash = await _hash_file(problem_file)
        converted_dir = os.path.join(workspace, _CONVERTED_PROBLEMS_DIR)
        converted_file = os.path.join(converted_dir, f"{file_hash}.{self.converter}")
        if not await aos.path.exists(converted_file):
            await aos.makedirs(converted_dir, exist_ok=True)
            output, _, _ = await run_docker_container(self.converter, problem_file)
            async with aiofiles.open(converted_file, "w") as f:
                await f.write(output)
        return converted_file

    async def run_on_problem(
        self, workspace: str, problem_file: str, timeout: int | None = None
    ) -> tuple[RunResult, RunStats | None]:
        converted_file = await self.ensure_converted(workspace, problem_file)
        return await self.run_on_problem_direct(converted_file, timeout)
