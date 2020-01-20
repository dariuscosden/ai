import re
from ..memory import known_words


# sanitizes the string before passing it on
def sanitize_input(string):

    # keeps only one ?
    if '?' in string:
        string = string.replace("?", "")
        string += '?'

    print(f'What I understood: {string}\n')

    return string


# returns words from string
def return_words_from_input(input):
    words_list = []

    # starts building the words list
    string_words = re.split('(\W+)', input)

    # iterates through each item in the list
    for word_index, word in enumerate(string_words):

        # ignores any empty spaces
        if word in [' ', '']:
            continue

        # removes any extra space
        word = word.strip(' ')

        # appends to the words list
        if word in known_words.punctuation_symbols:
            words_list.append(word)
        else:
            words_list.append(word)

    print(f'I generated the following words list: {words_list}\n')

    return words_list
