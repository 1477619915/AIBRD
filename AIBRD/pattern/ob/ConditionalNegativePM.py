from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.ButNegativePM import ButNegativePM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ConditionalNegativePM(ObservedBehaviorPatternMatcher):
    PUNCTUATION = {",", "_"}

    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()
        conditional_indexes = SentenceUtils.find_lemmas_in_tokens(self.CONDITIONAL_TERMS, tokens)

        # 没有条件语句
        if not conditional_indexes:
            return 0

        # 根据条件语句拆分句子
        sub_sentences = SentenceUtils.find_sub_sentences(sentence, conditional_indexes)

        # 如果条件语句前有句子，则跳过它 -> 关注的是条件后的内容
        start_index = 1 if conditional_indexes[0] > 0 else 0
        for i in range(start_index, len(sub_sentences)):
            sub_sentence = sub_sentences[i]
            sub_sentence_tokens = sub_sentence.tokens

            # 查找子句中的标点符号
            punct = SentenceUtils.find_lemmas_in_tokens(self.PUNCTUATION, sub_sentence_tokens)

            # 困难情况：没有标点符号。尝试从后往前查找子句。检查否定句之前是否有内容。
            if not punct:
                is_negative = False
                for j in range(len(sub_sentence_tokens) - 1, 0, -1):
                    neg_sent = Sentence(sub_sentence.get_id(), sub_sentence_tokens[j:])

                    if self.is_negative(neg_sent):
                        is_negative = True
                        break

                if is_negative and len(sub_sentence_tokens) > 1 and self.find_verbs(sub_sentence_tokens):
                    return 1

            # 简单情况：有标点符号（',', '_', '-'）。确保条件语句和标点符号之间有内容，并且标点符号之后有否定句。
            else:
                sub_sub_sentences = SentenceUtils.find_sub_sentences(sub_sentence, punct)
                if sub_sub_sentences and sub_sub_sentences[0].tokens:
                    for j in range(1, len(sub_sub_sentences)):
                        if self.is_negative(sub_sub_sentences[j]):
                            return 1

        # 如果至少有一个条件语句，并且没有子句为负面句
        return 0

    def is_negative(self, sentence):
        pattern = self.find_first_pattern_that_matches(sentence, ButNegativePM.NEGATIVE_PMS)
        return pattern is not None

    def find_verbs(self, tokens):
        verbs = []
        contains_aux = False
        for i in range(len(tokens) - 1):
            token = tokens[i]
            add = True
            if token.general_pos == "VB":
                if i == 0:
                    add = False
                elif token.lemma in ["be", "have"] and token.pos != "VB":
                    contains_aux = True
                elif (token.pos in ["VBG", "VBN"]) and contains_aux:
                    add = False
                elif i - 1 >= 0 and tokens[i - 1].word.lower() == "to" and token.pos == "VB":
                    add = False
                if add:
                    verbs.append(i)
        return verbs

