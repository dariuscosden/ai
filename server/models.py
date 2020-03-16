from server.database import db

# categories to words relationship
categories = db.Table('categories',
                      db.Column('category_id', db.Integer, db.ForeignKey(
                          'category.id'), primary_key=True),
                      db.Column('word_id', db.Integer, db.ForeignKey(
                          'word.id'), primary_key=True)
                      )


# concepts to words relationship
concepts = db.Table('concepts',
                    db.Column('concept_id', db.Integer, db.ForeignKey(
                        'concept.id'), primary_key=True),
                    db.Column('word_id', db.Integer, db.ForeignKey(
                        'word.id'), primary_key=True)
                    )


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String, nullable=False)

    # categories relationship
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
                                 backref=db.backref('words', lazy=True))

    # concepts relationship
    concepts = db.relationship('Concept', secondary=concepts, lazy='subquery',
                               backref=db.backref('related_words', lazy=True))

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
    type = db.Column(db.String, nullable=True)
    string = db.Column(db.String, nullable=True)

    # gets the words related to the concept in an organized fashion

    # TODO: build out this function
    def get_words(self):
        return self.words

    # repr
    def __repr__(self):
        return f"<co-{self.string.upper()}>"


class ConceptRelationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # concept noun relationship
    concept_noun_id = db.Column(db.Integer, db.ForeignKey('concept.id'))
    concept_noun = db.relationship(
        "Concept", backref="noun_relationships", foreign_keys=[concept_noun_id])

    # concept verb relationship
    concept_verb_id = db.Column(db.Integer, db.ForeignKey('concept.id'))
    concept_verb = db.relationship(
        "Concept", backref="verb_relationships", foreign_keys=[concept_verb_id])

    # concept adjective relationship
    concept_adjective_id = db.Column(db.Integer, db.ForeignKey('concept.id'))
    concept_adjective = db.relationship(
        "Concept", backref="adjective_relationships", foreign_keys=[concept_adjective_id])

    # repr
    def __repr__(self):
        return f"<cor-{self.concept_noun} & {self.concept_verb} & {self.concept_adjective}>"
