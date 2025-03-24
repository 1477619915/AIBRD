import pandas as pd

from pattern.eb.ExpBehaviorLiteralMultiSentencePM import ExpBehaviorLiteralMultiSentencePM
from pattern.eb.ExpBehaviorLiteralSentencePM import ExpBehaviorLiteralSentencePM
from pattern.eb.ExpectSentencePM import ExpectSentencePM
from pattern.eb.InsteadExpBehaviorPM import InsteadExpBehaviorPM
from pattern.eb.ShouldPM import ShouldPM
from pattern.eb.WouldBeSentencePM import WouldBeSentencePM

from pattern.ob.ActionSubjectPM import ActionSubject
from pattern.ob.AfterNegativePM import AfterNegativePM
from pattern.ob.AttachRefPM import AttachRefPM
from pattern.ob.ButNegativePM import ButNegativePM
from pattern.ob.ButPM import ButPM
from pattern.ob.ConditionalNegativePM import ConditionalNegativePM
from pattern.ob.ConditionalPositivePM import ConditionalPositivePM
from pattern.ob.DescriptionPM import DescriptionPM
from pattern.ob.DesptitePM import DesptitePM
from pattern.ob.ErrorCondPM import ErrorCondPM
from pattern.ob.ErrorNounPhrasePM import ErrorNounPhrasePM
from pattern.ob.ErrorTermSubjectPM import ErrorTermSubjectPM
from pattern.ob.FoundPM import FoundPM
from pattern.ob.FrequencyAdverbPM import FrequencyAdverbPM
from pattern.ob.HappensPM import HappensPM
from pattern.ob.InsteadOfObPM import InsteadOfObPM
from pattern.ob.LeadsToNegativePM import LeadsToNegativePM
from pattern.ob.LogContainsPM import LogContainsPM
from pattern.ob.NegativeAdjOrAdvPM import NegativeAdjOrAdvPM
from pattern.ob.NegativeAfterPM import NegativeAfterPM
from pattern.ob.NegativeAuxVerbPM import NegativeAuxVerbPM
from pattern.ob.NegativeConditionalPM import NegativeConditionalPM
from pattern.ob.NegativeVerbPM import NegativeVerbPM
from pattern.ob.NoLongerPM import NoLongerPM
from pattern.ob.NoNounPM import NoNounPM
from pattern.ob.NonTermPM import NonTermPM
from pattern.ob.NounNotPM import NounNotPM
from pattern.ob.ObsBehaviorLiteralMultiStncePM import ObsBehaviorLiteralMultiStncePM
from pattern.ob.ObsBehaviorLiteralStncePM import ObsBehaviorLiteralStncePM
from pattern.ob.ObservePM import ObservePM
from pattern.ob.OnlyPM import OnlyPM
from pattern.ob.OutPutVerbPM import OutPutVerbPM
from pattern.ob.PassiveVoicePM import PassiveVoicePM
from pattern.ob.PositiveConditionPM import PositiveConditionPM
from pattern.ob.ProblemInPM import ProblemInPM
from pattern.ob.SeemsPM import SeemsPM
from pattern.ob.SeemsToBePM import SeemsToBePM
from pattern.ob.SimplePresentPM import SimplePresentPM
from pattern.ob.StillSentencePM import StillSentencePM
from pattern.ob.TimeAdverbNegativePM import TimeAdverbNegativePM
from pattern.ob.TimeAdverbPositivePM import TimeAdverbPositivePM
from pattern.ob.UnableToPM import UnableToPM
from pattern.ob.VerbToBeNegativePM import VerbToBeNegativePM
from pattern.ob.VerbErrorPM import VerbErrorPM
from pattern.ob.VerbNoPM import VerbNoPM
from pattern.ob.WorksFinePM import WorksFinePM
from pattern.ob.WorksButPM import WorksButPM

from pattern.sr.ActionMultiPM import ActionsMultiPM
from pattern.sr.ActionsInfinitivePM import ActionsInfinitivePM
from pattern.sr.CodeRefPM import CodeRefPM
from pattern.sr.ConditionalObservedBehaviorPM import ConditionalObservedBehaviorPM
from pattern.sr.LabeledCodeFragmentsPM import LabeledCodeFragmentsPM
from pattern.sr.LabeledListPM import LabeledListPM
from pattern.sr.SimplePastParagraphPM import SimplePastParagraphPM


def match_patterns(sentence, patterns):
    result_vector = []
    for pattern in patterns:
        result_vector.append(pattern.match_sentence(sentence))
    return result_vector


# 读取数据并处理
data = pd.read_csv("statistic_label.csv")
data.dropna(subset=['sentence'], inplace=True)
sentences = list(data['sentence'].apply(str))

# 创建语篇模式实例的列表
pattern_instances = [ExpBehaviorLiteralMultiSentencePM(), ExpBehaviorLiteralSentencePM(), ExpectSentencePM(),
                     InsteadExpBehaviorPM(), ShouldPM(), WouldBeSentencePM(), ActionSubject(), AfterNegativePM(),
                     AttachRefPM(), ButNegativePM(), ButPM(), ConditionalNegativePM(), ConditionalPositivePM(),
                     DescriptionPM(), DesptitePM(), ErrorCondPM(), ErrorNounPhrasePM(), ErrorTermSubjectPM(),
                     FoundPM(), FrequencyAdverbPM(), HappensPM(), InsteadOfObPM(), LeadsToNegativePM(),
                     LogContainsPM(), NegativeAdjOrAdvPM(), NegativeAfterPM(), NegativeAuxVerbPM(),
                     NegativeConditionalPM(), NegativeVerbPM(), NoLongerPM(), NoNounPM(),
                     NonTermPM(), NounNotPM(), ObsBehaviorLiteralMultiStncePM(), ObsBehaviorLiteralStncePM(),
                     ObservePM(), OnlyPM(), OutPutVerbPM(), PassiveVoicePM(), PositiveConditionPM(), ProblemInPM(),
                     SeemsPM(), SeemsToBePM(), SimplePresentPM(), StillSentencePM(),
                     TimeAdverbPositivePM(), TimeAdverbNegativePM(), UnableToPM(), VerbErrorPM(), VerbNoPM(),
                     VerbToBeNegativePM(), WorksButPM(), WorksFinePM(), ActionsMultiPM(), ActionsInfinitivePM(),
                     CodeRefPM(), ConditionalObservedBehaviorPM(), LabeledCodeFragmentsPM(), LabeledListPM(),
                     SimplePastParagraphPM()
                     ]

# 遍历句子并判断匹配
result_vectors = []
for sentence in sentences:
    result_vector = match_patterns(sentence, pattern_instances)
    print(result_vector)
    result_vectors.append(result_vector)









