import os, json, copy, requests
import pattern.en
from . import known_words

# can compute how many chances there are for each len of subject

# any word that's not a verb left of the noun is part of the subject until.. ',', '.', verb?, 'conjunction'
# any word that's not a '.', ',', 'preposition', noun?, 'conjunction' is part of the predicate
# humans do it this way

# if you use the relationships between the words with mathematical operations and since we have them segmented by subject, definition, predicate, etc.. it is mathematically predictable


# checks if word is already in memory
def check_if_word_in_memory(word, infinitive, singular, words_dir):

    # adds '_' to punctuations
    if word in known_words.punctuation_symbols:
        word = '_' + word

    _w = word[:2]
    _i = '_' + infinitive[:1]
    _s = '_' + singular[:1]
    file_name = word + '.json'
    infinitive_name = '_' + infinitive + '.json'
    singular_name = '_' + singular + '.json'

    # assigns paths
    word_path = os.path.join(words_dir, _w, file_name)
    infinitive_path = os.path.join(words_dir, _i, infinitive_name)
    singular_path = os.path.join(words_dir, _s, singular_name)

    # check if word_path exists
    if os.path.isfile(word_path):

        # checks if infinitive_path also exists
        if os.path.isfile(infinitive_path):

            # checks if singular path also exists
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

# creates a regular conjugated verb file
def get_regular_verb_conjugated_json(word, words_dir, infinitive, infinitive_id):

    # sets json_word
    lexical_entry = {
                "entries": [
                    {
                    "homographNumber": "000",
                    "senses": [
                        {
                        "crossReferenceMarkers": [
                            "conjugated form of {}".format(infinitive)
                        ],
                        "crossReferences": [
                            {
                            "id": "{}".format(infinitive),
                            "text": "{}".format(infinitive),
                            "type": "see also"
                            }
                        ],
                        "id": "{}".format(infinitive_id)
                        }
                    ]
                    }
                ],
                "language": "en",
                "lexicalCategory": "Verb",
                "pronunciations": [
                    {
                    "audioFile": "http://audio.oxforddictionaries.com/en/mp3/gave_gb_2.mp3",
                    "dialects": [
                        "British English"
                    ],
                    "phoneticNotation": "IPA",
                    "phoneticSpelling": "\u0261e\u026av"
                    }
                ]
                }

    return lexical_entry

# gets the plural word json
def get_plural_word_json(word, words_dir, singular, singular_id, singular_type):

    # sets the json_word
    lexical_entry = {
                "entries": [
                    {
                    "homographNumber": "000",
                    "senses": [
                        {
                        "crossReferenceMarkers": [
                            "plural of {}".format(singular)
                        ],
                        "crossReferences": [
                            {
                            "id": "{}".format(singular),
                            "text": "{}".format(singular),
                            "type": "see also"
                            }
                        ],
                        "id": "{}".format(singular_id)
                        }
                    ]
                    }
                ],
                "language": "en",
                "lexicalCategory": "{}".format(singular_type),
                "pronunciations": [
                    {
                    "audioFile": "http://audio.oxforddictionaries.com/en/mp3/gave_gb_2.mp3",
                    "dialects": [
                        "British English"
                    ],
                    "phoneticNotation": "IPA",
                    "phoneticSpelling": "\u0261e\u026av"
                    }
                ]
                }

    return lexical_entry

# gets the punctuation json
def get_punctuation_json(word, words_dir):

    # sets the json_word
    lexical_entry = {
                "entries": [],
                "language": "en",
                "lexicalCategory": "Punctuation"
                }

    return lexical_entry

# gets word from oxford
def save_word_to_memory(word, words_dir):

    # used to check if the word is a conjugated verb
    infinitive = pattern.en.conjugate(word.strip('_'), tense="INFINITIVE")
    infinitive_found = False

    # used to check if the word is a pluralized word
    singular = pattern.en.singularize(word.strip('_'))
    singular_found = False


    # checks if word is in memory
    if check_if_word_in_memory(word, infinitive, singular, words_dir):
        print('I have already learnt the word \"{}\"'.format(word))
    else:
        print('Currently learning the word \"{}\"'.format(word))

        # sets the initial json_word data
        json_word = {
        "metadata": {
            "provider": "Oxford University Press"
        },
        "results": [
            {
                "id": "{}".format(word.strip('_')),
                "language": "en",
                "lexicalEntries": []
            }
        ]
        }

        # checks if word is a punctuation
        if word in known_words.punctuation_symbols:

            # gets json_word for the punctuation
            punctuation_json = get_punctuation_json(word, words_dir)
            
            # adds it to json_word
            json_word['results'][0]['lexicalEntries'].append(punctuation_json)

            # create a file
            create_word_file('_' + word, words_dir, json_word)
            
            return

        # api info - dariuscosden1@gmail.com
        app_id = 'ea68edf8'
        app_key = '9b45243c723d928e576407c01a8e3a8a'
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'

        # handles the infinitive
        infinitive_request = requests.get(
            url + infinitive,
            headers={
                'app_id': app_id,
                'app_key': app_key
            })

        # checks the status code
        if infinitive_request.status_code != 404:
            
            # sets the json data variables
            infinitive_data = infinitive_request.json()
            infinitive_json = json.dumps(infinitive_request.json(), indent=2)
            lexical_entries = infinitive_data['results'][0]['lexicalEntries']

            # loops through the infinitive lexical entries
            for le in lexical_entries:

                # checks the lexicalCategory for verb
                if le['lexicalCategory'] == 'Verb':
                    
                    # gets the infinitive variables
                    infinitive_id = le['entries'][0]['senses'][0]['id']

                    # gets the conjugated variables
                    conjugated_word = get_regular_verb_conjugated_json(word, words_dir, infinitive, infinitive_id)

                    # appends to json_word
                    json_word['results'][0]['lexicalEntries'].append(conjugated_word)

            # creates a word file for the infinitive
            create_word_file('_' + infinitive, words_dir, infinitive_json)
            infinitive_found = True

        # handles the singular
        singular_request = requests.get(
            url + singular,
            headers={
                'app_id': app_id,
                'app_key': app_key
            })

        # checks the status code
        if singular_request.status_code != 404:

            # sets the json data variables
            singular_data = singular_request.json()
            singular_json = json.dumps(singular_data, indent=2)
            lexical_entries = singular_data['results'][0]['lexicalEntries']

            # loops through the singular lexical entries
            for le in lexical_entries:

                # checks the lesicalCategory for noun
                if le['lexicalCategory'] == 'Noun':

                    # gets the singular variables
                    singular_id = le['entries'][0]['senses'][0]['id']
                    singular_type = le['lexicalCategory']

                    # gets the plural variables
                    plural_word = get_plural_word_json(word, words_dir, singular, singular_id, singular_type)

                    # appends to json_word
                    json_word['results'][0]['lexicalEntries'].append(plural_word)

            # creates a word file for the singular
            create_word_file('_' + singular, words_dir, singular_json)
            singular_found = True


        # fetches from oxford with initial word
        request = requests.get(
            url + word.lower().strip('_'),
            headers={
                'app_id': app_id,
                'app_key': app_key
            })

        # handles a 404 error from request
        if request.status_code == 404:

            # converts to json str
            json_word = json.dumps(json_word, indent=2)

            # creates a word file with the data so far
            create_word_file(word, words_dir, json_word)

        else:

            # gets data from request
            _json_data = request.json()
            _json_word = json.dumps(_json_data, indent=2)
            lexical_entries = _json_data['results'][0]['lexicalEntries']

            # checks for cross reference verbs
            for le in lexical_entries:

                # checks if 'Other'
                if le['lexicalCategory'] == 'Other':
                    cross_reference = le['entries'][0]['senses'][0]['crossReferences'][0]['id']

                    # gets its json_file
                    cross_reference = return_json_word_path('_' + cross_reference, words_dir)
                    cross_reference = json.loads(open(cross_reference).read())

                    # finds the verb word_type for the cross reference
                    cr_lexical_entries = cross_reference['results'][0]['lexicalEntries']
                    for cr_le in cr_lexical_entries:

                        if cr_le['lexicalCategory'] == 'Verb':
                            le['lexicalCategory'] = 'Verb'
                            break
                            

            # adds any lexical entry that is not from request
            for le in json_word['results'][0]['lexicalEntries']:

                # appends if not there
                if le not in lexical_entries:
                    lexical_entries.append(le)

            # converts to json str
            json_word = json.dumps(json_word, indent=2)

            # creates a word file with the data
            create_word_file(word, words_dir, json_word)

        return True

