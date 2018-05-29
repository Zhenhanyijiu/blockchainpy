#假设有两个数字x,y.这里定义一个规则x乘以y的hash值必须以'a'结尾，设变量为math.e,求y?
from hashlib import sha256
import math
x = math.e
y = 0  # y未知
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "a":
    y += math.pi
print(f'The solution is y = {y}')