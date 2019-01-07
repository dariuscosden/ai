from ..memory import memory, known_words
import json

# can compute how many chances there are for each len of subject

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way


# computes the subject
def compute_subject(words, words_dir):

    # printing stuff
    print("\nAnalyzing for the subject\n")

    # setting the initial variables
    subject = ''
    simple_subject = ''

    # setting the initial word order
    word_order = []

    # initial general for loop
    for word_index, word in enumerate(words):

        # sets the json_path
        json_path = memory.return_json_word_path(word, words_dir)

        # gets the file json_word
        json_word = json.loads(open(json_path).read())

        # gets the word_type
        word_type = json_word['results'][0]['lexicalEntries'][0][
            'lexicalCategory']

        # appends to word_order
        word_order.append(("{}".format(word), word_type, word_index))

        print("{} - {}".format(word, word_type))

    # sets the first_noun_or_pronoun
    first_noun_or_pronoun = None

    # finds the noun and sets it
    for word_index, word in enumerate(word_order):

        # sets the space
        space = ''

        # checks if noun
        if word[1] == 'Noun' or word[1] == 'Pronoun':

            # assigns the first noun
            first_noun_or_pronoun = word
            break

    # checks the words to the left of the first_noun_or_pronoun for determiners & modifiers
    for word_left in word_order[:first_noun_or_pronoun[2] + 1]:

        # stop condition
        if word_left[1] not in [
                'Noun', 'Pronoun', 'Determiner', 'Adjective', 'Conjunction'
        ]:
            continue

        # checks if subject is empty
        if subject != '':
            space = ' '

        # appends noun to subject
        subject += space + word_left[0].strip('_')

    # checks the words to the right of the first_noun_or_pronoun for prepositions & complete subjects
    for word_right in word_order[first_noun_or_pronoun[2] + 1:]:

        # handles if it finds a pronoun
        if word_right[1] == 'Pronoun':

            # if the word right after it is a verb
            if word_order[word_right[2] + 1][1] == 'Verb':

                # sets the initial sub_words
                sub_words = []
                sub_words_verb_found = False

                # appends word_right to sub_words
                sub_words.append(word_right)

                # appends all words to the right of word_right until a verb
                for sub_word_right in word_order[word_right[2] + 1:]:

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

                    # appends to subject
                    if subject != '':
                        space = ' '

                    subject += space + sub_word[0].strip('_')

            break

        # handles if it finds a verb
        if word_right[1] == 'Verb':
            break

        # appends to subject
        if subject != '':
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