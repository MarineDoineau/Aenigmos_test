from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Questions dynamiques
QUESTIONS = {
    "q1": {
        "text": "Quel est ton objectif principal ?",
        "choices": {
            "sport": "Faire du sport",
            "business": "Créer un business",
            "dev": "Apprendre à coder"
        }
    },
    "q2_sport": {
        "text": "Quel type de sport préfères-tu ?",
        "choices": {
            "muscu": "Musculation",
            "cardio": "Cardio"
        }
    },
    "q2_business": {
        "text": "Quel domaine t'intéresse ?",
        "choices": {
            "ecommerce": "E-commerce",
            "saas": "SaaS"
        }
    },
    "q2_dev": {
        "text": "Quel langage t'intéresse ?",
        "choices": {
            "python": "Python",
            "javascript": "JavaScript"
        }
    }
}

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

@app.route("/question/<question_id>", methods=["GET", "POST"])
def question(question_id):
    if request.method == "POST":
        answer = request.form.get("answer")
        session[question_id] = answer

        if question_id == "q1":
            return redirect(url_for("question", question_id=f"q2_{answer}"))
        else:
            return redirect(url_for("result"))

    question_data = QUESTIONS.get(question_id)
    if not question_data:
        return redirect(url_for("home"))

    return render_template("question.html", question=question_data, question_id=question_id)

@app.route("/result")
def result():
    answers = dict(session)

    recommendation = "Merci pour tes réponses !"

    if answers.get("q1") == "sport":
        recommendation = "Programme sportif personnalisé en préparation 💪"
    elif answers.get("q1") == "business":
        recommendation = "Stratégie business personnalisée 🚀"
    elif answers.get("q1") == "dev":
        recommendation = "Roadmap développeur personnalisée 💻"

    return render_template("result.html", recommendation=recommendation, answers=answers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
