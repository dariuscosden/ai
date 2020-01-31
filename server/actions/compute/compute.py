from ..memory import memory, known_words
import json

from flask import current_app as app
from server.models import Category
import operator

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way


# computes categories
def assign_points(category, words, word, direction, values, points):

    # sets word categories
    adjective = Category.query.filter_by(string='adjective').first()
    conjunction = Category.query.filter_by(string='conjunction').first()
    determiner = Category.query.filter_by(string='determiner').first()
    noun = Category.query.filter_by(string='noun').first()
    preposition = Category.query.filter_by(string='preposition').first()
    pronoun = Category.query.filter_by(string='pronoun').first()
    verb = Category.query.filter_by(string='verb').first()

    # handles left direction
    if direction == 'left':

        if word['index'] > 0:
            previous_word = words[word['index'] - 1]

            for value in values:
                if any(v in previous_word['categories'] for v in values):
                    word['categories'][category] += points
                    break

    # handles right direction
    if direction == 'right':

        if word['index'] < len(words) - 1:
            next_word = words[word['index'] + 1]

            for value in values:
                if any(v in next_word['categories'] for v in values):
                    word['categories'][category] += points
                    break

    return


# computes the subject
def compute_subject(words):

    if app.config['DEBUG']:
        print('********************\n')
        print("Analyzing for the subject...\n")

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
    conjunction = Category.query.filter_by(string='conjunction').first()
    determiner = Category.query.filter_by(string='determiner').first()
    noun = Category.query.filter_by(string='noun').first()
    preposition = Category.query.filter_by(string='preposition').first()
    pronoun = Category.query.filter_by(string='pronoun').first()
    verb = Category.query.filter_by(string='verb').first()

    # word computation begins here
    for word in words:

        # handles determiners
        if determiner in word['categories']:

            # check the word to the right for noun, adjective
            assign_points(
                determiner,
                words,
                word,
                'right',
                [noun, adjective],
                5
            )

        # handles nouns
        if noun in word['categories']:

            # check the word to the left for determiner, adjective
            assign_points(
                noun,
                words,
                word,
                'left',
                [determiner, adjective],
                5
            )

            # check the word to the right for verb
            assign_points(
                noun,
                words,
                word,
                'right',
                [verb],
                5
            )

            # check the word to the right for noun
            assign_points(
                noun,
                words,
                word,
                'right',
                [noun],
                -5
            )

        # handles adjectives
        if adjective in word['categories']:

            # check the word to the left for verb or determiner
            assign_points(
                adjective,
                words,
                word,
                'left',
                [verb, determiner],
                5
            )

            # check the word to the right for a determiner, pronoun, or noun
            assign_points(
                adjective,
                words,
                word,
                'right',
                [determiner, pronoun, noun],
                5
            )

        # handles verbs
        if verb in word['categories']:

            # check the word to the left for determiner, pronoun, noun
            assign_points(
                verb,
                words,
                word,
                'left',
                [determiner, pronoun, noun],
                5
            )

            # check the word to the right for a determiner, pronoun, or noun
            assign_points(
                verb,
                words,
                word,
                'right',
                [determiner, pronoun, noun],
                5
            )

        # handles conjunctions
        if conjunction in word['categories']:

            # check the word to the right for a determiner, pronoun, or noun
            assign_points(
                conjunction,
                words,
                word,
                'right',
                [determiner, pronoun, noun],
                5
            )

        # handles prepositions
        if preposition in word['categories']:

            # check the word to the right for a determiner, pronoun, or noun
            assign_points(
                preposition,
                words,
                word,
                'right',
                [determiner, pronoun, noun],
                5
            )

    if app.config['DEBUG']:
        for word in words:
            print(
                f'{word["string"]}\n------\n{word["categories"]}\n')

    # here we compile the words into the
    # maximum value computed for each object
    #
    # i.e. we assign 'noun' or 'verb' to each
    # word depending on the computations above
    #
    #
    computed_words = []
    for word in words:

        category = max(word['categories'].items(),
                       key=operator.itemgetter(1))[0]

        word_object = {
            "string": word['string'],
            "category": category,
            "index": word['index'],
        }

        computed_words.append(word_object)

    words = computed_words

    if app.config['DEBUG']:
        print('********************\n')
        print('Collapsing the word categories...\n')

    if app.config['DEBUG']:
        for word in words:
            print(f'{word["string"]} | {word["category"]}\n')

    # this section finds the subject of the input
    # by assuming that the first noun in the
    # given input is the simple subject
    #
    # it then attempts to find the remainder of
    # the subject by looping through the words
    # to the left and right of the simple subject
    #
    #
    simple_subject = None

    # loops through the words to find the first noun
    for word in words:
        if word['category'] == noun:
            simple_subject = word
            break

    if app.config['DEBUG']:
        print('********************\n')
        print(f'The simple subject is: {simple_subject["string"]}\n')

    if app.config['DEBUG']:
        print('********************\n')
        print(f'Finding the complete subject...\n')

    complete_subject = []
    last_index = simple_subject['index']

    # loops through the words to the left of the subject until
    # it finds a verb
    for word in reversed(words[:simple_subject['index'] + 1]):

        if word['category'] == verb:
            break

        complete_subject.insert(0, word['string'])

    # loops through the words to the right of the subject until
    # it finds a verb
    for word in words[simple_subject['index'] + 1:]:

        if word['category'] == verb:
            break

        complete_subject.append(word['string'])
        last_index = word['index']

    if app.config['DEBUG']:
        print(f'The complete subject is: {complete_subject}\n')

    return words, complete_subject, last_index


# computes the predicate
def compute_predicate(words, last_index):

    if app.config['DEBUG']:
        print('********************\n')
        print("Analyzing for the predicate...\n")

    # this section computes the predicate by looping
    # through the words starting from the last index
    # and assuming that everything is the predicate
    # until...
    #
    #
    predicate = []
    for word in words[last_index + 1:]:

        predicate.append(word['string'])

    if app.config['DEBUG']:
        print(f'The predicate is: {predicate}\n')

    return
