import matplotlib.pyplot as plt
import numpy as np
import math


def index_to_points(index, rows=17, cols=13):
    y = math.floor(index/cols)
    x = index-(cols*y)
    return [x, y]


if __name__ == '__main__':
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
    # plt.xlabel("latitude")
    # plt.ylabel("longitude")
    # plt.plot(X, Y, marker='.', color='k', linestyle='none')
    # plt.plot(recharging_points[:, 0], recharging_points[:, 1], "ro")
    # plt.show()

    x = [100, 500, 1000, 1500, 2000, 2500, 3000]
    y = [5340/60, 1014/60, 507/60, 274/60, 110/60, 70/60, 40/60]
    plt.xlabel("Number of drones")
    plt.ylabel("Time taken in hrs")
    y1 = [7066/60, 1482/60, 788/60, 555/60, 444/60, 320/60, 210/60]
    y2 = [5120/60, 980/60, 476/60, 252/60, 97/60, 58/60, 33/60]
    # plt.plot(x,y)
    plt.plot(x, y, 'r-')
    plt.plot(x, y1, 'b-')
    plt.plot(x,y2,'g-')
    plt.legend(['FCFS_optimised','FCFS','GA'])
    plt.show()
    plt.savefig("recharging_points.png")
