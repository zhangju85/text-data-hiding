import numpy as np

from readOriginalDocx import orignalDocxAbst

oda = orignalDocxAbst("text exam.docx")
abst = oda.generateAbst()
print("abst的类型：",type(abst))
def biAbsthash(dig):
        # print("OriginalHash: " +dig)   #使用int函数将16进制字符串转化为10进制整数
        a = [dig[i:i + 2] for i in range(0, len(dig), 2)]
        print("a", a)
        # x = bin(int(dig, 16))[2:]
        # # print("hash值的二进制编码", b)
        # a = list(x)
        # # b = np.array(a)
        listdigests = []
        for i in range(len(a)):
                # print(int(output[i],16))
                listdigests.append(int(a[i], 16))
        # print("listSecrets", listdigests)

        # TODO 将每个byte的10进制转化为二进制数组
        list_data = []
        for j in range(len(listdigests)):
                binarySecrets = (str(bin(int(listdigests[j]))).replace("0b", "")).zfill(8)
                # print("binarySecrets", binarySecrets)
                for i in range(len(binarySecrets)):
                        # 二进制转成list
                        list_data.append(int(binarySecrets[i]))
        temp1 = np.array(list_data)
        # print("temp", temp1)
        return temp1
print("b",biAbsthash(abst))

