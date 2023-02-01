
#嵌入
import copy

import numpy as np
import math
import docx
# from docx import Document
# from docx import Document
# from docx.shared import RGBColor
from binhash import biAbsthash, abst
# from charToNdarray import charToNdarray
#

# global_num_pixels_changed=None
"""
    用MPM22方法来嵌入信息
    输入: 1、word文档的RGB列表,仅取R列表即可，需要Ndarray类型
          2、文字内容,可以传入字符串类型,但算法中需要Ndarray类型
    输出: 1、改后的RGB列表,仅有R列表
"""
# def set_global_num_pixels_changed(num_pixels_changed):
#     global_num_pixels_changed=num_pixels_changed





def MPM2022(word_original_rgbList, m, k=5):
    RChannel_array = np.array(word_original_rgbList)
    print(" origin_array:",RChannel_array)

    secret_string = biAbsthash(m)
    print("secret_string",secret_string)
    n = 4  # 此算法在R通道中嵌入
    k2 = k + 1
    moshu0 = 2 ** (k + 1)  # 模数的底数
    moshu1 = 2 ** k  # 模数的底数

    # 将分成n个像素一组,保证整数组，不足的补零
    # num_RChannel_groups = RChannel_array.size
    numPG = math.ceil(RChannel_array.size / n)
    # print("numPG:",numPG)
    PGoriginalValue = np.zeros((numPG, n), dtype="int")
    PGhighPartValue = np.zeros((numPG, n), dtype="int")
    PGlowerMask = 2 ** k2 - 1  # used for spliting lower and higher bits
    # print("PGlowerMask:", PGlowerMask)
    for i in range(0, numPG, 1):
        for j2 in range(0, n, 1):
            if i * n + j2 < RChannel_array.size:
                PGoriginalValue[i, j2] = RChannel_array[i * n + j2]  # 原像素值
                PGhighPartValue[i, j2] = RChannel_array[i * n + j2] & (
                        255 - PGlowerMask)  # higher part, used for searching the highest pixel value
    # print("PGoriginalValue:",PGoriginalValue)
    # print("PGhighPartValue:", PGhighPartValue)

    numBitsPerPG = n * k + 1  # 每组pixcel嵌入的bit数
    numSecretGroups = math.ceil(secret_string.size / numBitsPerPG)# 给秘密信息进行分组
    # print("secret_string.size:", secret_string.size)
    # print("numSecretGroups:", numSecretGroups)
    secretGroup = np.zeros((numSecretGroups, numBitsPerPG), dtype="int")# 给秘密信息组赋值为0
    secret_string_copy = secret_string.copy()
    for i in range(0, numSecretGroups, 1):# 给秘密信息组赋值
        for j2 in range(0, numBitsPerPG, 1):
            if i * numBitsPerPG + j2 < secret_string.size:
                secretGroup[i, j2] = secret_string_copy[i * numBitsPerPG + j2]
                # print("secret_group[i, j]",secretGroup[i, j2])
    # print("secret_group",secretGroup)



    # 将一组的秘密信息转化为十进制数字d
    secret_d_array = np.zeros((numSecretGroups), dtype="int")  # 待嵌入的secret值
    for i in range(0, numSecretGroups, 1):
        for j2 in range(0, numBitsPerPG, 1):
            # secret_d_array[i]+=(2 ** j) * secret_group[i,j] #低位在前
            secret_d_array[i] += (2 ** (numBitsPerPG - 1 - j2)) * secretGroup[i, j2]  # 高位在前,decimal value
    # print("secret_d_array", secret_d_array)
    assert (numPG > numSecretGroups)
    # PGembedded = copy.deepcopy(PGoriginalValue)

    """
        嵌入过程：
        将n个像素分为一组
        每组像素嵌入nk+1个二进制位，分为n组，一组k+1位,n-1组k位
        selIndex为索引，找出像素组的一个像素，来嵌入最前面的k+1位

    """
    # 开始进行嵌入
    embedded_RChannel_group = copy.deepcopy(PGoriginalValue)
    # print("embedded_RChannel_group", embedded_RChannel_group)
    # RChannels_group = copy.deepcopy(PGoriginalValue)
    # print("RChannels_group",RChannels_group)
    num_pixels_changed = 0
    for i in range(0, numSecretGroups, 1):
        # 找出pixel组中的一个pixel，用来嵌入最前面的k+1 bit
        selIndex = i % n
        # print("selIndex", selIndex)
        firstk1BitsDvalue = int(secret_d_array[i] / (2 ** ((n - 1) * k)))  # 取出k+1 bits
        # print("firstk1BitsDvalue", firstk1BitsDvalue)
        kBitsGroup = np.zeros(n, dtype=int)  # get k bits group in the rest
        # 第selIndex个不用，保持为0
        lastBitsDvalue = int(secret_d_array[i]) & (2 ** ((n - 1) * k) - 1)#lastBitsDvalue是剩下的秘密信息
        # 将剩下的秘密信息分为k位一组，存放在kBitsGroup中
        for j in range(0, selIndex, 1):
            kBitsGroup[j] = int(lastBitsDvalue / (2 ** ((n - j - 2) * k))) & (2 ** k - 1)
        for j in range(selIndex + 1, n, 1):
            kBitsGroup[j] = int(lastBitsDvalue / (2 ** ((n - j - 1) * k))) & (2 ** k - 1)
        # print("lastBitsDvalue", lastBitsDvalue)
        # print("kBitsGroup", kBitsGroup)
        # 确保转换没有错误
        v1 = firstk1BitsDvalue
        v2 = v1 * (2 ** ((n - 1) * k))
        tmpValue = 0
        for j2 in range(0, selIndex, 1):
            v3 = kBitsGroup[j2]
            tmpValue += v3 * (2 ** ((n - j2 - 2) * k))
        for j2 in range(selIndex + 1, n, 1):
            v3 = kBitsGroup[j2]
            tmpValue += v3 * (2 ** ((n - j2 - 1) * k))
        assert (v2 + tmpValue == secret_d_array[i])

        # 确保转换没有错误
        v1 = firstk1BitsDvalue
        v2 = v1 * (2 ** ((n - 1) * k))
        tmpValue = 0
        for j2 in range(0, selIndex, 1):
            v3 = kBitsGroup[j2]
            tmpValue += v3 * (2 ** ((n - j2 - 2) * k))
        for j2 in range(selIndex + 1, n, 1):
            v3 = kBitsGroup[j2]
            tmpValue += v3 * (2 ** ((n - j2 - 1) * k))
        assert (v2 + tmpValue == secret_d_array[i])

        # 开始嵌入
        # search x for firstk1BitsDvalue，查找满足以下条件的x值
        diffMin = 99999999
        xSel = -9999
        # 嵌入k+1位的秘密信息
        for x in range(-moshu0, moshu0 + 1, 1):
            t = PGoriginalValue[i, selIndex]#原始像素值
            if ((t + x) % moshu0 == firstk1BitsDvalue) and ((t + x) >= 0) and ((t + x) <= 255):
                tDiff = x ** 2
                # 选取最优的x值
                if tDiff < diffMin:
                    diffMin = tDiff
                    xSel = x
                    print("xSel0:",xSel)
        embedded_RChannel_group[i, selIndex] = PGoriginalValue[i, selIndex] + xSel
        num_pixels_changed += 1

        # 嵌入k位的秘密信息，像素值是0到selIndex之间的
        # search x for kBitsGroup
        for j1 in range(0, selIndex, 1):
            diffMin = 99999999
            xSel = -9999
            for x in range(-moshu1, moshu1 + 1, 1):
                t = PGoriginalValue[i, j1]
                if ((t + x) % moshu1 == kBitsGroup[j1]) and ((t + x) >= 0) and ((t + x) <= 255):
                    tDiff = x ** 2
                    if tDiff < diffMin:
                        diffMin = tDiff
                        xSel = x
                        print("xSel1:", xSel)
            embedded_RChannel_group[i, j1] = PGoriginalValue[i, j1] + xSel
            num_pixels_changed += 1

        # 嵌入k位的秘密信息，像素值是selIndex到n之间的
        for j1 in range(selIndex + 1, n, 1):
            diffMin = 99999999
            xSel = -9999
            for x in range(-moshu1, moshu1 + 1, 1):
                t = PGoriginalValue[i, j1]
                if ((t + x) % moshu1 == kBitsGroup[j1]) and ((t + x) >= 0) and ((t + x) <= 255):
                    tDiff = x ** 2
                    if tDiff < diffMin:
                        diffMin = tDiff
                        xSel = x
                        print("xSel2:", xSel)
            embedded_RChannel_group[i, j1] = PGoriginalValue[i, j1] + xSel
            num_pixels_changed += 1
        print("embedded_RChannel_group:", embedded_RChannel_group)

            # embedded_RChannel_group_f = embedded_RChannel_group.flatten()
            # print("embedded_RChannel_group_f", embedded_RChannel_group_f)
        # num_pixels_changed = numSecretGroups * n

        # 计算ppb时用到分母
        print("num_pixels_changed:", num_pixels_changed)
        # set_global_num_pixels_changed(num_pixels_changed)
        print("使用了多少pixel来进行嵌入:",num_pixels_changed)
    print(" embedded_RChannel_group",  embedded_RChannel_group)
    rate_ebedding = len(secret_string)/num_pixels_changed * 3
    embedded_RChannel_group_f = embedded_RChannel_group.flatten()#三元组转换成一元组
    #返回 秘密字符串长度、R通道嵌入展平成一组、嵌入组数、嵌入率；
    return len(secret_string),embedded_RChannel_group_f,embedded_RChannel_group,rate_ebedding



if __name__ == '__main__':
    from changeWordColor import changeWordColor1
    doc = docx.Document('Purchasing Contract.docx')
    R_channel =  changeWordColor1(doc)
    used, res,sec,bpc = MPM2022(R_channel, abst, 5)
    print("res", res)
    print("sec",sec)
    print("bpc",bpc)#bpp指的是嵌入容量
