import pandas as pd
from collections import Counter

# 读取CSV文件
df = pd.read_csv('statistic.csv')

# 创建一个空的 Counter 对象
pattern_counter = Counter()

# 遍历每一行
for index, row in df.iterrows():
    patterns = str(row['patterns'])
    patterns = patterns.split(',') if ',' in patterns else [patterns]
    pattern_counter.update(patterns)

# 使用most_common方法按频率降序排列统计结果
sorted_pattern_counts = pattern_counter.most_common()

# 打开一个txt文件用于写入结果
with open('pattern_counts.txt', 'w') as file:
    # 写入统计结果
    for pattern, count in sorted_pattern_counts:
        file.write(f"{pattern}: {count}\n")

