from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class NoNounPM(ObservedBehaviorPatternMatcher):
    NO_TERMS = {"no", "nothing", "none", "neither"}

    POST_NO_TERMS = {"NN", "VB", "DT", "MD", "IN", "JJ", "RP", "WH", "``"}

    PRE_NO_POS = {"VB"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()

        start = 0
        while start < len(tokens):
            current = tokens[start]
            previous_gen_pos = "OK" if start == 0 else tokens[start - 1].get_general_pos()

            # 如果在 NO_TERMS 前有动词，则匹配模式为 S_OB_VERB_NO
            if current.get_lemma() in self.NO_TERMS and previous_gen_pos not in self.PRE_NO_POS:
                return self.match_sub_sentence(Sentence(sentence.get_id(), tokens[start:]))

            start += 1

        return 0

    def match_sub_sentence(self, sentence):
        tokens = sentence.get_tokens()
        if len(tokens) > 2:
            if tokens[0].get_lemma() in self.NO_TERMS:
                next_token = tokens[1]
                # 检查句子是否不是 S_OB_NO_LONGER
                if tokens[0].get_word().lower() == "no" and next_token.get_word().lower() == "longer":
                    return 0
                elif any(next_token.get_general_pos() == t for t in self.POST_NO_TERMS):
                    return 1

        return 0

