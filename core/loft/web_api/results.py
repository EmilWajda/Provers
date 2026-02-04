from quart import Quart


async def get_benchmarks(workspace: str):
    return {}


async def create_benchmark(workspace: str):
    return {}


async def benchmark_websocket(workspace: str):
    pass


def register_results_routes(app: Quart) -> None:
    app.route("/api/workspaces/<workspace>/results")(get_benchmarks)
    app.route("/api/workspaces/<workspace>/results", methods=["POST"])(create_benchmark)
    app.websocket("/ws/workspaces/<workspace>/results")(benchmark_websocket)
