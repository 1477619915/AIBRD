from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class HappensPM(ObservedBehaviorPatternMatcher):
    VERBS = {"happen", "occur"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        verbs = self.found_index_tokens(tokens)
        if len(verbs) > 0:
            return 1
        return 0

    def find_index_tokens(self, tokens):
        index_conditional_terms = []
        for i, token in enumerate(tokens):
            if SentenceUtils.lemmas_contain_token(self.VERBS, token) and token.general_pos == "VB":
                index_conditional_terms.append(i)

        return index_conditional_terms

