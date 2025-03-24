from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Sentence import Sentence


class SentenceUtils:

    CLAUSE_SEPARATORS = {";", ",", "-", "_", "--", ":"}
    POS_SEPARATORS = {"CC"}
    TERM_SEPARATORS = {"and", "or", "but"}
    AMBIGUOUS_POS_VERBS = {"put", "set", "cut", "quit", "shut", "hit"}
    UNDETECTED_VERBS = {"boomark", "build", "cache", "change", "check",
                        "clic", "click", "copy", "drag", "enter", "export",
                        "file", "fill", "goto", "import", "input", "insert", "install",
                        "load", "long-press", "open",
                        "paste", "post", "press", "release", "rename", "return", "right-click", "run",
                        "scale", "scroll", "select", "show", "start", "stop", "surf",
                        "switch",
                        "tap", "try", "type", "use", "view", "visit",
                        "yield"}

    def match_terms_by_lemma(self, terms, token):
        return any(t.lower() == token.get_lemma().lower() for t in terms)

    def check_html_code(self, tokens, ampersandIdx):
        numTextTokens = self.check_x_tokens_for_html_code(tokens, ampersandIdx, 3)
        if numTextTokens == -1:
            numTextTokens = self.check_x_tokens_for_html_code(tokens, ampersandIdx, 4)
        return numTextTokens

    def check_x_tokens_for_html_code(self, tokens, ampersand_idx, num_toks):
        to_idx = len(tokens)
        if ampersand_idx + num_toks < len(tokens):
            to_idx = ampersand_idx + num_toks

        token_sublist = tokens[ampersand_idx:to_idx]
        text = TextProcessor.get_string_from_lemmas(Sentence("0", token_sublist))
        match = re.match(r'& # \d+ ;|& #[xX] [0-9a-fA-F]+ ;|& #[xX][0-9a-fA-F]+ ;', text)

        if match:
            return num_toks

        return -1

    def extract_clauses(self, sentence):
        tokens = sentence.get_tokens()
        clauses = []
        clause_tokens = []

        current_clause = 0
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if (self.match_terms_by_lemma(self.CLAUSE_SEPARATORS, token) or
                    self.match_terms_by_pos(self.POS_SEPARATORS, token) or
                    self.match_terms_by_lemma(self.TERM_SEPARATORS, token)):

                allow_split = True
                num_next_tokens = 1

                if token.get_lemma() == "-" and (i + 1 < len(tokens) and tokens[i + 1].get_lemma() == ">"):
                    allow_split = False
                elif token.get_lemma() == "&":
                    num_toks = self.check_html_code(tokens, i)
                    if num_toks != -1:
                        allow_split = False
                        num_next_tokens = num_toks

                if allow_split:
                    if clause_tokens:
                        clauses.append(Sentence(f"{sentence.get_id()}.{current_clause}", clause_tokens))
                        clause_tokens = []
                    i += 1
                else:
                    for j in range(i, i + num_next_tokens):
                        clause_tokens.append(tokens[j])
                    i += num_next_tokens
            else:
                clause_tokens.append(token)
                i += 1

        if clause_tokens:
            clauses.append(Sentence(f"{sentence.get_id()}.{current_clause}", clause_tokens))

        return clauses

    def is_imperative_sentence(self, tokens, enable_verb_tagged_as_nouns, is_present_tense):
        # Check for imperative tokens based on tense
        if is_present_tense:
            if self.check_for_present_imperative_tokens(tokens, enable_verb_tagged_as_nouns):
                return True
        else:
            if self.check_for_past_imperative_tokens(tokens):
                return True

        # Check for labels in the first labelLength terms: find the token ":"
        label_length = 5
        idx = -1
        for i, token in enumerate(tokens):
            if token.get_lemma() == ":":
                idx = i

        # If ":" is found, check for imperative tokens
        if idx != -1 and idx + 2 < len(tokens):
            if is_present_tense:
                return self.check_for_present_imperative_tokens(tokens[idx + 1:], enable_verb_tagged_as_nouns)
            else:
                return self.check_for_past_imperative_tokens(tokens[idx + 1:])

        return False

    def check_for_present_imperative_tokens(self, tokens, enable_verb_tagged_as_nouns):
        tokens_no_special_char = self.get_tokens_no_special_chars(tokens)
        if tokens_no_special_char is None:
            return False

        if len(tokens_no_special_char) < 2:
            return False

        first_token = tokens_no_special_char[0]
        second_token = tokens_no_special_char[1]

        if (first_token.get_pos() in ["VBN", "VBD", "VBG", "VBZ"] and not (
                self.lemmas_contain_token(self.AMBIGUOUS_POS_VERBS, first_token))):
            return False

        def is_verb_in_present(token):
            return token.get_pos() in ["VB", "VBP"]

        if is_verb_in_present(first_token):
            return True
        else:
            if second_token is not None:
                if (first_token.get_pos() in ["RB", "JJ"] and (is_verb_in_present(second_token)
                                                               or (second_token.get_pos() == "NN" and self.words_contain_token(
                                                                   self.UNDETECTED_VERBS, second_token))
                                                               or self.lemmas_contain_token(self.AMBIGUOUS_POS_VERBS,
                                                                                       second_token))
                        and len(tokens_no_special_char) > 2):
                    return True

                if len(tokens_no_special_char) > 3:
                    third_token = tokens_no_special_char[2]
                    if ((first_token.get_pos() == "RB" and second_token.get_pos() == "RB")
                            and (is_verb_in_present(third_token)
                                 or (third_token.get_pos() == "NN" and self.words_contain_token(self.UNDETECTED_VERBS,
                                                                                           third_token))
                                 or self.lemmas_contain_token(self.AMBIGUOUS_POS_VERBS, third_token))):
                        return True

            if self.lemmas_contain_token(self.UNDETECTED_VERBS, first_token) or self.lemmas_contain_token(self.AMBIGUOUS_POS_VERBS, first_token):
                return True

            if enable_verb_tagged_as_nouns:
                artificial_sentence = self.append_pronoun(tokens_no_special_char)

                if (artificial_sentence.get_tokens()[1].get_pos() == "VBP"
                        and not artificial_sentence.get_tokens()[2].get_general_pos() == "VB"):
                    return True

        return False

    def get_tokens_no_special_chars(self, tokens):
        # Make sure we discard non-word tokens at the beginning of the sentence
        idx = -1
        for i, token in enumerate(tokens):
            if re.match(r'^\w.*', token.get_lemma()):
                idx = i
                break

        # The sentence is full of non-word tokens
        if idx == -1:
            return None

        # Work only with word tokens
        return tokens[idx:]

    def lemmas_contain_token(self, lemmas, token):
        return self.string_equals_to_any_token(lemmas, token)

    def string_equals_to_any_token(self, tokens, string):
        if string is None:
            return False
        return any(token.lower() == string.lower() for token in tokens)

    def words_contain_token(self, words, token):
        return any(token.lower() == word.lower() for word in words)

    def append_pronoun(self, tokens):
        sentence_text = " ".join([token.get_word().lower() for token in tokens])

        # Appends an "I" to the beginning of the tokens, attempting to nudge
        # the tagger into recognizing an infinitive verb as such.
        artificial_sentence_text = f"I {sentence_text}"

        # You will need to implement a function similar to parse_sentence
        # in Python to create the Sentence object.
        return self.parse_sentence("0", artificial_sentence_text)

    def parse_sentence(self, sentence_id, sentence_txt):
        sentence_escaped = sentence_txt

        if not sentence_escaped.strip():
            return None

        sentences = TextProcessor.process_text(sentence_escaped, True)

        if sentences is not None:
            all_tokens = TextProcessor.get_all_tokens(sentences)
            return Sentence(sentence_id, all_tokens, sentence_escaped)

    def check_for_past_imperative_tokens(self, tokens):
        tokens_no_special_char = self.get_tokens_no_special_chars(tokens)
        if tokens_no_special_char is None:
            return False

        if len(tokens_no_special_char) < 2:
            return False

        first_token = tokens_no_special_char[0]
        second_token = tokens_no_special_char[1]

        # regular case, the sentence starts with a verb
        if first_token.get_pos() == "VBD" or first_token.get_pos() == "VBN":
            return True
        else:
            if second_token is not None:

                # case: the sentence starts with an adverb/adjective and then with a verb
                if (first_token.get_pos() == "RB" or first_token.get_pos() == "JJ") and \
                        (second_token.get_pos() == "VBD" or first_token.get_pos() == "VBN") and len(tokens_no_special_char) > 2:
                    return True

                if len(tokens_no_special_char) > 3:
                    third_token = tokens_no_special_char[2]
                    # case: the sentence starts with two adverbs and then with a verb
                    return (first_token.get_pos() == "RB" and second_token.get_pos() == "RB") and \
                        (third_token.get_pos() == "VBD" or first_token.get_pos() == "VBN")

        return False

    def break_by_parenthesis(self, sentence):
        sub_sentences = []
        sub_sentence = Sentence(sentence.id, [])
        tokens = sentence.tokens

        j = 0
        while j < len(tokens):
            current = tokens[j]

            if current.lemma == "-lrb-":
                s1, s1size = self.closing_par_sentence(sentence, j + 1)
                end = j + s1size + 1

                if end < len(tokens) and tokens[end].lemma == "-rrb-":
                    sub_sentences.append(s1)
                    j = end
                else:
                    sub_sentence.add_token(current)
            else:
                sub_sentence.add_token(current)

            j += 1

        if sub_sentence is not None and not sub_sentence.get_tokens():
            sub_sentences.append(sub_sentence)

        return sub_sentences

    def closing_par_sentence(self, sentence, start):
        sub_sentence = Sentence(sentence.get_id(), [])
        tokens = sentence.get_tokens()

        for j in range(start, len(tokens)):
            current = tokens[j]

            if current.lemma == "-rrb-":
                return sub_sentence
            else:
                sub_sentence.add_token(current)

        return sub_sentence

    def find_lemmas_in_tokens(self, lemmas, tokens):
        lemma_indexes_in_tokens = []
        for i, token in enumerate(tokens):
            if self.lemmas_contain_token(lemmas, token):
                lemma_indexes_in_tokens.append(i)
        return lemma_indexes_in_tokens

    def lemmas_contain_token(self, lemmas, token):
        return self.string_equals_to_any_token(lemmas, token.get_lemma())

    def string_equals_to_any_token(self, tokens, string):
        if string is None:
            return False
        return any(token.lower() == string.lower() for token in tokens)

    def find_sub_sentences(self, sentence, separator_indexes):
        sub_sentences = []
        if not separator_indexes:
            sub_sentences.append(sentence)
        else:
            for i in range(len(separator_indexes) + 1):
                start = 0 if i == 0 else separator_indexes[i - 1] + 1
                end = len(sentence.tokens) if i == len(separator_indexes) else separator_indexes[i]
                if end > start:
                    sub_sentence = Sentence(sentence.id, sentence.tokens[start:end])
                    sub_sentences.append(sub_sentence)
        return sub_sentences

    def sentence_contains_any_lemma_in(self, sentence, lemmas):
        return self.tokens_contain_any_lemma_in(sentence.get_tokens(), lemmas)

    def tokens_contain_any_lemma_in(self, tokens, lemmas):
        return self.find_lemmas_in_tokens(lemmas, tokens) is not None

    def find_obs_behavior_sentence(self, sentences, patterns):
        for i in range(len(sentences) - 1, -1, -1):
            sentence = sentences[i]
            for pm in patterns:
                if pm.match_sentence(sentence) == 1:
                    return i
        return -1

    def is_question(self, sentence):
        tokens = sentence.get_tokens()
        if not tokens:
            return False
        if tokens[-1].get_lemma() == "?":
            return True
        return False


