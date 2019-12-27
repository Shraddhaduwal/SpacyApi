from db import db
from models.spacy_models import JsonEncodedDict


class Results(db.Model):
    __tablename__ = 'Results'

    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(JsonEncodedDict)

    def __init__(self, results):
        self.results = results

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

