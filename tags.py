import numpy as np
import pandas as pd
import csv

f = open('Tags.csv','w',encoding='utf-8')

csv_writer = csv.writer(f)

csv_writer.writerow(['tag1', 'tag2', 'tag3', 'tag4'])


# # 创建一个示例DataFrame
# data = {'A': [1, 2, 3],
#         'B': [4, 5, 6],
#         'C': [7, 8, 9],
#         'D': [10, 11, 12],
#         'E': [13, 14, 15]}
# df = pd.DataFrame(data)


# df.to_csv('Tags.csv')
