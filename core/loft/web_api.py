from os import path
from quart import Quart

app = Quart("loft", static_url_path="/")


@app.route("/")
async def index():
    if app.static_folder and path.exists(path.join(app.static_folder, "index.html")):
        return await app.send_static_file("index.html")
    return "This LOFT instance has missing static files. The API is still available."
