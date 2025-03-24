from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.SeemsToBePM import SeemsToBePM
from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class SeemsPM(ObservedBehaviorPatternMatcher):
    SEEM_VERBS = {"seem", "appear", "look"}

    OTHER_SEEM = [SeemsToBePM()]

    def match_sentence(self, sentence):
        # Check that is not other seem pattern
        if self.is_other_seem(sentence):
            return 0

        txt = TextProcessor.get_string_from_lemmas(sentence)
        if re.match(r".*(appear|seem|look)(ed|s|ing)? (to|that|like|each|as|none)[^A-Za-z].*", txt):
            return 1

        tokens = sentence.get_tokens()
        terms = self.find_seem_verbs(tokens)

        for term in terms:
            if term + 1 < len(tokens):
                next_token = tokens[term + 1]
                if next_token.get_general_pos() in ["NN", "RB", "JJ", "DT"]:
                    return 1

        return 0

    def is_other_seem(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.OTHER_SEEM)

    def find_seem_verbs(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.SEEM_VERBS, tokens)
