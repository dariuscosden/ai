import requests, json


# gets word from oxford
def get_word_from_oxford(word):
    # dariuscosden1@gmail.com
    app_id = 'ea68edf8'
    app_key = '9b45243c723d928e576407c01a8e3a8a'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + word.lower(
    )

    # fetches from oxford
    request = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

    # creates json
    json_word = json.dumps(r.json(), indent=2)

    return json_word
