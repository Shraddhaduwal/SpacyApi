import spacy
from spacy.matcher import Matcher
from collections import Counter

from db import db

nlp = spacy.load("en_core_web_sm")


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

    def words_without_stopwords(self):
        """Words without stop_words, spaces, punctuations"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(self.text_description).lower())  # Expected is string type object but text is list and converting into lowercase
        text_without_stopwords = [str(token) for token in doc if token.is_stop is False if token.is_punct is False\
                                  if token.is_space is False]
        # Token is a spacy.tokens.doc.Doc object and cannot be Json serialized, we need to convert it into string again
        return {'text_without_stopwords': text_without_stopwords}

    def total_nouns(self):
        """Noun words, total no of nouns, nouns frequencies"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(self.text_description).lower())
        nouns = [token.text for token in doc if token.pos_ == 'NOUN']
        noun_frequency = Counter(nouns)
        favorite_noun = max(noun_frequency, key=noun_frequency.get)
        return {'nouns': nouns,
                'noun_count': len(nouns),
                'noun_frequency': noun_frequency,
                'favorite_noun': favorite_noun}

    def total_adjectives(self):
        """Adjectives, total no of adjectives, adjective frequencies"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        print(nlp.pipe_names)
        doc = nlp(str(self.text_description).lower())
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

    def total_verbs(self):
        """Verbs, total no of verbs, verb frequencies"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(self.text_description).lower())
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        verb_frequency = Counter(verbs)
        favorite_verb = max(verb_frequency, key=verb_frequency.get)
        return {'verbs': verbs,
                'verb_count': len(verbs),
                'verb_frequency': verb_frequency,
                'favorite_verb': favorite_verb}

    def noun_noun_phrase(self):
        """Noun-Noun phrases and their frequencies"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(self.text_description).lower())
        noun_noun_phrases =[chunk.text for chunk in doc.noun_chunks]
        noun_noun_phrase_frequency = Counter(noun_noun_phrases)
        favorite_noun_noun = max(noun_noun_phrase_frequency, key=noun_noun_phrase_frequency.get)
        return {'noun_noun_phrases': noun_noun_phrases,
                'noun_noun_phrase_count': len(noun_noun_phrases),
                'noun_noun_phrase_frequency': noun_noun_phrase_frequency,
                'favorite_noun_noun_phrase': favorite_noun_noun}

    def noun_adj_phrase(self):
        """Gives Noun-adjective phrases from the text and their frequencies"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        doc = nlp(str(self.text_description).lower())
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

    def adj_noun_phrase(self):
        """Gives adjective-noun phrases from the text and their frequencies"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        doc = nlp(str(self.text_description).lower())

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

    def sentences_with_two_or_more_nouns(self):
        """Sentences with two or more nouns"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        matched_sentences = []

        def collect_sents(matcher, doc_inside, i, matches):
            match_id, start, end = matches[i]
            span = doc_inside[start:end]
            sents = span.sent
            matched_sentences.append(sents.text)
        pattern = [{'POS': 'NOUN'}, {'POS': 'NOUN'}, {'POS': 'NOUN', 'OP': '*'}]
        matcher.add('SENTENCES_WITH_2_OR_MORE_NOUNS', collect_sents, pattern)
        doc = nlp(str(self.text_description).lower())
        match = matcher(doc)
        return matched_sentences

    def sentences_with_two_or_more_adj(self):
        """Sentences with two or more adjectives"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        matched_sentences = []

        def collect_sents(matcher, doc, i, matches):
            match_id, start, end = matches[i]
            span = doc[start:end]
            sents = span.sent
            matched_sentences.append(sents.text)

        pattern = [{'POS': 'ADJ'}, {'POS': 'ADJ'}, {'POS': 'ADJ', 'OP': '*'}]
        matcher.add('SENTENCES_WITH_2_OR_MORE_ADJ', collect_sents, pattern)
        doc = nlp(str(self.text_description).lower())
        matches = matcher(doc)

        return matched_sentences

    def sentences_with_two_or_more_verbs(self):
        """Sentences with two or more verbs"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        matcher = Matcher(nlp.vocab)
        doc = nlp(str(self.text_description).lower())
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

    def sentences_without_noun(self):
        """Sentences without noun"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(self.text_description).lower())

        sentences = []
        for sentence in list(doc.sents):
            for token in sentence:
                if token.pos_ == 'NOUN':
                    sentences.append(sentence)
                    break

        return sentences

    def sentences_without_adj(self):
        """Sentences without adjectives"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(self.text_description).lower())

        sentences = []
        for sentence in list(doc.sents):
            for token in sentence:
                if token.pos_ == 'ADJ':
                    sentences.append(sentence)
                    break

        return sentences

    def sentences_without_verbs(self):
        """Sentences without verbs"""
        nlp.pipe(self.text_description, disable=['tokenizer', 'tagger', 'parser', 'ner', 'textcat', '...'])
        doc = nlp(str(self.text_description).lower())
        sentences = []
        for sentence in list(doc.sents):
            for token in sentence:
                if token.pos_ == 'VERB':
                    sentences.append(sentence)
                    break

        return sentences

    def person_names(self):
        """Person names and their frequencies"""
        nlp.pipe(self.text_description, disable=["tokenizer", "tagger", "parser", "ner", "textcat", "..."])
        doc = nlp(str(self.text_description).lower())

        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        name_frequency = Counter(names)

        try:
            # Person name with maximum frequency
            favorite_name = max(name_frequency, key=name_frequency.get)

            return {'person_names': names,
                    'person_name_frequency': name_frequency,
                    'favorite_person_name': favorite_name}
        except Exception:
            return {'message': 'No favorite person name'}

    def tense(self):
        """Total present tense, past tense and future tense sentences"""
        nlp.pipe(self.text_description, disable=["tokenizer", "tagger", "parser", "ner", "textcat", "..."])
        doc = nlp(str(self.text_description).lower())

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
