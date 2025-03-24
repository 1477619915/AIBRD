from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class OnlyPM(ObservedBehaviorPatternMatcher):
    ONLY = "only"

    ALLOWED_PREPS = {"that"}

    PRESENT_TENSE_VERBS = {"crash", "build", "return", "copy"}

    PUNCTUATION = {",", ";", ":", "--"}

    def match_sentence(self, sentence):
        punctuation = self.find_punctuation(sentence.tokens)
        sub_sentences = SentenceUtils.find_sub_sentences(sentence, punctuation)

        for sub_sentence in sub_sentences:
            tokens = sub_sentence.tokens
            if self.contains_only(tokens) and not self.is_eb_modal(tokens):
                return 1
        return 0

    def contains_only(self, tokens):
        for i in range(len(tokens)):
            current = tokens[i]

            # Find every "only"
            if (current.general_pos == "RB" or current.general_pos == "JJ") and current.lemma == self.ONLY:
                # The right "only"
                previous = tokens[i - 1] if i - 1 >= 0 else None
                next_token = tokens[i + 1] if i + 1 < len(tokens) else None

                if previous and previous.general_pos == "IN" and SentenceUtils.lemmas_contain_token(self.ALLOWED_PREPS, previous):
                    continue

                # The one that comes before or after a verb
                if (previous and previous.general_pos == "VB") or (next_token and next_token.general_pos == "VB") or \
                        (SentenceUtils.lemmas_contain_token(self.PRESENT_TENSE_VERBS, previous) and previous.pos == "NNS") or \
                        (SentenceUtils.lemmas_contain_token(self.PRESENT_TENSE_VERBS,next_token) and next_token.pos == "NNS"):
                    return True

                # The one that precedes a verb in infinitive
                if next_token and next_token.general_pos == "TO":
                    after_to = tokens[i + 2] if i + 2 < len(tokens) else None

                    if after_to and after_to.general_pos == "VB":
                        return True

        return False

    def find_punctuation(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.PUNCTUATION, tokens)


