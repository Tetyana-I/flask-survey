from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, satisfaction_survey, personality_quiz

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_code_here"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

@app.route('/')
def choose_the_servey():
    """ start-page that allows a user to choose a survey from a survey list """
    return render_template('choose_survey.html', surveys=surveys.items())

@app.route('/start-page', methods=['POST'])
def start_survey():
    """render a page for the chosen survey that shows the user the title of the survey, the instructions, and a button to start the survey;
    setup session variables """
    current_survey=surveys[request.form.get('choice')] #current survey object
    session['title'] = current_survey.title
    session['num_of_questions'] = len(current_survey.questions)
    session['survey'] = request.form['choice'] # key of current survey in surveys list
    session['comments'] = []
    return render_template('start.html', instructions = current_survey.instructions)

@app.route('/start', methods=['POST'])
def handling_start():
    """ Set a current session responses-list to an empty list and redirect to the start of the survey """
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<question_number>')
def question_page(question_number):
    """ Page shows a form asking the current question, and listing the choices as radio buttons, also comments if are allowed """
    answers = session['responses']
    if len(answers) == session['num_of_questions']:
        return render_template('thanks.html')
    if len(answers) == int(question_number):
        number = int(question_number)
    else:
        flash('Could you please answer this question, you tried to access an invalid question','error')
        number = len(answers)
    current_survey = surveys[session['survey']] 
    current_question = current_survey.questions[number]
    return render_template('question.html', number = number, choices = current_question.choices, question = current_question.question, title = current_survey.title, allow_text = current_question.allow_text)


@app.route('/answer', methods=['POST'])
def handling_answer():
    """ function appends the answer to responses list, adds comments if necessary and then redirect user to the next question; if no more questions in the survey - render thanks page ."""
    comment = request.form.get('comment')
    current_answer = request.form.get('choice')
    answers = session['responses']
    if current_answer:
        answers.append(current_answer)
        session['responses'] = answers
        if comment:
            comments = session['comments']
            comments.append((len(answers),comment))
            session['comments'] = comments
    else:
        flash('We are still waiting for your response!','error')
    if len(answers) < session['num_of_questions']:
        next_question = f"/questions/{len(answers)}"
        return redirect(next_question)
    else:
        return render_template('thanks.html')

