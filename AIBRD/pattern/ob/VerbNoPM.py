from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class VerbNoPM(ObservedBehaviorPatternMatcher):
    NEGATIVE_TERMS = {"no", "nothing"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        verbs = self.find_verbs(tokens)

        for verb in verbs:
            for i in range(verb + 1, verb + 5):
                if i < len(tokens):
                    next_token = tokens[i]
                    if next_token.get_lemma() in self.NEGATIVE_TERMS:
                        return 1

        return 0

    def find_verbs(self, tokens):
        verbs = []
        for i, token in enumerate(tokens):
            if token.get_general_pos() == "VB" or token.get_lemma() in SentenceUtils.UNDETECTED_VERBS:
                verbs.append(i)
        return verbs
