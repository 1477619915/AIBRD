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
import pickle

from trainModel import train_model, test_model



if __name__ == '__main__':
    model_config = modelConfig()
    print("开始读入文件！")
    data = pd.read_csv("/root/autodl-tmp/AIBRD/new_statistic.csv")
    data.dropna(subset=['sentence'], inplace=True)

    # 获取句子和标签列
    sentences = list(data['sentence'].apply(str))
    labels = list(data['label'])
    patterns = list(data['patterns'])
    positive_sentences = [sentence for sentence, label in zip(sentences, data['label']) if label != 0]
    negative_sentences = [sentence for sentence, label in zip(sentences, data['label']) if label == 0]  
    

    # 使用预训练模型BERT特征表示
    tokenizer = BertTokenizer.from_pretrained(model_config.bert_path)
    result_comments_id = tokenizer(sentences,
                                   padding="max_length",
                                   truncation=True,
                                   max_length=200,
                                   return_tensors='pt')

    input_ids = result_comments_id['input_ids']

    # 语篇模式特征表示
    pattern_vect = patternVect()
    pattern_feature = pattern_vect.match_patterns(patterns).to('cuda')

    context = ContextVect()
    bug_reports = context.bug_reports("/root/autodl-tmp/AIBRD/new_statistic.csv")
    keywords = context.extract_keywords(sentences, labels, positive_sentences, negative_sentences, 'information', 200)
    cooccurrence_matrix = context.cooccurrence_frequency(bug_reports, keywords)
    print(cooccurrence_matrix)
    def save_data(keywords, cooccurrence_matrix, keywords_path='keywords.pkl', matrix_path='cooccurrence_matrix.pkl'):
        # 保存关键词列表
        with open(keywords_path, 'wb') as f:
            pickle.dump(keywords, f)
        
        # 保存共现矩阵
        with open(matrix_path, 'wb') as f:
            pickle.dump(cooccurrence_matrix, f)
        print(f"Data saved: keywords -> {keywords_path}, cooccurrence_matrix -> {matrix_path}")
    # 调用保存函数
    save_data(keywords, cooccurrence_matrix)

    # 关键词特征
    keyword_feature = context.keyword_feature(sentences, keywords)
    keyword_feature = torch.from_numpy(keyword_feature)
    # 共现频率特征
    cooccurrence_feature = context.cooccurrence_feature(bug_reports, cooccurrence_matrix, keywords)
    cooccurrence_feature = torch.from_numpy(cooccurrence_feature)
    # 同位关系特征
    apposition_feature = context.apposition_feature(bug_reports, keywords)
    apposition_feature = torch.from_numpy(apposition_feature)

    print("Keyword Feature Size:", keyword_feature.size())
    print("Cooccurrence Feature Size:", cooccurrence_feature.size())
    print("Apposition Feature Size:", apposition_feature.size())
    print("pattern_feature Size:", pattern_feature.size())

    context.plot_cooccurrence_graph(keywords, cooccurrence_matrix, save_path='cooccurrence_graph.png')

    contenx_feature = torch.cat((keyword_feature, cooccurrence_feature, apposition_feature), dim=-1)

    contenx_feature = torch.tensor(contenx_feature, dtype=torch.float32).to('cuda')

    X = input_ids
    y = torch.from_numpy(data['label'].values).long()
    z = pattern_feature
    t = contenx_feature

    X_train, X_test, y_train, y_test, z_train, z_test, t_train, t_test = train_test_split(X,
                                                                                          y,
                                                                                          z,
                                                                                          t,
                                                                                          test_size=0.3,
                                                                                          shuffle=True,
                                                                                          stratify=y,
                                                                                          random_state=0)
    X_valid, X_test, y_valid, y_test, z_valid, z_test, t_valid, t_test = train_test_split(X_test,
                                                                                          y_test,
                                                                                          z_test,
                                                                                          t_test,
                                                                                          test_size=0.5,
                                                                                          shuffle=True,
                                                                                          stratify=y_test,
                                                                                          random_state=0)

    # 计算每个类别的权重
    class_sample_count = np.array([len(np.where(y_train == t)[0]) for t in np.unique(y_train)])
    weight = 1. / class_sample_count
    samples_weight = np.array([weight[t] for t in y_train])

    # 使用权重创建 WeightedRandomSampler 实例
    sampler = WeightedRandomSampler(samples_weight, len(samples_weight), replacement=True)

    train_data = TensorDataset(X_train, y_train, z_train, t_train)
    valid_data = TensorDataset(X_valid, y_valid, z_valid, t_valid)
    test_data = TensorDataset(X_test, y_test, z_test, t_test)
    train_loader = DataLoader(train_data,
                              shuffle=False,
                              sampler=sampler,
                              batch_size=model_config.batch_size,
                              drop_last=True)
    valid_loader = DataLoader(valid_data,
                              batch_size=model_config.batch_size,
                              drop_last=True)
    test_loader = DataLoader(test_data,
                             batch_size=model_config.batch_size,
                             drop_last=True)

    if (model_config.use_cuda):
        print('Run on GPU.')
    else:
        print('No GPU available, run on CPU.')

    train_model(model_config, train_loader, valid_loader)
    test_model(model_config, test_loader)



