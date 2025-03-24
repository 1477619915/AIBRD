from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM
from pattern.ob.NegativeTerms import NegativeTerms
from pattern.ob.ProblemInPM import ProblemInPM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ErrorNounPhrasePM(ObservedBehaviorPatternMatcher):
    def match_sentence(self, sentence):
        pm = VerbToBeNegativePM()
        clauses = SentenceUtils.extract_clauses(sentence)
        num_valid_clauses = 0
        for clause in clauses:
            punctuation = SentenceUtils.find_lemmas_in_tokens({"\"", "``"}, clause.tokens)
            sub_clauses = SentenceUtils.find_sub_sentences(clause, punctuation)
            for sub_clause in sub_clauses:
                prepositions = self.find_prepositions(sub_clause.tokens)
                if prepositions:
                    continue
                if any(tok.pos == "WDT" for tok in sub_clause.tokens):
                    continue
                error_noun_phrase_result = self.check_error_noun_phrase(sub_clause.tokens)
                sentence_id = sentence.id
                sub_clause_tokens = sub_clause.tokens
                if error_noun_phrase_result != 0 and pm.match_sentence(Sentence(sentence_id, sub_clause_tokens)) == 0:
                    num_valid_clauses += 1
                    break
        if num_valid_clauses > 0:
            return 1
        return 0

    def find_prepositions(self, tokens):
        lemma_indexes_in_tokens = []
        for i, token in enumerate(tokens):
            check_token = True

            # Check for "a lot of"
            if token.lemma == "of":
                if i - 2 >= 0 and tokens[i - 2].lemma == "a" and tokens[i - 1].lemma == "lot":
                    check_token = False

            if check_token and SentenceUtils.lemmas_contain_token(ProblemInPM.PREP_TERMS, token):
                lemma_indexes_in_tokens.append(i)

        return lemma_indexes_in_tokens

    def check_error_noun_phrase(self, tokens):
        contains_negative_noun = False
        for i, token in enumerate(tokens):
            # Negative nouns
            if token.lemma in NegativeTerms.NOUNS and token.general_pos in ["NN", "VB", "CD"]:
                contains_negative_noun = True
                break
            # Exceptions
            elif token.lemma.endswith("exception") and token.general_pos == "NN":
                contains_negative_noun = True
                break
            # Errors
            elif token.lemma.endswith("error") and token.general_pos == "NN":
                contains_negative_noun = True
                break
            # Negative adjectives
            elif token.lemma in NegativeTerms.ADJECTIVES and token.general_pos in ["JJ", "NN", "RB", "VB"]:
                if len(tokens) > 1:
                    contains_negative_noun = True
                    break
            # Additional negative adjectives (checking by word)
            elif token.word in NegativeTerms.ADJECTIVES and i - 1 >= 0 and tokens[i - 1].general_pos == "DT":
                contains_negative_noun = True
            # Stack trace
            elif token.lemma.lower() == "stack" and i + 1 < len(tokens) and tokens[i + 1].lemma.lower() == "trace":
                contains_negative_noun = True
                break
            # Missing labeled as VBG
            elif token.lemma.lower() == "miss" and token.pos == "VBG":
                contains_negative_noun = True
                break
            elif token.lemma.lower() == "force" and i + 1 < len(tokens) and tokens[i + 1].lemma.lower() == "close":
                contains_negative_noun = True
                break

        if contains_negative_noun and not (tokens[-1].pos == "VBD" or tokens[-1].pos == "VBN"):
            return 1

        return 0
