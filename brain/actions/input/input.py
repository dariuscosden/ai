# sanitizes the string before passing it on
def sanitize_input(string):

    # keeps only one ?
    if '?' in string:
        string = string.replace("?", "")
        string += '?'

    print('What I understood: {}\n'.format(string))

    return string


# returns words from string
def return_words_from_input_string(input_string):
    string_words = input_string.split(" ")
    words = []
    question = False
    exclamation = False

    # handles '?' and '!'
    for word in string_words:
        if "?" in word:
            word = word.replace('?', '')
            question = True
        if "!" in word:
            word = word.replace('!', '')
            exclamation = True
        words.append('_' + word)

    # checks for question mark
    if question:
        words.append('?')
    if exclamation:
        words.append('!')

    print('I generated the following words list: {}\n'.format(words))

    return words