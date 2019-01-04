from models import models
from actions.memory import memory
from actions.input import input
import os, time

# directories
current_dir = os.path.dirname(os.path.abspath(__file__))
memory_dir = current_dir + '/data/memory'
words_dir = memory_dir + '/words'
tasks_dir = memory_dir + '/tasks'
verbs_dir = memory_dir + '/verbs'

# start timing
start_time = time.time()

from pattern.en import conjugate, tenses

# end timing
end_time = time.time()
print(str(int(round((end_time - start_time) * 1000, 0))) + 'ms')

# start timing
start_time = time.time()

print(conjugate('had', '3sg'))

# end timing
end_time = time.time()
print(str(int(round((end_time - start_time) * 1000, 0))) + 'ms')

exit()

# it takes the root verb of the word from the conjugation on both sides (input and output)
# then matches it to the response so that it can understand that the task has been answered
# take also the reference with pronoun and pass it to answer in the function

# user input
input_string = "i went here yesterday"

# show thinking
print('\n-----------THIS IS MY THOUGHT PROCESS-----------\n')

# sanitizes input
input_string = input.sanitize_input(input_string)

# converts to words
words = input.return_words_from_input_string(input_string)

# gets word data and creates a file
for index, word in enumerate(words):
    memory.save_word_to_memory(word, words_dir, verbs_dir)

memory.compute_word_tree(words, words_dir)

exit()

# creates task file and variables
task_id, file_path = create.create_task_file(input_string, words, words_dir,
                                             tasks_dir)
file_name = file_path.split('/')[len(file_path.split('/')) - 1].strip('.py')
date_dir = file_path.split('/')[len(file_path.split('/')) - 2]

# gets and imports the task
exec("from data.memory.tasks.{}.{} import {}".format(date_dir, file_name,
                                                     file_name))
exec("task = {}".format(file_name))

if task.type == 'question':
    response = 'You have asked me a question'
elif task.type == 'statement':
    response = 'You have given a statement'

print('\n')
# show response
print('-----------THIS IS MY RESPONSE-----------')
print('\n')

print(response)

print('\n')

print('- me :)')
# end timing
end_time = time.time()
print(str(int(round((end_time - start_time) * 1000, 0))) + 'ms')
