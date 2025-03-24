from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
import re
from pattern.sr.LabeledListPM import LabeledListPM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ActionsInfinitivePM(StepsToReproducePatternMatcher):
    BULLET_POS = {"CD", "LS", "：", "-LRB-", "-RRB-"}
    MISTAGGED_VERBS = {"type"}
    non_letters = re.compile(r"[\.\\d]")

    def match_sentence(self, sentence):
        # 提取不包含列表标记的句子
        tokens_no_bullet = LabeledListPM.get_tokens_no_bullet(sentence)

        if not tokens_no_bullet:
            return 0

        no_bullets_sentence = Sentence("0", tokens_no_bullet)

        clauses = SentenceUtils.extract_clauses(no_bullets_sentence)

        for clause in clauses:
            is_imp = SentenceUtils.is_imperative_sentence(clause, True)
            if is_imp:
                return 1  # 如果包含命令性动词，返回1表示匹配

        return 0  # 如果没有匹配的命令性动词，返回0表示不匹配





