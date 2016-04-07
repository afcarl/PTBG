__author__ = 'luocheng'


import numpy as np

def linearfit(x, y):
    z1 = np.polyfit(x,y,1,full=True)
    return z1[0],z1[1]


#
#
# X=[ 1 ,2  ,3 ,4 ,5 ,6]
# Y=[ 2.5 ,3.51 ,4.45 ,5.52 ,6.47 ,7.51]
#
#
# z1 = np.polyfit(X, Y, 1)
# p1 = np.poly1d(z1)
# print z1  #[ 1.          1.49333333]
# print p1  # 1 x + 1.493
#
# z1 = np.polyfit(X, Y, 1,full=True)
# print z1[0]
# print z1[1]
# print z1
#
# import matplotlib.pyplot as plt
