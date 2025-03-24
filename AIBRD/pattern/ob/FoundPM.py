from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class FoundPM(ObservedBehaviorPatternMatcher):
    FIND_TERMS = {"find", "discover"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        finds = self.find_finds(tokens)

        if finds is not None:
            return 1

        return 0

    def find_finds(self, tokens):
        finds = []

        for i in range(len(tokens)):
            current = tokens[i]

            # Look for every "find"
            if current.general_pos == "VB" and SentenceUtils.lemmas_contain_token(self.FIND_TERMS, current):

                # The right "find"
                if i - 1 >= 0:
                    previous = tokens[i - 1]

                    # The one preceded by pronoun
                    if (current.pos in ["VBD", "VBP", "VBN"] and
                            (previous.general_pos == "PRP" or previous.word.lower() == "i")):
                        finds.append(i)
                    # The one preceded by a verb that is in turn preceded by a pronoun
                    elif previous.general_pos == "VB" and i - 2 >= 0:
                        if tokens[i - 2].general_pos == "PRP":
                            finds.append(i)
                    # The one preceded by a conjunction that is in turn preceded by a pronoun
                    elif previous.general_pos == "CC":
                        for j in range(i - 2, -1, -1):
                            if tokens[j].general_pos == "PRP":
                                finds.append(i)

        return finds
