import logging
import re
import pandas as pd
from SparkApi import SparkApi
import string

# 星火大模型账号：汤宇航
appid = "ac206fdc"     # 填写控制台中获取的 APPID 信息
api_secret = "NDRlMzVkMzg5NTg5ZGUzOGE5MTFmNTA1"   # 填写控制台中获取的 APISecret 信息
api_key ="f666001df752c2f0cc59cdbe48c1d418"    # 填写控制台中获取的 APIKey 信息

#  用于配置大模型版本
domain = "generalv3"   # v3.0版本

# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址

text =[]

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

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

sentences = [clean_sentence(sentence) for sentence in sentences]
sentences = [value for value in sentences if value]

head_list = []
relationship_list = []
tail_list = []
total = 4911

# 配置日志
logging.basicConfig(filename='triple_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 写入匹配的三元组
file_path = "triple.txt"
for i in range(4911, len(sentences)):
    text.clear()
    SparkApi.answer = ""
    total = total + 1
    sentence = sentences[i]
    question = checklen(getText("user", "从句子中提取（实体，关系，实体）三元组，输出格式为：(entity,relationship,entity)，"
                                        "如果不满足三元组或者没有提供句子，返回不存在即可，不用说其他的,句子为：" + sentence))
    try:
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    except Exception as e:
        print("total的值为：", total)
        break

    pattern = r'(\([^)]+\))'
    matches = re.findall(pattern, SparkApi.answer)
    if matches is not None:
        with open(file_path, 'a') as file:  # 使用 'a' 模式打开文件
            file.write(f"{i}\t")
            for head_rela_tail in matches:
                if re.findall(r'不存在', head_rela_tail):
                    continue
                head = re.findall(r'\((.*?),', head_rela_tail)
                rela = re.findall(r',(.*?),', head_rela_tail)
                tail = re.findall(r',([^,]+)\)', head_rela_tail)
                if not head or not rela or not tail:
                    continue
                head_list.append(head[0])
                relationship_list.append(rela[0])
                tail_list.append(tail[0])

                # 实时写入文件
                file.write(f"({head[0]},{rela[0]},{tail[0]})\t")

                # 记录到日志
                logging.info(f"Processed total={total}, head={head[0]}, rela={rela[0]}, tail={tail[0]}")
            file.write(f"\n")

print(f"Data written to {file_path}")






