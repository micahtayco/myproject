from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "samplekey"   # secret key is required for session


# quotes
def load_quotes():
    with open('quotes.txt', encoding='utf-8') as file:
        return file.read().splitlines()


# Landing Page
@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')

    if 'users' not in session:
        session['users'] = {}

    users = session['users']

    # if new user → create entry
    if name not in users:
        users[name] = {
            "tasks": [],
            "mood": None
        }

    # save current user
    session['name'] = name
    session['users'] = users

    return redirect(url_for('result'))


@app.route('/result', methods=['GET', 'POST'])
def result():

    name = session.get('name')
    users = session.get('users', {})

    # get current user data
    user = users.get(name, {"tasks": [], "mood": None})

    tasks = user["tasks"]
    mood = user["mood"]

    if request.method == 'POST':

        # update mood
        if request.form.get('mood'):
            user["mood"] = request.form.get('mood')

        # add task
        if request.form.get('task'):
            tasks.append({
                "text": request.form.get('task'),
                "done": False
            })

        # checkbox toggle
        if request.form.get('index') is not None:
            index = int(request.form.get('index'))
            tasks[index]["done"] = True if request.form.get('done') == "on" else False

        
        # delete task
        if request.form.get('delete') is not None:
            index = int(request.form.get('delete'))
            tasks.pop(index)

        # save back to session
        users[name] = user
        session['users'] = users

        return redirect(url_for('result'))

    quotes = load_quotes()
    chosen_quote = random.choice(quotes)

    return render_template(
        'result.html',
        name=name,
        quote=chosen_quote,
        mood=mood,
        tasks=tasks
    )

# always last
if __name__ == '__main__':
    app.run(debug=True)