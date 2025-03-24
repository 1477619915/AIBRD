from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class LogContainsPM(ObservedBehaviorPatternMatcher):
    LOG_VERBS = {"be", "contain", "look", "say", "see", "show", "tell"}

    def match_sentence(self, sentence):
        logs = self.find_log(sentence.get_tokens())
        if logs:
            phrases = SentenceUtils.find_sub_sentences(sentence, logs)

            for phrase in phrases:
                if self.find_output_signal(phrase.tokens):
                    return 1

    def find_log(self, tokens):
        logs = []

        for i, current in enumerate(tokens):
            if current.general_pos == "NN" and (
                    re.match(r".*[^A-Za-z]?log[s]?", current.lemma) or re.match(r".*[^A-Za-z]?dump[s]?",
                                                                                current.lemma)):
                logs.append(i)

        return logs

    def find_output_signal(self, tokens):
        signal = []

        for i, token in enumerate(tokens):
            if token.general_pos == "VB" and SentenceUtils.lemmas_contain_token(self.LOG_VERBS, token):
                signal.append(i)
            elif token.lemma == ":":
                signal.append(i)
            elif token.general_pos == "NN" and token.lemma == "message":
                signal.append(i)

        return signal

