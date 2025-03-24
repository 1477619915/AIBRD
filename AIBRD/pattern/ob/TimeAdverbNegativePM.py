from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ButNegativePM import ButNegativePM
from pattern.processor.TextProcessor import TextProcessor
import re


class TimeAdverbNegativePM(ObservedBehaviorPatternMatcher):
    TIME_ADVERBS = {"currently", "again", "now"}

    FIRST_POS_TIME_ADVERBS = {"then", "now", "again"}

    ADVERBIAL_TIME_CLAUSES = r"(as soon as|right now|once again|for the moment|up to now|as it stand|for a brief moment|for a moment|in this moment|every time)"

    def match_sentence(self, sentence):
        sub_sentences = SentenceUtils.break_by_parenthesis(sentence)

        for sub_sentence in sub_sentences:
            tokens = sub_sentence.get_tokens()

            if not tokens:
                continue

            if SentenceUtils.lemmas_contain_token(self.FIRST_POS_TIME_ADVERBS, tokens[0]) \
                    or SentenceUtils.sentence_contains_any_lemma_in(sub_sentence, self.TIME_ADVERBS) \
                    or re.search(self.ADVERBIAL_TIME_CLAUSES, TextProcessor.get_string_from_lemmas(sub_sentence)):

                if self.is_negative(sub_sentence):
                    return 1

        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, ButNegativePM.NEGATIVE_PMS)
