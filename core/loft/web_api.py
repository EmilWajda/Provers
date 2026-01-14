from quart import Quart

app = Quart("loft")

@app.route("/")
async def index():
    return "Welcome to the LOFT Web API!"
