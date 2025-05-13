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

def get_all_word_scores(all_words, petal_letters, mandatory_letter):
    all_scores = []
    for word in all_words:
        word_scores = score_word(word, petal_letters, mandatory_letter)
        all_scores.append(word_scores)
    return sorted(all_scores, key=lambda x:x['scores'][0]['score'], reverse=True)

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
        scores.append({"letter": letter,
                       "score": petal_letter_score})
    sorted_scores = sorted(scores, key=lambda x:x['score'], reverse=True)
    return {"word": word, "scores": sorted_scores}

def get_best_12_words(all_word_scores, petal_letters):

    # This assumes all_scores is sorted by score, descending
    petal_letter_words = {}
    for letter in petal_letters:
        petal_letter_words[letter] = 0

    def answer_complete(petal_letter_words):
        for value in petal_letter_words.values():
            if value < 2:
                return False
        return True
    
    def score_answer(answer):
        score = 0
        for item in answer:
            score += item['score']
        return score
    
    def print_answer(answer):
        answer_str = ''
        for item in answer:
            if len(answer_str) == 0:
                answer_str = "%s:%s:%s" % (item['word'], item['letter'], item['score'])
            else:
                answer_str = "%s, %s:%s:%s" % (answer_str, item['word'], item['letter'], item['score'])
        print("%s: %s" % (score_answer(answer), answer_str))
    
    def get_best_words(words, answer, petal_letter_words):
        if answer_complete(petal_letter_words):
            print_answer(answer)
            return answer
        else:
            best_score = 0
            best_answer = None
            current_word = words[0]
            remaining_words = words.copy()
            remaining_words.remove(current_word)
            for score in current_word['scores']:
                if petal_letter_words[score['letter']] < 2:
                    new_petal_letter_words = petal_letter_words.copy()
                    new_petal_letter_words[score['letter']] += 1
                    if len(answer) == 0:
                        new_answer = [{'word': current_word['word'],
                                   'letter': score['letter'],
                                   'score': score['score']}]
                    else:
                        new_answer = answer.copy()
                        new_answer.append({'word': current_word['word'],
                                   'letter': score['letter'],
                                   'score': score['score']})
                    current_answer = get_best_words(remaining_words, new_answer, new_petal_letter_words)
                    if score_answer(current_answer) > best_score:
                        best_score = score_answer(current_answer)
                        best_answer = current_answer
            return best_answer
        
    best_answer = get_best_words(all_word_scores, {}, petal_letter_words)
    return best_answer
                



if __name__ == "__main__":
    petal_letters = ['A', 'L', 'R', 'G', 'I', 'C']
    mandatory_letter = 'E'
    all_words = get_all_words(petal_letters, mandatory_letter, 7)
    all_word_scores = get_all_word_scores(all_words, petal_letters, mandatory_letter)
    best_12_words = get_best_12_words(all_word_scores, petal_letters)



