from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("questions.json", encoding="utf-8") as f:
    questions = json.load(f)

@app.route("/", methods=["GET", "POST"])
def questionnaire():
    if request.method == "POST":
        answers = dict(request.form)
        return answers

    return render_template("index.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
