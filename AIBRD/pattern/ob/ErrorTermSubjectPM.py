from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ErrorTermSubjectPM(ObservedBehaviorPatternMatcher):

    NEGATIVE_PMS = [ProblemInPM(), ErrorNounPhrasePM()]

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()

        verb_indexes = self.find_verbs(tokens)

        # 如果没有动词，无法匹配 S_OB_ERROR_AS_SUBJECT
        if not verb_indexes:
            return 0

        sub_sentences = SentenceUtils.find_sub_sentences(sentence, verb_indexes)

        # 如果最后一个动词之后还有内容，我们忽略它
        end = len(sub_sentences) if verb_indexes[-1] == len(tokens) - 1 else len(sub_sentences) - 1
        for i in range(end):
            sub_sentence = sub_sentences[i]
            if self.is_negative(sub_sentence):
                return 1

        return 0

    def find_verbs(self, tokens):
        verbs = []
        for i in range(len(tokens)):
            token = tokens[i]

            if token.get_general_pos() == "VB":
                verb_idx = i
                add = True
                # 忽略句子开头的动词
                if i == 0:
                    add = False
                else:
                    # 检查错误标记的动词堆栈，当句子中出现 "stack trace" 时
                    if token.get_lemma() == "stack":
                        if i + 1 < len(tokens) and tokens[i + 1].get_lemma() == "trace":
                            add = False
                    # 忽略在介词或限定词之后出现的动词
                    if i - 1 >= 0:
                        prev_token = tokens[i - 1]

                        if prev_token.get_lemma() == "to":
                            verb_idx = i - 1
                        elif SentenceUtils.lemmas_contain_token(ProblemInPM.PREP_TERMS,
                                                                prev_token) or prev_token.get_general_pos() == "DT":
                            add = False

                if add:
                    verbs.append(verb_idx)
        return verbs

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)

