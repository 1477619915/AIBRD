from pattern.PatternMatcher import PatternMatcher
from abc import ABCMeta


class ExpectedBehaviorPatternMatcher(PatternMatcher, metaclass=ABCMeta):
    def get_type(self):
        return self.EB