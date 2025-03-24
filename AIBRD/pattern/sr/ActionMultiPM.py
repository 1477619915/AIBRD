from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.processor.TextProcessor import TextProcessor
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils


class ActionsMultiPM(StepsToReproducePatternMatcher):
    def match_sentence(self, sentence):
        # Check if the sentence contains "should"
        if any(tok.get_lemma() == "should" for tok in sentence.get_tokens()):
            return 0

        clauses = SentenceUtils.extract_clauses(sentence)

        for clause in clauses:
            if SentenceUtils.is_imperative_sentence(clause):
                return 1


        return 0

