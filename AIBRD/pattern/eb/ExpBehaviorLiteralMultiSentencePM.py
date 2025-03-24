from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ExpBehaviorLiteralMultiSentencePM(ExpectedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        text = TextProcessor.get_string_from_lemmas(sentence)
        if re.match(r"(?s)(\W+ )?expect(ed)? ((result|behavio(u)?r) ?)?(:|-+|\W+)?$", text):
            return 1
        elif re.match(r"(?s)(\W+ )?describe the result you expect( (:|-+|\W+))?$", text):
            return 1
        elif re.match(r"^expect( log)? message$", text):
            return 1
        elif re.match(r"^expect , in both case : .+", text):
            return 1

        return 0

