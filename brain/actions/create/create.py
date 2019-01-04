from models import models
import os, time
from random import randint
from ..compute import compute


# creates a word instance
def create_word_file(word, json_word, words_dir):
    _w = word[:2]
    word_dir = os.path.join(words_dir, _w)

    # checks if word[:2] directory exists
    if not os.path.isdir(word_dir):
        os.mkdir(word_dir)

    file_name = word + '.json'
    json_path = os.path.join(word_dir, file_name)

    # opens the file
    word_file = open(json_path, 'w')

    # writes
    word_file.write(json_word)
    word_file.close()

    return json_path


# creates a task instance
def create_task_file(input_string, words, words_dir, tasks_dir):

    # global variables
    date_dir = os.path.join(tasks_dir, time.strftime("_%Y_%m_%d"))
    task_id = 123
    task_variable = '_' + str(task_id)
    task_status = 'incomplete'

    # assigns type to task
    task_type, confidence = compute.compute_task(input_string, words,
                                                 words_dir, date_dir)

    # checks if today directory exists
    if not os.path.isdir(date_dir):
        os.mkdir(date_dir)

    file_name = '_' + str(task_id) + '.py'
    file_path = os.path.join(date_dir, file_name)

    # opens the file
    word_file = open(file_path, 'w')

    # writes
    word_file.write("from models import models\n\n")

    # creates the task instance
    word_file.write("# task\n")
    word_file.write(
        '{} = models.Task(id={}, words={}, type=\"{}\", status=\"{}\")'.format(
            task_variable, task_id, words, task_type, task_status))

    # returns the task
    return task_id, file_path
