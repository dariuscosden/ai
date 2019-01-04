import os, json, copy, requests

# can compute how many chances there are for each len of subject

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way


# checks if word is already in memory
def check_if_word_in_memory(word, words_dir, verbs_dir):
    _w = word[:2]
    file_name = word + '.json'

    # checks if word file exists
    file_path = os.path.join(words_dir, _w, file_name)
    if os.path.isfile(file_path):
        return True

    # check if verb file exists
    file_path = os.path.join(verbs_dir, _w, file_name)
    if os.path.isfile(file_path):
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


# checks if the verb is regular
def check_if_verb(word):

    # sets default to false
    infinitive = False

    return infinitive


# creates a verb file
def create_verb_file(word, verbs_dir):

    # starting letter
    _w = word[:2]

    # _w dir
    verb_dir = os.path.join(verbs_dir, _w)

    # makes letter directory if it doesn't exist
    if not os.path.isdir(verb_dir):
        os.mkdir(verb_dir)

    # setting the file_path
    file_path = os.path.join(verb_dir, '{}.json'.format(word))

    # checking if file already exists
    if not os.path.isfile(file_path):

        response = requests.get(
            "https://ceneezer-conjugate-v1.p.rapidapi.com/?mode=conjugate&verb={}"
            .format(word.lower().strip('_')),
            headers={
                "X-RapidAPI-Key":
                "fneO3dRIhBmshxGkZdYouEDCAb2pp1zexlWjsn0RF5A4lEyKUd"
            })

        if response.status_code == 200:

            # getting json data
            data = response.json()[0]

            # creating file
            file = open(file_path, 'w')
            file.write(json.dumps(data, indent=2))
            file.close()

            return file_path

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
def save_word_to_memory(word, words_dir, verbs_dir):

    # checks if word is in memory
    if check_if_word_in_memory(word, words_dir, verbs_dir):
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
            create_verb_file(word, verbs_dir)
            return

        # creates json
        data = request.json()
        json_word = json.dumps(data, indent=2)

        # checks if word is a verb
        word_type = data['results'][0]['lexicalEntries'][0]['lexicalCategory']

        # creates verb file
        if word_type == 'Verb':
            create_verb_file(word, verbs_dir)

        # checks for irregular verb from oxford
        elif word_type == 'Other':
            cross_reference = '_' + data['results'][0]['lexicalEntries'][0][
                'entries'][0]['senses'][0]['crossReferences'][0]['id']

            # creates verb file
            if cross_reference:
                create_verb_file(word, verbs_dir)

        create_word_file(word, words_dir, json_word)

        return True


# computes word tree
def compute_word_tree(words, words_dir):

    # # compute the initial word info
    # _words, determiners, pronouns, nouns, verbs, adjectives = compute_initial_word_info(
    #     words, words_dir)

    return