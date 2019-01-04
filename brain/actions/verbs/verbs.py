import requests, json, os


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
    file_path = os.path.join(verb_dir, '_{}.json'.format(word))

    # checking if file already exists
    if not os.path.isfile(file_path):

        response = requests.get(
            "https://ceneezer-conjugate-v1.p.rapidapi.com/?mode=conjugate&verb={}"
            .format(word.lower()),
            headers={
                "X-RapidAPI-Key":
                "fneO3dRIhBmshxGkZdYouEDCAb2pp1zexlWjsn0RF5A4lEyKUd"
            })

        # getting json data
        data = response.json()

        # creating file
        file = open(file_path, 'w')
        file.write(data)
        file.close()
