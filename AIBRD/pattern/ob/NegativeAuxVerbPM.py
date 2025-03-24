from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class NegativeAuxVerbPM(ObservedBehaviorPatternMatcher):

    ADDITIONAL_AUX_VERBS = {"didnt", "doesn t", "doen t", "dosent", "haven t", "dont",
                            "cant", "cannote", "don t", "s not", "can t", "wont", "isn t",
                            "isnt", "aren t", "ca not", "has no",
                            "have no", "didn t", "dose not"}
    POS_LEMMAS = {"MD-can", "VB-do", "VB-be", "MD-would", "VB-have", "MD-will", "MD-could", "MD-may"}

    def match_sentence(self, tokens):
        nots = self.find_nots(tokens)

        for not_index in nots:
            # No previous token
            if not_index - 1 < 0:
                continue

            previous_token = tokens[not_index - 1]
            # Regular case: "the user is not..."
            if self.is_auxiliary_token(previous_token):
                if not_index - 3 < 0:
                    return 1

                # Avoid: when you do not
                prev_token2 = tokens[not_index - 2]
                prev_token3 = tokens[not_index - 3]
                if not (SentenceUtils.match_terms_by_lemma(self.CONDITIONAL_TERMS, prev_token3) and prev_token2.general_pos == "PRP"):
                    return 1
            # Case: "the user is maybe not..."
            elif not_index - 2 >= 0 and previous_token.general_pos == "RB" and self.is_auxiliary_token(
                    tokens[not_index - 2]):
                return 1
            else:
                # Case: the user is ... and (hence also) not ...
                # The "hence also" is optional
                # Basically, we accept a lot of RBs preceding the not and then an "and"
                # The following condition checks for no previous "not"s
                if not_index == 0:
                    # Find the "and" preceding the RBs (if any)
                    and_index = -1
                    all_are_tokens_rb = True
                    for j in range(not_index - 1, -1, -1):
                        current_token = tokens[j]
                        if all_are_tokens_rb and current_token.general_pos == "CC" and current_token.lemma == "and":
                            and_index = j
                            break
                        elif not current_token.general_pos == "RB":
                            all_are_tokens_rb = False
                            break

                    if and_index != -1 and and_index - 1 > 0:
                        sub_sentence_tokens = tokens[:and_index - 1]
                        # Any auxiliary verb?
                        there_is_aux_token = any(self.is_auxiliary_token(tok) for tok in sub_sentence_tokens)
                        if there_is_aux_token:
                            return 1

                # Case: "the user is making [subject] not... "
                if not_index - 3 >= 0:
                    previous_token2 = tokens[not_index - 2]
                    previous_token3 = tokens[not_index - 3]
                    if self.is_auxiliary_token(
                            previous_token3) and previous_token2.pos == "VBG" and previous_token2.lemma == "make" and (
                            previous_token.general_pos == "NN" or previous_token.general_pos == "PRP"):
                        return 1

        # Find misspelled cases
        if self.find_additional_aux_verbs(tokens):
            return 1

        return 0

    # 返回tokens中包含的not相关的词汇索引
    def find_nots(self, tokens):
        nots = []
        for i, token in enumerate(tokens):
            if self.is_not(token):
                nots.append(i)
        return nots

    # 检查给定的token是否包含not等词汇
    def is_not(self, token):
        return (token.pos == "RB" and token.lemma.lower() == "not") or token.word.upper() == "NOT" or\
                token.lemma.lower() == "n't"

    # 检查token是否为助动词
    def is_auxiliary_token(self, aux_token):
        pos_lemma = aux_token.general_pos + "-" + aux_token.lemma.lower()
        return any(pos_lemma == p for p in self.POS_LEMMAS)

    # 检查是否有附加的助动词
    def find_additional_aux_verbs(self, tokens):
        for token in tokens:
            lemma = token.lemma.lower()
            if any(lemma == p for p in self.ADDITIONAL_AUX_VERBS):
                return True

        for i in range(len(tokens) - 1):
            token1 = tokens[i]
            token2 = tokens[i + 1]
            word = (token1.lemma + " " + token2.lemma).lower()

            if any(word == p for p in self.ADDITIONAL_AUX_VERBS):
                return True

        return False
