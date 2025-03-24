import nltk
from collections import Counter
import pandas as pd

# 下载NLTK的词性标注数据
nltk.download('averaged_perceptron_tagger')

df = pd.read_csv("statistic_label.csv")
df.dropna(subset=['sentence'], inplace=True)
sentences_with_label_not_zero = df.loc[df['label'] != 0, 'sentence']  # 获取标签不为0的句子
sentences_with_label_zero = df.loc[df['label'] == 0, 'sentence']  # 获取标签为0的句子

# 定义名词和动词的词性标签
noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

# 初始化名词和动词列表
noun_list = []
verb_list = []

# 遍历每个句子
for sentence in sentences_with_label_not_zero:
    # 对句子进行词性标注
    tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))

    # 提取名词和动词
    for word, tag in tagged_words:
        if tag in noun_tags:
            noun_list.append(word.lower())  # 将名词转换为小写形式并加入名词列表
        elif tag in verb_tags:
            verb_list.append(word.lower())  # 将动词转换为小写形式并加入动词列表

# 统计词频并取出出现频率前100的名词和动词
noun_freq = Counter(noun_list)
verb_freq = Counter(verb_list)

# 标签为0的句子中关键词的词频统计
noun_freq_label_zero = Counter()
verb_freq_label_zero = Counter()

# 遍历标签为0的句子
for sentence in sentences_with_label_zero:
    # 对句子进行词性标注
    tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))

    # 统计名词和动词出现的词频
    for word, tag in tagged_words:
        if tag in noun_tags:
            noun_freq_label_zero[word.lower()] += 1
        elif tag in verb_tags:
            verb_freq_label_zero[word.lower()] += 1

# 过滤关键词列表中在标签为0的句子中出现频率较多的关键词
threshold = 200
filtered_nouns = [noun for noun, freq in noun_freq.most_common(100) if noun_freq_label_zero[noun] < threshold]
filtered_verbs = [verb for verb, freq in verb_freq.most_common(100) if verb_freq_label_zero[verb] < threshold]

print("Filtered Nouns:", filtered_nouns)
print("Filtered Verbs:", filtered_verbs)
print(len(filtered_nouns))
print(len(filtered_verbs))

# # 打开文件以写入模式
# with open("filtered_nouns.txt", "w", encoding="utf-8") as noun_file:
#     # 写入名词
#     noun_file.write("Filtered Nouns:\n")
#     for noun in filtered_nouns:
#         noun_file.write(noun + "\n")
#
# # 打开文件以写入模式
# with open("filtered_verbs.txt", "w", encoding="utf-8") as verb_file:
#     # 写入动词
#     verb_file.write("Filtered Verbs:\n")
#     for verb in filtered_verbs:
#         verb_file.write(verb + "\n")
