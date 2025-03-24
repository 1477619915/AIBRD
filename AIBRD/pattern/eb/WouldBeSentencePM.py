from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class WouldBeSentencePM(ExpectedBehaviorPatternMatcher):
    MODALS = {"would", "might"}

    POSITIVE_ADJECTIVES = {"nice", "great", "super", "useful", "convenient", "ideal", "neat", "better", "helpful",
                           "fine", "cool", "good", "optimal", "fantastic"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()

        modal_tokens = self.find_modal_tokens(tokens)

        for modal in modal_tokens:
            try:
                adv_or_verb_to_be1 = tokens[modal + 1]

                if adv_or_verb_to_be1.lemma == "be":
                    adj_or_adv = tokens[modal + 2]

                    if adj_or_adv.general_pos == "RB":
                        adj = tokens[modal + 3]

                        if adj.pos == "JJ" and SentenceUtils.lemmas_contain_token(self.POSITIVE_ADJECTIVES, adj):
                            return 1
                    elif adj_or_adv.pos == "JJ" and SentenceUtils.lemmas_contain_token(self.POSITIVE_ADJECTIVES, adj_or_adv):
                        return 1
                elif adv_or_verb_to_be1.pos == "RB":
                    adv_or_verb_to_be2 = tokens[modal + 2]
                    if adv_or_verb_to_be2.lemma == "be":
                        adj_or_adv = tokens[modal + 3]
                        if adj_or_adv.pos == "RB":
                            adj = tokens[modal + 4]
                            if adj.pos == "JJ" and SentenceUtils.lemmas_contain_token(self.POSITIVE_ADJECTIVES, adj):
                                return 1
                        elif adj_or_adv.pos == "JJ" and SentenceUtils.lemmas_contain_token(self.POSITIVE_ADJECTIVES, adj_or_adv):
                            return 1

            except IndexError:
                pass

        return 0

    def find_modal_tokens(self, tokens):
        modal_tokens = []
        for i, modal in enumerate(tokens):
            if (modal.pos == "MD" and SentenceUtils.lemmas_contain_token(self.MODALS, modal)) or modal.lemma == "d":
                modal_tokens.append(i)
        return modal_tokens
