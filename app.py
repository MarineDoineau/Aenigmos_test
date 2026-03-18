from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Charger les questions depuis le JSON
with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        answers = {}

        # Récupérer les réponses du formulaire
        for q in QUESTIONS:
            answer = request.form.get(f"q{q['id']}")
            answers[str(q['id'])] = answer

        # Stocker en session (pour affichage et modification)
        session['answers'] = answers

        # 🔥 Sauvegarde dans un fichier texte
        try:
            with open("responses.txt", "a", encoding="utf-8") as f:
                f.write(json.dumps(answers, ensure_ascii=False) + "\n")
        except Exception as e:
            print("Erreur lors de la sauvegarde :", e)

        return redirect(url_for("result"))

    # Récupérer les réponses existantes (si déjà remplies)
    answers = session.get('answers', {})

    return render_template(
        "questionnaire.html",
        questions=QUESTIONS,
        answers=answers
    )

@app.route("/result")
def result():
    answers = session.get('answers', {})
    return render_template("result.html", answers=answers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)