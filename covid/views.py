from covid import app

@app.route("/")
def index():
    return "Flask esta funcionando desde views!"