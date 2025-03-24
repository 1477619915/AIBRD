from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ProblemInPM(ObservedBehaviorPatternMatcher):
    NEGATIVE_PMS = ErrorNounPhrasePM()
    PREP_TERMS = {"about", "as", "at", "between", "during", "for",
                  "from", "in", "into", "of", "on", "over", "to", "up", "with", "within"}

    def match_sentence(self, sentence):
        for ss in SentenceUtils.break_by_parenthesis(sentence):
            sub_sentences = SentenceUtils.extract_clauses(ss)

            for sub_sentence in sub_sentences:
                tokens = sub_sentence.get_tokens()
                preps = self.find_prepositions(tokens)

                # No prepositions
                if not preps:
                    continue

                for prep_idx in preps:
                    sub_stnc1 = Sentence(".1", tokens[:prep_idx])
                    sub_stnc2 = Sentence(".2", tokens[prep_idx + 1:])

                    is_stnc1_negative = self.is_negative(sub_stnc1)
                    is_stnc2_negative = self.is_negative(sub_stnc2)

                    if is_stnc1_negative:
                        verbs = self.find_problematic_verbs(sub_stnc2.get_tokens())
                        if not verbs:
                            continue

                        return 1
                    elif is_stnc2_negative:
                        verbs = self.find_problematic_verbs(sub_stnc1.get_tokens())
                        if not verbs:
                            continue

                        return 1

        return 0

    def find_prepositions(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.PREP_TERMS, tokens)

    def is_negative(self, sentence):
        pattern = self.find_first_pattern_that_matches(sentence, self.NEGATIVE_PMS)
        return pattern is not None

    def find_problematic_verbs(self, tokens):
        verbs = []
        for i, token in enumerate(tokens):
            if token.get_general_pos() == "VB":
                add = True

                # Disregard verb if it starts the sentence
                if i == 0:
                    add = False
                else:
                    # Cases with gerund and past participle verbs
                    if token.get_pos() in ["VBG", "VBD", "VBN"]:
                        if i - 1 >= 0:
                            prev_token = tokens[i - 1]
                            # Disregard verbs that come after a noun
                            if prev_token.get_general_pos() != "NN":
                                add = False
                        if i + 1 < len(tokens):
                            post_token = tokens[i + 1]
                            # Disregard verbs that go after a preposition
                            if not SentenceUtils.lemmas_contain_token(self.PREP_TERMS, post_token):
                                add = False

                    # Disregard the verb "build" if it ends the sentence
                    if token.get_lemma() == "build" and i == len(tokens) - 1:
                        add = False
                    # Disregard the verb "build" that precedes the word "panel"
                    if token.get_lemma() == "build" and i + 1 < len(tokens) and tokens[i + 1].get_lemma() == "panel":
                        add = False
                    # Disregard verbs that come before a preposition
                    if i - 1 >= 0:
                        prev_token = tokens[i - 1]
                        if SentenceUtils.lemmas_contain_token(self.PREP_TERMS, prev_token):
                            add = False

                if add:
                    verbs.append(i)
        return verbs
