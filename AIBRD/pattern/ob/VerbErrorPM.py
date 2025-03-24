from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class VerbErrorPM(ObservedBehaviorPatternMatcher):
    NEGATIVE_PMS = [ProblemInPM(), ErrorNounPhrasePM()]

    VERB_TERMS = {"output", "return", "got", "get", "result", "crash"}

    NOT_VERBS = {"warning", "spam", "voided", "be"}

    CLAUSE_SEPARATORS = {";", ","}

    def match_sentence(self, sentence):
        sentences = SentenceUtils.break_by_parenthesis(sentence)

        for sent in sentences:
            sub_sentences = SentenceUtils.extract_clauses(sent, self.CLAUSE_SEPARATORS)

            for sub_sentence in sub_sentences:
                tokens = sub_sentence.get_tokens()
                verbs = self.find_all_verbs(tokens)

                for verb in range(len(verbs)):
                    # there's nothing after the verb
                    if verbs[verb] + 1 >= len(tokens):
                        continue

                    start = verbs[verb] + 1
                    after_verb_token = tokens[start]

                    # the token after the verb is a preposition or a personal pronoun
                    while self.token_is_prep(after_verb_token) or after_verb_token.get_general_pos() == "PRP":
                        start += 1
                        if start < len(tokens):
                            after_verb_token = tokens[start]
                        else:
                            break  # continue to the next verb

                    end = start + 1

                    while end <= len(tokens):
                        clause = Sentence(sentence.get_id(), tokens[start:end])
                        if self.is_negative(clause):
                            return 1
                        end += 1

        return 0

    def find_all_verbs(self,tokens):
        verbs = []
        for i, token in enumerate(tokens):
            if (
                    token.get_general_pos() == "VB" or token.get_lemma() in self.VERB_TERMS) and token.get_lemma() not in self.NOT_VERBS:
                # if i + 1 < len(tokens) and tokens[i + 1].get_general_pos() != "VB":
                verbs.append(i)
        return verbs

    def is_negative(self, sentence):
        tokens = sentence.get_tokens()
        if len(tokens) > 1:
            if tokens[0].get_lemma() == "no":
                sub_sentence = Sentence(sentence.get_id(), tokens[1:])
                if not self.sentence_matches_any_pattern_in(sub_sentence, self.NEGATIVE_PMS):
                    return False

        pattern = self.find_first_pattern_that_matches(sentence, self.NEGATIVE_PMS)
        # 调试消息
        # if pattern is not None:
        #     print("match: " + pattern.__class__.__name__)
        #     return True

        return pattern is not None

    def token_is_prep(self, token):
        return SentenceUtils.lemmas_contain_token(ProblemInPM.PREP_TERMS,token)


