from os import path
from quart import Quart
from aiofiles import os as aos
from quart_cors import cors 

app = Quart("loft", static_url_path="/")

# 2. ODBLOKUJ CORS (To naprawi błąd w konsoli przeglądarki)
app = cors(app, allow_origin="*")

@app.route("/")
async def index():
    if app.static_folder and await aos.path.exists(path.join(app.static_folder, "index.html")):
        return await app.send_static_file("index.html")
    return "This LOFT instance has missing static files. The API is still available."


@app.route("/api/workspaces")
async def get_workspaces():
    workspaces_dir = "workspaces"

    await aos.makedirs(workspaces_dir, exist_ok=True)

    workspaces = [
        name for name in await aos.listdir(workspaces_dir)
        if await aos.path.isdir(path.join(workspaces_dir, name))
    ]

    return { "workspaces": workspaces }
        

