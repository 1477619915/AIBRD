import numpy as np
from gensim.models import KeyedVectors,word2vec,Word2Vec
import jieba
import multiprocessing
import pandas as pd
import nltk
print("word2vec程序开始运行！")

# 下载NLTK的词性标注数据
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


def stopwordlist():
    stopwords = [line.strip() for line in open('autodl-tmp/stopword.txt', 'r').readlines()]
    return stopwords


# 读取数据集中非0标签的句子
data = pd.read_csv('autodl-tmp/new_statistic.csv')
print("word2vec程序开始运行！")
data.dropna(subset=['sentence'], inplace=True)
sentences = list(data['sentence'].apply(str))
sentences = [sentence for sentence, label in zip(sentences, data['label']) if label != 0]

stopwords = stopwordlist()
sentences_cut = []

# nltk分词
for sentence in sentences:
    tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
    cuts = []
    for word, tag in tagged_words:
        if word not in stopwords:
            cuts.append(word.lower())
    sentences_cut.append(cuts)

with open('autodl-tmp/data.txt', 'w', encoding='utf-8') as f:
    for ele in sentences_cut:
        f.write(str(ele))

sentences = list(word2vec.LineSentence('autodl-tmp/data.txt'))

model = Word2Vec(sentences, vector_size=200, min_count=3, window=5, sg=0, workers=multiprocessing.cpu_count())
print(model)

model.save('/root/autodl-tmp/word2vec/word2vec.model')
model.wv.save_word2vec_format('/root/autodl-tmp/word2vec/word21vec.vector')
model.wv.save_word2vec_format('/root/autodl-tmp/word2vec/word21vec.bin')






