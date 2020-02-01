from flask import current_app as app
from flask import Response, request
from server.database import db
import json
import os
from server.actions.input import input
from server.actions.memory import memory
from server.actions.compute import compute

from server.models import Word

# directories
current_dir = os.path.dirname(os.path.abspath(__file__))
memory_dir = current_dir + '/data/memory'
words_dir = memory_dir + '/words'
tasks_dir = memory_dir + '/tasks'


# handles the user inputs
@app.route('/listen', methods=['POST'])
def listen():

    # this section takes in user input, sanitizes it
    # and creates database entries based on what
    # has been submitted
    #
    # this uses various functions from the 'input' and 'memory'
    # folders
    #
    #
    user_input = input.sanitize_input(request.form['input'])
    words = input.return_words_from_input(user_input)

    words = memory.add_words_to_memory(words)

    # this section computes the subject, predicate,
    # and eventually the word tree of the current input
    #
    # it uses various functions from the 'compute' folders
    #
    # note: at this point the words contain the database
    # entries
    #
    #
    words, complete_subject, last_index = compute.compute_subject(words)
    predicate = compute.compute_predicate(words, last_index)

    # this section computes the tense of the subject
    # and feeds it onwards
    #
    #
    subject_tense = compute.compute_subject_tense(complete_subject)

    # this section computes the connection between the
    # subject and predicate of the input
    #
    # this connection will then be used by the intelligence
    # to figure out what the intention of the input was
    #
    #
    returned_subject = compute.compute_subject_return(
        complete_subject, subject_tense)

    returned_predicate = compute.compute_predicate_return(
        predicate, subject_tense)

    returned_input = compute.compute_input_return(
        returned_subject, returned_predicate)

    return Response(status=200)
