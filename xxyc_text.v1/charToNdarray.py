import binascii
import numpy as np
np.set_printoptions(threshold=np.inf)


from docx import Document
import hashlib

'''
    生成原始word文本的摘要
    生成秘密信息
'''




# TODO 将字转化成对应的二进制数组

# 文字转ndarray,存到word文档中
# charStr = "我叫李藤"
# 参数charStr应该改成文件，



    # # print(binascii.b2a_hex(charStr.encode("utf8")))
    # # print(charStr.encode("utf8"))
    # # print(str(binascii.b2a_hex(charStr.encode("utf8")))[2:-1])
    # #
def charToNdarray(charStr):

    # TODO 先对charStr进行编码，转换成二进制，再用binascii.b2a_hex转化成16进制
    charStr = str(binascii.b2a_hex(charStr.encode("utf8")))[2:-1]
    # print("utf8",charStr.encode("utf8"))
    print("charStr", charStr)
    print("len(charStr)",len(charStr))

    n = 2
    # TODO 每两个16进制放在一起，就是一个byte 8位
    output = [charStr[i:i + n] for i in range(0, len(charStr), n)]
    print("output",output)

    # TODO 每个byte对应的十进制
    listSecrets = []
    for i in range(len(output)):
        # print(int(output[i],16))
        listSecrets.append(int(output[i], 16))
    print("listSecrets",listSecrets)

    # TODO 将每个byte的10进制转化为二进制数组
    list_data = []
    for j in range(len(listSecrets)):
        binarySecrets = (str(bin(int(listSecrets[j]))).replace("0b", "")).zfill(8)
        print("binarySecrets",binarySecrets)
        for i in range(len(binarySecrets)):
            # 二进制转成list
            list_data.append(int(binarySecrets[i]))
    temp = np.array(list_data)
    print("temp",temp)
    return temp

# charStr = str(binascii.b2a_hex(abst.encode("utf8")))[2:-1]
# print("abst:" +abst)
# print("charStr:" +charStr)
# n = 2
# output = [charStr[i:i + n] for i in range(0, len(charStr), n)]
# print("output:" +output)
print("秘密信息的二进制编码",charToNdarray('1111111111'))
# def charToNdarray(charStr):
# b=bin(int(abst,16))[2:] # 我写的
# listHash = []
# listHash = listHash.append(b)
# print("listHash",listHash)
# print("hash值的二进制编码",b)

