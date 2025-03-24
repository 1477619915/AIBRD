from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.NoLongerPM import NoLongerPM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.NoNounPM import NoNounPM
from pattern.ob.ErrorTermSubjectPM import ErrorTermSubjectPM


from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence


class ButNegativePM(ObservedBehaviorPatternMatcher):
    NEGATIVE_PMS = [NegativeAuxVerbPM(), NegativeVerbPM(), NoLongerPM(), VerbErrorPM(), VerbToBeNegativePM(),
                    NegativeAdjOrAdvPM(), UnableToPM(), VerbNoPM(), ProblemInPM(), NoNounPM(), ErrorTermSubjectPM(),
                    ErrorNounPhrasePM()]
    # 创建包含负面词汇的集合
    NEGATIVE_TERMS = {"no", "nothing", "not", "never"}

    from pattern.Utils.SentenceUtils import SentenceUtils
    from pattern.entity.Token import Token
    from pattern.entity.Sentence import Sentence

    def match_sentence(self, sentence):
        sub_tokens = sentence.get_tokens()
        buts = SentenceUtils.find_lemmas_in_tokens(self.CONTRAST_TERMS, sub_tokens)

        for but in buts:
            if but + 1 < len(sub_tokens):
                next_token = sub_tokens[but + 1]
                if next_token.get_lemma() in self.NEGATIVE_TERMS:
                    return 1

                sentence2 = Sentence(sentence.get_id(), sub_tokens[but + 1:])
                if self.is_negative(sentence2):
                    return 1

        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)
