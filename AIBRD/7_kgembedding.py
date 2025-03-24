import pandas as pd
import numpy as np
import re

def clean_sentence(sentence):
    characters_to_replace = ['.', '`', '*', '#', '$', '~', '"', '<', '>', '(', ')', '»', '«']
    for char in characters_to_replace:
        sentence = sentence.replace(char, '')
    sentence = re.sub(r'--', ' ', sentence)
    sentence = sentence.lower()
    sentence = ' '.join(sentence.split())
    return sentence


data = pd.read_csv("statistic_label.csv")
data.dropna(subset=['sentence'], inplace=True)
sentences = list(data['sentence'].apply(str))

cleaned_sentences = [clean_sentence(sentence) for sentence in sentences]
# 分配标号给非空句子，并保持原始顺序
current_id = 0

# 匹配原始数据集中被cleaned后为空的句子置为-1，按照顺序重新编码
final_sentences_with_ids = []

for i in range(len(sentences)):
    sentence = sentences[i]
    cleaned_sentence = cleaned_sentences[i]

    if cleaned_sentence:  # 如果清理后的句子不为空
        final_sentences_with_ids.append((current_id, sentence))
        current_id += 1
    else:  # 如果清理后的句子为空
        final_sentences_with_ids.append((-1, sentence))

# 输出最终结果
# for sentence_id, sentence in final_sentences_with_ids:
#     print(f"ID: {sentence_id}, Sentence: {sentence}")

# 读取包含索引和句子的文本文件
with open('triple.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()

# 创建一个字典，将索引映射到句子
Dict = {}   # ID对应的三元组为
current_index = None
id = 0
for entry in data:
    # 去除首尾空格
    entry = entry.strip()
    # 确保不是空行
    if entry:
        current_index, triple = id, entry.split('\t', 1)
        id = id + 1
        Dict[current_index] = triple

id_triple_dict = {}
for index, triple in Dict.items():
    if len(triple) == 1:
        id_triple_dict[index] = ""
    else:
        id_triple_dict[index] = triple[1]
# 输出id和triple
# for index, sentence in id_triple_dict.items():
#     print(f"ID: {index}, Triple: {sentence}")

# 将id，sentence，triple对应存储到id_sentence_triple
id_sentence_triple = []
for index1, sentence in final_sentences_with_ids:
    if index1 != -1:
        triple = id_triple_dict.get(index1, '')
        id_sentence_triple.append([index1, sentence, triple])
    else:
        id_sentence_triple.append([index1, sentence, ''])

# 读入entities和relations
entities = pd.read_csv("kg_task/data/kg/entities.tsv")
relations = pd.read_csv("kg_task/data/kg/relations.tsv")
entities = list(entities['entity'].apply(str))
relations = list(relations['relation'].apply(str))

# 读入entity_embedding和relation_embedding
entity_embedding = np.load("kg_task/ckpts/TransE/kg_TransE_l2_entity.npy")
relation_embedding = np.load("kg_task/ckpts/TransE/kg_TransE_l2_relation.npy")

# 计算出三元组的向量
def triple_embedding(entity1, relationship, entity2):
    entity1_index = entities.index(entity1)
    relationship_index = relations.index(relationship)
    entity2_index = entities.index(entity2)

    entity1_embedding = entity_embedding[entity1_index]
    relationship_embedding = relation_embedding[relationship_index]
    entity2_embedding = entity_embedding[entity2_index]
    print(entity1_embedding)
    print(len(entity1_embedding))
    print(relationship_embedding)
    print(entity2_embedding)

triple_embedding('docker', 'doesn\'t log', 'exec commands')



