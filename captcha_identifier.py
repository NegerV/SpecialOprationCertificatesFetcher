"""
@Time: 2024/02
@author: NegerV

"""

# 导入requests和cv2库，用于发送HTTP请求和处理图片
import requests
import cv2
# 导入计算机识别模块
import pytesseract
# 导入图像模块，形成图像
from PIL import Image
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# 定义一个函数，用于识别验证码

pytesseract.pytesseract.tesseract_cmd = r'D:\个人软件\图像识别\Tesseract-OCR\tesseract.exe'


def recognize_text(image):
    # 读取图像文件，转换为灰度图
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用pytesseract库，对图像进行数字识别，得到文本结果
    text = pytesseract.image_to_string(gray, config="--psm 6 digits")

    # 打印文本结果
    return text
