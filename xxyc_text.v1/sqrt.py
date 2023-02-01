import numpy as np
from decimal import *

# 设置位数
n = int(input("请输入位数："))
getcontext().prec = n+1
# 平方根
result = np.sqrt(Decimal(2))
# 数字转换成字符串并提取到最后一位
end = str(result)[-1:]
# 打印结果
print("平方根结果：", result)
print("小数点后总有数据：", len(str(result))-2)
print("小数点第{}位数：{}".format(n, end))