from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

USER_RESPONSES = []

@app.route('/')
def show_main_page():
    return render_template("main.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/questions/<q_number>')
def show_question(q_number):
    q_number = int(q_number)
    current_question = satisfaction_survey.questions[q_number]
    return render_template("question.html", question_number=q_number, question_text=current_question.question, choices = current_question.choices)

@app.route('/answer/<q_number>', methods=["POST"])
def add_response(q_number):
    answer = request.form["answer"]
    # add answer to the list of user responses
    USER_RESPONSES.append(answer)
    q_number = int(q_number)
    next_q_number = q_number + 1
    next_q_number = str(next_q_number)
    return redirect('/questions/' + next_q_number)