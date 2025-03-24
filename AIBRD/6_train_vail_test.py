import random

# 读取数据文件
with open('unique_kg.txt', 'r',  encoding='utf-8') as file:
    data_lines = file.readlines()

# 打乱数据
random.shuffle(data_lines)

# 计算分割比例
total_lines = len(data_lines)
train_size = int(0.8 * total_lines)
valid_size = int(0.1 * total_lines)

# 分割数据
train_data = data_lines[:train_size]
valid_data = data_lines[train_size:train_size+valid_size]
test_data = data_lines[train_size+valid_size:]

# 写入分割后的数据文件
with open('train.txt', 'w',  encoding='utf-8') as file:
    file.writelines(train_data)

with open('valid.txt', 'w',  encoding='utf-8') as file:
    file.writelines(valid_data)

with open('test.txt', 'w',  encoding='utf-8') as file:
    file.writelines(test_data)
