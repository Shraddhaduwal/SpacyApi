from flask_restful import Resource, reqparse
from models.spacy_models import DataModel


# Resource class also called Model class
class Data(Resource):
    parser = reqparse.RequestParser()  # initialization of the object of reqparse
    parser.add_argument('text_description', required=True, help='This field cannot be empty')
    # The parser searches for the arguments described in it and make changes to them and ignores the other args

    def get(self, text_id):
        text = DataModel.find_by_text_id(text_id)
        if text:
            obj = DataModel(text_id, text.text_description)  # class object instance
            result = obj.words_without_stopwords()
            nouns = obj.total_nouns()
            adjectives = obj.total_adjectives()
            verbs = obj.total_verbs()
            noun_noun_phrases = obj.noun_noun_phrase()
            noun_adj_phrases = obj.noun_adj_phrase()
            adj_noun_phrases = obj.adj_noun_phrase()
            sentences_with_two_or_more_nouns = obj.sentences_with_two_or_more_nouns()
            sentences_with_two_or_more_adj = obj.sentences_with_two_or_more_adj()
            sentences_with_two_or_more_verbs = obj.sentences_with_two_or_more_verbs()
            sentences_without_nouns = obj.sentences_without_noun()
            sentences_without_adjectives = obj.sentences_without_adj()
            sentences_without_verbs = obj.sentences_without_verbs()
            person_names = obj.person_names()
            tenses = obj.tense()

            return {'word_without_stopwords': result,
                    'nouns': nouns,
                    'adjectives': adjectives,
                    'verbs': verbs,
                    'noun_noun_phrases': noun_noun_phrases,
                    'noun_adj_phrases': noun_adj_phrases,
                    'adj_noun_phrases': adj_noun_phrases,
                    'sentences_with_one_or_more_nouns': str(sentences_with_two_or_more_nouns),
                    'sentences_with_one_or_more_adj': str(sentences_with_two_or_more_adj),
                    'sentences_with_one_or_more_verbs': str(sentences_with_two_or_more_verbs),
                    'sentences_without_nouns': str(sentences_without_nouns),
                    'sentences_without_adjectives': str(sentences_without_adjectives),
                    'sentences_without_verbs': str(sentences_without_verbs),
                    'person_names': person_names,
                    'sentences_with_different_tenses': str(tenses)}

        return {"message": "Something is wrong"}

    def post(self, text_id):
        if DataModel.find_by_text_id(text_id):
            return {'message': 'The text with text_id {} already exists'.format(text_id)}, 400

        request_data = Data.parser.parse_args()  # Execution
        text = DataModel(text_id, request_data['text_description'])
        try:
            text.save_to_db()
        except Exception:
            return {'message': 'An error occurred while inserting the item'}, 500

        return text.json(), 201

    def delete(self, text_id):
        text = DataModel.find_by_text_id(text_id)
        if text:
            text.delete_from_db()

        return {'message': 'text with text_id {} deleted'.format(text_id)}

    def put(self, text_id):
        request_data = Data.parser.parse_args()  # Execution

        text = next(filter(lambda x: x['text_id'] == text_id, text_list), None)
        if text is None:
            text = {
                'text_id': text_id,
                'text_description': request_data['text description']
            }
            text_list.append(text)
        else:
            text.update(request_data)
        return text


class AllData(Resource):
    def get(self):
        return {'text list': text_list}
