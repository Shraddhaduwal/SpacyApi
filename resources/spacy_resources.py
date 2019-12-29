from flask_restful import Resource, reqparse
from models.spacy_models import DataModel
from models.results import Results
from nlp import operations


# Resource class also called Model class
class Data(Resource):
    parser = reqparse.RequestParser()  # initialization of the object of reqparse
    parser.add_argument('text_description', required=True, help='This field cannot be empty')
    # The parser searches for the arguments described in it and make changes to them and ignores the other args

    def get(self, text_id):
        text = DataModel.find_by_text_id(text_id)
        if text:
            obj = DataModel(text_id, text.text_description)  # class object instance
            text_desc = obj.text_description
            # passing text_description(attribute of obj) to text_desc and to operations.py

            result = operations.words_without_stopwords(text_desc)
            obj_result = Results(result)
            obj_result.save_to_db()

            nouns = operations.total_nouns(text_desc)
            obj_noun = Results(nouns)
            obj_noun.save_to_db()

            adjectives = operations.total_adjectives(text_desc)
            obj_adjectives = Results(adjectives)
            obj_adjectives.save_to_db()

            verbs = operations.total_verbs(text_desc)
            obj_verbs = Results(verbs)
            obj_verbs.save_to_db()

            noun_noun_phrases = operations.noun_noun_phrase(text_desc)
            obj_noun_noun = Results(noun_noun_phrases)
            obj_noun_noun.save_to_db()

            noun_adj_phrases = operations.noun_adj_phrase(text_desc)
            obj_noun_adj = Results(noun_adj_phrases)
            obj_noun_adj.save_to_db()

            adj_noun_phrases = operations.adj_noun_phrase(text_desc)
            obj_adj_noun = Results(adj_noun_phrases)
            obj_adj_noun.save_to_db()

            sentences_with_two_or_more_nouns = operations.sentences_with_two_or_more_nouns(text_desc)
            obj_sentences_noun = Results(sentences_with_two_or_more_nouns)
            obj_sentences_noun.save_to_db()

            sentences_with_two_or_more_adj = operations.sentences_with_two_or_more_adj(text_desc)
            obj_sentences_adj = Results(sentences_with_two_or_more_adj)
            obj_sentences_adj.save_to_db()

            sentences_with_two_or_more_verbs = operations.sentences_with_two_or_more_verbs(text_desc)
            obj_sentences_verbs = Results(sentences_with_two_or_more_verbs)
            obj_sentences_verbs.save_to_db()

            sentences_without_nouns = operations.sentences_without_noun(text_desc)
            obj_sentences_without_noun = Results(sentences_without_nouns)
            obj_sentences_without_noun.save_to_db()

            sentences_without_adjectives = operations.sentences_without_adj(text_desc)
            obj_sentences_without_adjectives = Results(sentences_without_adjectives)
            obj_sentences_without_adjectives.save_to_db()

            sentences_without_verbs = operations.sentences_without_verbs(text_desc)
            obj_sentences_without_verbs = Results(sentences_without_verbs)
            obj_sentences_without_verbs.save_to_db()

            person_names = operations.person_names(text_desc)
            obj.names = Results(person_names)
            obj.names.save_to_db()

            tenses = operations.tense(text_desc)
            obj_tense = Results(tenses)
            obj_tense.save_to_db()

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
                    'sentences_with_different_tenses': tenses}

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
