from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load questions from a JSON file
def load_questions():
    with open('questions.json') as f:
        return json.load(f)

questions = load_questions()

@app.route('/')
def index():
    return render_template('index.html')  # School level selection page

@app.route('/quiz/<level>')
def quiz(level):
    if level in questions:
        return render_template('quiz.html', questions=questions[level], level=level)
    else:
        return "Invalid level", 404

@app.route('/result', methods=['POST'])
def result():
    data = request.json
    correct_answers = []
    score = 0

    for i, q in enumerate(data['questions']):
        correct = questions[data['level']][i]['correct']
        selected_answer = q['selected']
        correct_answer = questions[data['level']][i]['options'][correct]

        # Check if the answer is correct
        if selected_answer == correct:
            score += 1

        correct_answers.append({
            'question': q['question'],
            'options': q['options'],
            'selected': selected_answer,
            'correct': correct_answer,
            'explanation': questions[data['level']][i]['explanation'],
            'funFact': questions[data['level']][i]['funFact']
        })
    
    # Return the result details along with score and explanations
    return jsonify(correct_answers)

if __name__ == '__main__':
    app.run(debug=True)
