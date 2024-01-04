from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def show_main_page():
    user_responses = session.get('responses', None)
    if user_responses is not None:
        if len(user_responses) >= len(satisfaction_survey.questions):
            flash("You've already completed the survey!")
            return redirect('/thanks')
        elif len(user_responses) != 0:
            flash("You've still got some questions to answer!")
            return redirect('/questions/' + str(len(user_responses))) 
    return render_template("main.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/start-survey', methods=["POST"])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<q_number>')
def show_question(q_number):
    if session.get('responses', None) is None:
        flash("Please click the button to start the survey.")
        return redirect('/')
    
    q_number = int(q_number)
    if q_number != len(session["responses"]) and len(session["responses"]) < len(satisfaction_survey.questions):
        flash("You've tried to go to the wrong question! Here is the next one.")
        return redirect('/questions/' + str(len(session["responses"])))
    elif len(session["responses"]) >= len(satisfaction_survey.questions):
        flash("You've already completed the survey!")
        return redirect('/thanks')
    current_question = satisfaction_survey.questions[q_number]
    return render_template("question.html", question_number=q_number, question_text=current_question.question, choices = current_question.choices)

@app.route('/answer', methods=["POST"])
def add_response():
    answer = request.form["answer"]
    # add answer to the list of user responses
    user_responses = session["responses"]
    user_responses.append(answer)
    session["responses"] = user_responses
    
    if len(session["responses"]) >= len(satisfaction_survey.questions):
        return redirect('/thanks')
    return redirect('/questions/' + str(len(session["responses"])))

@app.route('/thanks')
def show_thanks():
    if session.get('responses', None) is None:
        flash("Please click the button to start the survey.")
        return redirect('/')
    elif len(session['responses']) < len(satisfaction_survey.questions):
        flash("You still have some questions to complete!")
        return redirect('/questions/' + str(len(session['responses'])))
    return render_template("thanks.html", survey_name=satisfaction_survey.title)