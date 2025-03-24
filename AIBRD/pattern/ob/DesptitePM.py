from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class DesptitePM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        index = self.adverb_index(tokens)

        if index > 0:
            t1 = tokens[:index]
            t2 = tokens[index:]
            first = False

            for token in t1:
                if token.get_general_pos() == "VB":
                    first = True

            if not first:
                for token in t2:
                    if token.get_general_pos() == "VB":
                        first = True
            else:
                return 1

        elif index == 0:
            for token in tokens:
                if token.get_general_pos() == "VB":
                    return 1

        return 0

    def adverb_index(self, tokens):
        for i in range(len(tokens)):
            if tokens[i].get_lemma() in ["although", "despite"]:
                return i
            elif i + 1 < len(tokens) and tokens[i].get_lemma() == "even" and tokens[i + 1].get_lemma() in ["if",
                                                                                                           "though",
                                                                                                           "after",
                                                                                                           "when"]:
                return i
            elif i + 2 < len(tokens) and tokens[i].get_lemma() == "in" and tokens[i + 1].get_lemma() == "spite" and \
                    tokens[i + 2].get_lemma() == "of":
                return i
        return -1

