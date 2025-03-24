from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.processor.TextProcessor import TextProcessor
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.sr.LabeledListPM import LabeledListPM
from pattern.Utils.SimpleTenseChecker import SimpleTenseCheck


class SimplePastParagraphPM(StepsToReproducePatternMatcher):
    EXCLUDED_VERBS = {"notice"}

    def match_sentence(self, sentence):
        token_no_bullet = LabeledListPM.get_tokens_no_bullet(sentence)
        if token_no_bullet is not None:
            return 0

        num = self.count_num_clauses_in_simple_past(sentence)
        if num > 0:
            return 1

        return 0

    def count_num_clauses_in_simple_past(self, sentence):
        past_checker = SimpleTenseCheck.create_past_checker_only_pronouns(self.EXCLUDED_VERBS)
        return past_checker.count_num_clauses(sentence)



