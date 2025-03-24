from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.NoLongerPM import NoLongerPM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.NoNounPM import NoNounPM
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.ErrorTermSubjectPM import ErrorTermSubjectPM
from pattern.ob.PassiveVoicePM import PassiveVoicePM
from pattern.ob.StillSentencePM import StillSentencePM
from pattern.ob.SeemsPM import SeemsPM
from pattern.ob.WorksFinePM import WorksFinePM
from pattern.ob.HappensPM import HappensPM
from pattern.eb.WouldBeSentencePM import WouldBeSentencePM
import re

from pattern.processor.TextProcessor import TextProcessor
from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ConditionalObservedBehaviorPM(StepsToReproducePatternMatcher):
    # 定义排除的动词集合
    EXCLUDED_VERBS = {"do", "be", "have", "want", "feel", "deal", "look", "decide", "need"}

    # 定义观察行为模式匹配器列表
    OB_PMS = [
        NegativeAuxVerbPM(),
        NegativeVerbPM(),
        NoLongerPM(),
        VerbErrorPM(),
        VerbToBeNegativePM(),
        NegativeAdjOrAdvPM(),
        UnableToPM(),
        VerbNoPM(),
        ProblemInPM(),
        NoNounPM(),
        ErrorTermSubjectPM(),
        ErrorNounPhrasePM(),
        PassiveVoicePM(),
        StillSentencePM(),
        SeemsPM(),
        WorksFinePM(),
        HappensPM()
    ]

    def match_sentence(self, sentence):
        pm2 = WouldBeSentencePM()
        if pm2.match_sentence(sentence) != 0:
            return 0

        clauses = SentenceUtils.extract_clauses(sentence)

        idx = self.find_conditional_and_tense_token(clauses)

        if idx == -1:
            return 0

        cond_clause = clauses[idx]
        cond_clause_tokens = cond_clause.getTokens()

        idx_cond = self.find_conditional_and_tense_token(cond_clause_tokens)
        pre_clause = Sentence("0", cond_clause_tokens[:idx_cond])
        pre_clause_tokens = pre_clause.getTokens()

        if any(tok.lemma == "please" for tok in pre_clause_tokens):
            return 0

        pre_clause_txt = TextProcessor.get_string_from_lemmas(pre_clause)
        if re.match(r".*no matter.*", pre_clause_txt):
            return 0

        remaining_clauses = clauses[idx + 1:]

        valid_sentence = self.check_for_remaining_clauses(remaining_clauses)
        if valid_sentence:
            return 1
        else:
            for pm in self.OB_PMS:
                if pm.matchSentence(pre_clause) == 1:
                    return 1

            post_clause = Sentence("0", cond_clause_tokens[idx_cond + 1:])
            for pm in self.OB_PMS:
                if pm.matchSentence(post_clause) == 1:
                    return 1

            if idx - 1 >= 0:
                previous_clause = clauses[idx - 1]
                for pm in self.OB_PMS:
                    if pm.matchSentence(previous_clause) == 1:
                        return 1

        return 0

    def find_first_cond_clause_in_present(self, clauses):
        for i, clause in enumerate(clauses):
            clause_tokens = clause.get_tokens()
            is_valid = self.check_conditional_and_tense(clause_tokens)
            if is_valid:
                return i
        return -1

    def check_conditional_and_tense(self, clause_tokens):
        return self.find_conditional_and_tense_token(clause_tokens) != -1

    def find_conditional_and_tense_token(self, clause_tokens):
        cond_terms = SentenceUtils.find_lemmas_in_tokens(self.CONDITIONAL_TERMS, clause_tokens)

        for cond_term in cond_terms:
            if cond_term + 1 < len(clause_tokens):
                next_token = clause_tokens[cond_term + 1]

                # case: "when running"
                if next_token.get_pos() == "VBG" and SentenceUtils.lemmas_contain_token(self.EXCLUDED_VERBS, next_token):
                    return cond_term
                elif self.is_simple_tense_with_pronoun(next_token, cond_term, clause_tokens, False):
                    return cond_term
                elif self.is_present_perfect(cond_term, clause_tokens):
                    return cond_term
                else:
                    if cond_term + 3 < len(clause_tokens):
                        next_token2 = clause_tokens[cond_term + 2]
                        next_token3 = clause_tokens[cond_term + 3]
                        pronouns = {"i", "we", "you"}

                        # case: When we are running
                        if (next_token3.get_pos() == "VBG"
                                and not SentenceUtils.lemmas_contain_token(self.EXCLUDED_VERBS, next_token)
                                and any(pron for pron in pronouns if next_token.get_lemma().equalsIgnoreCase(pron))
                                and next_token2.get_lemma() == "be"):
                            return cond_term

                    if cond_term + 4 < len(clause_tokens):
                        next_token2 = clause_tokens[cond_term + 2]
                        next_token3 = clause_tokens[cond_term + 3]
                        next_token4 = clause_tokens[cond_term + 4]
                        subjects = {"user", "patient"}
                        pos_to_be = {"VBZ", "VBP"}
                        pos_verb = {"VBD", "VBN"}

                        # case: when a user is prompted
                        if (any(subj for subj in subjects if next_token2.get_lemma() == subj)
                                and next_token3.get_pos() in pos_to_be
                                and next_token3.get_lemma() == "be"
                                and next_token4.get_pos() in pos_verb):
                            return cond_term

        return -1

    def is_simple_tense_with_pronoun(self, next_token, cond_term, clause_tokens, accept_it_pronoun):
        if (next_token.get_general_pos() == "PRP" or next_token.get_pos() == "WDT" or next_token.get_lemma() in {"i", "anyone"}) and (accept_it_pronoun or next_token.get_lemma() != "it"):

            if cond_term + 2 < len(clause_tokens):
                next_token2 = clause_tokens[cond_term + 2]
                if self.is_simple_tense(cond_term, next_token2, clause_tokens):
                    return True

        return False

    def is_simple_tense(self, cond_term, next_token2, clause_tokens):
        if (next_token2.get_pos() in {"VBP", "VBZ", "VB", "VBD", "VBN"} and
                not SentenceUtils.lemmas_contain_token(self.EXCLUDED_VERBS, next_token2)):
            return True

        elif next_token2.get_pos() == "RB":
            if cond_term + 3 < len(clause_tokens):
                next_token3 = clause_tokens[cond_term + 3]
                if (next_token3.get_pos() in {"VBP", "VBZ", "VB", "VBD", "VBN"} and
                        not SentenceUtils.lemmas_contain_token(self.EXCLUDED_VERBS, next_token3)):
                    return True

        elif (next_token2.get_pos() in {"VBP", "VBZ", "VB"} and next_token2.get_lemma() == "do" and
              cond_term + 1 < len(clause_tokens) and not clause_tokens[cond_term + 1].get_general_pos() == "VB" and
              cond_term + 3 < len(clause_tokens) and not clause_tokens[cond_term + 3].get_lemma() == "not"):

            return True

        return False

    def is_present_perfect(self, cond_term, clause_tokens):
        if cond_term + 3 >= len(clause_tokens):
            return False

        next_token = clause_tokens[cond_term + 1]
        next_token2 = clause_tokens[cond_term + 2]
        next_token3 = clause_tokens[cond_term + 3]

        if (next_token.get_general_pos() == "PRP" and next_token2.get_lemma() == "have" and
                (next_token3.get_pos() == "VBD" or next_token3.get_pos() == "VBN")):
            return True

        return False

    def check_for_remaining_clauses(self, remaining_clauses):
        # Check for present tense clauses
        idx_last_present_clause = -1
        for i, clause in enumerate(remaining_clauses):
            clause_tokens = clause.get_tokens()
            if clause_tokens:
                if self.is_simple_tense_with_pronoun(clause_tokens[0], -1, clause_tokens, True):
                    idx_last_present_clause = i
                elif self.is_simple_tense(-1, clause_tokens[0], clause_tokens):
                    idx_last_present_clause = i

        if idx_last_present_clause != -1:
            return True

        # Search for OB clauses
        idx2 = SentenceUtils.find_obs_behavior_sentence(remaining_clauses, self.OB_PMS)
        if idx2 != -1:
            return True

        # Cases: OB clauses like "but not if the..."
        # Only the first two tokens are checked (i.e., 'not' and 'if') because
        # the 'but' token is removed when the sentence is split in clauses
        return any(clause.get_tokens()[0].get_lemma() == "not" and
                   clause.get_tokens()[1].get_lemma() == "if" for clause in remaining_clauses if
                   len(clause.get_tokens()) > 2)

