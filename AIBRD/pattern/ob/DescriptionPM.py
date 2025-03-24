from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
import re


class DescriptionPM(ObservedBehaviorPatternMatcher):

    def match_sentence(self, sentence):
        text = TextProcessor.get_string_from_lemmas(sentence)
        patterns = [
            r"^[^a-z]*description[ ]?:.*",
            r"[^a-z]*problem description[ ]?:.*",
            r"[^a-z]*description of (the )?problem[ ]?:.*",
            r"[^a-z]*describe the result you receive[ ]?:.*"
        ]

        for pattern in patterns:
            if re.match(pattern, text):
                return 1
        
        return 0