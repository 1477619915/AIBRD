from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
import re


class ObsBehaviorLiteralStncePM(ObservedBehaviorPatternMatcher):

    def match_sentence(self, sentence):
        text = " ".join(sentence.lemmas)

        # Define the regular expressions
        patterns = [
            r"(?s)[^a-z]*((actual|observed|current) )((result|behavior|description|situation) )?([:\\|\\-+]).*",
            r"(?s)[^a-z]*((actual|observed|current) )?((result|behavior|description|situation) )([:\\|\\-+]).*",
            r"(?s)[^a-z]*((actual|observed|current) )((result|behavior|description|situation) )([:\\|\\-+])?.*"
        ]

        # Check if any pattern matches
        for pattern in patterns:
            if re.match(pattern, text):
                return 1

        return 0
