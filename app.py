from flask import Flask, render_template, request, redirect, url_for, session
import json
import gspread
import os

app = Flask(__name__)
app.secret_key = "secret"

with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

SHEET_ID = "1N9ZXLVYHfz6giwu5C1xLFm1RFmFpK49UQNF0ff56Lds"

gc = gspread.service_account(filename="service_account.json")
sh = gc.open_by_key(SHEET_ID)
worksheet = sh.sheet1


@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":

        answers = {}

        for q in QUESTIONS:

            answers[str(q['id'])] = request.form.get(f"q{q['id']}")

        hints_used = request.form.get("hints_used")

        session['answers'] = answers

        row = [answers.get(str(q['id']), "") for q in QUESTIONS]

        row.append(hints_used)

        worksheet.append_row(row)

        return redirect(url_for("result"))

    answers = session.get('answers',{})

    return render_template("questionnaire.html",
                           questions=QUESTIONS,
                           answers=answers)


@app.route("/result")
def result():

    answers = session.get('answers',{})

    return render_template("result.html",answers=answers)


if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)