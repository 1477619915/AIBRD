from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
import re


class NonTermPM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()

        if self.contains_non_term(tokens) and not self.is_eb_modal(tokens) and not self.contains_would(tokens):
            return 1
        return 0

    def contains_would(self, tokens):
        for i in range(len(tokens)):
            current = tokens[i]
            if current.general_pos == "MD" and current.lemma == "would":
                return True
            elif current.general_pos == "NN" and current.lemma == "d" and i - 1 >= 0:
                previous = tokens[i - 1]
                if previous.general_pos == "NN" or previous.general_pos == "PRP":
                    return True
        return False

    def contains_non_term(self, tokens):
        for current in tokens:
            if (current.general_pos == "NN" or current.general_pos == "JJ") and \
                    re.match(r'non([-])?[a-z]+', current.lemma) and current.lemma != "none":
                return True
            elif current.general_pos == "JJ" and current.lemma == "non":
                return True
        return False


