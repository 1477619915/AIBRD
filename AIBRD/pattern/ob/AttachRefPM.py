from pattern.ObservedBehaviorPatternMatcher import ObservedBehaviorPatternMatcher
from pattern.ExpectedBehaviorPatternMatcher import ExpectedBehaviorPatternMatcher
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.ErrorTermSubjectPM import ErrorTermSubjectPM
from pattern.ob.InsteadOfObPM import InsteadOfObPM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.NoNounPM import NoNounPM


class AttachRefPM(ObservedBehaviorPatternMatcher):
    ATTACH_VERB = "attach"
    ATTACH_NOUN = "attachment"
    ATTACHMENTS = {"screenshot", "screen", "log", "report", "document", "file", "sample", "example", "docx", "test",
                   "project"}

    NEGATIVE_PMS = [
        ErrorNounPhrasePM(),
        NegativeAdjOrAdvPM(),
        NoNounPM(),
        ErrorTermSubjectPM(),
        InsteadOfObPM(),
        NegativeVerbPM(),
        NegativeAuxVerbPM()
    ]

    def match_sentence(self, sentence):
        if self.contains_attachment(sentence.tokens) and self.is_negative(sentence):
            return 1
        return 0

    def is_negative(self, sentence):
        return self.sentence_matches_any_pattern_in(sentence, self.NEGATIVE_PMS)

    def contains_attachment(self, tokens):
        attach_term = False
        attached_element = False

        for i, current in enumerate(tokens):
            # check for the noun "attachment" or verb "attach"
            if (current.general_pos == "NN" and current.lemma == self.ATTACH_NOUN) or \
                    (current.general_pos == "VB" and current.lemma == self.ATTACH_VERB):

                if i > 0:
                    previous = tokens[i - 1]
                    if previous.general_pos != "IN" and previous.general_pos != "TO":
                        attach_term = True
                else:
                    attach_term = True

            # to match cases such as: "example/test" or "test.odb"
            elif current.general_pos == "NN" and any(
                    current.lemma.match(r'[A-Za-z]*/?[/.]?{0}/?[/.]?[A-Za-z]*'.format(attachment)) for attachment in
                    self.ATTACHMENTS):
                attached_element = True

        # check if there's any attachment term and the element that is attached
        return attach_term and attached_element


