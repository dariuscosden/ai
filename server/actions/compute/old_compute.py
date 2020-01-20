# from . import known_words
import operator, os, json, copy
from ..check import check
from ..oxford import oxford
from ..create import create


# gets the word type from json_path
def get_word_type_from_json(json_path, words_dir):
    json_file = open(json_path)
    data = json.load(json_file)

    # gets the word type
    word_type = data['results'][0]['lexicalEntries'][0]['lexicalCategory']

    # handles other type
    if word_type == 'Other':

        # checks for other -> verb
        cross_reference = '_' + data['results'][0]['lexicalEntries'][0][
            'entries'][0]['senses'][0]['crossReferences'][0]['id']

        # if there is a cross_reference, get the word
        if cross_reference:

            # fetches cross_reference json_path if available
            json_path = check.return_json_word_path(cross_reference, words_dir)

            # checks cross_reference lexicalCategory
            if json_path:
                json_file = open(json_path)
                data = json.load(json_file)

                # gets the word type
                word_type = data['results'][0]['lexicalEntries'][0][
                    'lexicalCategory']

            # fetches word from oxford
            else:

                # gets word from oxford
                json_word = oxford.get_word_from_oxford(cross_reference)

                # creates json_word file and returns its path
                json_path = create.create_word_file(cross_reference, json_word,
                                                    words_dir)

                # opens and reads the json_path
                json_file = open(json_path)
                data = json.load(json_file)

                # gets the word type
                word_type = data['results'][0]['lexicalEntries'][0][
                    'lexicalCategory']

    return word_type


# computes string to words
def compute_string_to_words(string):
    string_words = string.split(" ")
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


# computes words and adds their data
def compute_initial_word_info(words, words_dir):

    # enhanced words list
    _words = []

    # word_type lists
    determiners = []
    pronouns = []
    nouns = []
    verbs = []
    adjectives = []

    # loops through each word to add initial info
    for word in words:

        # gets json_path
        json_path = check.return_json_word_path(word, words_dir)

        # if json_path
        if json_path:

            # gets word type and assigns it
            word_type = get_word_type_from_json(json_path, words_dir)

            # handles determiners
            if word_type == 'Determiner':

                # adds necessary data to _word
                _word = {
                    'string': word,
                    'json_path': json_path,
                    'type': word_type,
                    'references': []
                }

                # appends accordingly
                determiners.append(_word)
                _words.append(_word)

            # handles pronouns
            if word_type == 'Pronoun':

                # adds necessary data to _word
                _word = {
                    'string': word,
                    'json_path': json_path,
                    'type': word_type,
                    'references': []
                }

                # appends accordingly
                pronouns.append(_word)
                _words.append(_word)

            # handles nouns
            if word_type == 'Noun':

                # adds necessary data to _word
                _word = {
                    'string': word,
                    'json_path': json_path,
                    'type': word_type,
                    'determiners': [],
                    'modifiers': []
                }

                # appends accordingly
                nouns.append(_word)
                _words.append(_word)

            # handles verbs
            if word_type == 'Verb':

                # adds necessary data to _word
                _word = {
                    'string': word,
                    'json_path': json_path,
                    'type': word_type,
                    'references': []
                }

                # appends accordingly
                verbs.append(_word)
                _words.append(_word)

            # handles adjectives
            if word_type == 'Adjective':

                # adds necessary data to _word
                _word = {
                    'string': word,
                    'json_path': json_path,
                    'type': word_type,
                    'references': []
                }

                # appends accordingly
                adjectives.append(_word)
                _words.append(_word)

            # handles adjectives
            if word_type == 'Adverb':

                # adds necessary data to _word
                _word = {
                    'string': word,
                    'json_path': json_path,
                    'type': word_type,
                    'references': []
                }

                # appends accordingly
                adjectives.append(_word)
                _words.append(_word)

    return _words, determiners, pronouns, nouns, verbs, adjectives


# adds adjacent words to _word
def add_adjacent_words(_words):

    adjacent_words = []

    # strips unneccesary adjacent data from _words
    for word in _words:
        d = {}
        d['string'] = word['string']
        d['json_path'] = word['json_path']
        d['type'] = word['type']

        adjacent_words.append(d)

    # loops through each word to add adjacent words
    for word_index, word in enumerate(_words):

        # returns adjacent words
        words_to_the_left = adjacent_words[:word_index]
        words_to_the_right = adjacent_words[word_index + 1:]

        # appends the adjacent words
        _words[word_index]['words_to_the_left'] = words_to_the_left
        _words[word_index]['words_to_the_right'] = words_to_the_right

    return _words


# adds links to other _words
def add_links_to_words(_words):

    # loops through each word
    for word_index, word in enumerate(_words):

        # handles determiners
        if word['type'] == 'Determiner':

            # checks words to the right for noun
            for word_to_the_right in word['words_to_the_right']:

                # checks if noun
                if word_to_the_right['type'] == 'Noun':

                    # assigns it as a reference
                    word['references'].append(word_to_the_right)

                    # breaks the loop
                    break

        # handles pronouns
        if word['type'] == 'Pronoun':

            # checks words to the right for noun
            for word_to_the_right in word['words_to_the_right']:

                # checks if noun
                if word_to_the_right['type'] == 'Noun':

                    # assigns it as a reference
                    word['references'].append(word_to_the_right)

                    # breaks the loop
                    break

        # handles nouns
        if word['type'] == 'Noun':

            # checks words to the left for determiners
            for word_to_the_left in word['words_to_the_left']:

                # if it lands on a pronoun
                if word_to_the_left['type'] == 'Determiner':

                    # assigns it as a reference
                    word['determiners'].append(word_to_the_left)

                    break

            # checks words to the left for modifiers (adjectives)
            for word_to_the_left in word['words_to_the_left']:

                # if it lands on a verb
                if word_to_the_left['type'] == 'Adjective':

                    # assigns it as a modifier
                    word['modifiers'].append(word_to_the_left)

        # handles adjectives
        if word['type'] == 'Adjective':

            # checks words to the left for noun (predicative)
            for word_to_the_left in word['words_to_the_left']:

                # if it lands on a verb
                if word_to_the_left['type'] == 'Noun':

                    # assigns it as a reference
                    word['references'].append(word_to_the_left)

                    break

            # checks words to the right for noun (attributive)
            for word_to_the_right in word['words_to_the_right']:
                if word_to_the_right['type'] == 'Noun':

                    # assigns it as a reference
                    word['references'].append(word_to_the_right)

                    break

        # handles verbs
        elif word['type'] == 'Verb':

            # checks each word to the left
            for word_to_the_left in word['words_to_the_left']:
                if word_to_the_left['type'] == 'Noun':

                    word['references'].append(word_to_the_left)

                    break

            # checks each word to the right
            for word_to_the_right in word['words_to_the_right']:
                if word_to_the_right['type'] == 'Noun':

                    word['references'].append(word_to_the_right)

                    break

        # handles verbs
        elif word['type'] == 'Adverb':

            # checks each word to the left
            for word_to_the_left in word['words_to_the_left']:
                if word_to_the_left['type'] == 'Adjective':

                    word['references'].append(word_to_the_left)

                    break

            # checks each word to the right
            for word_to_the_right in word['words_to_the_right']:
                if word_to_the_right['type'] == 'Adjective':

                    word['references'].append(word_to_the_right)

                    break

    print(json.dumps(_words, indent=2))

    return _words


# creates and initializes the task points dict
def initialize_task_points_dict():

    # initiates tracking of type points
    types = {'question': 0, 'statement': 0, 'action': 0}
    total_points = 0

    return types, total_points


# computes the words and assigns them correctly
def compute_task_type(words, _words, words_dir, determiners, pronouns, nouns,
                      verbs, adjectives, types, total_points):

    # question symbol
    if any("?" in s for s in words):
        types['question'] += 10
        total_points += 10

    # computing verbs
    print('computing words')

    # runs through each word
    for word_index, word in enumerate(_words):

        # checks for interrogative_words
        if word['string'] in known_words.interrogative_words:
            types['question'] += 10
            total_points += 10

            # checks if it is in the first position
            if word_index == 0:
                types['question'] += 10
                total_points += 10

                # checking if next word is verb
                if _words[word_index + 1]['type'] == 'Verb':
                    types['question'] += 20
                    total_points += 20

        # handles verbs
        if word['type'] == 'Verb':

            # finds first noun to the right of verb
            for word_right in word['words_to_the_right']:
                if word_right['type'] == 'Noun':
                    types['question'] += 10
                    total_points += 10
                    break

            # finds the first noun to the left of verb
            for word_left in word['words_to_the_left']:
                if word_left['type'] == 'Noun':
                    types['statement'] += 3
                    total_points += 3
                    break

    # gets the maximum key
    type = max(types.items(), key=operator.itemgetter(1))[0]

    # computes the confidence
    type_points = types[type]
    confidence = round(type_points / total_points * 100, 2)

    return type, confidence


# computes the predicate
def compute_predicate(_words):

    # predicate list
    predicate = {'string': ''}

    # runs through each word
    for word_index, word in enumerate(_words):

        # checks for verb
        if word['type'] == 'Verb':

            # checks if verb is main verb

            # totals
            total_length = len(word['words_to_the_right']) + 1
            index = 1

            # adds verb to predicate_string
            if index < total_length:
                predicate['string'] += word['string'].strip('_') + ' '
                index += 1
            else:
                predicate['string'] += word['string'].strip('_')

            # checks the words to the right word for nouns or pronouns
            for word_to_the_right in word['words_to_the_right']:

                # handles determiners
                if word_to_the_right['type'] == 'Determiner':

                    # checks the references
                    for reference in word_to_the_right['references']:
                        continue

                if word_to_the_right['type'] in ['Pronoun', 'Noun']:
                    continue

            # adds simple predicate (verb)
            predicate['verb'] = word['string']

            break

    return predicate


# computes the subject
def compute_subject(_words):

    # subject dict
    subject = {'string': ''}

    # runs through each word
    for word in _words:

        # finds the first noun
        if word['type'] == 'Noun':

            # totals
            total_length = len(word['determiners']) + len(
                word['modifiers']) + 1
            index = 1

            # adds determiners
            subject['determiners'] = []
            for determiner in word['determiners']:
                subject['determiners'].append(determiner['string'])

                # checks for spacing
                if index < total_length:
                    subject['string'] += determiner['string'].strip('_') + ' '
                    index += 1
                else:
                    subject['string'] += determiner['string'].strip('_')

            # adds modifiers
            subject['modifiers'] = []
            for modifier in word['modifiers']:
                subject['modifiers'].append(modifier['string'])

                # checks for spacing
                if index < total_length:
                    subject['string'] += modifier['string'].strip('_') + ' '
                    index += 1
                else:
                    subject['string'] += modifier['string'].strip('_')

            # adds noun
            subject['noun'] = word['string']

            # checks for spacing
            if index < total_length:
                subject['string'] += word['string'].strip('_') + ' '
                index += 1
            else:
                subject['string'] += word['string'].strip('_')

            break

    return subject


# computes its response
def compute_response(input_string, task_type, confidence, subject, predicate):

    # empty response dict
    response = {}

    # adds the input string
    response['input_string'] = input_string

    # adds the subject
    response['subject'] = subject

    # adds the predicate
    response['predicate'] = predicate

    # handles statement
    if task_type == 'statement':

        # adds base response
        response['response_string'] = 'You have given me a statement. '

        # expands its response to include the subject
        response['response_string'] += 'You\'re telling me that {} {}.'.format(
            subject['string'], predicate['string'])

    # handles questions
    if task_type == 'question':

        # adds base response
        response['response_string'] = 'You have asked me a question. '

        # expands its response to include the subject
        response['response_string'] += 'You\'re asking me if {} {}.'.format(
            subject['string'], predicate['string'])

    return response


# computes the task and all of its info
def compute_task(input_string, words, words_dir, date_dir):

    # compute the initial word info
    _words, determiners, pronouns, nouns, verbs, adjectives = compute_initial_word_info(
        words, words_dir)

    # adds adjacent words
    _words = add_adjacent_words(_words)

    # initiates task points dict
    types, total_points = initialize_task_points_dict()

    # computes the task_type
    task_type, confidence = compute_task_type(
        words, _words, words_dir, determiners, pronouns, nouns, verbs,
        adjectives, types, total_points)

    print('\n')
    print('task type computation')
    print("task_type is \'{}\' with {}% confidence - ({})".format(
        type, confidence, types))

    # TODO add confidence confirmation function

    # adds references to words
    _words = add_links_to_words(_words)

    # computes the predicate
    predicate = compute_predicate(_words)

    # computes the subject
    subject = compute_subject(_words)

    # computes its response
    response = compute_response(input_string, task_type, confidence, subject,
                                predicate)

    # writes response to file
    response_file = open(os.path.join(date_dir, 'response.json'), 'w')
    response_file.write(json.dumps(response, indent=2))

    # print('\nmy response is: \n {}'.format(json.dumps(response, indent=2)))

    return task_type, confidence
