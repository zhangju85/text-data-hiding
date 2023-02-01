import docx
import numpy as np
import math
# -*- coding: utf-8 -*-
from MPM import MPM2022
from binhash import biAbsthash
from strToChar import strToChar

"""
    恢复过程：
    先恢复k+1位，再恢复剩下的K位的秘密信息，组合在一起

"""
def MPMrecover(word_updated_rgbList, secret_string_size, k=3):
    #print("word_updated_rgbList:",word_updated_rgbList)
    n = 3
    numBitsPerPG = n * k + 1  # 每组pixcel嵌入的bit数
    numSecretGroups = math.ceil(secret_string_size / numBitsPerPG)
    #print("numSecretGroups:", numSecretGroups)
    moshu0 = 2 ** (k + 1) #模数的底数,k+1位bits的底数
    moshu1 = 2 ** k #模数的底数
    RChannel_array  = np.array(word_updated_rgbList)
    #print("RChannel_array:", RChannel_array)
    # 恢复，提取加密数据
    recover_d_array = np.zeros(numSecretGroups)
    #print("recover_d_array:", recover_d_array)
    B = ""#整个秘密信息
    for i in range(0, numSecretGroups,1):
        #恢复k+1位的秘密信息
        selIndex = i % n
        #print("selIndex",selIndex)
        #print("RChannel_array[i, selIndex]:", RChannel_array[i, selIndex])#嵌入后的像素值
        v1 =RChannel_array[i, selIndex] % moshu0 #word_updated_rgbList[i, selIndex]指的是嵌入函数中的PGembedded，嵌入后的像素组
        # v1指的是提取出来的十进制的秘密信息
        #print("moshu0", moshu0)
        B1= bin(v1)[2:].zfill(4)#转换成二进制
        #print("V1",v1)

        #print("B1", B1)
        # print("B1的类型",type(B1))

        # # 恢复剩余的n-1 pixel
        tmpValue = 0
        for j2 in range(0, selIndex, 1):
            v2 =  RChannel_array[i, j2] % moshu1
            B2= bin(v2)[2:].zfill(3)
            #print("moshu1", moshu1)
            #print("v2",v2)
            #print("B2", B2)
            B1 = B1 + B2
            #print("B1", B1)

            # tmpValue += v3 * (2 ** ((n - j2 - 2) * k))
        for j2 in range(selIndex + 1, n, 1):
            v2 =  RChannel_array[i, j2] % moshu1
            # tmpValue += v3 * (2 ** ((n - j2 - 1) * k))
            B2 = bin(v2)[2:].zfill(3)
            #print("v2", v2)
            #print("B2", B2)
            B1 = B1 + B2
            #print("B1", B1)
        #print("B1", B1)
        B += B1
    #print("B", B)
        # C1 = C1+B1
        # print("C1", C1)
        # recover_d_array[i] = v2 + tmpValue
    #     assert (int((recover_d_array[i] - secret_d_array[i]).sum()) == 0)#secret_d_array表待嵌入的秘密值
    #
    # assert (int((recover_d_array - secret_d_array).sum()) == 0)

    # print("===================")
    # resultList = ""
    # 恢复出的和以前的应该是一致的
    # for i in range(0, numSecretGroups):
    #     #print(int(recover_d_array[i]))
    #     if(i == numSecretGroups-1 ):
    #         #print('二进制数为：' + ((str(bin(int(recover_d_array[i]))).replace("0b", "")).zfill(secret_string_size%k))[::-1])
    #         bushu = 4
    #         if(secret_string_size%k) != 0:
    #             bushu = secret_string_size%k
    #         resultList = resultList + (((str(bin(int(recover_d_array[i]))).replace("0b", "")).zfill(bushu))[::-1])
    #     else:
    #         # print('二进制数为：' + ((str(bin(int(recover_d_array[i]))).replace("0b","")).zfill(4))[::-1])
    #         resultList = resultList + (((str(bin(int(recover_d_array[i]))).replace("0b","")).zfill(4))[::-1])
    # # print(type(resultList))
    # st = strToChar(resultList)
    return B

# Rlist = [49,66,64,56,64,53,60,59,63,70,55,60,53,55,60,60,58,58,67,66,53,54,64,54,
#  53,56,57,46,64,55,63,46,66,61,66,43,63,62,66,53,69,66,53,52,61,51,58,56,
#  58,59,64,57,61,57,73,63,53,60,66,64]
#
#
# RR_channel = np.array(Rlist)
# print(RR_channel)

# print(MPMrecover(RR_channel,256,4))
from changeWordColor import changeWordColor1
from readOriginalDocx import orignalDocxAbst

doc = docx.Document('Purchasing Contract.docx')
R_channel = changeWordColor1(doc)


oda = orignalDocxAbst("Purchasing Contract.docx")
abst = oda.generateAbst()
print("size",type(R_channel))
# used, res,sec = MPM2022(R_channel, abst, 3)
used, res,sec,a = MPM2022(R_channel, abst, 3)
RR_channel = np.array(sec)
print("RR_channel",RR_channel)
secret_string = biAbsthash(abst)
m = secret_string.size
print("m",m)
print(MPMrecover(RR_channel,m,3))

# def SB19recover(word_updated_rgbList, secret_string_size, k=4):
#     num_secret_groups = math.ceil(secret_string_size / k)
#     moshu = k * k
#     RChannel_array  = np.array(word_updated_rgbList)
#
#     # 恢复，提取加密数据
#     recover_d_array = np.zeros(num_secret_groups)
#     for i in range(0, num_secret_groups):
#         recover_d_array[i] = RChannel_array [i] % moshu
#
#     print("===================")
#     resultList = ""
#     # 恢复出的和以前的应该是一致的
#     for i in range(0, num_secret_groups):
#         #print(int(recover_d_array[i]))
#         if(i == num_secret_groups-1 ):
#             #print('二进制数为：' + ((str(bin(int(recover_d_array[i]))).replace("0b", "")).zfill(secret_string_size%k))[::-1])
#             bushu = 4
#             if(secret_string_size%k) != 0:
#                 bushu = secret_string_size%k
#             resultList = resultList + (((str(bin(int(recover_d_array[i]))).replace("0b", "")).zfill(bushu))[::-1])
#         else:
#             # print('二进制数为：' + ((str(bin(int(recover_d_array[i]))).replace("0b","")).zfill(4))[::-1])
#             resultList = resultList + (((str(bin(int(recover_d_array[i]))).replace("0b","")).zfill(4))[::-1])
#
#     # print(type(resultList))
#     res = strToChar(resultList)
#     return res

# Rlist = [247,246,241,241,249,248]
# RR_channel = np.array(Rlist)
# print(RR_channel)
# print(SB19recover(RR_channel,24,4))


# 测试SB19
# np.set_printoptions(threshold=np.inf)
# np.random.seed(1203)
# s_data = np.random.randint(0, 2, 2000)
# print(s_data)
#
# im = Image.open(r"C:\\Users\\liteng0264\\Desktop\\result\\SB19.png")
# im2 = im.convert('L')
# img_array1 = np.array(im2)
# img_array3 = img_array1.flatten()
# s_data = np.random.randint(0, 2, 2000)
# SB19recover(img_array3,2000,2)
