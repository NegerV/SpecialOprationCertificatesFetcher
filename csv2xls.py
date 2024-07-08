"""
@Time: 2024/02
@author: NegerV

"""

import pandas as pd
# 导入 datetime 模块
import datetime


# 定义一个函数，接受一个list作为参数，返回提取后的list
def extract_dicts(lst):
    if len(lst) <= 1:
        return lst
        # 创建一个空集合，用来记录每个dict除了actual_review_time之外的其他项组成的元组
    tuple_set = set()
    # 遍历list中的每个dict
    for d in lst:
        # 将dict除了actual_review_time之外的其他项组成一个不可变的元组，添加到集合中
        t = tuple((k, v) for k, v in d.items() if k != 'actual_review_time')
        tuple_set.add(t)
    # 创建一个空list，用来存放提取后的dict
    result = []
    # 再次遍历list中的每个dict
    for d in lst:
        # 将dict除了actual_review_time之外的其他项组成一个不可变的元组
        t = tuple((k, v) for k, v in d.items() if k != 'actual_review_time')
        # 如果元组不在集合中，说明它没有和其他dict完全相同，可以提取
        if t not in tuple_set:
            result.append(d)
        # 如果元组在集合中，说明它和另一个dict只有actual_review_time这一项不同，需要进一步判断
        elif t in tuple_set:
            # 如果它的actual_review_time的值是""，说明它是多余的，不提取
            if d['actual_review_time'] == "":
                continue
            # 否则，说明它是有效的，可以提取
            else:
                result.append(d)
    # 返回结果list
    return result


# 获取当前的日期和时间
now = datetime.datetime.now()
# 获取当前的年份和月份
year = now.year
month = now.month

df = pd.read_csv("data.csv")
df = df.fillna("")
df = df[["unit", "name", "job_type", "get_licence_time", "busi", "operational_item", "final_review_time",
         "actual_review_time", "start_time", "end_time"]]

file_path = "./" + str(year) + "年" + str(month) + "月划小登高证.xlsx"
df.to_excel(file_path, index=False)
