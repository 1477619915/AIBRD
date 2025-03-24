import stanfordnlp
from nltk.stem import PorterStemmer
from pattern.entity.Token import Token

class TextProcessor:

    SPACE = " "
    PARENTHESIS = ["-LCB-", "-RCB-", "-LRB-", "-RRB-", "-LSB-", "-RSB-"]
    PARENTHESIS2 = ["LCB", "RCB", "LRB", "RRB", "LSB", "RSB"]
    SPACE = " "

    POS_TAGS = {
        "JJ": "JJ",
        "JJR": "JJ",
        "JJS": "JJ",
        "NN": "NN",
        "NNS": "NN",
        "NNP": "NN",
        "NNPS": "NN",
        "PRP": "PRP",
        "PRP$": "PRP",
        "RB": "RB",
        "RBR": "RB",
        "RBS": "RB",
        "VB": "VB",
        "VBD": "VB",
        "VBG": "VB",
        "VBN": "VB",
        "VBP": "VB",
        "VBZ": "VB",
        "WDT": "WH",
        "WP": "WH",
        "WP$": "WH",
        "WRB": "WH"
    }

    def get_string_from_lemmas(self, sentence):
        buffer = []
        tokens = sentence.get_tokens()
        for token in tokens:
            buffer.append(token.get_lemma())
            buffer.append(self.SPACE)
        return " ".join(buffer).strip()

    def process_text(self, text, check_for_identifiers):
        # Initialize the StanfordNLP pipeline
        nlp = stanfordnlp.Pipeline()

        # Process the input text
        doc = nlp(text)

        parsed_sentences = []
        id_counter = 0

        for sentence in doc.sentences:
            token_list = sentence.tokens
            sentence_text = " ".join([token.text for token in token_list])

            # Assuming you have a Token class similar to the one used in your Java code
            parsed_sentence = Sentence(str(id_counter), sentence_text)

            for token in token_list:
                parsed_token = parse_token(token, check_for_identifiers)
                parsed_sentence.add_token(parsed_token)

            parsed_sentences.append(parsed_sentence)
            id_counter += 1

        return parsed_sentences

    def parse_token(self, token, check_for_identifiers):
        word = token.text
        lemma = token.words[0].lemma.lower()
        pos = token.upos

        if check_for_identifiers:
            # Match identifiers like "org.Class"
            # Match method calls such as "call(param1)"
            if ('.' in word) or ('(' in word and ')' in word) and len(word) > 1:
                pos = "NN"

        general_pos = self.get_general_pos(pos)
        stem = self.stemming_porter(word).lower()

        parsed_token = Token(word, general_pos, pos, lemma, stem)
        return parsed_token

    def get_general_pos(self, pos):
        tag = self.POS_TAGS.get(pos)
        if tag is not None:
            return tag
        return pos

    def stemming_porter(self, token):
        stemmer = PorterStemmer()
        stemmed_token = stemmer.stem(token)
        return stemmed_token

    def get_all_tokens(self, sentences):
        tokens = []
        for sentence in sentences:
            tokens.extend(sentence.get_tokens())
        return tokens




