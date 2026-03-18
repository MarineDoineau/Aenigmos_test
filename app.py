from flask import Flask, render_template, request, redirect, url_for, session, send_file
import json
import csv
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Charger les questions
with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

CSV_FILE = "responses.csv"

# Créer le CSV avec entêtes si inexistant
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        headers = [f"Q{q['id']}" for q in QUESTIONS]
        writer.writerow(headers)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        answers = {}
        for q in QUESTIONS:
            answer = request.form.get(f"q{q['id']}")
            answers[str(q['id'])] = answer

        session['answers'] = answers

        # 🔥 Ajouter les réponses dans le CSV
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            row = [answers.get(str(q['id']), "") for q in QUESTIONS]
            writer.writerow(row)

        return redirect(url_for("result"))

    answers = session.get('answers', {})
    return render_template("questionnaire.html", questions=QUESTIONS, answers=answers)

@app.route("/result")
def result():
    answers = session.get('answers', {})
    return render_template("result.html", answers=answers)

# Route pour télécharger le CSV (optionnel)
@app.route("/download")
def download_csv():
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)