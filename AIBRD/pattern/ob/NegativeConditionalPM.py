from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.ButNegativePM import ButNegativePM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class NegativeConditionalPM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        indexes = self.find_conditionals(tokens)

        if len(indexes) > 0:
            for integer in indexes:
                if integer > 0 and integer < len(tokens) - 1:
                    neg_clause = Sentence(sentence.get_id(), tokens[0:integer])
                    if self.is_negative(neg_clause):
                        return 1

        return 0

    def find_conditionals(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.CONDITIONAL_TERMS, tokens)

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, ButNegativePM.NEGATIVE_PMS)


