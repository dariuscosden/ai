from . import known_words
import operator, os, json, copy, requests
from .compute import compute_initial_word_info
from ..check import check
from ..oxford import oxford
from ..create import create

# can compute how many chances there are for each len of subject

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way


# checks if the verb is regular
def check_if_regular_verb(word):

    # sets default to false
    infinitive = False

    return infinitive


# gets word from oxford
def get_word_from_oxford(word):

    print('Currently learning the word \"{}\"'.format(word))

    # dariuscosden1@gmail.com
    app_id = 'ea68edf8'
    app_key = '9b45243c723d928e576407c01a8e3a8a'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'

    # fetches from oxford
    request = requests.get(
        url + word.lower(), headers={
            'app_id': app_id,
            'app_key': app_key
        })

    # checks status code
    if request.status_code == 404:

        # checks if the verb is a regular verb
        infinitive = check_if_regular_verb(word)

        # uses the infitive form if so
        if infinitive:
            request = requests.get(
                url + infinitive.lower(),
                headers={
                    'app_id': app_id,
                    'app_key': app_key
                })

            # creates json
            json_word = json.dumps(request.json(), indent=2)

    else:
        # creates json
        json_word = json.dumps(request.json(), indent=2)

    return json_word


# computes word tree
def compute_word_tree(words, words_dir):

    # compute the initial word info
    _words, determiners, pronouns, nouns, verbs, adjectives = compute_initial_word_info(
        words, words_dir)

    return