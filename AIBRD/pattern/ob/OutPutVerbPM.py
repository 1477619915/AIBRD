from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class OutPutVerbPM(ObservedBehaviorPatternMatcher):
    OUTPUT_VERBS = {"output", "display", "show", "return", "report", "pop"}

    def match_sentence(self, sentence):
        tokens = sentence.tokens
        verbs = self.get_verbs(tokens)

        for verb_idx in verbs:
            verb_token = tokens[verb_idx]

            if verb_token.general_pos == "VB":
                return 1
            else:
                if 0 <= verb_idx - 1 < len(tokens) and 0 <= verb_idx + 1 < len(tokens):
                    prev_token = tokens[verb_idx - 1]
                    next_token = tokens[verb_idx + 1]

                    # no surrounding verbs
                    if not (prev_token.general_pos == "VB" or next_token.general_pos == "VB") and \
                            not prev_token.general_pos == "DT" and \
                            not SentenceUtils.lemmas_contain_token(self.OUTPUT_VERBS, prev_token) and \
                            not SentenceUtils.lemmas_contain_token(self.OUTPUT_VERBS, next_token):

                        # avoid "is not output"
                        if 0 <= verb_idx - 2 < len(tokens):
                            prev_token2 = tokens[verb_idx - 2]
                            if not (prev_token2.lemma == "be" or prev_token.lemma == "not"):
                                return 1
                        else:
                            return 1

        return 0

    def get_verbs(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.OUTPUT_VERBS, tokens)
