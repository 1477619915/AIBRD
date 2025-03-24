import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.processor.TextProcessor import TextProcessor
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils


class LabeledListPM(StepsToReproducePatternMatcher):

    # 定义为检测到的标签集合
    UNDETECTED_LABELS = {
        "step to reproduce", "step to repro", "reproduce step", "step by step :",
        "str :", "s2r :", "bulleted list bug :", "- step to replicate on the app",
        "reproduce as follow :", "what I have try :", "a similar bug :",
        "here be the step :", "reproduction step :"
    }

    # 定义结束字符集合
    REGEX_ENDING_CHAR = r'(:|\.|\-|\(|#)'

    def match_sentence(self, sentence):
        label_idx = self.get_label_index(sentence)
        if label_idx == 0:
            return 0

        tokens_no_bullet = self.get_tokens_no_bullet(sentence)
        if tokens_no_bullet is None:
            return 0

        if self.check_imperative_clauses(tokens_no_bullet) or self.is_a_noun_phrase(tokens_no_bullet) or \
            self.starts_with_noun_phrase(tokens_no_bullet) or self.is_past_tense_action(tokens_no_bullet):
            return 1

    # 判断句子是否包含标签
    def get_label_index(self, sentence):
            text = TextProcessor.get_string_from_lemmas(sentence)
            b = re.match(
                r'(?s).*step( how)? to (reproduce|recreate|create|replicate)( the (problem|issue|behavior|bug))? '
                + self.REGEX_ENDING_CHAR + '.*', text) or \
                re.match(r'(?s)' + self.REGEX_ENDING_CHAR + '+ ?step( how)? to (reproduce|recreate|create|replicate)( the (problem|issue|behavior|bug))?( ?'
                    + self.REGEX_ENDING_CHAR + '+)?', text) or \
                re.match(r'step|repro|repro step|step to repro ' + self.REGEX_ENDING_CHAR, text) or \
                re.match(r'(how )?to (reproduce|reporduce|recreate|replicate) ' + self.REGEX_ENDING_CHAR + '+', text) or \
                re.match(r'(?s)step( how)? to (reproduce|recreate|create|replicate)( the (problem|issue|behavior|bug))? with.*', text) or \
                re.match(r'(?s).+follow(ing)? (scenario|step) :' + self.REGEX_ENDING_CHAR, text)

            if b:
                return 1
            else:
                b = any(label.lower() == text.lower() for label in self.UNDETECTED_LABELS)
                if b:
                    return 1
            return 0

    # 移除标点符号并提取单词
    def get_tokens_no_bullet(self, sentence):
        text = TextProcessor.get_string_from_lemmas(sentence)
        tokens = sentence.get_tokens()
        tokens_no_bullet = tokens

        # no parentheses
        if not re.match(r'^(-lcb-|-rcb-|-lrb-|-rrb-|-lsb-|-rsb-) \D+ .+', text):

            # cases like: 1 -
            if re.match(r'^(\d+ \-+).+', text):
                tokens_no_bullet = tokens[2:]

            # cases like: [1], (1), {1}
            # ---------------
            elif re.match(r'^(-lsb- \d+(\w+)? -rsb-).+', text):
                tokens_no_bullet = tokens[3:]

            elif re.match(r'^(-lcb- \d+(\w+)? -rcb-).+', text):
                tokens_no_bullet = tokens[3:]

            elif re.match(r'^(-lrb- \d+(\w+)? -lsb-).+', text):
                tokens_no_bullet = tokens[3:]

            # cases like: 1 .
            elif re.match(r'^(\d+ \.).+', text):
                tokens_no_bullet = tokens[2:]

            # cases like: 1. or -
            elif re.match(r'^(\d+|\-|\*).+', text):
                tokens_no_bullet = tokens[1:]

            # cases like: step1 :
            elif re.match(r'^[a-zA-Z]+\d+ :.*', text):
                tokens_no_bullet = tokens[2:]

        return tokens_no_bullet

    # 检查句子是否包含命令语句
    def check_imperative_clauses(self, tokens_no_bullet):
        clauses = SentenceUtils.extract_clauses(Sentence("0", tokens_no_bullet))
        for clause in clauses:
            if SentenceUtils.is_imperative_sentence(clause, True):
                return True
        return False

    # 判断句子是否以过去动词开头
    def is_past_tense_action(self, tokens_no_bullet):
        if len(tokens_no_bullet) > 1:
            first_token = tokens_no_bullet[0]
            return first_token.get_pos() == "VBD" or first_token.get_pos() == "VBN"
        return False

    # 是否存在名词
    def is_a_noun_phrase(self, tokens):
        for i in range(1, len(tokens)):
            token = tokens[i]
            if token.general_pos == "VB":
                return False
        return any(tok.general_pos == "NN" and tok.lemma != "..." for tok in tokens)

    # 是否以名词开头
    def starts_with_noun_phrase(self, tokens):
        if len(tokens) == 1:
            if tokens[0].general_pos == "NN":
                return True
        elif len(tokens) > 1:
            first_token = tokens[0]
            second_token = tokens[1]

            if first_token.general_pos == "JJ" and second_token.general_pos == "VB":
                return True
            if (first_token.general_pos == "JJ" and second_token.general_pos == "NN") or (
                    first_token.general_pos == "NN" and second_token.general_pos == "JJ"):
                return True

        return False







