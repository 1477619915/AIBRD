from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.ErrorTermSubjectPM import ErrorTermSubjectPM
from pattern.ob.LeadsToNegativePM import LeadsToNegativePM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.NoLongerPM import NoLongerPM
from pattern.ob.NoNounPM import NoNounPM
from pattern.ob.NounNotPM import NounNotPM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM


class NegativeAfterPM(ObservedBehaviorPatternMatcher):
    NEGATIVE_PMS = [NegativeAuxVerbPM(), NegativeVerbPM(), NoLongerPM(), VerbErrorPM(), VerbToBeNegativePM(),
                    NegativeAdjOrAdvPM(), UnableToPM(), VerbNoPM(), ProblemInPM(), LeadsToNegativePM(),
                    ErrorNounPhrasePM(), ErrorTermSubjectPM(), NoNounPM(), NounNotPM(),
                    VerbToBeNegativePM(), VerbNoPM()]

    AFTER = {"after"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()

        for after_index in self.find_afters(tokens):
            if after_index != -1 and after_index > 0:
                first = Sentence(sentence.get_id(), tokens[:after_index])
                tokens_first = first.get_tokens()

                if not self.is_eb_modal(tokens_first):
                    if self.is_negative(first):
                        return 1
        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)

    def find_afters(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.AFTER, tokens)

