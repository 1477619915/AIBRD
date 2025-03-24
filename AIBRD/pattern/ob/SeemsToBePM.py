from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class SeemsToBePM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        txt = TextProcessor.get_string_from_lemmas(sentence)
        if re.match(r".*(appear|seem|look)(ed|s|ing)? to (not )?be.*", txt):
            return 1

        return 0
