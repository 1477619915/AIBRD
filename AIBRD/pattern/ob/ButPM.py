from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ButNegativePM import ButNegativePM
from pattern.ob.WorksButPM import WorksButPM


class ButPM(ObservedBehaviorPatternMatcher):
    PUNCTUATION = {";", "--"}

    def match_sentence(self, sentence):
        sub_sentences = SentenceUtils.find_sub_sentences(sentence, self.find_punctuation(sentence.tokens))

        for sub_sentence in sub_sentences:
            sub_tokens = sub_sentence.tokens
            buts = SentenceUtils.find_lemmas_in_tokens(self.CONTRAST_TERMS, sub_tokens)

            pmw = WorksButPM()
            match1 = pmw.match_sentence(sub_sentence)
            if match1 == 0:
                for but in buts:
                    sentence2 = Sentence(sub_sentence.id, sub_tokens[but + 1:])
                    if not self.is_negative(sentence2):
                        return 1

        return 0

    def find_punctuation(self, tokens):
        symbols = SentenceUtils.find_lemmas_in_tokens(self.PUNCTUATION, tokens)
        if symbols and symbols[-1] == len(tokens) - 1:
            return symbols[:-1]
        return symbols

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, ButNegativePM.NEGATIVE_PMS)

