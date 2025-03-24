from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.NegativeAfterPM import NegativeAfterPM


class PositiveConditionPM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        conditional_term_positions = self.find_conditionals(tokens)

        if conditional_term_positions is not None and len(conditional_term_positions) > 0:
            # There is a conditional expression, now check that the first part is not EB.
            for ctp in conditional_term_positions:
                if ctp > 0:
                    sentence2 = Sentence(sentence.get_id(), tokens[:ctp])
                    tok2 = sentence2.get_tokens()
                    if not self.is_eb_modal(tok2) and not self.is_negative(sentence2):
                        return 1
        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, NegativeAfterPM.NEGATIVE_PMS)

    def find_conditionals(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.CONDITIONAL_TERMS, tokens)
