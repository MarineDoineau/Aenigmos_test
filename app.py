from flask import Flask, render_template, request, redirect, url_for, session
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Charger les questions depuis le JSON
with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# --- Configuration Google Sheets ---
SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "service_account.json"  # ton fichier JSON
SHEET_ID = "1N9ZXLVYHfz6giwu5C1xLFm1RFmFpK49UQNF0ff56Lds"  # remplace par l'ID de ta Sheet

# Connexion à Google Sheets
try:
    gc = gspread.service_account(filename=CREDS_FILE)
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.worksheet("Sheet1")  # utiliser la première feuille
except Exception as e:
    print("Erreur de connexion Google Sheets :", e)
    worksheet = None  # pour éviter les crashs

# --- Route principale ---
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        answers = {}
        for q in QUESTIONS:
            answer = request.form.get(f"q{q['id']}")
            answers[str(q['id'])] = answer

        # Stocker les réponses en session pour pré-remplissage
        session['answers'] = answers

        # Debug console
        print("DEBUG answers:", answers)

        # Envoyer dans Google Sheets
        if worksheet:
            row = [answers.get(str(q['id']), "") for q in QUESTIONS]
            try:
                worksheet.append_row(row)
                print("✅ Ligne ajoutée à Google Sheets")
            except Exception as e:
                print("Erreur Google Sheets:", e)
        else:
            print("⚠️ Worksheet non initialisé, réponses non envoyées")

        return redirect(url_for("result"))

    # Pré-remplissage si déjà répondu
    answers = session.get('answers', {})
    return render_template("questionnaire.html", questions=QUESTIONS, answers=answers)

# --- Page résultat ---
@app.route("/result")
def result():
    answers = session.get('answers', {})
    return render_template("result.html", answers=answers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)