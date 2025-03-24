from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.ErrorTermSubjectPM import ErrorTermSubjectPM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.NoLongerPM import NoLongerPM
from pattern.ob.NoNounPM import NoNounPM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM


class AfterNegativePM(ObservedBehaviorPatternMatcher):
    NEGATIVE_PMS = [
        NegativeAuxVerbPM(),
        NegativeVerbPM(),
        NoLongerPM(),
        VerbErrorPM(),
        VerbToBeNegativePM(),
        NegativeAdjOrAdvPM(),
        UnableToPM(),
        VerbNoPM(),
        ProblemInPM(),
        NoNounPM(),
        ErrorTermSubjectPM(),
        ErrorNounPhrasePM()
    ]

    AFTER = {"after"}

    PUNCTUATION = {",", "_", "-"}

    def match_sentence(self, sentence):
        super_sentences = SentenceUtils.break_by_parenthesis(sentence)

        for super_sentence in super_sentences:
            afters = SentenceUtils.find_lemmas_in_tokens(self.AFTER, super_sentence.get_tokens())

            # No "after" found
            if not afters:
                continue

            # Split sentences based on "after"
            sub_sentences = SentenceUtils.find_sub_sentences(super_sentence, afters)

            # If there's a sentence before the "after" term, skip it. The focus is on what's after "after."
            for i in range(1, len(sub_sentences)) if afters[0] > 0 else range(len(sub_sentences)):
                sub_sentence = sub_sentences[i]
                punctuation = self.find_punctuation(sub_sentence.get_tokens())

                # Hard case: No punctuation. Try subsentences from end to beginning and check if there's something before the negative sentence.
                if not punctuation:
                    for j in range(len(sub_sentence.get_tokens()) - 1, -1, -1):
                        neg_sent = Sentence(sub_sentence.get_id(), sub_sentence.get_tokens()[j:])
                        if self.is_negative(neg_sent) and j > 1:
                            return 1
                # Easy case: There is punctuation (',', '_', '-'). Make sure there's something between "after" and the punctuation, and check for a negative sentence after the punctuation.
                else:
                    sub_sub_sentences = SentenceUtils.find_sub_sentences(sub_sentence, punctuation)
                    if sub_sub_sentences[0].get_tokens():
                        for j in range(1, len(sub_sub_sentences)):
                            sentence2 = sub_sub_sentences[j]
                            if self.is_negative(sentence2):
                                return 1

        return 0

    def is_negative(self, sentence):
        pattern = self.find_first_pattern_that_matches(sentence, self.NEGATIVE_PMS)
        # debugging messages
        # if pattern is not None:
        #     print("match:", pattern.__class__.__name__)
        return pattern is not None

    def find_punctuation(self, tokens):
        symbols = [i for i, token in enumerate(tokens) if token in self.PUNCTUATION]

        # Avoid the symbol if it is located at the end of the list of tokens
        if symbols and symbols[-1] == len(tokens) - 1:
            return symbols[:-1]

        return symbols


