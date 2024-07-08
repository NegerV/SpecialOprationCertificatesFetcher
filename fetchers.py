"""
@Time: 2024/02
@author: NegerV

"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from captcha_identifier import recognize_text
from license_fetcher import *
import pandas as pd
import os
import csv

# 不直接打开
edge_options = Options()
edge_options.add_argument("--headless")

# 筛选
df = pd.read_excel("./综合化维护人员台账.xls")
# df = df.drop(0)
df = df.fillna("")
tmp_list = list()
code2name_list = list()
for col in ["姓名", "身份证号码", "经营单元", "岗位类型"]:
    lst = df[col].tolist()
    tmp_list.append(lst)

for i in range(len(tmp_list[0])):
    # print(type(tmp_list[-1][i]))
    # 身份证号码, 姓名, 经营单元, 岗位类型
    lst = [tmp_list[1][i].strip(), tmp_list[0][i].strip(), tmp_list[2][i].strip(), tmp_list[-1][i].strip()]
    code2name_list.append(lst)


# 获取数据
def output2files(data):
    # 检查文件是否存在，如果不存在，就创建一个空文件
    if not os.path.exists("./data.csv"):
        open("./data.csv", "w", encoding="utf-8").close()

    for d in data:
        with open("./data.csv", "a", encoding="utf-8") as csv_file:
            # 创建一个csv写入器，指定字段名和分隔符
            writer = csv.DictWriter(csv_file, fieldnames=d.keys(), delimiter=",")
            # 如果文件是空的，就写入表头（字段名）
            if os.stat("./data.csv").st_size == 0:
                writer.writeheader()
            # 写入一行数据，使用字典的值
            writer.writerow(d)


for lst in code2name_list[:]:
    count = code2name_list.index(lst) + 1
    driver = webdriver.Edge(options=edge_options)
    # driver.maximize_window()
    driver.get("https://cx.mem.gov.cn/special?index=0")
    # my_action = ActionChains(driver)
    sleep(2)
    # 证件类型
    span = driver.find_element(By.XPATH,
                               "//*[@id='app']/div/div[2]/div[2]/div/div[2]/div[1]/form/div[1]/div/div/div[1]/input")
    # my_action.move_to_element(span)
    span.click()
    sleep(1)
    span = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/ul/li[1]")
    # my_action.move_to_element(span)
    span.click()

    # 证件号码
    usercode = driver.find_element(By.XPATH,
                                   "//*[@id='app']/div/div[2]/div[2]/div/div[2]/div[1]/form/div[2]/div/div/input")
    usercode.send_keys(lst[0])

    # 姓名
    username = driver.find_element(By.XPATH,
                                   "//*[@id='app']/div/div[2]/div[2]/div/div[2]/div[1]/form/div[3]/div/div/input")
    username.send_keys(lst[1])

    # 根据图片源属性值定位元素
    captcha_codes = 0
    source = driver.page_source + "验证码错误"
    while int(captcha_codes) not in range(1000, 10000) or "验证码错误" in source:
        # 定位验证码位置
        image = driver.find_element(By.XPATH,
                                    "//*[@id='app']/div/div[2]/div[2]/div/div[2]/div[1]/form/div[4]/div/div/img")
        image.click()
        # 缓冲等待时间
        sleep(3)
        image_data = image.screenshot("./captcha.png")  # 截取当前显示区域内该元素的截图数据
        captcha_codes = recognize_text("./captcha.png")  # 调用函数获取

        # 输入验证码
        captcha_element = driver.find_element(By.XPATH,
                                              "//*[@id='app']/div/div[2]/div[2]/div/div[2]/div[1]/form/div[4]/div/div[1]/div/input")
        captcha_element.clear()
        captcha_element.send_keys(captcha_codes)
        source = driver.page_source

        # 输入确认
    enter = driver.find_element(By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div/div[2]/div[1]/div/button[2]")
    enter.click()

    # 加载时间
    sleep(2)

    # 获取刷新后页面信息
    source = driver.page_source
    with open('./test.html', "w", encoding="utf-8") as fp:
        fp.write(source)

    return_button = driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div[2]/div[2]/button[2]")

    if "没有查询到相关证件信息！" in source:
        print("当前表格编号:", count, ", 没有查询到相关证件信息!", "问题员工:", lst[1])
        license_data = get_error_license_data(lst[2], lst[0], lst[1], lst[-1])
        output2files(license_data)
        print(license_data)
    else:
        print("当前表格编号:", count, ", 没事，当前员工为:", lst[1])
        license_data = get_license_data(lst[2], lst[0], lst[1], lst[-1])
        if len(license_data) == 0:
            license_data = get_empty_license_data(lst[2], lst[0], lst[1], lst[-1])
        output2files(license_data)
        print(license_data)

    driver.close()
