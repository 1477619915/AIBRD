import math
from modelConfig import modelConfig
from ContextVect import ContextVect
import pandas as pd
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, WeightedRandomSampler
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer
from patternVect import patternVect

from trainModel import train_model, test_model


if __name__ == '__main__':
    model_config = modelConfig()
    print("测试二义性数据")
    data = pd.read_csv("/root/autodl-tmp/AIBRD/new_statistic.csv")
    data.dropna(subset=['sentence'], inplace=True)

    # 获取句子和标签列
    sentences = list(data['sentence'].apply(str))
    labels = list(data['label'])
    patterns = list(data['patterns'])
    positive_sentences = [sentence for sentence, label in zip(sentences, data['label']) if label != 0]
    negative_sentences = [sentence for sentence, label in zip(sentences, data['label']) if label == 0]  

    # ambiguity数据集的读取
    ambiguity = pd.read_csv("/root/autodl-tmp/AIBRD/ambiguity_statistic_total.CSV")
    ambiguity.dropna(subset=['sentence'], inplace=True)
    ambiguity_sentences = list(ambiguity['sentence'].apply(str))
    ambiguity_labels = list(ambiguity['label'])
    ambiguity_patterns = list(ambiguity['patterns'])
    

    # 使用预训练模型BERT特征表示
    tokenizer = BertTokenizer.from_pretrained(model_config.bert_path)
    result_comments_id = tokenizer(ambiguity_sentences,
                                   padding="max_length",
                                   truncation=True,
                                   max_length=180,
                                   return_tensors='pt')

    input_ids = result_comments_id['input_ids']

    # 语篇模式特征表示
    pattern_vect = patternVect()
    pattern_feature = pattern_vect.match_patterns(ambiguity_patterns).to('cuda')

    context = ContextVect()
    bug_reports = context.bug_reports("/root/autodl-tmp/AIBRD/statistic.csv")
    keywords = context.extract_keywords(sentences, labels, positive_sentences, negative_sentences, 'information', 200)
    cooccurrence_matrix = context.cooccurrence_frequency(bug_reports, keywords)
    print(cooccurrence_matrix)

    # 关键词特征
    keyword_feature = context.keyword_feature(ambiguity_sentences, keywords)
    keyword_feature = torch.from_numpy(keyword_feature)
    # 共现频率特征
    cooccurrence_feature = context.ambiguity_cooccurrence_feature(ambiguity_sentences, cooccurrence_matrix, keywords)
    cooccurrence_feature = torch.from_numpy(cooccurrence_feature)
    # 同位关系特征
    apposition_feature = context.ambiguity_apposition_feature(ambiguity_sentences, keywords)
    apposition_feature = torch.from_numpy(apposition_feature)

    print("Keyword Feature Size:", keyword_feature.size())
    print("Cooccurrence Feature Size:", cooccurrence_feature.size())
    print("Apposition Feature Size:", apposition_feature.size())
    print("pattern_feature Size:", pattern_feature.size())

    contenx_feature = torch.cat((keyword_feature, cooccurrence_feature, apposition_feature), dim=-1)

    contenx_feature = torch.tensor(contenx_feature, dtype=torch.float32).to('cuda')

    X = input_ids
    y = torch.from_numpy(ambiguity['label'].values).long()
    z = pattern_feature
    t = contenx_feature

    test_data = TensorDataset(X, y, z, t)
    test_loader = DataLoader(test_data,
                             batch_size=model_config.batch_size,
                             drop_last=True)

    if (model_config.use_cuda):
        print('Run on GPU.')
    else:
        print('No GPU available, run on CPU.')

    test_model(model_config, test_loader)



