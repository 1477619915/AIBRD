from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ActionSubject(ObservedBehaviorPatternMatcher):
    VERBS_AS_NOUNS = {"copy", "drag", "insert"}

    PUNCTUATION = {":", ";", "."}

    def match_sentence(self, sentence):
        sub_sentences = SentenceUtils.find_sub_sentences(sentence, self.find_punctuation(sentence.get_tokens()))

        for sub_sentence in sub_sentences:
            tokens = sub_sentence.get_tokens()
            first = tokens[0]
            if first.get_pos() == "VBG" or (
                    first.get_word().lower().endswith("ing") and first.get_general_pos() == "NN"):
                for i in range(1, len(tokens)):
                    token = tokens[i]
                    if token.get_general_pos() == "VB":
                        return 1
                    elif token.get_general_pos() == "NN" and SentenceUtils.lemmas_contain_token(self.VERBS_AS_NOUNS, token):
                        return 1
        return 0

    def find_punctuation(self, tokens):
        symbols = SentenceUtils.find_lemmas_in_tokens(self.PUNCTUATION, tokens)
        if symbols and symbols[-1] == len(tokens) - 1:
            return symbols[:-1]
        return symbols

