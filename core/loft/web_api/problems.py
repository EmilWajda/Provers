import aiofiles
import json
from random import randint
from os import path
from quart import Quart, request
from aiofiles import os as aos
from ..tptp_builder import TPTPBuilder
from ..docker import run_tptp_checker
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
    return {
        "problems": {path.relpath(f, workspace_path).replace("\\", "/"): await _extract_problem_data(f) for f in files}
    }


async def generate_problem(workspace: str):
    data = await request.get_json()
    problem_name = data.get("problem")
    params = data.get("params")
    seed = data.get("seed") or randint(0, 2**32 - 1)

    if not problem_name or not params:
        return {"error": "Problem name and parameters are required."}, 400

    if problem_name not in KNOWN_PROBLEMS:
        return {"error": f"Unknown problem type: {problem_name}"}, 400

    generator_class = KNOWN_PROBLEMS[problem_name]
    try:
        generator = generator_class(seed, params)
        tptp_output = TPTPBuilder().build_annotated_tptp_str(generator)
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    problem_dir, suggested = generator.get_suggested_path()
    suggested += ".tptp"

    workspace_path = path.join("workspaces", workspace)
    directory = path.join(workspace_path, problem_dir)
    await aos.makedirs(directory, exist_ok=True)

    file_path = path.join(directory, suggested)

    async with aiofiles.open(file_path, "w") as f:
        await f.write(tptp_output)

    is_valid = await run_tptp_checker(file_path)
    if not is_valid:
        return {"error": "Generated TPTP problem syntax is invalid. Please report this issue to the developers."}, 500

    rel_path = path.join(problem_dir, suggested).replace("\\", "/")
    return {"path": rel_path}


async def delete_problem(workspace: str):
    data = await request.get_json()
    problem_path = data.get("path")
    if not problem_path:
        return {"error": "Problem path is required."}, 400

    workspace_path = path.join("workspaces", workspace)
    full_path = path.join(workspace_path, problem_path)

    if not path.normpath(full_path).startswith(path.normpath(workspace_path)):
        return {"error": "Invalid path."}, 403

    if await aos.path.exists(full_path):
        await aos.remove(full_path)
        return {}
    return {"error": "File not found."}, 404


async def rename_problem(workspace: str):
    data = await request.get_json()
    old_path = data.get("path")
    new_name = data.get("newName")

    if not old_path or not new_name:
        return {"error": "Path and newName are required."}, 400

    workspace_path = path.join("workspaces", workspace)
    full_old_path = path.join(workspace_path, old_path)

    if not path.normpath(full_old_path).startswith(path.normpath(workspace_path)):
        return {"error": "Invalid path."}, 403

    if not await aos.path.exists(full_old_path):
        return {"error": "File not found."}, 404

    new_name = new_name.strip()
    if not new_name or new_name.replace(".", "") == "":
        return {"error": "Invalid new name."}, 400

    directory = path.dirname(full_old_path)

    ext = ""
    if full_old_path.endswith(".tptp"):
        ext = ".tptp"
    elif full_old_path.endswith(".p"):
        ext = ".p"
    else:
        # Fallback if there's no known extension (shouldn't happen but just in case)
        _, ext = path.splitext(full_old_path)

    full_new_path = path.join(directory, new_name + ext)

    if path.normpath(full_old_path) == path.normpath(full_new_path):
        return {}

    if await aos.path.exists(full_new_path):
        return {"error": "File with this name already exists."}, 400

    await aos.rename(full_old_path, full_new_path)
    return {}


def register_problem_routes(app: Quart) -> None:
    app.route("/api/problems")(get_problem_info)
    app.route("/api/workspaces/<workspace>/problems")(get_workspace_problems)
    app.route("/api/workspaces/<workspace>/problems", methods=["POST"])(generate_problem)
    app.route("/api/workspaces/<workspace>/problems", methods=["PUT"])(rename_problem)
    app.route("/api/workspaces/<workspace>/problems", methods=["DELETE"])(delete_problem)
