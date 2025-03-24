from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.NoNounPM import NoNounPM
from pattern.ob.ProblemInPM import ProblemInPM


class ErrorCondPM(ObservedBehaviorPatternMatcher):
    NEGATIVE_PMS = [ProblemInPM(), NoNounPM(), ErrorNounPhrasePM()]

    def match_sentence(self, sentence):
        for ss in SentenceUtils.break_by_parenthesis(sentence):
            tokens = ss.get_tokens()
            cond_indexes = SentenceUtils.find_lemmas_in_tokens(self.CONDITIONAL_TERMS, tokens)
            if cond_indexes:
                for cond_index in cond_indexes:
                    if cond_index > 0 and cond_index < len(tokens) - 1:
                        error_clause = Sentence(ss.get_id(), tokens[:cond_index])
                        if self.is_negative(error_clause):
                            return 1
        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)
