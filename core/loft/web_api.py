from os import path
from quart import Quart, request
from aiofiles import os as aos

app = Quart("loft", static_url_path="/")


async def _remove_directory(dir_path: str) -> None:
    """Recursively delete a directory and all its contents."""
    for entry in await aos.listdir(dir_path):
        full_path = path.join(dir_path, entry)
        if await aos.path.isdir(full_path):
            await _remove_directory(full_path)
        else:
            await aos.remove(full_path)
    await aos.rmdir(dir_path)


@app.route("/")
async def index():
    if app.static_folder and await aos.path.exists(path.join(app.static_folder, "index.html")):
        return await app.send_static_file("index.html")
    return "This LOFT instance has missing static files. The API is still available."


@app.route("/api/workspaces")
async def get_workspaces():
    await aos.makedirs("workspaces", exist_ok=True)
    workspaces = [
        name for name in await aos.listdir("workspaces") if await aos.path.isdir(path.join("workspaces", name))
    ]
    return {"workspaces": workspaces}


@app.route("/api/workspaces", methods=["POST"])
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


@app.route("/api/workspaces", methods=["DELETE"])
async def delete_workspace():
    data = await request.get_json()
    workspace_name = data.get("name")
    if not workspace_name:
        return {"error": "Workspace name is required."}, 400
    workspace_path = path.join("workspaces", workspace_name)
    if not await aos.path.exists(workspace_path):
        return {"error": "Workspace does not exist."}, 400
    await _remove_directory(workspace_path)
    return {}
