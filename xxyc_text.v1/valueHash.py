

'''
    生成原始word文本的摘要
'''
import binascii
import numpy as np

from readOriginalDocx import orignalDocxAbst
import  MPM #get_global_num_pixels_changed from

# a=MPM.get_global_num_pixels_changed()

# np.set_printoptions(threshold=np.inf)


from docx import Document
import hashlib


class orignalDocxAbst():
    def __init__(self, filePath):
        self.filepath = filePath

    def generateAbst(self):
        # word文件的位置
        document = Document(self.filepath)

        # 只能读取非表格的word文本,可以分段
        # print("读取非表格中的内容：")
        all_paragraphs = document.paragraphs
        # 测试all_paragraphs的类型,list
        # print(type(all_paragraphs))

        # 打印每个段落的内容
        # for paragraph in all_paragraphs:
            # print(paragraph.text)
            # 测试paragraph的类型,str
            # print(type(paragraph.text))

        # 设置totalText,合并所有段后,生成摘要
        totalText = ""

        # 空格会影响SHA256的摘要,因此空格也必须保留
        for paragraph in all_paragraphs:
            totalText = totalText + paragraph.text

        # 整个word的文本
        # print("整个word的文本: " + totalText)

        # 利用SHA256算法,将word的文本生成摘要
        hash = hashlib.sha256();
        hash.update(bytes(totalText, encoding='utf-8'))
        digest = hash.hexdigest()
        # print("原摘要: " + ZhaiYao)

        return digest

    # if __name__ == '__main__':
    #     oda = orignalDocxAbst("Purchasing Contract.docx")
    #     abst = oda.generateAbst()
    #     print("OriginalHash: " + abst)
