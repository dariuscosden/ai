from server.database import db

categories = db.Table('categories',
                      db.Column('category_id', db.Integer, db.ForeignKey(
                          'category.id'), primary_key=True),
                      db.Column('word_id', db.Integer, db.ForeignKey(
                          'word.id'), primary_key=True)
                      )


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String, nullable=False)

    # categories relationship
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
                                 backref=db.backref('words', lazy=True))

    # concept relationship
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'))

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
        return f"<w-{self.string.upper()}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String, nullable=False)

    # repr
    def __repr__(self):
        return f"<c-{self.string.upper()}>"


class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # words relationship
    words = db.relationship('Word', backref='concept', lazy=True)

    # repr
    def __repr__(self):
        return f"<Concept - {self.string}>"
