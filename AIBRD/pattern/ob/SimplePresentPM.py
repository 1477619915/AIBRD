from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SimpleTenseChecker import SimpleTenseChecker
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
from pattern.ob.PassiveVoicePM import PassiveVoicePM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM


class SimplePresentPM(ObservedBehaviorPatternMatcher):

    NEGATIVE_PMS = [NegativeAuxVerbPM(), NegativeVerbPM(), NoLongerPM(), VerbErrorPM(),
                    VerbToBeNegativePM(), NegativeAdjOrAdvPM(), UnableToPM(), VerbNoPM(),
                    ProblemInPM(), NoNounPM(), ErrorTermSubjectPM(), ErrorNounPhrasePM(),
                    NoLongerPM(), PassiveVoicePM()]

    FORBIDDEN_TERMS = {"if", "upon", "when", "whenever", "whereas", "although", "but", "however", "nevertheless", "though", "yet","while", "after", "because"}

    def match_sentence(self, sentence):
        sub_sentences = SentenceUtils.break_by_parenthesis(sentence)

        for sub_sentence in sub_sentences:
            checker = SimpleTenseChecker.create_present_checker_pronouns_and_nouns(None)
            num_clauses = checker.count_num_clauses(sub_sentence)

            if num_clauses > 0 and not self.is_negative(sub_sentence) and not SentenceUtils.sentence_contains_any_lemma_in(
                    sub_sentence, self.FORBIDDEN_TERMS):
                return 1

        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)


