# http://www.scrabbleplayers.org/w/NASPA_Zyzzyva_Linux_Installation
WORD_FILE_NAME = 'NWL2020.txt'

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
                best_12_words.append(score)
                found_words.append(score['word'])
                petal_letter_words[score['letter']] = petal_letter_words[score['letter']] + 1
            if len(best_12_words) == 12:
                break

    return best_12_words


