from pattern.PatternMatcher import PatternMatcher
from abc import ABCMeta


class StepsToReproducePatternMatcher(PatternMatcher, metaclass=ABCMeta):
    def get_type(self):
        return self.SR