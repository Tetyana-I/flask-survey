# just to check
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_code_here"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# responses = []
number_of_questions = len(satisfaction_survey.questions)

@app.route('/')
def start_survey():
    """a start-page for a survey that shows the user the title of the survey, the instructions, and a button to start the survey """
    # responses.clear()
    return render_template('start.html', title = satisfaction_survey.title, instructions = satisfaction_survey.instructions)

@app.route('/start', methods=['POST'])
def handling_start():
    """ WHY DO WE NEED POST??? """
    responses = session["responses",[]]
    return redirect('/question/0')

@app.route('/questions/<question_number>')
def question_page(question_number):
    """ Page shows a form asking the current question, and listing the choices as radio buttons """
    if len(responses) == number_of_questions:
        return render_template('thanks.html')
    if len(responses) == int(question_number):
        number = int(question_number)
    else:
        flash('Could you please answer this question, you tried to access an invalid question','error')
        number = len(responses)
    current_question = satisfaction_survey.questions[number]
    return render_template('question.html', number = number, choices = current_question.choices, question = current_question.question)


@app.route('/answer', methods=['POST'])
def handling_answer():
    """ function appends the answer to responses list, and then redirect user to the next question."""
    current_answer = request.form.get('choice')
    if current_answer:
        responses.append(current_answer)
    else:
        flash('We are still waiting for your response!','error')
    if len(responses) < number_of_questions:
        next_question = f"/questions/{len(responses)}"
        return redirect(next_question)
    else:
        return render_template('thanks.html')

