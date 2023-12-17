from flask import Flask, render_template, request, redirect
import os
import sys
import blossom

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/build', methods=['GET', 'POST'])
def build():
    try:
        build_file = open('static/build.txt')
        build_stamp = build_file.readlines()[0]
        build_file.close()
    except FileNotFoundError:
        from datetime import date
        build_stamp = generate_build_stamp()
    results = 'Running %s %s.\nBuild %s.\nPython %s.' % (sys.argv[0], app.name, build_stamp, sys.version)
    return results

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    form = request.form
    petal_letters = []
    for i in range(6):
        petal_letters.append(form.get('petal%s' % i).upper())
    center_letter = form.get("center").upper()
    all_words = blossom.get_all_words(petal_letters, center_letter, min_word_length=6)
    all_scores = blossom.get_scores(all_words, petal_letters, center_letter)
    best_12_words = blossom.get_best_12_words(all_scores, petal_letters)
    total_score = 0
    for word in best_12_words:
        total_score += word['score']
    solution_content = render_template('solution.html', words=best_12_words, total=total_score)
    return render_template('index.html', 
                           solution=solution_content, 
                           center=center_letter,
                           petal0=petal_letters[0],
                           petal1=petal_letters[1],
                           petal2=petal_letters[2],
                           petal3=petal_letters[3],
                           petal4=petal_letters[4],
                           petal5=petal_letters[5])

@app.route('/clear', methods=['GET', 'POST'])
def clear():
    return redirect('/')

print('Starting %s %s' % (sys.argv[0], app.name))
print('Python: ' + sys.version)


def generate_build_stamp():
    from datetime import date
    return 'Development build - %s' % date.today().strftime("%m/%d/%y")

try:
    build_file = open('static/build.txt')
    build_stamp = build_file.readlines()[0]
    build_file.close()
except FileNotFoundError:
    from datetime import date
    build_stamp = generate_build_stamp()
print('Running build: %s' % build_stamp)
print('\nEnvironment Variables:')
for key in os.environ.keys():
    print('%s: \t\t%s' % (key, os.environ[key]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))



