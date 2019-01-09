from ..memory import memory, known_words
import json

# can compute how many chances there are for each len of subject

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way


# computes the words and what they are
def compute_words(words, words_dir):

    # setting up the main variable
    _words = []

    # initial general for loop
    for word_index, word in enumerate(words):

        # adds '_' to punctuations
        if word in known_words.punctuation_symbols:
            word = '_' + word

        # sets the json_path
        json_path = memory.return_json_word_path(word, words_dir)

        # gets the file json_word
        json_word = json.loads(open(json_path).read())

        # gets the lexical_entries
        lexical_entries = json_word['results'][0]['lexicalEntries']

        # sets up possibilities variable
        possibilities = []

        # loops through each and appends to possibilities
        for le in lexical_entries:
            possibilities.append({le['lexicalCategory']: 0})

        # appends to word_order
        _words.append(("{}".format(word), possibilities, word_index))

        print("{} - {}".format(word, possibilities))

    print(_words)

    # loop to start computing its confidence
    for _word_index, _word in enumerate(_words):

        # handles determiners
        determiner = [d for d in _word[1] if 'Determiner' in d]
        if len(determiner) > 0:

            # looks to the next word and checks if it is a noun
            next_word = _words[_word_index + 1]
            noun = [n for n in next_word[1] if 'Noun' in n]
            if len(noun) > 0:
                determiner[0]['Determiner'] += 1

        # handles pronouns
        pronoun = [p for p in _word[1] if 'Pronoun' in p]
        if len(pronoun) > 0:

            # looks to next word and checks if it is a verb
            next_word = _words[_word_index + 1]
            verb = [v for v in next_word[1] if 'Verb' in v]
            if len(verb) > 0:
                pronoun[0]['Pronoun'] += 1

        # handles nouns
        noun = [p for p in _word[1] if 'Noun' in p]
        if len(noun) > 0:

            # looks to next word and checks if it is a verb
            next_word = _words[_word_index + 1]
            verb = [v for v in next_word[1] if 'Verb' in v]
            if len(verb) > 0:
                noun[0]['Noun'] += 1

    print(_words)

    return _words


# computes the subject
def compute_subject(words, words_dir):

    # printing stuff
    print("\nAnalyzing for the subject\n")

    # setting the initial variables
    subject = ''
    simple_subject = ''

    # setting the initial word order
    _words = compute_words(words, words_dir)

    # sets the first_noun_or_pronoun
    first_noun_or_pronoun = None

    # finds the noun and sets it
    for word_index, word in enumerate(_words):

        # sets the space
        space = ''

        # checks if noun
        if word[1] == 'Noun' or word[1] == 'Pronoun':

            # assigns the first noun
            first_noun_or_pronoun = word
            break

    # checks the words to the left of the first_noun_or_pronoun for determiners & modifiers
    for word_left in _words[:first_noun_or_pronoun[2] + 1]:

        # sets the space
        space = ''

        # stop condition
        if word_left[1] not in [
                'Noun', 'Pronoun', 'Determiner', 'Adjective', 'Conjunction'
        ]:
            continue

        # checks if subject is empty
        if subject != '' and word_left[0].strip(
                '_') not in known_words.punctuation_symbols:
            space = ' '

        # appends noun to subject
        subject += space + word_left[0].strip('_')

    # checks the words to the right of the first_noun_or_pronoun for prepositions & complete subjects
    for word_right in _words[first_noun_or_pronoun[2] + 1:]:

        # sets the space
        space = ''

        # appends a comma, if there is
        if word_right[0] == '_,':
            subject += word_right[0].strip('_')
            continue

        # handles if it finds a pronoun
        if word_right[1] == 'Pronoun':

            # if the word right after it is a verb
            if _words[word_right[2] + 1][1] == 'Verb':

                # sets the initial sub_words
                sub_words = []
                sub_words_verb_found = False

                # appends word_right to sub_words
                sub_words.append(word_right)

                # appends all words to the right of word_right until a verb
                for sub_word_right in _words[word_right[2] + 1:]:

                    # stops if it finds a verb
                    if sub_word_right[1] == 'Verb':

                        # checks if sub word verb has been found
                        if not sub_words_verb_found:
                            sub_words_verb_found = True
                        else:
                            break

                    # appends to sub_words
                    sub_words.append(sub_word_right)

                # appends sub_words to subject
                for sub_word in sub_words:

                    # sets the space
                    space = ''

                    # appends to subject
                    if subject != '' and sub_word[0].strip(
                            '_') not in known_words.punctuation_symbols:
                        space = ' '

                    subject += space + sub_word[0].strip('_')

            break

        # handles if it finds a verb
        if word_right[1] == 'Verb':
            break

        # appends to subject
        if subject != '' and word_right[0].strip(
                '_') not in known_words.punctuation_symbols:
            space = ' '

        # appends to subject
        subject += space + word_right[0].strip('_')

    print("\nThe subject is: \"{}\"\n".format(subject))

    return subject


# computes the predicate
def compute_predicate(words, words_dir):

    predicate = ''

    return predicate


# computes the word tree
def compute_word_tree(words, words_dir):

    # computes the subject
    subject = compute_subject(words, words_dir)

    # computes the predicate
    predicate = compute_predicate(words, words_dir)

    return subject, predicate