from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ButNegativePM import ButNegativePM
from pattern.ob.TimeAdverbNegativePM import TimeAdverbNegativePM
from pattern.processor.TextProcessor import TextProcessor


class TimeAdverbPositivePM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        sub_sentences = SentenceUtils.break_by_parenthesis(sentence)

        for sub_sentence in sub_sentences:
            tokens = sub_sentence.get_tokens()

            if not tokens:
                continue

            first_token_time_adverb = SentenceUtils.lemmas_contain_token(TimeAdverbNegativePM.FIRST_POS_TIME_ADVERBS,
                                                                         tokens[0])
            contains_time_adverb = SentenceUtils.sentence_contains_any_lemma_in(sub_sentence,
                                                                                TimeAdverbNegativePM.TIME_ADVERBS)
            matches_adverbial_clauses = TextProcessor.get_string_from_lemmas(sub_sentence).match(
                ".*" + TimeAdverbNegativePM.ADVERBIAL_TIME_CLAUSES + ".*")

            if first_token_time_adverb or contains_time_adverb or matches_adverbial_clauses:
                if not self.is_negative(sub_sentence):
                    return 1

        return 0

    def is_negative(self, sentence):
        pm = self.find_first_pattern_that_matches(sentence, ButNegativePM.NEGATIVE_PMS)
        # if pm is not None:
        #     print(pm.__class__.__name__)
        return pm is not None

