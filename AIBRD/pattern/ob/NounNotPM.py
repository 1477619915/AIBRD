from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class NounNotPM(ObservedBehaviorPatternMatcher):
    NOT = {"not"}

    def match_sentence(self, sentence):
        tokens2 = sentence.get_tokens()
        not_tokens = self.find_nots(tokens2)

        for not_tok in not_tokens:
            if not_tok - 1 >= 0:
                noun_token = self.get_noun_token(tokens2, not_tok)
                if noun_token is None:
                    continue

                if not_tok + 1 < len(tokens2):
                    next_idx = self.get_next_valid_token(tokens2, not_tok + 1)

                    if next_idx != -1:
                        token = tokens2[next_idx]

                        if token.get_general_pos() == "JJ" or token.get_pos() == "VBG" or token.get_pos() == "VBN" or token.get_pos() == "VBD" or token.get_pos() == "VB":
                            return 1
                        else:
                            next_next_idx = self.get_next_valid_token(tokens2, next_idx + 1)
                            if next_next_idx != -1:
                                token2 = tokens2[next_next_idx]
                                if token.get_general_pos() == "RB":
                                    if token2.get_general_pos() == "JJ" or token2.get_pos() == "VBG" or token2.get_pos() == "VBN" or token2.get_pos() == "VBD" or token2.get_pos() == "VB":
                                        return 1
                                elif token.get_pos() == "VB":
                                    if token2.get_general_pos() == "RB":
                                        return 1
        return 0

    def get_next_valid_token(self, tokens, ini):
        for i in range(ini, len(tokens)):
            if tokens[i].get_lemma().isalpha():
                return i
        return -1

    def get_noun_token(self, tokens, not_tok):
        for i in range(not_tok - 1, -1, -1):
            token = tokens[i]
            if token.get_general_pos() == "NN":
                return token
            elif not token.get_lemma().isalpha():
                return None
        return None

    def find_nots(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.NOT, tokens)

