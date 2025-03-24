from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeTerms import NegativeTerms


from pattern.processor.TextProcessor import TextProcessor
from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
import re


class NegativeAdjOrAdvPM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        tokens = sentence.get_tokens()

        # Cases such as: "is/are not" + (adverb) verb in pp or adj
        nots = self.find_nots(tokens)
        for not_idx in nots:
            try:
                next_token = tokens[not_idx + 1]
                verb_token = tokens[not_idx - 1]

                if NegativeAuxVerbPM.is_auxiliary_token(verb_token):
                    continue

                if next_token.get_general_pos() == "RB":
                    index = not_idx + 2
                    if index < len(tokens):
                        next_token2 = tokens[index]
                        if next_token2.get_pos() in ["VBN", "VBD"]:
                            return 1
                        elif next_token2.get_pos() == "JJ":
                            return 1
                elif next_token.get_pos() in ["VBN", "VB", "VBD"]:
                    return 1
                elif next_token.get_pos() == "JJ":
                    return 1
            except IndexError:
                pass

        # Cases such as is/are + negative verb in pp or adj
        to_be_verbs = self.find_to_be_verbs(tokens)
        for to_be_verb_idx in to_be_verbs:
            try:
                next_token = tokens[to_be_verb_idx + 1]

                if next_token.get_pos() in ["VBN", "VB"] and next_token.get_lemma() in NegativeTerms.VERBS:
                    return 1
                elif next_token.get_general_pos() == "JJ" and next_token.get_lemma() in NegativeTerms.ADJECTIVES:
                    return 1
                elif next_token.get_general_pos() == "RB":
                    index = to_be_verb_idx + 2
                    if index < len(tokens):
                        next_token2 = tokens[index]
                        if next_token2.get_pos() == "VBN" and next_token2.get_lemma() in NegativeTerms.VERBS:
                            return 1
                        elif next_token2.get_general_pos() == "JJ" and next_token2.get_lemma() in NegativeTerms.ADJECTIVES:
                            return 1
                elif next_token.get_general_pos() == "IN":
                    index = to_be_verb_idx + 2
                    if index < len(tokens):
                        next_token2 = tokens[index]
                        if next_token.get_lemma().lower() == "out" and next_token2.get_lemma().lower() == "of":
                            return 1
            except IndexError:
                pass

        any_match2 = any(t.get_pos() == "VBG" and t.get_lemma().lower() == "miss" for t in tokens)
        if any_match2:
            return 1

        any_match4 = any(t.get_pos() == "VBN" and t.get_lemma().lower() == "break" for t in tokens)
        if any_match4:
            return 1

        any_match3 = any(t.get_pos() == "JJ" and t.get_lemma().lower() in NegativeTerms.ADJECTIVES for t in tokens)
        if any_match3:
            return 1

        any_match = any(t.get_pos() == "RB" and t.get_lemma().lower() in NegativeTerms.ADVERBS for t in tokens)
        if any_match:
            return 1

        str = TextProcessor.get_string_from_lemmas(sentence)
        if "go cpu bind" in str:
            return 1

        if re.match(r".*(page( .*)? down).*", str):
            return 1

        # Search for "messed up", not at the beginning of the sentence
        for i in range(1, len(tokens) - 1):
            token = tokens[i]

            if (token.get_pos() in ["VBD", "VBZ"] and token.get_lemma().lower() == "mess"):
                next_token = tokens[i + 1]
                if next_token.get_lemma().lower() == "up":
                    return 1

        return 0

    def find_nots(self, tokens):
        nots = []
        for i, token in enumerate(tokens):
            pos = token.get_pos()
            if (pos == "RB" and token.get_lemma().lower() == "not") or token.get_word().upper() == "NOT":
                nots.append(i)
        return nots

    def find_to_be_verbs(self, tokens):
        to_bes = []
        for i, token in enumerate(tokens):
            pos = token.get_general_pos()
            if pos == "VB" and token.get_lemma().lower() == "be":
                to_bes.append(i)
        return to_bes

