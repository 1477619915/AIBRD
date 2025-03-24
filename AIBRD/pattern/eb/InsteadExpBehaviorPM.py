from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class InsteadExpBehaviorPM(ExpectedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        # no questions
        if SentenceUtils.is_question(sentence):
            return 0

        txt = TextProcessor.get_string_from_lemmas(sentence)
        if re.match(r".+(instead of|rather than|in lieu of).+", txt):
            return 1

        return 0
