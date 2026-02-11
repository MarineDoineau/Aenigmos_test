from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Charger les questions depuis le JSON
with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Récupérer toutes les réponses
        answers = {}
        for q in QUESTIONS:
            answer = request.form.get(f"q{q['id']}")
            answers[str(q['id'])] = answer
        session['answers'] = answers
        return redirect(url_for("result"))

    return render_template("questionnaire.html", questions=QUESTIONS)

@app.route("/result")
def result():
    answers = session.get('answers', {})
    return render_template("result.html", answers=answers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
