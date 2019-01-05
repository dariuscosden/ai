from flask import current_app as app
from flask import Response, request
import pattern.en
import json, os
from .actions.memory import memory
from .actions.input import input

# directories
current_dir = os.path.dirname(os.path.abspath(__file__))
memory_dir = current_dir + '/data/memory'
words_dir = memory_dir + '/words'
tasks_dir = memory_dir + '/tasks'
verbs_dir = memory_dir + '/verbs'


# handles the user inputs
@app.route('/listen', methods=['POST'])
def listen():

    data = request.form
    user_input = data['input']

    # sanitizes the input
    user_input = input.sanitize_input(user_input)

    # converts to words
    words = input.return_words_from_input(user_input)

    # gets word data and creates a file
    for index, word in enumerate(words):
        memory.save_word_to_memory(word, words_dir, verbs_dir)

    print(words)

    return Response(status=200)