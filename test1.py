# import test2
# def show():
#     print("test01")
#
# if __name__ == '__main__':
#     show()
#     test2.show2()

# -*- coding: UTF-8 -*_
from PIL import Image
import pytesseract
import json
import re
import os


class Languages:
    CHS = 'chi_sim'     # 中文
    CHT = 'chi_tra'     # 繁体
    ENG = 'eng'         # 英文

# 调用tesseract-ocr
def img_to_str(image_path, lang):
    return pytesseract.image_to_string(Image.open(image_path), lang)

def save(text):
    # 遍历后的图片提取文字，保存到txt
    fs = open("gg_ocr.txt", 'w+', encoding='utf-8')
    fs.write(text)
    fs.close()
    # file = open("../txt/gg_ocr.txt", 'w+', encoding='utf-8')
    # # 格式化存储
    # for k, v in re.items():
    #     line = "filename :" + name + "\t" + k.encode("utf-8") + "\t" + str(v) + "\n"
    #     file.write(line)
    # file.close()

def main(image_path):
    if image_path is None or len(image_path) == 0:
        print("图片不存在。")
    else:
        # 识别
        lang = Languages.ENG
        text = img_to_str(image_path, lang)
        print("内容？", text, type(text))
        # 保存
        save(text)
if __name__=='__main__':
    print('当前路径是：', os.getcwd())
    image_path = '3.jpg'
    main(image_path)
    print("识别完成。")