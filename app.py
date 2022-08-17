from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'words'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# fake database
responses = []

@app.route("/")
def home_page():
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions
    
    return render_template('home.html', title=title, instructions=instructions)

@app.route("/thankyou")
def thank_you_page():
    return render_template("/thank_you.html")

@app.route("/questions/<num>")
def questions_page(num):
    if int(num) != len(responses):
        flash("Naughty!  Naughty!  You tried to go where you weren't supposed to!")
        return redirect(f"/questions/{len(responses)}")
    question = surveys.satisfaction_survey.questions[int(num)].question
    choices = surveys.satisfaction_survey.questions[int(num)].choices
    num = num

    return render_template('question.html', question=question, choices=choices, num=num)

@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form["answer"]
    responses.append(answer)

    if len(responses) < len(surveys.satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/thankyou")