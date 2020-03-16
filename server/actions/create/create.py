from flask import current_app as app
from server.models import Category, Concept, ConceptRelationship, Word
from server.database import db


# creates concepts for a given list of words
def create_concepts(words):

    if app.config['DEBUG']:
        print('********************\n')
        print('Now creating concepts...\n')

    # gets categories
    adjective = Category.query.filter_by(string='adjective').first()
    adverb = Category.query.filter_by(string='adverb').first()
    conjunction = Category.query.filter_by(string='conjunction').first()
    determiner = Category.query.filter_by(string='determiner').first()
    noun = Category.query.filter_by(string='noun').first()
    preposition = Category.query.filter_by(string='preposition').first()
    pronoun = Category.query.filter_by(string='pronoun').first()
    verb = Category.query.filter_by(string='verb').first()

    # creates empty concepts list
    concepts = []

    # loops through the words
    for word in words:

        # sets concept type
        concept_type = ''
        if word['category'] == noun:
            concept_type = 'noun'
        elif word['category'] == verb:
            concept_type = 'verb'
        elif word['category'] == adjective:
            concept_type = 'adjective'
        else:
            continue

        # only runs if concept type is one of the above
        if concept_type:

            # checks and creates concept type if needed
            concept = Concept.query.filter_by(
                string=word['word'].string).first()

            # if no concept has been found, it creates it
            if not concept:
                concept = Concept(
                    type=concept_type,
                    string=word['word'].string,
                )
                db.session.add(concept)

            # if concept is found but of a different type, it creates another one
            if concept.type != concept_type:
                concept = Concept(
                    type=concept_type,
                    string=word['word'].string,
                )
                db.session.add(concept)

            # adds the word to the concept
            concept.related_words.append(word['word'])

            concepts.append(concept)

            if app.config['DEBUG']:
                print(f'{concept}')

    if app.config['DEBUG']:
        print('\n')

    return concepts


# creates concept relationships given a list of concepts
def create_concept_relationships(concepts):

    if app.config['DEBUG']:
        print('********************\n')
        print('Now creating concept relationships...\n')

    # sets up variables
    concept_noun = None
    concept_verb = None
    concept_adjective = None

    # loops through the concepts
    for concept in concepts:

        if concept.type == 'noun':
            concept_noun = concept
        elif concept.type == 'verb':
            concept_verb = concept
        elif concept.type == 'adjective':
            concept_adjective = concept

    # creates a concept relationship
    concept_relationship = ConceptRelationship()
    db.session.add(concept_relationship)

    # adds relationship ids
    concept_relationship.concept_noun = concept_noun
    concept_relationship.concept_verb = concept_verb
    concept_relationship.concept_adjective = concept_adjective

    db.session.commit()

    if app.config['DEBUG']:
        print(concept_relationship)

    if app.config['DEBUG']:
        print('\n')
