import binascii
# -*- coding: utf-8 -*-
import numpy as np

binaryBit = "111001101000100010010001"
"""
二进制流转化为对应字符

"""
def strToChar(binaryBit):
    # TODO 将每8个位变成一组，
    n = 8
    output = [binaryBit[i:i+n] for i in range(0, len(binaryBit), n)]

    # TODO 将每8个位变成10进制数  [230, 136, 145]
    listPixels = []
    for i in range(len(output)):
        # print(int(output[i],2))
        listPixels.append(int(output[i],2))


    print("listPixels",listPixels)

    # TODO 变成16进制 ['e6', '88', '91']
    list_data = []
    for j in range(len(listPixels)):
        binaryPixel = ((hex(int(listPixels[j]))).replace("0x", "")).zfill(2)
        list_data.append((binaryPixel))

    print("list_data",list_data)

    byteStr = ""
# todo ['e6', '88', '91'] to e68891 数组合在一起
    for t in range(len(list_data)):
        byteStr = byteStr + list_data[t]

    print("byteStr" ,byteStr)

    s = bytes(byteStr, encoding="utf8")
    print(s)
    #返回由十六进制字符串hexstr表示的二进制数据
    res = binascii.a2b_hex(s)
    print("res",res)
    # todo e68891 to "我" 将16进制数变为字符
    print("res.decodeutf8",res.decode("utf8"))

    return res.decode("utf8")
# print(strToChar("111001101000100010010001"))