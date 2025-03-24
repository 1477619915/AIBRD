from pattern.processor.TextProcessor import TextProcessor
import re

from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.entity.Sentence import Sentence


class SimpleTenseChecker:
    PRESENT_POS = {"VBP", "VBZ", "VB"}
    PRESENT_EXCLUDED_VERBS = {"be", "seem", "can"}
    PRESENT_UNDETECTED_VERBS = {"set", "put", "close", "cache", "scale", "change", "type", "input"}

    PAST_POS = {"VBD", "VBN"}
    PAST_UNDETECTED_VERBS = {"set", "put"}

    DEFAULT_PRONOUN_LEMMAS = {"i", "we"}
    DEFAULT_PRONOUN_POS_LEMMA = {"NN-user", "PRP-i", "PRP-we", "PRP-you"}

    DEFAULT_PRONOUN_POS = {"PRP"}


    def __init__(self, part_of_speeches=None, undetected_verbs=None, verbs_to_avoid=None,
                 pronouns_general_pos=None, pronouns_lemmas=None, pronouns_pos_lemmas=None, is_checker_present=False):
        self.part_of_speeches = part_of_speeches if part_of_speeches is not None else set()
        self.undetected_verbs = undetected_verbs if undetected_verbs is not None else set()
        self.verbs_to_avoid = verbs_to_avoid if verbs_to_avoid is not None else set()
        self.pronouns_general_pos = pronouns_general_pos if pronouns_general_pos is not None else set()
        self.pronouns_lemmas = pronouns_lemmas if pronouns_lemmas is not None else set()
        self.pronouns_pos_lemmas = pronouns_pos_lemmas if pronouns_pos_lemmas is not None else set()
        self.is_checker_present = is_checker_present if is_checker_present is not None else True

    def create_past_checker_only_pronouns(self, verbs_to_avoid):
        self.__init__(self.PAST_POS, self.PAST_UNDETECTED_VERBS, verbs_to_avoid, self.DEFAULT_PRONOUN_POS, self.DEFAULT_PRONOUN_LEMMAS, self.DEFAULT_PRONOUN_POS_LEMMA, True)
        return self

    def create_present_checker_pronouns_and_nouns(self, verbs_to_avoid):
        self.__init__(self.PAST_POS, self.PAST_UNDETECTED_VERBS, verbs_to_avoid, {"PRP", "NN"}, self.DEFAULT_PRONOUN_LEMMAS, self.DEFAULT_PRONOUN_POS_LEMMA, True)
        return self

    def count_num_clauses(self, sentence):
        num_clauses = 0
        clauses = SentenceUtils.extract_clauses(sentence)
        idx_first_clause = self.find_first_clause_in_tense(clauses)

        if idx_first_clause != -1:
            num_clauses += 1
            remaining_clauses = clauses[idx_first_clause + 1:]

            for clause in remaining_clauses:
                if self.check_clause_in_tense(clause) or self.check_clause_in_tense_with_pronoun(clause):
                    num_clauses += 1
        return num_clauses

    def find_first_clause_in_tense(self, clauses):
        for i, sentence in enumerate(clauses):
            if self.check_clause_in_tense_with_pronoun(sentence):
                return i
        return -1

    def check_clause_in_tense_with_pronoun(self, tokens):
        verbs = self.find_verbs_in_tense(tokens)

        for verb_idx in verbs:
            if verb_idx - 1 >= 0:
                is_negative = tokens[verb_idx + 1].lemma == "not" if verb_idx + 1 < len(tokens) else False
                is_perfect_tense = tokens[verb_idx].lemma == "have" and verb_idx + 1 < len(tokens) and tokens[
                    verb_idx + 1].general_pos == "VB"
                prev_token = tokens[verb_idx - 1]

                if self.check_for_subject(prev_token) and not is_negative and not is_perfect_tense:
                    return True
                elif prev_token.general_pos == "RB":
                    if verb_idx - 2 >= 0:
                        prev_token_2 = tokens[verb_idx - 2]
                        if self.check_for_subject(prev_token_2) and not is_negative and not is_perfect_tense:
                            return True
                elif prev_token.lemma == "do" and verb_idx - 2 >= 0:
                    prev_token_2 = tokens[verb_idx - 2]
                    if self.check_for_subject(prev_token_2) and not is_negative and not is_perfect_tense:
                        return True

        return False

    def find_verbs_in_tense(self, tokens):
        idxs = []
        for i, token in enumerate(tokens):
            if self.check_for_verb(token):
                # 没有助动词
                if token.lemma == "do" and i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if not (next_token.general_pos == "VB" or next_token.lemma in self.undetected_verbs):
                        idxs.append(i)
                else:
                    idxs.append(i)
            else:
                # 情况： "I did execute..."
                # 如果句子是过去式，我应该检查当前标记的现在时态以及前一个标记的过去时态和动词 "do"
                if not self.is_checker_present:
                    if i - 1 >= 0 and (token.pos in self.PRESENT_POS or token.lemma in self.undetected_verbs):
                        previous_token = tokens[i - 1]
                        if previous_token.lemma == "do" and self.check_for_verb(previous_token):
                            idxs.append(i)
        return idxs

    def check_for_verb(self, token):
        return (any(pos == token.pos for pos in self.part_of_speeches) or
                any(verb == token.lemma for verb in self.undetected_verbs)) and \
            not any(verb == token.lemma for verb in self.verbs_to_avoid)

    def check_for_subject(self, token):
        general_pos = token.general_pos
        lemma = token.lemma.lower()
        return any(general_pos == pos for pos in self.pronouns_general_pos) or \
            any(lemma == lem for lem in self.pronouns_lemmas) or \
            any(pos_lemma == general_pos + "-" + lemma for pos_lemma in self.pronouns_pos_lemmas)

    def check_clause_in_tense(self, clause):
        tokens = clause.tokens
        if len(tokens) < 2:
            return False

        token = tokens[0]

        # case: perform(ed)
        if self.check_for_verb(token):
            return True
        else:
            # case: simply perform(ed)
            if len(tokens) > 2:
                next_token = tokens[1]
                if token.general_pos == "RB" or token.lemma == "than":  # typo: then -> than
                    if self.check_for_verb(next_token):
                        return True
        return False



