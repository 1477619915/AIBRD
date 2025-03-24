from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
import re


class InsteadOfObPM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        txt = TextProcessor.get_string_from_lemmas(sentence)

        if re.search(r'.*[^A-Za-z]?(instead|rather than|in lieu of)[^A-Za-z]?.*', txt):
            return 1

        return 0

