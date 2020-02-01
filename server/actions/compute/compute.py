from flask import current_app as app
from server.models import Category, Word
from server.actions.memory import memory
from server.data import known_words
import json
import operator
import pattern.en

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way


# computes categories
def compute_points(category, words, word, direction, values, points):

    # gets categories
    adjective = Category.query.filter_by(string='adjective').first()
    adverb = Category.query.filter_by(string='adverb').first()
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
                    if category in word['categories']:
                        word['categories'][category] += points
                    break

    # handles right direction
    if direction == 'right':

        if word['index'] < len(words) - 1:
            next_word = words[word['index'] + 1]

            for value in values:
                if any(v in next_word['categories'] for v in values):
                    if category in word['categories']:
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
            "word": word,
            "categories": categories,
            "index": index,
        }

        enhanced_words.append(word_object)

    # brings everything back to words
    words = enhanced_words

    # gets categories
    adjective = Category.query.filter_by(string='adjective').first()
    adverb = Category.query.filter_by(string='adverb').first()
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
            compute_points(
                determiner,
                words,
                word,
                'right',
                [noun, adjective],
                5
            )

        # handles pronouns
        if pronoun in word['categories']:

            # check the word to the right for verb
            compute_points(
                pronoun,
                words,
                word,
                'right',
                [verb],
                5
            )

            # check the word to the right for verb
            compute_points(
                noun,
                words,
                word,
                'right',
                [verb],
                -5
            )

        # handles nouns
        if noun in word['categories']:

            # check the word to the left for determiner, adjective
            compute_points(
                noun,
                words,
                word,
                'left',
                [determiner, adjective],
                5
            )

            # check the word to the right for verb
            compute_points(
                noun,
                words,
                word,
                'right',
                [verb],
                5
            )

            # check the word to the right for noun
            compute_points(
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
            compute_points(
                adjective,
                words,
                word,
                'left',
                [verb, determiner],
                5
            )

            # check the word to the right for a determiner, pronoun, or noun
            compute_points(
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
            compute_points(
                verb,
                words,
                word,
                'left',
                [determiner, pronoun, noun],
                5
            )

            # check the word to the right for a determiner, pronoun, or noun
            compute_points(
                verb,
                words,
                word,
                'right',
                [determiner, pronoun, noun],
                5
            )

        # handles adverbs
        if adverb in word['categories']:

            # check the word to the left for verb
            compute_points(
                adverb,
                words,
                word,
                'left',
                [verb],
                5
            )

            # check the word to the right for an adjective
            compute_points(
                adverb,
                words,
                word,
                'right',
                [adjective],
                5
            )

        # handles conjunctions
        if conjunction in word['categories']:

            # check the word to the right for a determiner, pronoun, or noun
            compute_points(
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
            compute_points(
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
                f'{word["word"]}\n------\n{word["categories"]}\n')

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
            "word": word['word'],
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
            print(f'{word["word"]} | {word["category"]}\n')

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
        if word['category'] in [noun, pronoun]:
            simple_subject = word
            break

    if app.config['DEBUG']:
        print('********************\n')
        print(f'The simple subject is: {simple_subject["word"]}\n')

    if app.config['DEBUG']:
        print('********************\n')
        print(f'Finding the complete subject...\n')

    complete_subject = []
    debug_complete_subject = []
    last_index = simple_subject['index']

    # loops through the words to the left of the subject until
    # it finds a verb
    for word in reversed(words[:simple_subject['index'] + 1]):

        if word['category'] == verb:
            break

        complete_subject.insert(0, word)
        debug_complete_subject.insert(0, word['word'])

    # loops through the words to the right of the subject until
    # it finds a verb
    for word in words[simple_subject['index'] + 1:]:

        if word['category'] == verb:
            break

        complete_subject.append(word)
        debug_complete_subject.append(word['word'])
        last_index = word['index']

    if app.config['DEBUG']:
        print(f'The complete subject is: {debug_complete_subject}\n')

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
    debug_predicate = []
    for word in words[last_index + 1:]:

        predicate.append(word)
        debug_predicate.append(word['word'])

    if app.config['DEBUG']:
        print(f'The predicate is: {debug_predicate}\n')

    return predicate


# computes the tense of the subject
def compute_subject_tense(words):

    # creates the tense object
    tense = {
        "person": {
            1: 0,
            2: 0,
            3: 0,
        },
        "number": {
            "singular": 0,
            "plural": 0
        }
    }

    # loops through the words
    for word in words:

        # handles determiners
        determiner = Category.query.filter_by(string="determiner").first()
        if word['category'] == determiner:

            # handles singular determiners
            if word['word'].string in known_words.singular_determiners:
                tense["person"][3] += 5
                tense["number"]["singular"] += 5

            # handles plural determiners
            if word['word'].string in known_words.plural_determiners:
                tense["person"][3] += 5
                tense["number"]["plural"] += 5

        # handles pronouns
        pronoun = Category.query.filter_by(string="pronoun").first()
        if word['category'] == pronoun:

            # checks for singular pronouns
            if word['word'].string in ['you']:
                tense["person"][2] += 5
                tense["number"]["singular"] += 5

            # checks for singular pronouns
            if word['word'].string in ['he', 'she']:
                tense["person"][3] += 5
                tense["number"]["singular"] += 5

        # handles nouns
        noun = Category.query.filter_by(string="noun").first()
        if word['category'] == noun:

            # checks for i
            if word['word'].string == 'i':
                tense["person"][1] += 5
                tense["number"]["singular"] += 5

            # checks if it can get the singular
            singular = pattern.en.singularize(word['word'].string)
            if singular != word['word'].string:
                tense["number"]["singular"] -= 5
                tense["number"]["plural"] += 5

    # computes the tense
    computed_tense = {
        "person": max(tense['person'].items(),
                      key=operator.itemgetter(1))[0],
        "number": max(tense['number'].items(),
                      key=operator.itemgetter(1))[0],
    }

    return computed_tense


# computes the return of a given set of words
def compute_subject_return(words, tense):

    # handles first person
    if tense['person'] == 1 and tense["number"] == 'singular':

        # loops through the words
        for word in words:

            # personal pronouns
            noun = Category.query.filter_by(string='noun').first()
            if word['word'].string == 'i' and noun in word['word'].categories:

                # adds you to dictionary
                memory.add_words_to_memory(['you'])
                you = Word.query.filter_by(string='you').first()

                # replaces the word i to you
                words[words.index(word)]['word'] = you

                break

    # handles second person
    if tense['person'] == 2 and tense["number"] == 'singular':

        # loops through the words
        for word in words:

            # personal pronouns
            pronoun = Category.query.filter_by(string='pronoun').first()
            if word['word'].string == 'you' and pronoun in word['word'].categories:

                # adds you to dictionary
                memory.add_words_to_memory(['i'])
                i = Word.query.filter_by(string='i').first()

                # replaces the word i to you
                words[words.index(word)]['word'] = i

                break

    return words


# computes the return of a given set of words
def compute_predicate_return(words, tense):

    # sets reverse conjugation tense
    reverse_tense = {
        "person": tense["person"],
        "number": tense["number"]
    }

    # first person
    if tense["person"] == 1:
        reverse_tense["person"] = 2

    # second person
    if tense["person"] == 2:
        reverse_tense["person"] = 1

    main_verb = None

    # loops through the words
    verb = Category.query.filter_by(string='verb').first()
    for word in words:

        if verb in word['word'].categories:
            main_verb = word
            break

    # runs an infinitive function
    conjugation = pattern.en.conjugate(
        main_verb['word'].string,
        person=reverse_tense["person"],
        number=reverse_tense["number"],
    )

    memory.add_words_to_memory([conjugation])
    conjugation = Word.query.filter_by(string=conjugation).first()

    # replaces the word
    words[words.index(main_verb)]['word'] = conjugation

    return words


# computes the reply between the subject and the predicate
def compute_input_return(subject, predicate):

    if app.config['DEBUG']:
        print('********************\n')
        print("Computing the connection between the subject and the predicate...\n")

    debug_subject = [s['word'] for s in subject]
    debug_predicate = [p['word'] for p in predicate]

    # prints the connection
    print(f'You said that {debug_subject} {debug_predicate}.')

    return
