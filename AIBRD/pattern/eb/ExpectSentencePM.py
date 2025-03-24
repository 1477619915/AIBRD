from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.eb.ExpBehaviorLiteralSentencePM import ExpBehaviorLiteralSentencePM
from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ExpectSentencePM(ExpectedBehaviorPatternMatcher):
    WORK_VERBS = {"work", "behave"}

    def match_sentence(self, sentence):
        # Discard sentences with labels such as "expected behavior:"
        pm = ExpBehaviorLiteralSentencePM()
        match = pm.match_sentence(sentence)

        tokens = sentence.get_tokens()
        # Analyze the token after the label (e.g., expect. results: bla bla bla --> bla bla bla)
        if match > 0:
            i = self.find_first_token(tokens, ":")
            tokens = tokens[i + 1:]


        # Discard questions
        txt = TextProcessor.get_string_from_lemmas(sentence)

        if not txt.endswith("right ?") and SentenceUtils.is_question(sentence):
            return 0

        # Find "expect" verbs (any conjugation)
        exp_verbs = self.find_main_tokens(tokens)

        for exp_verb in exp_verbs:
            # Discard cases like "works as expected"
            if exp_verb - 2 >= 0:
                as_token = tokens[exp_verb - 1]
                verb_token = tokens[exp_verb - 2]

                if as_token.get_lemma() == "as" and SentenceUtils.lemmas_contain_token(self.WORK_VERBS, verb_token):
                    return 0

        # Accept any other case
        if exp_verbs:
            return 1

        # Match the noun "expectation"
        any_match2 = any(t.get_lemma().lower() == "expectation" and t.get_general_pos() == "NN" for t in tokens)
        if any_match2:
            return 1

        return 0

    def find_main_tokens(self, tokens):
        main_toenks = []
        for i, token in enumerate(tokens):
            # Match the verb in any conjugation
            if token.get_lemma().lower() == "expect" and token.get_general_pos() == "VB":
                main_toenks.append(i)
        return main_toenks

    def find_first_token(self, tokens, lemma):
        for i, token in enumerate(tokens):
            if token.get_lemma().lower() == lemma:
                return i
        return -1



