from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.processor.TextProcessor import TextProcessor

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
import re


class ObsBehaviorLiteralMultiStncePM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        text = TextProcessor.get_string_from_lemmas(sentence)

        # Define regular expressions for matching patterns
        pattern1 = r"^(.* )?(actual|observed|current) (result|behavior|behaviour|description|situation|symptom|log message|output)?([*:\\|\\-+])?.*"
        pattern2 = r"^(.* )?(result|behavior|behaviour|description|situation|symptom|log message|output) (actual|observed|current)([*:\\|\\-+])?.*"
        pattern3 = r"^(.* )?(actual|observed|current) (result|behavior|behaviour|description|situation|symptom|log message|output)([*:\\|\\-+])?.*"
        pattern4 = r"^(.* )?currently the (result|behavior|behaviour|description|situation|symptom|log message|output) of[A-Za-z`' ]+be to([*:\\|\\-+])?.*"

        # Check if the text matches any of the patterns
        if re.match(pattern1, text) or re.match(pattern2, text) or re.match(pattern3, text) or re.match(pattern4, text):
            return 1

        return 0

    