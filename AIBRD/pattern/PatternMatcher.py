import inspect
import logging
from abc import ABCMeta, abstractmethod



class PatternMatcher(metaclass=ABCMeta):
    def __init__(self):
        self.LOGGER = logging.getLogger(self.__class__.__name__)
        self.code = None
        self.name = None

    OB = "OB"
    EB = "EB"
    SR = "SR"

    CONDITIONAL_TERMS = {"if", "upon", "when", "whenever", "whereas", "while"}               # 条件词汇
    CONTRAST_TERMS = {"although", "but", "however", "nevertheless", "though", "yet"}         # 对比词汇

    @abstractmethod
    def match_sentence(self, sentence):
        pass

    # def match_paragraph(self, paragraph):
    #     return self.default_match_paragraph(paragraph)
    #
    # def default_match_paragraph(self, paragraph):
    #     sentences = paragraph.get_sentences()
    #     num_matches = 0
    #     for sentence in sentences:
    #         num_matches += self.match_sentence(sentence)
    #     return num_matches
    #
    # def match_document(self, bug_report):
    #     num_matches = 0
    #     paragraphs = bug_report.get_paragraphs()
    #     for paragraph in paragraphs:
    #         try:
    #             num_matches += self.match_paragraph(paragraph)
    #         except Exception as e:
    #             self.LOGGER.error(f"Error for bug {bug_report.get_id()}, paragraph: {paragraph.get_id()}: {str(e)}")
    #             raise e
    #     return num_matches

    @abstractmethod
    def get_type(self):
        pass

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.validate_name(name)
        self.name = name

    def validate_name(self, name, current_class):
        current_class = inspect.currentframe().f_back.f_locals['self'].__class__
        super_class_name = current_class.__bases__[0].__name__

        if ("_EB_" in name and super_class_name != "ExpectedBehaviorPatternMatcher") or \
           ("_SR_" in name and super_class_name != "StepsToReproducePatternMatcher") or \
           ("_OB_" in name and super_class_name != "ObservedBehaviorPatternMatcher"):
            raise RuntimeError(f"Wrong pattern-class mapping for {name}: {super_class_name}")

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + (0 if self.name is None else hash(self.name))
        return result

    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        other = PatternMatcher(obj)
        if self.name is None:
            if other.name is not None:
                return False
        else:
            if self.name != other.name:
                return False
        return True

    def find_first_pattern_that_matches(self, sentence, patterns):
        for pm in patterns:
            match = pm.match_sentence(sentence)
            if match == 1:
                return pm
        return None

    def sentence_matches_any_pattern_in(self, sentence, patterns):
        return self.find_first_pattern_that_matches(sentence, patterns) is not None

    @staticmethod
    def create_fake_pattern(name):
        class FakePatternMatcher(PatternMatcher):
            def match_sentence(self, sentence):
                return 0

            def get_type(self):
                return None

        pm = FakePatternMatcher()
        pm.name = name
        return pm
