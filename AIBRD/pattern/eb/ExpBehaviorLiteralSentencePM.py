from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ExpBehaviorLiteralSentencePM(ExpectedBehaviorPatternMatcher):

    def match_sentence(self, sentence):
        text = TextProcessor.get_string_from_lemmas(sentence)

        regex_prefix = r"(?s)(\W+ )?expect(ed)?( (result|behavio(u)?r))?( (:|-+))"
        b = re.match(regex_prefix + ".+", text)
        if b:
            # check for only "expect behavior", with no text after the label
            b = re.match(regex_prefix, text)
            if b:
                return 0
            else:
                return 1.
        else:
            b = re.match(r"expectation :.+", text)
            if b:
                return 1

            b = re.match(r"(?s)(\W+ )expect(ed)?( (result|behavio(u)?r)) .+", text)
            if b:
                return 1

        return 0
