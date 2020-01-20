from server.database import db


class Word:
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String, nullable=False)

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

    # repr
    def __repr__(self):
        return f"<Word - {self.string}>"


class Concept:
    id = db.Column(db.Integer, primary_key=True)

    # words relationship
    words = db.relationship('Word', backref='concept', lazy=True)

    # repr
    def __repr__(self):
        return f"<Concept - {self.string}>"
