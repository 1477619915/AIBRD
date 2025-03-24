from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ButNegativePM import ButNegativePM


class ConditionalPositivePM(ObservedBehaviorPatternMatcher):
    PUNCTUATION = {",", "_"}

    def match_sentence(self, sentence):
        # Split sentences based on "."
        super_sentences = SentenceUtils.break_by_parenthesis(sentence)

        for super_sentence in super_sentences:
            tokens = super_sentence.get_tokens()
            conditional_indexes = SentenceUtils.find_lemmas_in_tokens(self.CONDITIONAL_TERMS, tokens)

            if not conditional_indexes:

                # Split sentences based on conditionals
                sub_sentences = SentenceUtils.find_sub_sentences(super_sentence, conditional_indexes)

                # If there is a sentence before the conditional term, skip it.
                # The focus is on what is after the conditional.
                start_index = 1 if conditional_indexes[0] > 0 else 0

                for i in range(start_index, len(sub_sentences)):
                    sub_sentence = sub_sentences[i]
                    punctuation = self.find_punctuation(sub_sentence.get_tokens())

                    # Hard case: there is no punctuation.
                    if not punctuation:
                        is_neg = False
                        for j in range(len(sub_sentence.get_tokens()) - 1, 0, -1):
                            neg_sent = Sentence(sub_sentence.get_id(), sub_sentence.get_tokens()[j:])

                            if self.is_negative(neg_sent):
                                is_neg = True
                                break

                        if not is_neg and len(sub_sentence.get_tokens()) > 1 and self.find_verbs(sub_sentence.get_tokens()):
                            return 1

                    # Easy case: there is punctuation (',', '_', '-').
                    else:
                        sub_sub_sentences = SentenceUtils.find_sub_sentences(sub_sentence, punctuation)
                        if sub_sub_sentences[0].get_tokens():
                            is_pos = True
                            for j in range(1, len(sub_sub_sentences)):
                                if self.is_negative(sub_sub_sentences[j]):
                                    is_pos = False
                                    break

                            if is_pos:
                                return 1

        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, ButNegativePM.NEGATIVE_PMS)

    def find_punctuation(self, tokens):
        symbols = SentenceUtils.find_lemmas_in_tokens(self.PUNCTUATION, tokens)

        if symbols and symbols[-1] == len(tokens) - 1:
            return symbols[:-1]

        return symbols

    def find_verbs(self, tokens):
        verbs = []
        contains_aux = False
        for i in range(len(tokens) - 1):
            token = tokens[i]
            add = True
            if token.general_pos == "VB":
                if i == 0:
                    add = False
                elif token.lemma in ["be", "have"] and token.pos != "VB":
                    contains_aux = True
                elif (token.pos in ["VBG", "VBN"]) and contains_aux:
                    add = False
                elif i - 1 >= 0 and tokens[i - 1].word.lower() == "to" and token.pos == "VB":
                    add = False
                if add:
                    verbs.append(i)
        return verbs


