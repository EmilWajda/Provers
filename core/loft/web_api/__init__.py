from quart import Quart
from aiofiles import os as aos
from os import path
from .workspaces import register_workspace_routes
from .settings import register_settings_routes
from .problems import register_problem_routes
from .results import register_results_routes
from ..provers import KNOWN_PROVERS


app = Quart("loft", static_url_path="/")


@app.route("/")
async def index():
    if app.static_folder and await aos.path.exists(path.join(app.static_folder, "index.html")):
        return await app.send_static_file("index.html")
    return "This LOFT instance has missing static files. The API is still available."


@app.route("/api/provers")
def get_provers():
    return {"provers": list(KNOWN_PROVERS.keys())}


register_workspace_routes(app)
register_settings_routes(app)
register_problem_routes(app)
register_results_routes(app)
