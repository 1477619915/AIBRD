from pattern.PatternMatcher import PatternMatcher
from abc import ABCMeta


class ObservedBehaviorPatternMatcher(PatternMatcher, metaclass=ABCMeta):

    def get_type(self):
        return self.OB

    def is_eb_modal(self, tokens):
        for tok in tokens:
            if tok.get_general_pos() == "MD" and (tok.get_lemma() == "must" or tok.get_lemma() == "need"
                                                  or tok.get_lemma() == "should"):
                return True
        return False
