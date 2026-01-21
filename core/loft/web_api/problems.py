import aiofiles
import json
from os import path
from quart import Quart
from aiofiles import os as aos
from ..generators import KNOWN_PROBLEMS
from ..generators.param_spec import ParamSpec


_EXCLUDED_DIRECTORIES = {"convertion_cache", "results"}
_COMMENT_PREFIX = "% LOFT DATA: "


def get_problem_info():
    def map_params(params: dict[str, ParamSpec]):
        return {k: v.get_schema() for k, v in params.items()}

    return {
        "problems": {k: {"params": map_params(v.param_spec), "presets": v.presets} for k, v in KNOWN_PROBLEMS.items()}
    }


async def _find_tptp_files(dir_path: str) -> list[str]:
    tptp_files = []
    for entry in await aos.listdir(dir_path):
        full_path = path.join(dir_path, entry)
        if await aos.path.isdir(full_path):
            if entry not in _EXCLUDED_DIRECTORIES:
                tptp_files.extend(await _find_tptp_files(full_path))
        elif entry.endswith(".p") or entry.endswith(".tptp"):
            tptp_files.append(full_path)
    return tptp_files


async def _extract_problem_data(file_path: str) -> dict | None:
    async with aiofiles.open(file_path, "r") as f:
        comment = await f.readline()
        if comment.startswith(_COMMENT_PREFIX):
            data_str = comment[len(_COMMENT_PREFIX) :].strip()
            try:
                return json.loads(data_str)
            except json.JSONDecodeError:
                return None


async def get_workspace_problems(workspace: str):
    workspace_path = path.join("workspaces", workspace)
    if not await aos.path.exists(workspace_path):
        return {"error": "Workspace does not exist."}, 400
    files = await _find_tptp_files(workspace_path)
    return {"problems": {path.relpath(f, workspace_path): await _extract_problem_data(f) for f in files}}


def register_problem_routes(app: Quart) -> None:
    app.route("/api/problems")(get_problem_info)
    app.route("/api/workspaces/<workspace>/problems")(get_workspace_problems)
