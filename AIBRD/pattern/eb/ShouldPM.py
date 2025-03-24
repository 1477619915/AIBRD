from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ShouldPM(ExpectedBehaviorPatternMatcher):
    MODAL_TERMS = {"should", "shall"}

    def match_sentence(self, sentence):
        # 提取从句
        clauses = SentenceUtils.extract_clauses(sentence)

        num_valid_clauses = 0
        for clause in clauses:
            tokens = clause.get_tokens()

            # 查找情态动词
            idxs = SentenceUtils.find_lemmas_in_tokens(self.MODAL_TERMS, tokens)
            if not idxs:
                continue

            # 情态动词前没有负面助动词子句
            first_idx = idxs[0]
            pm = NegativeAuxVerbPM()
            match_sentence = pm.match_sentence(Sentence(clause.get_id(), tokens[:first_idx]))
            if match_sentence == 1:
                continue

            # 没有 "should be done"
            if first_idx + 2 < len(tokens):
                next_token1 = tokens[first_idx + 1]
                next_token2 = tokens[first_idx + 2]

                if next_token1.get_lemma() == "be" and next_token2.get_lemma() == "do":
                    continue

            num_valid_clauses += 1

        if num_valid_clauses > 0:
            return 1

        return 0
