import aiofiles
import asyncio
import json
from os import path
from aiofiles import os as aos
from quart import Quart, request, websocket
from ..benchmarks import BenchmarkOrchestrator

orchestrators: dict[str, BenchmarkOrchestrator] = {}  # workspace -> orchestrator


async def get_benchmarks(workspace: str):
    done = {}
    results_dir = path.join("workspaces", workspace, "results")
    if await aos.path.exists(results_dir):
        for file in await aos.listdir(results_dir):
            if not file.endswith(".json"):
                continue
            async with aiofiles.open(path.join(results_dir, file), "r") as f:
                content = await f.read()
                file_no_ext = file[:-5]
                done[file_no_ext] = json.loads(content)
                del done[file_no_ext]["filled_cells"]
    ongoing = []
    if workspace in orchestrators:
        orchestrator = orchestrators[workspace]
        for benchmark in orchestrator.queues.keys():
            ongoing.append(benchmark.to_dict())
            del ongoing[-1]["filled_cells"]
    return {"done": done, "ongoing": ongoing}


async def create_benchmark(workspace: str):
    data = await request.get_json()
    problems = data.get("problems") or []
    provers = data.get("provers") or []
    timeout = data.get("timeout")
    if workspace not in orchestrators:
        orchestrators[workspace] = BenchmarkOrchestrator(path.join("workspaces", workspace))
    orchestrator = orchestrators[workspace]
    benchmark = await orchestrator.start_benchmark(problems, provers, timeout)
    return {"benchmark": benchmark.timestamp.isoformat()}


async def benchmark_websocket(workspace: str):
    timestamp = websocket.args.get("benchmark") or ""
    if workspace in orchestrators:
        orchestrator = orchestrators[workspace]
        benchmark = orchestrator.get_ongoing(timestamp)
        if benchmark:
            benchmark_dict = benchmark.to_dict()
            del benchmark_dict["filled_cells"]
            await websocket.send_json(benchmark_dict)
            queue: asyncio.Queue[dict | None] = asyncio.Queue()
            orchestrator.readers[benchmark].append(queue)
            try:
                while True:
                    cell_dict = await queue.get()
                    if cell_dict is None:
                        break
                    await websocket.send_json(cell_dict)
            finally:
                orchestrator.readers.get(benchmark, [queue]).remove(queue)
            return
    possible_path = path.join("workspaces", workspace, "results", f"{timestamp}.json")
    if await aos.path.exists(possible_path):
        async with aiofiles.open(possible_path, "r") as f:
            content = await f.read()
            benchmark_dict: dict = json.loads(content)
            filled_cells = benchmark_dict.pop("filled_cells", [])
            await websocket.send_json(benchmark_dict)
            for cell_dict in filled_cells:
                await websocket.send_json(cell_dict)
    return {"error": "File not found."}, 404


def register_results_routes(app: Quart) -> None:
    app.route("/api/workspaces/<workspace>/results")(get_benchmarks)
    app.route("/api/workspaces/<workspace>/results", methods=["POST"])(create_benchmark)
    app.websocket("/ws/workspaces/<workspace>/results")(benchmark_websocket)
