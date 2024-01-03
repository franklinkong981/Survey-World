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
    if len(USER_RESPONSES) >= len(satisfaction_survey.questions):
        flash("You've already completed the survey!")
        return redirect('/thanks')
    elif len(USER_RESPONSES) != 0:
        flash("You've still got some questions to answer!")
        return redirect('/questions/' + str(len(USER_RESPONSES))) 
    return render_template("main.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/questions/<q_number>')
def show_question(q_number):
    q_number = int(q_number)
    if q_number != len(USER_RESPONSES) and len(USER_RESPONSES) < len(satisfaction_survey.questions):
        flash("You've tried to go to the wrong question! Here is the next one.")
        return redirect('/questions/' + str(len(USER_RESPONSES)))
    elif len(USER_RESPONSES) >= len(satisfaction_survey.questions):
        flash("You've already completed the survey!")
        return redirect('/thanks')
    current_question = satisfaction_survey.questions[q_number]
    return render_template("question.html", question_number=q_number, question_text=current_question.question, choices = current_question.choices)

@app.route('/answer', methods=["POST"])
def add_response():
    answer = request.form["answer"]
    # add answer to the list of user responses
    USER_RESPONSES.append(answer)
    if len(USER_RESPONSES) >= len(satisfaction_survey.questions):
        return redirect('/thanks')
    return redirect('/questions/' + str(len(USER_RESPONSES)))

@app.route('/thanks')
def show_thanks():
    if len(USER_RESPONSES) == 0:
        flash("You must complete the survey to reach the thank you page!")
        return redirect('/')
    elif len(USER_RESPONSES) < len(satisfaction_survey.questions):
        flash("You still have some questions to complete!")
        return redirect('/questions/' + str(len(USER_RESPONSES)))
    return render_template("thanks.html", survey_name=satisfaction_survey.title)