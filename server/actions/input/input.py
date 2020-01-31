from flask import current_app as app
import re
from ..memory import known_words


# sanitizes the string before passing it on
def sanitize_input(string):

    # keeps only one ?
    if '?' in string:
        string = string.replace("?", "")
        string += '?'

    if app.config['DEBUG']:
        print(f'\nWhat I understood: {string}')

    return string


# returns words from string
def return_words_from_input(input):

    # sets up words list
    words = []
    input = re.split('(\W+)', input)

    # iterates through each item in the list
    for word in input:

        # ignores any empty spaces
        if not word or ' ' in word:
            continue

        # removes any extra space
        word = word.strip(' ')

        # appends to the words list
        words.append(word)

    if app.config['DEBUG']:
        print(f'\nI generated the following words list: {words}')

    return words
