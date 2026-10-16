from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/repository")
def repository():
    return render_template("repository.html")


@app.route("/classroom-agent")
def classroom_agent():
    return render_template("classroom_agent.html")


@app.route("/prompt-to-game")
def prompt_to_game():
    return render_template("prompt_to_game.html")


if __name__ == "__main__":
    app.run(debug=True)