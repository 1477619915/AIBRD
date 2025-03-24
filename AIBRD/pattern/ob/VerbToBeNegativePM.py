from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.ProblemInPM import ProblemInPM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class VerbToBeNegativePM(ObservedBehaviorPatternMatcher):
    # Define sets and patterns
    NEGATIVE_TERMS = {"no", "nothing"}
    SUBJECT_TERMS = {"there", "these", "this", "here", "it"}
    NEGATIVE_PMS = ErrorNounPhrasePM()
    POS_LEMMAS = {"MD-can", "MD-would", "MD-will", "MD-could", "MD-may"}

    def match_sentence(self, sentence):
        clauses = SentenceUtils.extract_clauses(sentence)
        for clause in clauses:
            clause_tokens = clause.get_tokens()

            # Split sentences by prepositions
            prep = SentenceUtils.find_lemmas_in_tokens(ProblemInPM.PREP_TERMS, clause_tokens)
            sub_clauses = SentenceUtils.find_sub_sentences(clause, prep)

            for sub_clause in sub_clauses:
                sub_clause_tokens = sub_clause.get_tokens()

                # Find the subjects in the sub-clause
                subj_idx = self.find_subjects(sub_clause_tokens)

                for subj in subj_idx:

                    # Is the sub-clause long enough?
                    if subj + 2 >= len(sub_clause_tokens):
                        continue

                    next_token = sub_clause_tokens[subj + 1]
                    indx_nxt_tok2 = 2

                    # If the current token is modal, then check the next token
                    if self.is_modal(next_token):
                        next_token = sub_clause_tokens[subj + 2]
                        indx_nxt_tok2 = 3

                    # Enough tokens?
                    if subj + indx_nxt_tok2 >= len(sub_clause_tokens):
                        continue

                    # Verb to-be?
                    if next_token.get_lemma() == "be":

                        next_token2 = sub_clause_tokens[subj + indx_nxt_tok2]

                        # Case: there is no/nothing
                        if SentenceUtils.lemmas_contain_token(self.NEGATIVE_TERMS, next_token2):
                            return 1
                        else:

                            # Case: there is a bug/error/etc.
                            new_clause = Sentence(sentence.get_id(),
                                                  sub_clause_tokens[subj + indx_nxt_tok2:])
                            if self.is_negative(new_clause):
                                return 1
                            else:
                                # Case: there are differences...
                                if any(tok.get_lemma().equalsIgnoreCase("difference")
                                       for tok in new_clause.get_tokens()):
                                    return 1
        return 0

    def find_subjects(self, tokens):
        return SentenceUtils.find_lemmas_in_tokens(self.SUBJECT_TERMS, tokens)

    def is_modal(self, aux_token):
        pos_lemma = aux_token.get_general_pos() + "-" + aux_token.get_lemma().lower()
        return any(pos_lemma == p for p in self.POS_LEMMAS)

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)
