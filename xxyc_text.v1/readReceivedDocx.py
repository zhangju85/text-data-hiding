from docx import Document
import hashlib

'''
    生成接收word文本的摘要
'''
class receivedDocxAbst():
    def __init__(self, filePath):
        self.filepath = filePath

    def generateAbst(self):
        # word文件的位置
        document = Document(self.filepath)

        # 读取word文件的内容
        all_paragraphs = document.paragraphs
        # 设置totalText,合并所有段后,生成摘要
        totalText = ""
        # 空格会影响SHA256的摘要,因此空格也必须保留
        for paragraph in all_paragraphs:
            totalText = totalText + paragraph.text

        # 利用SHA256算法,将word的文本生成摘要
        hash = hashlib.sha256();
        hash.update(bytes(totalText, encoding='utf-8'))
        return hash.hexdigest()


'''
    指标：防御能力
'''
def defense_capacity(file):
    defense_indicate = 1
    print("defense_indicate", defense_indicate)
    oda = receivedDocxAbst(file)
    abst1 = oda.generateAbst()
    print("新的摘要： " , abst1)
    if abst != abst1:
        defense_indicate = 0
    print("defense_indicate", defense_indicate)


if __name__ == '__main__':
    oda = receivedDocxAbst('3.docx')
    abst = oda.generateAbst()
    print("接收文本的摘要: " + abst)
    defense_capacity('adding.docx')


    # defense_indicate = 1
    # print("defense_indicate", defense_indicate)
    # oda = receivedDocxAbst('color.docx')
    # abst1 = oda.generateAbst()
    # print("color.docx: " + abst1)
    # if abst != abst1:
    #     defense_indicate = 0
    # print("defense_indicate", defense_indicate)
        # oda = receivedDocxAbst('removing.docx')
        # abst2 = oda.generateAbst()
        # print("removing.docx: " + abst2)
        # if abst != abst2:
        #     defense_indicate = 0
        #     print("defense_indicate", defense_indicate)




