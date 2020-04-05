import argparse
from sys import argv
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import util
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from scipy.stats import multivariate_normal
import math
import scipy.stats
from copy import deepcopy
from mpl_toolkits import mplot3d


def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-format', '--format',
                        help='format of the file from which to extract dataframe', type=str)
    parser.add_argument('-region', '--region',
                        help='name of the region for data', type=str)
    parser.set_defaults(format='csv')

    args = parser.parse_args()
    df = util.get_restaurants(args.region, args.format == 'csv')
    return df, args.region, args.format == 'csv'


def calculate_rectangle_around_points(lat_min, long_min, lat_max, long_max):
    length = calculate_distance(lat_min, long_min, lat_max, long_min)
    breadth = calculate_distance(lat_min, long_min, lat_min, long_max)
    return length, breadth


def get_centre_to_origin_distance(centres, lat_min, long_min):
    distance_dictionary = {}
    for centre_values in centers:
        x = calculate_distance(lat_min, long_min, centre_values[0], long_min)
        y = calculate_distance(lat_min, long_min, lat_min, centre_values[1])
        distance_dictionary[centre_values] = [x, y]
    return distance_dictionary


def get_distance_between_grids(x1, y1, x2, y2, sector_distance=2):
    length = (x2 - x1) * sector_distance
    breadth = (y2 - y1) * sector_distance
    return math.sqrt(length ** 2 + breadth**2)


def write_dictionary(dictionary, fileName):
    fp = open(fileName, "w+")
    for item, value in dictionary.items():
        fp.write(str(item))
        for value_items in value:
            fp.write("," + str(value_items))
        fp.write("\n")


def plot_countour(x, y, Z):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    X, Y = np.meshgrid(x, y)
    print(Z)
    ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.set_xlabel('longitudinal grid number')
    ax.set_ylabel('latitudinal grid number')
    ax.set_zlabel('number of customers')
    plt.show()


def generate_data_points(centers, origin_distance, breadth, length):
    sector_distance = 2
    rows = math.ceil(length/sector_distance)
    cols = math.ceil(breadth/sector_distance)
    #mean_vector = [1000]*len(centers)
    #variance = [500]*len(centers)
    num_orders = 10000
    fp = 8
    fd = 5
    customer_matrix = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            demand = 0
            for k in range(len(centers)):
                centre_value = origin_distance[centers[k]]
                distance_from_centre = get_distance_between_grids(i, j, math.ceil(
                    centre_value[0]/sector_distance), math.ceil(centre_value[1]/sector_distance), sector_distance)
                demand = demand + \
                    math.ceil(scipy.stats.norm(0, 3).pdf(
                        distance_from_centre)*num_orders)
            customer_matrix[i][j] = int(demand)
    #np.savetxt("customer_demand.csv", customer_matrix, delimiter=",")
    omega = {}
    n_k = {}
    demand_dictionary = {}
    for i in range(rows):
        for j in range(cols):
            num_customers_one_way = []
            num_customers_two_way = []
            for ii in range(rows):
                for jj in range(cols):
                    if get_distance_between_grids(i, j, ii, jj, sector_distance) <= fd:
                        num_customers_two_way.append(ii*cols + jj)
                    if get_distance_between_grids(i, j, ii, jj, sector_distance) <= fp:
                        num_customers_one_way.append(ii*cols + jj)
            omega[i*cols + j] = num_customers_one_way
            n_k[i*cols + j] = num_customers_two_way
            demand_dictionary[i*cols + j] = [customer_matrix[i][j]]
    write_dictionary(demand_dictionary, "customer_demands.csv")
    write_dictionary(omega, "omega.csv")
    write_dictionary(n_k, "n_k.csv")
    plot_countour(np.arange(cols), np.arange(rows), customer_matrix)
    print(rows, cols)


# Create geneatic algorithm for set cover problem using fixed radius circles
if __name__ == '__main__':
    df, region, is_csv = parse_arguments()
    util.draw(df, region)
    if not is_csv:
        util.to_csv(df, region)
    data = df.values
    data = data[:, 1:]
    km = KMeans(n_clusters=6)
    km.fit(data)
    y = km.predict(data)
    sns.scatterplot(x="lat", y="lon", data=df, hue=y)
    centers = km.cluster_centers_
    print(len(y))
    # print(centers)
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    plt.savefig("fig/clusters" + region + ".png")
    plt.show()
    centers_location = deepcopy(centers)
    centers_location = np.asarray(centers_location)
    np.savetxt("centers.csv", centers_location, delimiter=",")
    # For Delhi : lat_min = 28.5285736999, long_min = 77.0439512, lat_max = 28.7446158, long_max = 77.3899722
    centers = [tuple(centers[i]) for i in range(len(centers))]
    print(centers[0][0])
    length, breadth = calculate_rectangle_around_points(
        28.5285736999, 77.0439512, 28.7446158, 77.3899722)
    distance_dictionary = get_centre_to_origin_distance(
        centers, 28.5285736999, 77.0439512)
    print(length, breadth)
    print(distance_dictionary)
    generate_data_points(centers, distance_dictionary, length, breadth)
