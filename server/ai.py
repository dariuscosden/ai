from flask import current_app as app
from flask import Response, request
import json
import os
from .actions.input import input
from .actions.memory import memory
from .actions.compute import compute

# directories
current_dir = os.path.dirname(os.path.abspath(__file__))
memory_dir = current_dir + '/data/memory'
words_dir = memory_dir + '/words'
tasks_dir = memory_dir + '/tasks'


# handles the user inputs
@app.route('/listen', methods=['POST'])
def listen():

    user_input = request.form['input']

    # sanitizes the input
    user_input = input.sanitize_input(user_input)

    # converts string to word list
    words = input.return_words_from_input(user_input)

    # gets word data and creates a file for each word
    for index, word in enumerate(words):
        memory.save_word_to_memory(word, words_dir)

    return

    # computes the word tree
    subject, predicate = compute.compute_word_tree(words, words_dir)

    return Response(status=200)
