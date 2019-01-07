import re
from ..memory import known_words


# sanitizes the string before passing it on
def sanitize_input(string):

    # keeps only one ?
    if '?' in string:
        string = string.replace("?", "")
        string += '?'

    print('What I understood: {}\n'.format(string))

    return string


# returns words from string
def return_words_from_input(input):
    words = []
    question = False
    exclamation = False

    # starts building the words list
    string_words = re.split('(\W+)', input)

    # iterates through each item in the list
    for word_index, word in enumerate(string_words):

        # removes any empty spaces
        if word == ' ' or word == '':
            continue

        # removes any extra space
        word = word.strip(' ')

        # appends to the words list
        if word in known_words.punctuation_symbols:
            words.append(word)
        else:
            words.append('_' + word)

    print('I generated the following words list: {}\n'.format(words))

    return words