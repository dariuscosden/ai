import os
import json
import copy
import requests
import pattern.en

from flask import current_app as app
from server.models import Word, Category
from server.database import db


# adds words to memory if they don't already exist
def add_words_to_memory(words):
    db_words = []

    if app.config['DEBUG']:
        print('********************\n')
        print('Now adding words to the database...\n')

    for w in words:

        # checks for existing word and creates one if needed
        word = Word.query.filter_by(string=w).first()

        # checks if conjugated
        conjugated = False
        infinitive = pattern.en.conjugate(w, 'INFINITIVE')
        if infinitive != w:
            conjugated = True

        # checks if plural
        plural = False
        singularized = pattern.en.singularize(w)
        if singularized != w:
            plural = True
            w = singularized

        if not word:

            # adds the word to the database
            word = Word(string=w)
            db.session.add(word)

            # adds the plural form
            if plural:
                plural_word = Word(string=pattern.en.pluralize(w))
                db.session.add(plural_word)

            # gets the word from oxford dictionaries api
            url = f"https://od-api.oxforddictionaries.com/api/v2/entries/en-us/{w.lower()}"
            r = requests.get(
                url,
                headers={
                    "app_id": app.config['OXFORD_APP_ID'],
                    "app_key": app.config['OXFORD_APP_KEY']
                }
            )

            # to json
            r = r.json()

            # gets the lexical categories
            for entry in r['results'][0]['lexicalEntries']:

                # sets the lexical category
                category = entry['lexicalCategory']['id']

                # checks for existing category
                c = Category.query.filter_by(string=category).first()
                if not c:
                    c = Category(string=category)
                    db.session.add(c)

                word.categories.append(c)

                # handles plural
                if plural:
                    plural_word.categories.append(c)

                if app.config['DEBUG']:
                    print(f'Added {word} to the {category} category')

                    # plural
                    if plural:
                        print(
                            f'Added {plural_word} to the {category} category')

            # adds verb category if conjugated
            if conjugated:
                verb = Category.query.filter_by(string='verb').first()

                if not verb:
                    verb = Category(string='verb')
                    db.session.add(verb)

                word.categories.append(verb)

                if app.config['DEBUG']:
                    print(f'Added {word} to the {verb} category')

            db.session.commit()

            if app.config['DEBUG']:
                print(f'Added {word} to the database')

        # debug
        else:

            if app.config['DEBUG']:
                print(f'Already have {word} in the database')

        db_words.append(word)

    if app.config['DEBUG']:
        print('\n')

    return db_words
