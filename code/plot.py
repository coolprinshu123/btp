import matplotlib.pyplot as plt
import numpy as np
import math


def index_to_points(index, rows=17, cols=13):
    y = math.floor(index/cols)
    x = index-(cols*y)
    return [x, y]


recharging_points_file = open("recharging_points.txt", "r")
recharging_points = []
for points in recharging_points_file:
    recharging_points.append(index_to_points(int(float(points.strip()))))
x = np.arange(13)
y = np.arange(17)
X, Y = np.meshgrid(x, y)
print(np.meshgrid(x, y))
#recharging_points = np.asarray([[10,2], [3,3], [0,5], [12,11], [2,12], [6,12], [11,12]])
#recharging_points = np.asarray([[11, 12], [4, 12], [12, 11], [0, 5], [8, 4], [2, 4]])
recharging_points = np.asarray(recharging_points)
print(recharging_points)
plt.plot(X, Y, marker='.', color='k', linestyle='none')
plt.plot(recharging_points[:, 0], recharging_points[:, 1], "ro")
plt.show()


# x = [1,2,3,4,5,6,7]
# y = [560,5570,8981,10664,11506,11703,11727]
# plt.xlabel("Number of recharging stations")
# plt.ylabel("Total number of customers covered")
# plt.plot(x,y)
# plt.plot(x,y,'ro')
# plt.show()
# plt.savefig("recharging_points.png")
