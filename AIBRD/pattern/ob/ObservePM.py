from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ObservePM(ObservedBehaviorPatternMatcher):
    OBSERVE = {"observe"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        observes = self.find_observe(tokens)

        if observes is not None:
            return 1

        return 0

    def find_observe(self, tokens):
        observe = []

        for i in range(len(tokens)):
            current = tokens[i]

            # Look for every "observe"
            if current.general_pos == "VB" and current.lemma == self.OBSERVE:

                # The right "observe"
                if current.pos in ["VBP", "VB", "VBD", "VBN"]:

                    # the one in the first position
                    if i == 0:
                        observe.append(i)
                    # the one followed by ":" or "that"
                    elif i + 1 < len(tokens) and (tokens[i + 1].lemma == ":" or tokens[i + 1].lemma == "that"):
                        observe.append(i)
                    # the one preceded by an item marker, cardinal number, or pronoun
                    elif i - 1 >= 0 and (tokens[i - 1].general_pos in ["LS", "CD", "PRP"]):
                        observe.append(i)

        return observe
