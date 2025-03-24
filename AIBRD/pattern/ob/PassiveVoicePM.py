import self as self

from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.NoLongerPM import NoLongerPM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.NoNounPM import NoNounPM
from pattern.ob.ErrorTermSubjectPM import ErrorTermSubjectPM
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class PassiveVoicePM(ObservedBehaviorPatternMatcher):
    AUXILIARS = {"be", "get"}

    # 定义观察行为模式匹配器列表
    NEGATIVE_PMS = [
        NegativeAuxVerbPM(),
        NegativeVerbPM(),
        NoLongerPM(),
        VerbErrorPM(),
        VerbToBeNegativePM(),
        NegativeAdjOrAdvPM(),
        UnableToPM(),
        VerbNoPM(),
        ProblemInPM(),
        NoNounPM(),
        ErrorTermSubjectPM(),
        ErrorNounPhrasePM(),
    ]

    # 创建禁止词汇集合
    FORBIDDEN_TERMS = self.CONDITIONAL_TERMS
    FORBIDDEN_TERMS.update(self.CONTRAST_TERMS)
    FORBIDDEN_TERMS.update(["after", "because"])  # 添加额外的词汇

    # 创建标点符号词汇集合
    PUNCTUATION = {";", "-", "_", "--"}

    def match_sentence(self, sentence):
        sub_sentences = SentenceUtils.break_by_parenthesis(sentence)

        for sub_sentence in sub_sentences:
            clauses = SentenceUtils.extract_clauses(sub_sentence)

            for clause in clauses:
                tokens = clause.get_tokens()

                if self.is_passive(tokens) and not self.is_eb_modal(tokens) and not self.is_negative(clause) \
                        and not SentenceUtils.sentence_contains_any_lemma_in(clause, self.FORBIDDEN_TERMS):
                    return 1

        return 0

    def is_passive(self, tokens):
        i = 0
        contains_auxiliar = False
        par = 0
        while i < len(tokens):
            current = tokens[i]
            if current.general_pos == "VB" and SentenceUtils.lemmas_contain_token(self.AUXILIARS, current) and par == 0:
                contains_auxiliar = True
                i += 1
                break
            elif current.lemma == "-lrb-":
                par += 1
            elif current.lemma == "-rrb-":
                par -= 1
            i += 1
        while contains_auxiliar and i < len(tokens):
            current = tokens[i]
            if (current.pos == "VBN" or current.pos == "VBD") and par == 0:
                return True
            elif SentenceUtils.lemmas_contain_token(self.PUNCTUATION, current):
                return False
            elif current.lemma == "-lrb-":
                par += 1
            elif current.lemma == "-rrb-":
                par -= 1
            i += 1
        return False

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)


