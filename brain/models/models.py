# word model
class Word:

    # initializes the class
    def __init__(self, string):
        self.string = string

    # gets the first letter
    def get_first_letter(self):
        return self.string[:2]

    # gets the second letter
    def get_second_letter(self):
        return self.string[2:3]

    # gets the non-string word
    def get_non_string_word(self):
        string = self.string.strip('"')
        string = string.strip("'")
        return string


# task model
class Task:

    # initializes the class
    def __init__(self, id, words, type, status):
        self.id = id
        self.words = words
        self.type = type
        self.status = status

    # returns the task words
    def get_task_words(self):
        return self.words
