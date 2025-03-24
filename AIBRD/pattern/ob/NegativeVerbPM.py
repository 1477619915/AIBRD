from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.NegativeTerms import NegativeTerms
from pattern.processor.TextProcessor import TextProcessor

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class NegativeVerbPM(ObservedBehaviorPatternMatcher):

    OTHER_NEGATIVE_TERMS = {"slow doen", "slow down", "faile",
                            "stucks up", "consume 100", "get turn into", "be out of", "pull out",
                             "faul", "hangs/get", "failes",
                             "timing out", "go away", "jitter", "failing", "be simply go", "be go"}

    def match_sentence(self, sentence):
        clauses_no_parentheses = SentenceUtils.break_by_parenthesis(sentence)
        for clause in clauses_no_parentheses:
            sub_clauses = SentenceUtils.extract_clauses(clause)
            for sub_clause in sub_clauses:
                sub_clause_tokens = sub_clause.get_tokens()
                for i in range(len(sub_clause_tokens)):
                    token = sub_clause_tokens[i]
                    if token.general_pos in {"VB", "NN", "JJ"} and SentenceUtils.lemmas_contain_token(NegativeTerms.VERBS, token):
                        if i - 1 >= 0:
                            prev_token = sub_clause_tokens[i - 1]
                            if not (prev_token.lemma in {"a", "the"}):
                                if i - 2 >= 0:
                                    prev_token2 = sub_clause_tokens[i - 2]
                                    if not (prev_token2.general_pos == "CD" and prev_token.lemma == "." and i - 2 == 0):
                                        return 1
                                else:
                                    if not (prev_token.lemma == "." or prev_token.general_pos == "CD" and i - 1 == 0):
                                        return 1
                        else:
                            if not token.general_pos == "NN":
                                return 1

                txt = TextProcessor.get_string_from_lemmas(sub_clause)

                if any(neg_term in txt for neg_term in self.OTHER_NEGATIVE_TERMS):
                    return 1

        return 0

