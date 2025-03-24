import pandas as pd

# 读取CSV文件
input_file_path = 'bee_label.csv'
output_file_path = 'new_bee_label.csv'
df = pd.read_csv(input_file_path)

# 定义替换规则
replace_rules = {
    # eb
    'sr.LabeledListPM': 'P_SR_LABELED_LIST',
    'ob.NegativeAuxVerbPM': 'S_OB_NEG_AUX_VERB',
    'ob.NegativeVerbPM': 'S_OB_NEG_VERB',
    'ob.VerbErrorPM': 'S_OB_VERB_ERROR',
    'eb.ShouldPM': 'S_EB_SHOULD',
    'sr.ActionsInfinitivePM': 'P_SR_ACTIONS_INF',
    'ob.ButNegativePM': 'S_OB_BUT_NEG',
    'ob.ObsBehaviorLiteralMultiStncePM': 'P_OB_OBSERVED_BEHAVIOR_MULTI',
    'ob.ConditionalNegativePM': 'S_OB_COND_NEG',
    'ob.NegativeAdjOrAdvPM': 'S_OB_NEG_ADV_ADJ',
    'sr.ConditionalObservedBehaviorPM': 'S_SR_COND_OBS',
    'eb.ExpBehaviorLiteralMultiSentencePM': 'P_EB_EXP_BEHAVIOR_MULTI',
    'ob.NegativeConditionalPM': 'S_OB_NEG_COND',
    'sr.ActionsMultiPM': 'P_SR_ACTIONS_MULTI_OBS_BEHAVIOR',
    'ob.ConditionalPositivePM': 'S_OB_COND_POS',
    'ob.ProblemInPM': 'S_OB_PROBLEM_IN',
    'sr.CodeRefPM': 'S_SR_CODE_REF',
    'eb.ExpBehaviorLiteralSentencePM': 'S_EB_EXP_BEHAVIOR',
    'ob.ErrorTermSubjectPM': 'S_OB_ERROR_AS_SUBJECT',
    'ob.LogContainsPM': 'P_OB_LOG_CONTAINS',
    'ob.ButPM': 'S_OB_BUT',
    'ob.ObsBehaviorLiteralStncePM': 'S_OB_OBS_BEHAVIOR',
    'ob.WorksFinePM': 'S_OB_WORKS_FINE',
    'ob.DescriptionPM': 'P_OB_DESCRIPTION',
    'sr.LabeledCodeFragmentsPM': 'P_SR_LABELED_CODE_FRAGS',
    'ob.OutputVerbPM': 'S_OB_OUTPUT_VERB',
    'ob.InsteadOfOBPM': 'S_OB_INSTEAD_OF',
    'ob.ErrorNounPhrasePM': 'S_OB_ERROR_NOUN_PHRASE',
    'ob.SeemsPM': 'S_OB_SEEMS',
    'sr.SimplePastParagraphPM': 'P_SR_SIMPLE_PAST',
    'ob.ErrorCondPM': 'S_OB_ERROR_COND',
    'ob.NegativeAfterPM': 'S_OB_NEG_AFTER',
    'ob.NounNotPM': 'S_OB_NOUN_NOT',
    'ob.FrequencyAdverbPM': 'S_OB_ADV_FREQ',
    'ob.OnlyPM': 'S_OB_ONLY',
    'ob.NoNounPM': 'S_OB_NO_NOUN',
    'ob.VerbToBeNegativePM': 'S_OB_VERB_TO_BE_NEGATIVE',
    'ob.PassiveVoicePM': 'S_OB_PASSIVE_VOICE',
    'ob.SimplePresentPM': 'S_OB_SIMPLE_PRESENT',
    'ob.StillSentencePM': 'S_OB_STILL',
    'ob.TimeAdverbPositivePM': 'S_OB_ADV_TIME_POS',
    'eb.InsteadExpBehaviorPM': 'S_EB_INSTEAD_OF_EXP_BEHAVIOR',
    'ob.AfterNegativePM': 'S_OB_AFTER_NEG',
    'ob.NoLongerPM': 'S_OB_NO_LONGER',
    'ob.TimeAdverbNegativePM': 'S_OB_ADV_TIME_NEG',
    'ob.LeadsToNegativePm': 'S_OB_LEADS_TO_NEG',
    'ob.HappensPM': 'S_OB_HAPPENS',
    'ob.SeemsToBePM': 'S_OB_SEEMS_TO_BE',
    'ob.PositiveConditionalPM': 'S_OB_POS_COND',
    'ob.DespitePM': 'S_OB_DESPITE',
    'eb.ExpectSentencePM': 'S_EB_EXPECTED',
    'eb.WouldBeSentencePM': 'S_EB_WOULD_BE',
    'ob.UnableToPM': 'S_OB_UNABLE_TO',
    'ob.VerbNoPM': 'S_OB_VERB_NO',
    'ob.ActionSubjectPM': 'S_OB_ACTION_SUBJECT',
    'ob.ObservePM': 'S_OB_OBSERVE',
    'ob.FoundPM': 'S_OB_FOUND',
    'ob.WorksButPM': 'S_OB_WORKS_BUT',
    'ob.AttachRefPM': 'S_OB_ATTACH_REF',
    'ob.NonTermPM': 'S_OB_NON_TERM',
}

# 处理patterns列的值
def replace_values(patterns):
    if pd.notna(patterns):  # 检查是否为NaN
        values = patterns.split(',')  # 将逗号分隔的值拆分成列表
        replaced_values = []
        for value in values:
            replaced_values.append(replace_rules.get(value.strip(), value))  # 替换每个值并添加到列表
        return ','.join(replaced_values)  # 将替换后的值重新用逗号连接
    return patterns

# 对patterns列应用替换函数
df['patterns'] = df['patterns'].apply(replace_values)

# 保存到新的CSV文件
df.to_csv(output_file_path, index=False)

print(f"处理完成，结果保存在 {output_file_path}")
