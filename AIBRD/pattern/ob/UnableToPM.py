from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.processor.TextProcessor import TextProcessor
from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class UnableToPM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        txt = TextProcessor.get_string_from_lemmas(sentence)
        if "unable to" in txt or "not be able to" in txt or "not able to" in txt:
            return 1

        return 0
