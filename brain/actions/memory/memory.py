import os, json, copy, requests
import pattern.en

# can compute how many chances there are for each len of subject

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way

# if you use the relationships between the words with mathematical operations and since we have them segmented by subject, definition, predicate, etc.. it is mathematically predictable


# checks if word is already in memory
def check_if_word_in_memory(word, infinitive, words_dir):
    _w = word[:2]
    file_name = word + '.json'
    infinitive_name = '_' + infinitive + '.json'

    # assigns paths
    word_path = os.path.join(words_dir, _w, file_name)
    infinitive_path = os.path.join(words_dir, _w, infinitive_name)

    # check if word_path exists
    if os.path.isfile(word_path):

        # checks if infinitive_path also exists
        if os.path.isfile(infinitive_path):
            return True

    return False


# returns a json word file for a given word
def return_json_word_path(word, words_dir):
    _w = word[:2]
    file_name = word + '.json'

    # checks if word file exists
    file_path = os.path.join(words_dir, _w, file_name)
    if os.path.isfile(file_path):
        return file_path
    else:
        return None


# creates a word file
def create_word_file(word, words_dir, json_word):

    # starting letter
    _w = word[:2]

    # _w dir
    word_dir = os.path.join(words_dir, _w)

    # makes letter directory if it doesn't exist
    if not os.path.isdir(word_dir):
        os.mkdir(word_dir)

    # setting the file_path
    file_path = os.path.join(word_dir, '{}.json'.format(word))

    # creating file
    file = open(file_path, 'w')
    file.write(json_word)
    file.close()


# gets word from oxford
def save_word_to_memory(word, words_dir):

    # used to check if the word is a conjugated verb
    infinitive = pattern.en.conjugate(word.strip('_'), tense="INFINITIVE")
    infinitive_found = False

    # checks if word is in memory
    if check_if_word_in_memory(word, infinitive, words_dir):
        print('I have already learnt the word \"{}\"'.format(word))
    else:
        print('Currently learning the word \"{}\"'.format(word))

        # dariuscosden1@gmail.com
        app_id = 'ea68edf8'
        app_key = '9b45243c723d928e576407c01a8e3a8a'
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'

        # fetches from oxford
        request = requests.get(
            url + word.lower().strip('_'),
            headers={
                'app_id': app_id,
                'app_key': app_key
            })

        # if it can't find it in oxford, it might be a regular verb
        if request.status_code == 404:

            # tries to query oxford again with the infinitive
            request = requests.get(
                url + infinitive,
                headers={
                    'app_id': app_id,
                    'app_key': app_key
                })

            # checks if request was successful
            if request.status_code == 404:
                print('I wasn\t able to understand "{}"'.format(word))
                return

            else:
                # sets data in json
                data = request.json()

                # sets json_word
                json_word = json.dumps(data, indent=2)

                # creates a pseudo word_file to keep track of learnt words
                pseudo_json = {
                    "metadata": {
                        "provider": "Oxford University Press"
                    },
                    "results": [{
                        "id": "{}".format(word.strip('_')),
                        "language": "en",
                        "lexicalEntries": [
                            {
                                "entries": [
                                    {
                                        "senses": [
                                            {
                                                "crossReferences": [
                                                    {
                                                        "id": "{}".format(infinitive)
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }]
                }
                pseudo_json = json.dumps(pseudo_json, indent=2)

                # creates a pseudo word file
                create_word_file(word, words_dir, pseudo_json)

                # creates a word file for the infinitive
                create_word_file('_' + infinitive, words_dir, json_word)

        else:

            # sets data in json
            data = request.json()

            # assigns lexicalEntries variable
            lexicalEntries = data['results'][0]['lexicalEntries']

            # runs through each lexicalEntry to catch a potential verb
            for le in lexicalEntries:

                # checks if it's a verb
                if le['lexicalCategory'] == 'Other' or le[
                        'lexicalCategory'] == 'Verb':

                    # checks for other -> verb
                    try:
                        cross_reference = le['entries'][0]['senses'][0][
                            'crossReferences'][0]['id']

                        # queries oxford with the infinitive instead
                        request = requests.get(
                            url + cross_reference,
                            headers={
                                'app_id': app_id,
                                'app_key': app_key
                            })

                        # if infinitive verb was found
                        if request.status_code != 404:

                            # sets the infinitive_found to true
                            infinitive_found = True

                            # updates data in json
                            verb_data = request.json()
                            json_verb = json.dumps(verb_data, indent=2)

                            # creates a file for the verb as well (doesn't interfere with original word_file creation)
                            create_word_file('_' + cross_reference, words_dir,
                                             json_verb)

                    except KeyError:
                        pass

            # if the infinitive still hasn't been found
            if not infinitive_found:

                # tries to query oxford again with the infinitive
                request = requests.get(
                    url + infinitive,
                    headers={
                        'app_id': app_id,
                        'app_key': app_key
                    })

                # checks if request was successful
                if request.status_code != 404:

                    # sets the infinitive_found to true
                    infinitive_found = True

                    # updates data in json
                    verb_data = request.json()
                    json_verb = json.dumps(verb_data, indent=2)

                    # creates a file for the verb as well (doesn't interfere with original word_file creation)
                    create_word_file('_' + infinitive, words_dir, json_verb)

        return True


# computes word tree
def compute_word_tree(words, words_dir):

    # # compute the initial word info
    # _words, determiners, pronouns, nouns, verbs, adjectives = compute_initial_word_info(
    #     words, words_dir)

    return