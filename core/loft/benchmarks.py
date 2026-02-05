import asyncio
import aiofiles
import json
from os import path
from aiofiles.os import makedirs
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Awaitable
from .provers import KNOWN_PROVERS
from .provers.run_output import RunResult, RunStats


@dataclass
class BenchmarkCell:
    problem: str
    prover: str
    result: RunResult | None = None  # None for ongoing benchmark
    stats: RunStats | None = None

    def to_dict(self) -> dict:
        return {
            "problem": self.problem,
            "prover": self.prover,
            "result": self.result.value if self.result else None,
            "stats": self.stats.to_dict() if self.stats else None,
        }


@dataclass(unsafe_hash=True)
class BenchmarkResult:
    problems: list[str] = field(hash=False)
    provers: list[str] = field(hash=False)
    timestamp: datetime = field(default_factory=datetime.now)
    filled_cells: list[BenchmarkCell] = field(default_factory=list, hash=False)

    def to_dict(self) -> dict:
        return {
            "problems": self.problems,
            "provers": self.provers,
            "timestamp": self.timestamp.isoformat(),
            "filled_cells": [cell.to_dict() for cell in self.filled_cells],
        }


@dataclass
class BenchmarkOrchestrator:
    workspace: str
    queues: dict[BenchmarkResult, asyncio.Queue[BenchmarkCell]] = field(default_factory=dict)
    readers: dict[BenchmarkResult, list[asyncio.Queue[dict | None]]] = field(default_factory=dict)
    tasks: set[asyncio.Task] = field(default_factory=set)

    async def start_benchmark(self, problems: list[str], provers: list[str], timeout: int) -> BenchmarkResult:
        benchmark = BenchmarkResult(problems, provers)
        queue = asyncio.Queue()
        for problem in problems:
            for prover in provers:
                await queue.put(BenchmarkCell(problem, prover))
        self.queues[benchmark] = queue
        self.readers[benchmark] = []
        task = asyncio.create_task(self.run_benchmark(benchmark, timeout))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return benchmark

    def get_ongoing(self, timestamp: str) -> BenchmarkResult | None:
        for benchmark in self.queues.keys():
            if benchmark.timestamp.isoformat() == timestamp:
                return benchmark
        return None

    async def run_benchmark(self, benchmark: BenchmarkResult, timeout: int) -> None:
        queue = self.queues[benchmark]
        while not queue.empty():
            cell = await queue.get()
            for reader in self.readers[benchmark]:
                await reader.put(cell.to_dict())
            prover = KNOWN_PROVERS[cell.prover]
            result, stats = await prover.run_on_problem(self.workspace, cell.problem, timeout=timeout)
            cell.result = result
            cell.stats = stats
            benchmark.filled_cells.append(cell)
            for reader in self.readers[benchmark]:
                await reader.put(cell.to_dict())
        for reader in self.readers[benchmark]:
            await reader.put(None)
        del self.queues[benchmark]
        del self.readers[benchmark]
        await self._save_result(benchmark)

    async def _save_result(self, benchmark: BenchmarkResult) -> None:
        results_dir = path.join(self.workspace, "results")
        await makedirs(results_dir, exist_ok=True)
        result_path = path.join(results_dir, f"{benchmark.timestamp.isoformat()}.json")
        async with aiofiles.open(result_path, "w") as f:
            json_str = json.dumps(benchmark.to_dict(), indent=4, ensure_ascii=False)
            await f.write(json_str)
