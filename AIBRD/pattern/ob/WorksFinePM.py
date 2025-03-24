from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class WorksFinePM(ObservedBehaviorPatternMatcher):
    WORK_TERMS = {"work", "succeed", "be", "function"}
    FINE_TERMS = {"correctly", "expect", "fine", "flawlessly", "good", "great", "normally", "ok", "perfectly",
                  "properly", "reliably", "well"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        works = self.find_works(tokens)

        if works:
            return 1

        return 0

    def find_works(self, tokens):
        finds = []

        i = 0
        while i < len(tokens):
            current = tokens[i]

            # Look for every "work"
            if (current.general_pos == "VB" or current.general_pos == "NN") and SentenceUtils.lemmas_contain_token(self.WORK_TERMS, current):

                if i - 1 >= 0:
                    previous = tokens[i - 1]
                    # The one preceded by a "do"
                    # case: "it does work..."
                    if previous.general_pos == "VB" and previous.lemma == "do":
                        finds.append(i)
                        break
                    else:
                        # the one that is not preceded by a "not"
                        # ignore cases like: "it does not work"
                        if previous.lemma == "not":
                            break

                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    # The one that precedes a "fine" term
                    # case: "it works fine"
                    if SentenceUtils.lemmas_contain_token(self.WORK_TERMS, next_token):
                        finds.append(i)
                    else:
                        # case: "it works just fine"
                        if next_token.general_pos == "RB" and i + 2 < len(tokens) and SentenceUtils.lemmas_contain_token(self.WORK_TERMS, tokens[i + 2]):
                            finds.append(i)
                        # The one that precedes an "as [fine term]"
                        # case: "work as expected"
                        elif next_token.lemma == "as" and i + 2 < len(tokens):
                            next2 = tokens[i + 2]
                            if SentenceUtils.lemmas_contain_token(self.WORK_TERMS, next2):
                                finds.append(i)
                        # The one that precedes a preposition
                        # case: "it works to something"
                        elif next_token.general_pos == "TO":
                            finds.append(i)
                        # The one that ends a sentence
                        # case: "it works!"
                        elif next_token.lemma.match("[^A-Za-z ]{1}"):
                            finds.append(i)
                else:
                    # case: "it works"
                    if i == len(tokens) - 1:
                        finds.append(i)

            i += 1

        return finds

