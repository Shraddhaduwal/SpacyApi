import json

from sqlalchemy.ext import mutable
from db import db


# Model class
class DataModel(db.Model):
    __tablename__ = 'spacy_db'

    id = db.Column(db.Integer, primary_key=True)
    text_id = db.Column(db.Integer, unique=True)
    text_description = db.Column(db.String(1000))

    def __init__(self, text_id, text_description):
        self.text_id = text_id
        self.text_description = text_description

    def json(self):
        return {'text_id': self.text_id, 'text_description': self.text_description}

    @classmethod
    def find_by_text_id(cls, text_id):  # Select * from spacy_db where text_id=text_id Limit=1
        return cls.query.filter_by(text_id=text_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            print(value)
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


mutable.MutableDict.associate_with(JsonEncodedDict)
