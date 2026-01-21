import aiofiles
import json
from os import path
from quart import Quart, request
from aiofiles import os as aos


async def get_workspace_settings(workspace: str):
    if not await aos.path.exists(path.join("workspaces", workspace)):
        return {"error": "Workspace does not exist."}, 400
    default_settings = {
        "seed": None,
        "timeout": 60,
    }
    settings_path = path.join("workspaces", workspace, "settings.json")
    if await aos.path.exists(settings_path):
        async with aiofiles.open(settings_path, "r") as f:
            content = await f.read()
            settings = json.loads(content)
            if "seed" in settings and (settings["seed"] is None or isinstance(settings["seed"], int)):
                default_settings["seed"] = settings["seed"]
            if "timeout" in settings and isinstance(settings["timeout"], int):
                default_settings["timeout"] = settings["timeout"]
    return default_settings


async def update_workspace_settings(workspace: str):
    if not await aos.path.exists(path.join("workspaces", workspace)):
        return {"error": "Workspace does not exist."}, 400
    data = await request.get_json()
    settings_path = path.join("workspaces", workspace, "settings.json")
    async with aiofiles.open(settings_path, "w") as f:
        await f.write(json.dumps(data))
    return {}


def register_settings_routes(app: Quart) -> None:
    app.route("/api/workspaces/<workspace>/settings")(get_workspace_settings)
    app.route("/api/workspaces/<workspace>/settings", methods=["PUT"])(update_workspace_settings)
