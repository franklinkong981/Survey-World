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

@app.route('/questions/0')
def show_question():
    return render_template("question.html")