import numpy as np
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import nltk
from collections import defaultdict, Counter
from nltk.corpus import wordnet
from sklearn.feature_selection import SelectKBest, chi2
from gensim.models import KeyedVectors
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

# # 下载NLTK的词性标注数据
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')

class ContextVect:
    word2vec_path = "/root/autodl-tmp/AIBRD/word2vec/word21vec.vector"
    model = KeyedVectors.load_word2vec_format(word2vec_path)
    max_length = 200
    word2vec_length = 200

    # 选取特定的上下文
    def select_context(self, target_sentence, bugreport_sentences):
        # 找到目标句子在所有句子中的索引位置
        target_index = bugreport_sentences.index(target_sentence)

        # 判断当前句子的位置并选择上下文句子
        if target_index <= 1:  # 如果目标句子是前两句
            context_sentences = bugreport_sentences[:5]
        elif target_index >= len(bugreport_sentences) - 2:  # 如果目标句子是倒数两句或最后一句
            context_sentences = bugreport_sentences[-5:]
        else:  # 其他情况选取当前句子的前两句和后两句
            start_index = max(0, target_index - 2)
            end_index = min(len(bugreport_sentences), target_index + 3)
            context_sentences = bugreport_sentences[start_index:end_index]
        context_sentences.remove(target_sentence)
        return context_sentences

    # 打包成bug reports
    def bug_reports(self, path):
        df = pd.read_csv(path)
        bug_reports_dict = {}

        # 遍历DataFrame的每一行
        for index, row in df.iterrows():
            # 获取当前行的project、id和sentence值
            project = row['project']
            id = row['id']
            sentence = row['sentence']

            # 如果project和id组合在bug_reports_dict中不存在，则创建一个新的列表来存储bugreport
            if (project, id) not in bug_reports_dict:
                bug_reports_dict[(project, id)] = []

            # 将当前行的sentence添加到相应的bugreport列表中
            bug_reports_dict[(project, id)].append(sentence)

        # 将bugreports转换为列表
        bug_reports_list = [{'project': key[0], 'id': key[1], 'bugreport': value} for key, value in
                            bug_reports_dict.items()]

        # 创建一个新的DataFrame来存储bugreports
        bug_reports_df = pd.DataFrame(bug_reports_list)
        bug_reports = list(bug_reports_df['bugreport'])
        # 将 bug_reports 中的每个 bug_report 中的每个句子都转换为字符串
        bug_reports = [[str(sentence) for sentence in bug_report] for bug_report in bug_reports]

        return bug_reports

    # NLTK处理后的句子
    def sentence_nltk(self, sentences):
        stopwords = [line.strip() for line in open('/root/autodl-tmp/AIBRD/stopword.txt', 'r').readlines()]
        sentences_cut = []
        for sentence in sentences:
            tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
            cuts = []
            for word, tag in tagged_words:
                if word.lower() not in stopwords:
                    cuts.append(word.lower())
            sentences_cut.append(cuts)

        sentences_result = []
        for ele in sentences_cut:
            ele = ' '.join(ele) + '\n'
            sentences_result.append(ele)
        return sentences_result

    # 得到关键词列表
    def extract_keywords(self, sentences, labels, positive_sentences, negative_sentences, method='tfidf', top_num=200):
        # 使用TF-IDF提取关键词
        if method == 'tfidf':
            sentences_result = self.sentence_nltk(positive_sentences)
            vectorizer = TfidfVectorizer()
            x = vectorizer.fit_transform(sentences_result)
            x = x.toarray()
            data = {'word': vectorizer.get_feature_names_out(),
                    'tfidf': x.sum(axis=0).tolist()}
            df = pd.DataFrame(data)
            df_sorted = df.sort_values(by="tfidf", ascending=False)
            keywords = df_sorted['word'].iloc[:top_num].tolist()

        # 使用信息增益TF-IDF提取关键词
        elif method == 'information':
            sentences_result = self.sentence_nltk(sentences)
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(sentences_result)

            # 使用信息增益进行特征选取
            selector_info_gain = SelectKBest(score_func=chi2, k=top_num)
            selected_features_info_gain = selector_info_gain.fit_transform(tfidf_matrix, labels)
            selected_feature_indices_info_gain = selector_info_gain.get_support(indices=True)
            selected_feature_names_info_gain = [vectorizer.get_feature_names_out()[index] for index in selected_feature_indices_info_gain]
 
            positive_related_words_list = []
            negative_related_words_list = []
            middle_related_words_list = []

            # 遍历选取的特征词语列表，统计它们在正样本和负样本中的出现次数
            for word in selected_feature_names_info_gain:
                # 统计词语在正样本中的出现次数
                count_positive = sum(word in sentence for sentence in positive_sentences)
                # 统计词语在负样本中的出现次数
                count_negative = sum(word in sentence for sentence in negative_sentences)

                # 如果词语在正样本中的出现次数多于在负样本中的出现次数，则认为它与正样本相关
                if count_positive > count_negative:
                    positive_related_words_list.append(word)
                # 如果词语在负样本中的出现次数多于在正样本中的出现次数，则认为它与负样本相关
                elif count_negative > count_positive:
                    negative_related_words_list.append(word)
                else:
                    middle_related_words_list.append(word)
            keywords = positive_related_words_list + negative_related_words_list

        elif method == 'frequency':
            tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
            key_list = []
            # 统计正样本中词性为tags的词
            for sentence in positive_sentences:
                tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
                for word, tag in tagged_words:
                    if tag in tags:
                        key_list.append(word.lower())

            key_freq = Counter(key_list)
            no_key_freq = Counter()

            # 统计负样本中词性为tags的词频
            for sentence in negative_sentences:
                tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
                for word, tag in tagged_words:
                    if tag in tags:
                        no_key_freq[word.lower()] += 1
            threshold = 100
            keywords = [word for word, freq in key_freq.most_common(200) if no_key_freq[word] < threshold]

        else:
            raise ValueError("Invalid method. Choose 'tfidf' or 'information' or 'frequency'.")

        return keywords

    # 对句子进行分词
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # 对句子列表进行分词
    def tokenize_sentences(self, sentences):
        # 创建一个空列表，用于存储所有句子的分词结果
        tokenized_words = []

        # 遍历句子列表，对每个句子进行分词
        for sentence in sentences:
            # 使用 NLTK 进行分词
            tokens = nltk.word_tokenize(sentence)
            # 将分词结果添加到 tokenized_words 列表中
            tokenized_words.extend(tokens)

        return tokenized_words

    # 对句子去停用词
    def remove_stop_sentence(self, sentence):
        stopwords = [line.strip() for line in open('/root/autodl-tmp/AIBRD/stopword.txt', 'r').readlines()]
        # 使用 NLTK 进行分词
        tokens = nltk.word_tokenize(sentence)
        # 过滤掉停用词
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
        # 将过滤后的单词重新组合成句子
        filtered_sentence = ' '.join(filtered_tokens)

        return filtered_sentence

    # 对句子列表去停用词
    def remove_stop_sentences(self, sentences):
        stopwords = [line.strip() for line in open('/root/autodl-tmp/AIBRD/stopword.txt', 'r').readlines()]
        filtered_sentences = []
        for sentence in sentences:
            if not isinstance(sentence, str):
                print("Error: sentence is not a string")
                continue  # 跳过当前句子，继续处理下一个句子
            # 使用 NLTK 进行分词
            tokens2 = nltk.word_tokenize(sentence)
            # 过滤掉停用词
            filtered_tokens = [token for token in tokens2 if token.lower() not in stopwords]
            # 将过滤后的单词重新组合成句子
            filtered_sentence = ' '.join(filtered_tokens)
            # 将处理后的句子添加到列表中
            filtered_sentences.append(filtered_sentence)

        return filtered_sentences

    # 计算keywords的共现频率
    def cooccurrence_frequency(self, bugreports, keywords):
        # 建立关键词到索引的映射
        keyword_to_index = {keyword: index for index, keyword in enumerate(keywords)}

        # 初始化共现矩阵
        cooccurrence_matrix = np.zeros((len(keywords), len(keywords)))

        # 为每个 bug report 创建关键词出现情况的字典
        bugreport_keyword_counts = []
        for bugreport in bugreports:
            keyword_counts = defaultdict(int)
            for sentence in bugreport:
                context = self.select_context(sentence, bugreport)
                sentence_processed = self.remove_stop_sentence(sentence)
                context_processed = self.remove_stop_sentences(context)
                sentence_words = self.tokenize_sentence(sentence_processed)
                context_words = self.tokenize_sentences(context_processed)
                for word1 in sentence_words:
                    for word2 in context_words:
                        if word1 in keywords and word2 in keywords:
                            keyword_counts[(word1, word2)] += 1
            bugreport_keyword_counts.append(keyword_counts)

        # 遍历每个 bug report，更新共现矩阵
        for keyword_counts in bugreport_keyword_counts:
            for (word1, word2), count in keyword_counts.items():
                index1 = keyword_to_index[word1]
                index2 = keyword_to_index[word2]
                cooccurrence_matrix[index1][index2] += count
                cooccurrence_matrix[index2][index1] += count

        return cooccurrence_matrix

    # word2vec的词嵌入
    def get_word_vector(self, word):
        words = self.model.index_to_key

        if word in words:
            vector = self.model.get_vector(word)
        else:
            vector = np.zeros(self.word2vec_length)
        return vector

    # word2vec的句嵌入
    def get_sentence_vector(self, sentence, keywords):
        tagged_word = nltk.pos_tag(nltk.word_tokenize(sentence))
        words = []
        for word, tag in tagged_word:
            if word.lower() in keywords:
                words.append(word)
        vector = np.zeros(self.word2vec_length)
        if len(words) > 0:
            vector = self.get_word_vector(words[0])
            for word in words:
                vector = (np.array(vector) + np.array(self.get_word_vector(word))) / 2
        return vector

    # 关键词特征
    def keyword_feature(self, sentences, keywords):
        word2vector = []
        for sentence in sentences:
            sentence_vector = self.get_sentence_vector(sentence, keywords)
            word2vector.append(sentence_vector)

        word2vector_feature = np.array(word2vector)
        word2vector_feature = np.tile(word2vector_feature[:, np.newaxis, :], (1, self.max_length, 1))
        return word2vector_feature

    # 单词与单词频率共现特征
    def word_cooccurrence_feature(self, cooccurrence_matrix, keyword_to_index, word1, word2):
        # 获取 word1 和 word2 的索引
        index1 = keyword_to_index[word1]
        index2 = keyword_to_index[word2]

        # 获取共现次数作为共现权重
        cooccurrence_weight = cooccurrence_matrix[index1][index2]
        weigth_factor = 0.001
        cooccurrence_vector = weigth_factor * cooccurrence_weight * self.get_word_vector(word2)

        return cooccurrence_vector

    # 共现频率矩阵特征
    def cooccurrence_feature(self, bugreports, cooccurrence_matrix, keywords):
        # 建立关键词到索引的映射
        keyword_to_index = {keyword: index for index, keyword in enumerate(keywords)}

        cooccurrence_feature = []
        for bugreport in bugreports:
            for sentence in bugreport:
                context = self.select_context(sentence, bugreport)
                sentence_processed = self.remove_stop_sentence(sentence)
                context_processed = self.remove_stop_sentences(context)
                sentence_words = self.tokenize_sentence(sentence_processed)
                context_words = self.tokenize_sentences(context_processed)

                sentence_vector = np.zeros(self.word2vec_length)
                count = 0
                for word1 in sentence_words:
                    for word2 in context_words:
                        if word1 in keywords and word2 in keywords:
                            sentence_vector += self.word_cooccurrence_feature(cooccurrence_matrix, keyword_to_index, word1, word2)
                            count += 1
                if count > 0:
                    sentence_vector = sentence_vector / count
                cooccurrence_feature.append(sentence_vector)

        cooccurrence_feature = np.array(cooccurrence_feature)
        cooccurrence_feature = np.tile(cooccurrence_feature[:, np.newaxis, :], (1, self.max_length, 1))

        return cooccurrence_feature

    # 同位关系
    def find_appositional_relationship(self, word):
        # 使用WordNet查找同位关系
        appositional_synsets = wn.synsets(word, pos=wn.NOUN)
        appositional_words = set()
        for synset in appositional_synsets:
            appositional_words.update([lemma.name() for lemma in synset.lemmas()])
        return appositional_words

    # 组成关系
    def find_compositional_relationship(self, word):
        # 使用WordNet查找组成关系
        compositional_synsets = wn.synsets(word, pos=wn.NOUN)
        compositional_words = set()
        for synset in compositional_synsets:
            hypernyms = synset.hypernyms()  # 获取上位词
            for hypernym in hypernyms:
                compositional_words.update([lemma.name() for lemma in hypernym.lemmas()])
        return compositional_words

    # 同位、组成关系特征
    def apposition_feature(self, bugreports, keywords):
        apposition_feature = []
        for bugreport in bugreports:
            for sentence in bugreport:
                sentence_processed = self.remove_stop_sentence(sentence)
                sentence_words = self.tokenize_sentence(sentence_processed)

                sentence_vector = np.zeros(self.word2vec_length)
                count_word = 0
                for word in sentence_words:
                    if word in keywords:
                        word_feature = np.zeros(self.word2vec_length)
                        apposition_composition_words = list(self.find_appositional_relationship(word).union(self.find_compositional_relationship(word)))
                        count = len(apposition_composition_words)
                        for word1 in apposition_composition_words:
                            word_feature += self.get_word_vector(word1)
                        if count > 1:
                            word_feature = word_feature / count
                        sentence_vector += word_feature
                        count_word += 1
                if count_word > 1:
                    sentence_vector = sentence_vector / count_word
                apposition_feature.append(sentence_vector)

        apposition_feature = np.array(apposition_feature)
        apposition_feature = np.tile(apposition_feature[:, np.newaxis, :], (1, self.max_length, 1))

        return apposition_feature
    

        # 获取ambiguity句子的共现矩阵特征
    def ambiguity_cooccurrence_feature(self, ambiguity_sentences, cooccurrence_matrix, keywords):
        # 建立关键词到索引的映射
        keyword_to_index = {keyword: index for index, keyword in enumerate(keywords)}

        cooccurrence_feature = []
        for ambiguity_sentence in ambiguity_sentences:
            ambiguity_context = self.get_ambiguity_context('/root/autodl-tmp/AIBRD/new_statistic.csv', '/root/autodl-tmp/AIBRD/ambiguity_statistic_total.CSV', ambiguity_sentence)
            sentence_processed = self.remove_stop_sentence(ambiguity_sentence)
            context_processed = self.remove_stop_sentences(ambiguity_context)
            sentence_words = self.tokenize_sentence(sentence_processed)
            context_words = self.tokenize_sentences(context_processed)

            sentence_vector = np.zeros(self.word2vec_length)
            count = 0
            for word1 in sentence_words:
                for word2 in context_words:
                    if word1 in keywords and word2 in keywords:
                        sentence_vector += self.word_cooccurrence_feature(cooccurrence_matrix, keyword_to_index, word1, word2)
                        count += 1
            if count > 0:
                sentence_vector = sentence_vector / count
            cooccurrence_feature.append(sentence_vector)
        cooccurrence_feature = np.array(cooccurrence_feature)
        cooccurrence_feature = np.tile(cooccurrence_feature[:, np.newaxis, :], (1, self.max_length, 1))

        return cooccurrence_feature
    
    # 获取ambiguity数据集的同位关系特征
    def ambiguity_apposition_feature(self, ambiguity_sentences, keywords):
        apposition_feature = []
        for sentence in ambiguity_sentences:
            sentence_processed = self.remove_stop_sentence(sentence)
            sentence_words = self.tokenize_sentence(sentence_processed)

            sentence_vector = np.zeros(self.word2vec_length)
            count_word = 0
            for word in sentence_words:
                if word in keywords:
                    word_feature = np.zeros(self.word2vec_length)
                    apposition_composition_words = list(self.find_appositional_relationship(word).union(self.find_compositional_relationship(word)))
                    count = len(apposition_composition_words)
                    for word1 in apposition_composition_words:
                        word_feature += self.get_word_vector(word1)
                    if count > 1:
                        word_feature = word_feature / count
                    sentence_vector += word_feature
                    count_word += 1
            if count_word > 1:
                sentence_vector = sentence_vector / count_word
            apposition_feature.append(sentence_vector)

        apposition_feature = np.array(apposition_feature)
        apposition_feature = np.tile(apposition_feature[:, np.newaxis, :], (1, self.max_length, 1))

        return apposition_feature

    
    # 获取ambiguity句子的在bug report中的上下文
    def get_ambiguity_context(self, file1_path, file2_path, ambiguity_sentence):
        # 读取CSV文件
        file1 = pd.read_csv(file1_path)
        file2 = pd.read_csv(file2_path)

        # 找到第二个文件中给定句子所在的行索引
        sentence_index = file2[file2['sentence'] == ambiguity_sentence].index

        if not sentence_index.empty:
            # 从第一个文件中找到相同句子的位置
            # 假设 project 和 id 也匹配
            project_id = file2.loc[sentence_index[0], 'project']
            sentence_id = file2.loc[sentence_index[0], 'id']

            # 在第一个文件中查找相同的行
            row_index = file1[(file1['project'] == project_id) &
                            (file1['id'] == sentence_id) &
                            (file1['sentence'] == ambiguity_sentence)].index

            if not row_index.empty:
                # 获取目标行索引
                target_index = row_index[0]

                # 获取上下文（上两句和下两句），排除目标句子
                start_index = max(0, target_index - 2)  # 防止索引越界
                end_index = min(len(file1), target_index + 3)  # 防止索引越界

                # 提取上下文内容
                context = file1.iloc[start_index:end_index]

                # 移除目标句子
                context = context[context['sentence'] != ambiguity_sentence]

                # 将上下文内容转换为列表
                context_list = context['sentence'].tolist()

                return context_list
            else:
                print(f"在第一个文件中未找到句子: {ambiguity_sentence}")
                return ['','','','']
        else:
            print(f"在第二个文件中未找到句子: {ambiguity_sentence}")
            return ['','','','']

    def plot_cooccurrence_graph(self, keywords, cooccurrence_matrix, save_path=None):
        # Step 1: 创建空的无向图
        G = nx.Graph()

        # Step 2: 添加节点
        G.add_nodes_from(keywords)

        # Step 3: 添加边和权重
        for i, word1 in enumerate(keywords):
            for j, word2 in enumerate(keywords):
                if i != j and cooccurrence_matrix[i][j] > 0.1:  # 只添加共现频率大于0.1的边，去除低权重边
                    G.add_edge(word1, word2, weight=cooccurrence_matrix[i][j])

        # Step 4: 生成不同颜色的节点
        colors = []
        for _ in range(len(keywords)):
            # 生成随机颜色
            colors.append("#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]))

        # Step 5: 使用 kamada_kawai_layout 布局算法，适合小图，优化美观
        pos = nx.kamada_kawai_layout(G)
        
        # 根据节点度数调整节点大小
        node_sizes = [300 + 1000 * G.degree(node) for node in G.nodes]

        # 根据权重绘制边的宽度
        edges = G.edges(data=True)
        edge_weights = [d['weight'] for (u, v, d) in edges]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=edge_weights, edge_color=edge_weights, edge_cmap=plt.cm.Blues)

        # 绘制节点，使用不同颜色和调整过的大小
        nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=node_sizes)

        # 绘制节点标签
        nx.draw_networkx_labels(G, pos, font_size=8)

        # 添加标题
        plt.title('Keyword Co-occurrence Graph', fontsize=16)

        # 保存或显示图像
        if save_path:
            plt.savefig(save_path, format='png')
            print(f"Graph saved as {save_path}")
        else:
            plt.show()



