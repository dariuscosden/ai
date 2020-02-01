from flask import current_app as app
import re


# sanitizes the string before passing it on
def sanitize_input(string):

    # keeps only one ?
    if '?' in string:
        string = string.replace("?", "")
        string += '?'

    if app.config['DEBUG']:
        print(f'\nWhat I understood: {string}\n')

    return string


# returns words from string
def return_words_from_input(input):

    # sets up words list
    words = []

    # TODO: sanitize input to remove numbers and unwanted characters
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
        print('********************\n')
        print(f'I generated the following words list: {words}\n')

    return words
