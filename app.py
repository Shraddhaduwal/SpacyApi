from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import spacy
from collections import Counter
from spacy.matcher import Matcher


# Init app
app = Flask(__name__)
# Init Api
api = Api(app)

text_list = []

nlp = spacy.load("en_core_web_sm")


# Model class
class DataModel:
    def __init__(self, text_id="", text_description=""):
        self.text_id = text_id
        self.text_description = text_description

    def words_without_stopwords(self, text_id):
        """Words without stop_words, spaces, punctuations"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]  # Generates a list type object
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(text).lower())  # Expected is string type object but text is list and converting into lowercase
        text_without_stopwords = [str(token) for token in doc if token.is_stop is False if token.is_punct is False\
                                  if token.is_space is False]
        # Token is a spacy.tokens.doc.Doc object and cannot be Json serialized, we need to convert it into string again
        return {'text': text_without_stopwords}

    def total_nouns(self, text_id):
        """Noun words, total no of nouns, nouns frequencies"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        print(nlp.pipe_names)
        doc = nlp(str(text).lower())
        nouns = [token.text for token in doc if token.pos_ == 'NOUN']
        noun_frequency = Counter(nouns)
        favorite_noun = max(noun_frequency, key=noun_frequency.get)
        return {'nouns': nouns,
                'noun_count': len(nouns),
                'noun_frequency': noun_frequency,
                'favorite_noun': favorite_noun}

    def total_adjectives(self, text_id):
        """Adjectives, total no of adjectives, adjective frequencies"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        print(nlp.pipe_names)
        doc = nlp(str(text).lower())
        adjectives = [token.text for token in doc if token.pos_ == 'ADJ']
        adj_frequency = Counter(adjectives)
        favorite_adjective = max(adj_frequency, key=adj_frequency.get)
        list_of_tuples = sorted(adj_frequency.items(), reverse=True, key=lambda x: x[1])
        top_ten_adjectives = list_of_tuples[:10]

        sents = doc.sents
        sentences_with_adj = []

        """Finding the average number of adjectives in each sentences"""
        # finding the sentences with adjectives
        for sent in sents:
            for token in sent:
                if token.pos_ == "ADJ":
                    sentences_with_adj.append(sent)
                    break

        # finding the number of adjectives in sentences from sentences_with_adjectives
        sentences_and_adj_count = Counter(sentences_with_adj)

        # counting the average number of adjectives in each sentences
        count = 0
        sum = 0
        for key in sentences_and_adj_count:
            count += 1
            sum += sentences_and_adj_count[key]
        avg_in_sentences = sum / count

        """Average number of adjectives in each paragraph"""
        # Splitting the text into paragraphs
        start = 0
        paragraph_list, paragraphs_with_adjectives = [], []
        for token in doc:
            if token.is_space and token.text.count("\n") > 1:
                paragraph_list.append(doc[start:token.i])
                start = token.i

        for para in paragraph_list:
            for token in para:
                if token.pos_ == "ADJ":
                    paragraphs_with_adjectives.append(para)

        # Counting the total number of adjectives in each paragraphs
        paragraphs_and_adj_count = Counter(paragraphs_with_adjectives)

        # Counting the average number of adjectives in each paragraphs
        for key in paragraphs_and_adj_count:
            count += 1
            sum = paragraphs_and_adj_count[key]
        avg_in_paragraphs = sum / count

        return {'adjectives': adjectives,
                'adj_count': len(adjectives),
                'adj_frequency': adj_frequency,
                'favorite_adjective': favorite_adjective,
                'top_ten_adjectives': top_ten_adjectives,
                'average_adj_in_sentences': avg_in_sentences,
                'average_adj_in_paragraphs': avg_in_paragraphs}

    def total_verbs(self, text_id):
        """Verbs, total no of verbs, verb frequencies"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(text).lower())
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        verb_frequency = Counter(verbs)
        favorite_verb = max(verb_frequency, key=verb_frequency.get)
        return {'verbs': verbs,
                'verb_count': len(verbs),
                'verb_frequency': verb_frequency,
                'favorite_verb': favorite_verb}

    def noun_noun_phrase(self, text_id):
        """Noun-Noun phrases and their frequencies"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(text).lower())
        noun_noun_phrases =[chunk.text for chunk in doc.noun_chunks]
        noun_noun_phrase_frequency = Counter(noun_noun_phrases)
        favorite_noun_noun = max(noun_noun_phrase_frequency, key=noun_noun_phrase_frequency.get)
        return {'noun_noun_phrases': noun_noun_phrases,
                'noun_noun_phrase_count': len(noun_noun_phrases),
                'noun_noun_phrase_frequency': noun_noun_phrase_frequency,
                'favorite_noun_noun_phrase': favorite_noun_noun}

    def noun_adj_phrase(self, text_id):
        """Gives Noun-adjective phrases from the text and their frequencies"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        doc = nlp(str(text).lower())
        try:
            pattern = [{'POS': 'NOUN'}, {'POS': 'ADJ'}]
            matcher.add('NOUN_ADJ_PATTERN', None, pattern)
            matches = matcher(doc)
            print("Total matches found:", len(matches))

            noun_adj_phrases = [doc[start:end].text for match_id, start, end in matches]
            print(noun_adj_phrases)
            noun_adj_phrase_frequency = Counter(noun_adj_phrases)
            favorite_noun_adj_phrase = max(noun_adj_phrase_frequency, key=noun_adj_phrase_frequency.get)

            return {'noun_adj_phrases': noun_adj_phrases,
                    'noun_adj_phrase_count': len(noun_adj_phrases),
                    'noun_adj_phrase_frequency': noun_adj_phrase_frequency,
                    'favorite_noun_adj_phrase': favorite_noun_adj_phrase}
        except Exception:
            pass

    def adj_noun_phrase(self, text_id):
        """Gives adjective-noun phrases from the text and their frequencies"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        doc = nlp(str(text))

        pattern = [{'POS': 'ADJ'}, {'POS': 'NOUN'}]
        matcher.add('ADJ_NOUN_PATTERN', None, pattern)
        matches = matcher(doc)
        print("Total matches found", len(matches))

        adj_noun_phrases = [doc[start:end].text for match_id, start, end in matches]
        adj_noun_phrase_frequency = Counter(adj_noun_phrases)
        favorite_adj_noun_phrase = max(adj_noun_phrase_frequency, key=adj_noun_phrase_frequency.get)
        return {'adj_noun_phrases': adj_noun_phrases,
                'adj_noun_phrase_count': len(adj_noun_phrases),
                'adj_noun_phrase_frequency': adj_noun_phrase_frequency,
                'favorite_adj_noun_phrase': favorite_adj_noun_phrase}

    def sentences_with_two_or_more_nouns(self, text_id):
        """Sentences with two or more nouns"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        matched_sentences = []

        def collect_sents(matcher, doc_inside, i, matches):
            match_id, start, end = matches[i]
            span = doc_inside[start:end]
            sents = span.sent
            matched_sentences.append(sents.text)
        pattern = [{'POS': 'NOUN'}, {'POS': 'NOUN'}, {'POS': 'NOUN', 'OP': '*'}]
        matcher.add('SENTENCES_WITH_2_OR_MORE_NOUNS', collect_sents, pattern)
        doc = nlp(str(text))
        match = matcher(doc)
        return matched_sentences

    def sentences_with_two_or_more_adj(self, text_id):
        """Sentences with two or more adjectives"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        matched_sentences = []

        def collect_sents(matcher, doc, i, matches):
            match_id, start, end = matches[i]
            span = doc[start:end]
            sents = span.sent
            matched_sentences.append(sents.text)

        pattern = [{'POS': 'ADJ'}, {'POS': 'ADJ'}, {'POS': 'ADJ', 'OP': '*'}]
        matcher.add('SENTENCES_WITH_2_OR_MORE_ADJ', collect_sents, pattern)
        doc = nlp(str(text))
        matches = matcher(doc)

        return matched_sentences

    def sentences_with_two_or_more_verbs(self, text_id):
        """Sentences with two or more verbs"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        doc = nlp(str(text))
        matches = matcher(doc)
        matched_sentences = []

        def collect_sents(matcher, doc, i, matches):
            match_id, start, end = matches[i]
            span = doc[start:end]
            sents = span.sent
            matched_sentences.append(sents.text)

        pattern = [{'POS': 'VERB'}, {'POS': 'VERB'}, {'POS': 'VERB', 'OP': '*'}]
        matcher.add('SENTENCES_WITH_2_OR_MORE_VERB', collect_sents, pattern)

        return matched_sentences

    def sentences_without_noun(self, text_id):
        """Sentences without noun"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(text))

        sentences = []
        for sentence in list(doc.sents):
            for token in sentence:
                if token.pos_ == 'NOUN':
                    sentences.append(sentence)
                    break

        return sentences

    def sentences_without_adj(self, text_id):
        """Sentences without adjectives"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(text))

        sentences = []
        for sentence in list(doc.sents):
            for token in sentence:
                if token.pos_ == 'ADJ':
                    sentences.append(sentence)
                    break
        return sentences

    def sentences_without_verbs(self, text_id):
        """Sentences without verbs"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(text))
        sentences = []
        for sentence in list(doc.sents):
            for token in sentence:
                if token.pos_ == 'VERB':
                    sentences.append(sentence)
                    break

        return sentences

    def person_names(self, text_id):
        """Person names and their frequencies"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=["tokenizer", "tagger", "parser", "ner", "textcat", "..."])
        doc = nlp(str(text))

        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        name_frequency = Counter(names)

        # Person name with maximum frequency
        favorite_name = max(name_frequency, key=name_frequency.get)

        return {'person_names': names,
                'person_name_frequency': name_frequency,
                'favorite_person_name': favorite_name}

    def tense(self, text_id):
        """Total present tense, past tense and future tense sentences"""
        text = [t['text_description'] for t in text_list if t['text_id'] == text_id]
        nlp.pipe(text, disable=["tokenizer", "tagger", "parser", "ner", "textcat", "..."])
        doc = nlp(str(text))

        sents = doc.sents
        sentences_with_verbs, present_tense_sentences, past_tense_sentences, future_tense_sentences = [], [], [], []

        # All sentences having verbs
        for sent in sents:
            for token in sent:
                if token.pos_ == "VERB":
                    sentences_with_verbs.append(sent)
                    break

        # Present tense sentences
        for sent in sentences_with_verbs:
            for token in sent:
                if token.tag_ in ["VBZ", "VBP", "VBG"]:
                    present_tense_sentences.append(sent)
                    break

        # Past tense sentences
        for sent in sentences_with_verbs:
            for token in sent:
                if token.tag_ in ["VBD", "VBN"]:
                    past_tense_sentences.append(sent)
                    break

        # Future tense sentences
        for sent in sentences_with_verbs:
            for token in sent:
                if token.tag_ in ["VBC", "VBF"]:
                    future_tense_sentences.append(sent)
                    break

        return {'present_tense_sentences': present_tense_sentences,
                'past_tense_sentences': past_tense_sentences,
                'future_tense_sentences': future_tense_sentences}


# Resource class also called Model class
class Data(Resource):
    parser = reqparse.RequestParser()  # initialization of the object of reqparse
    parser.add_argument('text_description', required=True, help='This field cannot be empty')
    # The parser searches for the arguments described in it and make changes to them and ignores the other args

    def get(self, text_id):
        # text = next(filter(lambda x: x['text_id'] == text_id, text_list), None)
        print('sentences', text_id)
        obj = DataModel()  # class object instance
        result = obj.words_without_stopwords(text_id)
        nouns = obj.total_nouns(text_id)
        adjectives = obj.total_adjectives(text_id)
        verbs = obj.total_verbs(text_id)
        noun_noun_phrases = obj.noun_noun_phrase(text_id)
        noun_adj_phrases = obj.noun_adj_phrase(text_id)
        adj_noun_phrases = obj.adj_noun_phrase(text_id)
        sentences_with_two_or_more_nouns = obj.sentences_with_two_or_more_nouns(text_id)
        sentences_with_two_or_more_adj = obj.sentences_with_two_or_more_adj(text_id)
        sentences_with_two_or_more_verbs = obj.sentences_with_two_or_more_verbs(text_id)
        sentences_without_nouns = obj.sentences_without_noun(text_id)
        sentences_without_adjectives = obj.sentences_without_adj(text_id)
        sentences_without_verbs = obj.sentences_without_verbs(text_id)
        person_names = obj.person_names(text_id)
        tenses = obj.tense(text_id)
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

        # return {'sentences_with_one_or_more_nouns': sentences_with_two_or_more_nouns}

    def post(self, text_id):
        request_data = Data.parser.parse_args()  # Execution

        if next(filter(lambda x: x['text_id'] == text_id, text_list), None):
            return {'message': 'The text with text_id {} already exists'. format(text_id)}, 400

        new_text = {
            'text_id': text_id,
            'text_description': request_data['text_description']
        }
        text_list.append(new_text)
        return new_text, 201

    def delete(self, text_id):
        global text_list
        text_list = list(filter(lambda x: x['text_id'] != text_id, text_list))
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


api.add_resource(Data, '/data/<string:text_id>')
api.add_resource(AllData, '/alldata')
# /data refers to root class that is Data and /data/<string:text_id> refers to the text we send from postman


# Run the server
if __name__ == '__main__':
    app.run(debug=True)
