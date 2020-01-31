from ..memory import memory, known_words
import json

from flask import current_app as app
from server.models import Category

# can compute how many chances there are for each len of subject

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way


# computes the words and what they are
def compute_words(words, words_dir):

    # setting up the main variable
    _words = []

    # initial word info
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
        possibilities = {}

        # loops through each and appends to possibilities
        for le in lexical_entries:
            possibilities[le['lexicalCategory']] = 0

        # appends to _words
        _words.append({
            "string": word,
            "type": possibilities,
            "index": word_index
        })

    # starts computing word_type confidences
    for _word_index, _word in enumerate(_words):

        # handles determiners
        if 'Determiner' in _word['type']:

            # checks if word to the right is a noun
            if _word_index < len(_words) - 1:
                next_word = _words[_word_index + 1]
                if 'Noun' in next_word['type']:
                    _word['type']['Determiner'] += 10

        # handles pronouns
        if 'Pronoun' in _word['type']:

            pass

        # handles nouns
        if 'Noun' in _word['type']:

            # check the word to the left for determiner, adjective
            if _word_index != 0:
                previous_word = _words[_word_index - 1]
                if 'Determiner' in previous_word[
                        'type'] or 'Adjective' in previous_word['type']:
                    _word['type']['Noun'] += 5

        # handles adjectives
        if 'Adjective' in _word['type']:

            # check the word to the left for verb
            if _word_index != 0:
                previous_word = _words[_word_index - 1]
                if 'Verb' in previous_word['type']:
                    _word['type']['Adjective'] += 5

            # check the word to the right for a determiner, pronoun, or noun
            if _word_index < len(_words) - 1:
                next_word = _words[_word_index + 1]
                if 'Determiner' in next_word['type'] or 'Pronoun' in next_word[
                        'type'] or 'Noun' in next_word['type']:
                    _word['type']['Adjective'] += 5

        # handles verbs
        if 'Verb' in _word['type']:

            # check the word to the right for a determiner, pronoun, or noun
            if _word_index < len(_words) - 1:
                next_word = _words[_word_index + 1]
                if 'Determiner' in next_word['type'] or 'Pronoun' in next_word[
                        'type'] or 'Noun' in next_word['type']:
                    _word['type']['Verb'] += 5

        # handles adverbs
        if 'Adverb' in _word['type']:

            # check the word to the right and see if it might be an adjective or adverb
            if _word_index < len(_words) - 1:
                next_word = _words[_word_index + 1]
                if 'Adjective' in next_word['type'] or 'Adverb' in next_word[
                        'type']:
                    _word['type']['Adverb'] += 5

        # handles conjunctions
        if 'Conjunction' in _word['type']:

            # check the word to the right for a determiner, pronoun, or noun
            if _word_index < len(_words) - 1:
                next_word = _words[_word_index + 1]
                if 'Determiner' in next_word['type'] or 'Pronoun' in next_word[
                        'type'] or 'Noun' in next_word['type']:
                    _word['type']['Conjunction'] += 5

        # handles prepositions
        if 'Preposition' in _word['type']:

            # check if word to the right is a determiner, pronoun, or noun
            if _word_index < len(_words) - 1:
                next_word = _words[_word_index + 1]
                if 'Determiner' in next_word['type'] or 'Pronoun' in next_word[
                        'type'] or 'Noun' in next_word['type']:
                    _word['type']['Preposition'] += 5

    # # loop to start computing its confidence
    # for _word_index, _word in enumerate(_words):

    #     # handles determiners
    #     determiner = [d for d in _word['type'] if 'Determiner' in d]
    #     if len(determiner) > 0:

    #         # looks to the next word and checks if it is a noun
    #         next_word = _words[_word_index + 1]
    #         noun = [n for n in next_word['type'] if 'Noun' in n]
    #         if len(noun) > 0:
    #             determiner[0]['Determiner'] += 1

    #     # handles pronouns
    #     pronoun = [p for p in _word['type'] if 'Pronoun' in p]
    #     if len(pronoun) > 0:

    #         # looks to next word and checks if it is a verb or noun
    #         if _word_index < len(_words) - 1:
    #             next_word = _words[_word_index + 1]

    #             # verb
    #             verb = [v for v in next_word['type'] if 'Verb' in v]
    #             if len(verb) > 0:
    #                 pronoun[0]['Pronoun'] += 1

    #             # noun
    #             noun = [n for n in next_word['type'] if 'Noun' in n]
    #             if len(noun) > 0:
    #                 pronoun[0]['Pronoun'] += 1

    #     # handles nouns
    #     noun = [p for p in _word['type'] if 'Noun' in p]
    #     if len(noun) > 0:

    #         # checks word to the left
    #         if _word_index > 0:
    #             word_to_the_left = _words[_word_index - 1]

    #             # if it's a determiner
    #             determiner = [
    #                 d for d in word_to_the_left['type'] if 'Determiner' in d
    #             ]
    #             if len(determiner) > 0:
    #                 noun[0]['Noun'] += 1

    #         # checks word to the right
    #         if _word_index < len(_words) - 1:
    #             word_to_the_right = _words[_word_index + 1]

    #             # if it's a verb
    #             verb = [v for v in word_to_the_right['type'] if 'Verb' in v]
    #             if len(verb) > 0:
    #                 noun[0]['Noun'] += 1

    #     print(max([next_word['type'][''] for x in dict_list]))

    for _word in _words:
        print(_word)

    return _words


# computes the subject
def compute_subject(words):

    if app.config['DEBUG']:
        print("\nAnalyzing for the subject...\n")

    subject = ''
    simple_subject = ''

    # this section computes the word categories
    # based on their existing potential lexical
    # categories
    #
    # for example: fire can be both a 'verb' and a
    # 'noun'. This section figures out with a certain
    # level of confidence which one it is
    #
    #
    enhanced_words = []
    for index, word in enumerate(words):

        # computes lexical categories
        categories = {}
        for category in word.categories:
            categories[category] = 0

        word_object = {
            "string": word,
            "categories": categories,
            "index": index,
        }

        enhanced_words.append(word_object)

    # brings everything back to words
    words = enhanced_words

    # sets word categories
    adjective = Category.query.filter_by(string='adjective').first()
    determiner = Category.query.filter_by(string='determiner').first()
    noun = Category.query.filter_by(string='noun').first()

    # word computation begins here
    for word in words:

        # handles nouns
        if noun in word['categories']:

            # check the word to the left for determiner, adjective
            if word['index'] > 0:
                previous_word = words[word['index'] - 1]

                if determiner in previous_word['categories'] or adjective in previous_word['categories']:
                    word['categories'][noun] += 5

    if app.config['DEBUG']:
        for word in enhanced_words:
            print(
                f'{word["string"]}\n------\n{word["categories"]}\n\n')

    return

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
