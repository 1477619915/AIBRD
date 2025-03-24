from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
import re


class FrequencyAdverbPM(ObservedBehaviorPatternMatcher):
    FA = "always|annually|constantly|continually|daily|eventually|ever|every day|every month|" + \
         "every time|every week|every year|fortnightly|frequently|from time to time|generally|" + \
         "infrequently|intermittently|monthly|most of the time|never|normally|now and then|" + \
         "occasionally|often|once in a while|periodically|rarely|" + \
         "regularly|seldom|sometimes|some time|usually|weekly|yearly"

    fa_list = FA.split("|")

    import re

    def match_sentence(self, sentence):
        text = sentence.get_text()
        contains_freq_adv = re.match(r'.*[^a-z]?(' + self.fa_list + ')[^a-z]?.*', text)

        tokens = sentence.get_tokens()
        verbs = self.find_verbs(tokens)

        if contains_freq_adv and verbs and not self.is_eb_modal(tokens):
            return 1

        return 0

    def find_verbs(self, tokens):
        verbs = []
        for i, token in enumerate(tokens):
            if token.general_pos == "VB" or token.lemma in SentenceUtils.UNDETECTED_VERBS:
                verbs.append(i)
        return verbs

