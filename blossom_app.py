from flask import Flask, render_template, request, redirect
import os
import sys
import logging
import requests

DICTIONARY_API_KEY = os.environ['DICTIONARY_API_KEY']

# http://www.scrabbleplayers.org/w/NASPA_Zyzzyva_Linux_Installation
WORD_FILE_NAME = 'NWL2020.txt'

#https://dictionaryapi.com/products/api-collegiate-dictionary
DICTIONARY_API = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s'

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_all_words(petal_letters, mandatory_letter, min_word_length):
    words = open(WORD_FILE_NAME, 'r')
    all_letters = [l for l in petal_letters]
    all_letters.append(mandatory_letter)
    all_words = []
    for word in words:
        if len(word) >= min_word_length and mandatory_letter in word:
            stripped_word = word.strip()
            if set(stripped_word).issubset(all_letters):
                all_words.append(stripped_word)

    words.close()
    return sorted(all_words, key=lambda x:len(x), reverse=True)

def get_scores(all_words, petal_letters, mandatory_letter):
    all_scores = []
    for word in all_words:
        word_scores = score_word(word, petal_letters, mandatory_letter)
        all_scores = all_scores + word_scores
    return sorted(all_scores, key=lambda x:x['score'], reverse=True)

def score_word(word, petal_letters, mandatory_letter):
    all_letters = petal_letters + [mandatory_letter]
    all_letters_set = set(all_letters)


    # Start scoring by calculating points for length
    if len(word) == 4:
        base_score = 2
    elif len(word) == 5:
        base_score = 4
    elif len(word) == 6:
        base_score = 6
    elif len(word) == 7:
        base_score = 12
    else:
        base_score = 12 + 3 * (len(word) - 7)

    # Next add 7 points if all 7 letters are used
    word_letters_set = set(word)
    if all_letters_set == word_letters_set:
        base_score += 7
    
    # Now calculate 5 point bonus for each of the petal letters
    scores = []
    for letter in petal_letters:
        petal_letter_score = base_score + word.count(letter) * 5
        scores.append({"word": word,
                       "letter": letter,
                       "score": petal_letter_score})
    return scores

def get_best_12_words(all_scores, petal_letters):

    # This assumes all_scores is sorted by score, descending
    best_12_words = []
    found_words = []
    petal_letter_words = {}
    for letter in petal_letters:
        petal_letter_words[letter] = 0

    for score in all_scores:
        if score['word'] not in found_words:
            if petal_letter_words[score['letter']] < 2:
                response = requests.get(DICTIONARY_API % (score['word'], DICTIONARY_API_KEY))
                if response.status_code == 200:
                    results = response.json()
                    x = results[0]
                    if isinstance(x, str):
                        log('invalid: %s' % score['word'])
                    else:
                        log('valid: %s' % score['word'])
                        best_12_words.append(score)
                        found_words.append(score['word'])
                        petal_letter_words[score['letter']] = petal_letter_words[score['letter']] + 1
            if len(best_12_words) == 12:
                break

    return best_12_words

def log(log_message):
    if app is not None:
        app.logger.info(log_message)
    else:
        print(log_message)

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
    all_words = get_all_words(petal_letters, center_letter, min_word_length=6)
    all_scores = get_scores(all_words, petal_letters, center_letter)
    best_12_words = get_best_12_words(all_scores, petal_letters)
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

log('Starting %s %s' % (sys.argv[0], app.name))
log('Python: ' + sys.version)


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
log('Running build: %s' % build_stamp)
log('\nEnvironment Variables:')
for key in os.environ.keys():
    log('%s: \t\t%s' % (key, os.environ[key]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))



