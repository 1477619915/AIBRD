from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class StillSentencePM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        txt = TextProcessor.get_string_from_lemmas(sentence)
        if re.match(r'.*[^a-z]?still .+', txt) or re.match(r'.+ still[^a-z]?.*', txt):
            return 1
        return 0
