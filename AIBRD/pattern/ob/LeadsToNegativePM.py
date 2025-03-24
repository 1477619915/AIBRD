from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeConditionalPM import NegativeConditionalPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.NoLongerPM import NoLongerPM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM


class LeadsToNegativePM(ObservedBehaviorPatternMatcher):
    CAUSE_VERBS = {"cause", "produce", "yield", "result", "lead"}

    NEGATIVE_PMS = [NegativeAuxVerbPM(), NegativeVerbPM(), NoLongerPM(), VerbErrorPM(),
                    VerbToBeNegativePM(), NegativeAdjOrAdvPM(), UnableToPM(), VerbNoPM(),
                    ProblemInPM(), ErrorNounPhrasePM(), NegativeConditionalPM()]

    def match_sentence(self, sentence):
        tokens = sentence.tokens
        index_verb = self.index_verb_tokens(tokens)

        # Check for results interpreted as noun and not as verb
        if index_verb == -1:
            index_verb = self.index_result_verb_as_noun(tokens)

        if 0 <= index_verb < len(tokens) - 1:
            first = Sentence(sentence.id, tokens[:index_verb])
            second = Sentence(sentence.id, tokens[index_verb + 1:])

            # Check that in the first sentence there is a noun or pronoun at least or terms are this
            tokens_first = first.tokens
            is_subject = False
            for token in tokens_first:
                if token.general_pos in ("NN", "PRP", "DT", "WH"):
                    is_subject = True

            # Check that the second sentence is negative
            if is_subject or index_verb == 0:
                if self.is_negative(second):
                    return 1

        return 0

    def index_verb_tokens(self, tokens):
        for i, token in enumerate(tokens):
            if token.general_pos == "VB" and SentenceUtils.lemmas_contain_token(self.CAUSE_VERBS, token):
                return i
        return -1

    def index_result_verb_as_noun(self, tokens):
        for i in range(len(tokens) - 1):
            if tokens[i].lemma == "result" and tokens[i + 1].lemma == "in":
                return i
        return -1

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)


