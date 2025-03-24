from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class WorksButPM(ObservedBehaviorPatternMatcher):

    FINE_TERM = {"fine", "great", "ok", "normally", "correctly", "flawlessly", "perfectly", "properly"}
    BUT_TERM = {"but", "except", "until", "however", "then", "although", "though", "nevertheless"}

    def match_sentence(self, sentence):
        tokens = sentence.tokens
        index_work = self.work_index(tokens)

        if index_work != -1 and index_work < len(tokens) - 1:
            # check for the fine term
            tok = tokens[index_work + 1]
            if SentenceUtils.lemmas_contain_token(self.FINE_TERM, tok):
                # check for the contrast term
                sentence2 = Sentence(sentence.id, tokens[index_work + 2:])
                tokens2 = sentence2.tokens
                for i in range(len(tokens2)):
                    token = tokens2[i]
                    if SentenceUtils.lemmas_contain_token(self.BUT_TERM, token):
                        return 1

        succeed_index = self.succeed_index(tokens)
        if succeed_index != -1:
            sentence2 = Sentence(sentence.id, tokens[succeed_index + 1:])
            tokens2 = sentence2.tokens
            for i in range(len(tokens2)):
                tok = tokens2[i]
                if SentenceUtils.lemmas_contain_token(self.BUT_TERM, tok):
                    return 1

        return 0

    def work_index(self, tokens):
        for i in range(len(tokens)):
            if tokens[i].general_pos == "VB" and (tokens[i].lemma in ["work", "function", "run"]):
                if i > 0 and tokens[i - 1].lemma != "not":
                    return i
        return -1

    def succeed_index(self, tokens):
        for i in range(len(tokens)):
            if tokens[i].general_pos == "VB" and (tokens[i].lemma in ["succeed", "work"]):
                if i - 1 >= 0 and tokens[i - 1].lemma != "not":
                    return i
        return -1



