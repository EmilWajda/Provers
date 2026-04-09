from quart import Quart, request
from aiofiles import os as aos
from os import path
from ..benchmarks import orchestrators


async def _remove_directory(dir_path: str) -> None:
    """Recursively delete a directory and all its contents."""
    for entry in await aos.listdir(dir_path):
        full_path = path.join(dir_path, entry)
        if await aos.path.isdir(full_path):
            await _remove_directory(full_path)
        else:
            await aos.remove(full_path)
    await aos.rmdir(dir_path)


async def get_workspaces():
    await aos.makedirs("workspaces", exist_ok=True)
    workspaces = [
        name for name in await aos.listdir("workspaces") if await aos.path.isdir(path.join("workspaces", name))
    ]
    return {"workspaces": workspaces}


async def create_workspace():
    data = await request.get_json()
    workspace_name = data.get("name")
    if not workspace_name:
        return {"error": "Workspace name is required."}, 400
    workspace_path = path.join("workspaces", workspace_name)
    if await aos.path.exists(workspace_path):
        return {"error": "Workspace already exists."}, 400
    await aos.makedirs(workspace_path)
    return {}


async def delete_workspace():
    data = await request.get_json()
    workspace_name = data.get("name")
    if not workspace_name:
        return {"error": "Workspace name is required."}, 400
    workspace_path = path.join("workspaces", workspace_name)
    if not await aos.path.exists(workspace_path):
        return {"error": "Workspace does not exist."}, 400
    orchestrator = orchestrators.get(workspace_name)
    if orchestrator and orchestrator.has_ongoing():
        return {"error": "Cannot delete workspace with ongoing benchmarks."}, 400
    await _remove_directory(workspace_path)
    if orchestrator:
        del orchestrators[workspace_name]
    return {}


async def rename_workspace():
    data = await request.get_json()
    old_name = data.get("name")
    new_name = data.get("newName")
    if not old_name or not new_name:
        return {"error": "Workspace name and newName are required."}, 400

    new_name = new_name.strip()
    if not new_name or new_name == "." or new_name == "..":
        return {"error": "Invalid workspace name."}, 400

    old_path = path.join("workspaces", old_name)
    new_path = path.join("workspaces", new_name)

    if not await aos.path.exists(old_path):
        return {"error": "Workspace does not exist."}, 400

    if old_name == new_name:
        return {}

    if await aos.path.exists(new_path):
        return {"error": "Workspace with this name already exists."}, 400

    orchestrator = orchestrators.get(old_name)
    if orchestrator and orchestrator.has_ongoing():
        return {"error": "Cannot rename workspace with ongoing benchmarks."}, 400
    await aos.rename(old_path, new_path)
    if orchestrator:
        del orchestrators[old_name]
    return {}


def register_workspace_routes(app: Quart) -> None:
    app.route("/api/workspaces")(get_workspaces)
    app.route("/api/workspaces", methods=["POST"])(create_workspace)
    app.route("/api/workspaces", methods=["PUT"])(rename_workspace)
    app.route("/api/workspaces", methods=["DELETE"])(delete_workspace)
