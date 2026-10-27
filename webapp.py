"""Web front end for the command-line programs in this repository.

Nothing in the original scripts is changed: each one is executed as a
subprocess with the values typed into the form fed to its stdin, and its own
stdout/stderr is displayed back. This exists so the tasks can be tried from a
browser.
"""

import os
import subprocess
import sys

from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

PROGRAMS = {
    "calculator": {
        "title": "Simple Calculator",
        "tagline": "Add, subtract, multiply or divide two numbers.",
        "script": "Calculator.py",
        "fields": [
            {"name": "num1", "label": "First number", "placeholder": "e.g. 12"},
            {"name": "num2", "label": "Second number", "placeholder": "e.g. 4"},
            {
                "name": "choice",
                "label": "Operation",
                "placeholder": "1 = add, 2 = subtract, 3 = multiply, 4 = divide",
            },
        ],
    },
    "password": {
        "title": "Password Generator",
        "tagline": "Generate a random password of any length.",
        "script": "PASSWORD GENERATOR",
        "fields": [
            {"name": "length", "label": "Password length", "placeholder": "e.g. 16"},
            {
                "name": "choice",
                "label": "Strength",
                "placeholder": "1 = letters, 2 = letters + numbers, 3 = letters + numbers + symbols",
            },
        ],
    },
    "rps": {
        "title": "Rock Paper Scissors",
        "tagline": "Play a round against the computer.",
        "script": "Rock Paper Scissors Game",
        "fields": [
            {"name": "user_choice", "label": "Your choice", "placeholder": "rock, paper or scissors"},
            {"name": "play_again", "label": "Play again?", "placeholder": "yes or no"},
        ],
    },
}


def run_program(program, values):
    """Run the original script, feeding it the form values on stdin."""
    stdin = "".join(f"{value}\n" for value in values)
    completed = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, program["script"])],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    output = completed.stdout
    if completed.stderr.strip():
        output = f"{output}\n{completed.stderr}".strip()
    return output


@app.route("/")
def index():
    return render_template("index.html", programs=PROGRAMS)


@app.route("/program/<key>", methods=["GET", "POST"])
def program_page(key):
    program = PROGRAMS.get(key)
    if program is None:
        return render_template("not_found.html"), 404

    values = request.form.getlist("value") if request.method == "POST" else []
    output = None
    error = None
    if request.method == "POST":
        if any(not value.strip() for value in values):
            error = "Please fill in every field."
        else:
            try:
                output = run_program(program, values)
            except subprocess.TimeoutExpired:
                error = "The program took too long to finish."

    return render_template(
        "program.html",
        key=key,
        program=program,
        values=values,
        output=output,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
