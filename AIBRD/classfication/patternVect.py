import math
import torch


class patternVect:
    pattern_labels = ['P_EB_EXP_BEHAVIOR_MULTI', 'S_EB_EXP_BEHAVIOR', 'S_EB_EXPECTED', 'S_EB_INSTEAD_OF_EXP_BEHAVIOR',
                      'S_EB_SHOULD', 'S_EB_WOULD_BE', 'S_OB_ACTION_SUBJECT', 'S_OB_AFTER_NEG', 'S_OB_ATTACH_REF',
                      'S_OB_BUT_NEG', 'S_OB_BUT', 'S_OB_COND_NEG', 'S_OB_COND_POS', 'P_OB_DESCRIPTION', 'S_OB_DESPITE',
                      'S_OB_ERROR_COND', 'S_OB_ERROR_NOUN_PHRASE', 'S_OB_ERROR_AS_SUBJECT', 'S_OB_FOUND',
                      'S_OB_ADV_FREQ',
                      'S_OB_HAPPENS', 'S_OB_INSTEAD_OF', 'S_OB_LEADS_TO_NEG', 'P_OB_LOG_CONTAINS', 'S_OB_NEG_ADV_ADJ',
                      'S_OB_NEG_AFTER', 'S_OB_NEG_AUX_VERB', 'S_OB_NEG_COND', 'S_OB_NEG_VERB', 'S_OB_NO_LONGER',
                      'S_OB_NO_NOUN', 'S_OB_NON_TERM', 'S_OB_NOUN_NOT', 'P_OB_OBSERVED_BEHAVIOR_MULTI',
                      'S_OB_OBS_BEHAVIOR',
                      'S_OB_OBSERVE', 'S_OB_ONLY', 'S_OB_OUTPUT_VERB', 'S_OB_PASSIVE_VOICE', 'S_OB_POS_COND',
                      'S_OB_PROBLEM_IN', 'S_OB_SEEMS', 'S_OB_SEEMS_TO_BE', 'S_OB_SIMPLE_PRESENT', 'S_OB_STILL',
                      'S_OB_ADV_TIME_POS', 'S_OB_ADV_TIME_NEG', 'S_OB_UNABLE_TO', 'S_OB_VERB_ERROR', 'S_OB_VERB_NO',
                      'S_OB_VERB_TO_BE_NEGATIVE', 'S_OB_WORKS_FINE', 'S_OB_WORKS_BUT',
                      'P_SR_ACTIONS_MULTI_OBS_BEHAVIOR',
                      'P_SR_ACTIONS_INF', 'S_SR_CODE_REF', 'S_SR_COND_OBS', 'P_SR_LABELED_CODE_FRAGS',
                      'P_SR_LABELED_LIST',
                      'P_SR_SIMPLE_PAST'
                      ]

    # 遍历每个句子，判断是否匹配[32,200,60]
    def match_patterns(self, patterns):
        result_vectors = []
        for pattern in patterns:
            result = []
            for a in range(200):
                if not isinstance(pattern, float) or not math.isnan(pattern):
                    result_vector = self.match_pattern(self.pattern_labels, str(pattern).split(','))
                else:
                    # 处理 NaN 值的情况
                    result_vector = [0] * len(self.pattern_labels)
                result.append(result_vector)
            result_vectors.append(result)

        result_vectors = torch.tensor(result_vectors)
        return result_vectors

    def match_pattern(self, pattern_labels, labels_to_match):
        result_vector = [1 if label in labels_to_match else 0 for label in pattern_labels]
        return result_vector

    # # 遍历每个句子，判断是否匹配[32,60]
    #
    # def match_patterns(self, patterns):
    #     result_vectors = []
    #     for pattern in patterns:
    #         if not isinstance(pattern, float) or not math.isnan(pattern):
    #             result_vector = self.match_pattern(self.pattern_labels, str(pattern).split(','))
    #         else:
    #             # 处理 NaN 值的情况
    #             result_vector = [0] * len(self.pattern_labels)
    #         result_vectors.append(result_vector)
    #
    #     result_vectors = torch.tensor(result_vectors)
    #     return result_vectors
