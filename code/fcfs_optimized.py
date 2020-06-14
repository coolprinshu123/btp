import networkx as nx
from main import calculate_distance
from main import get_distance_between_grids
from plot import index_to_points
import pandas as pd

fp = 8
fd = 5
rows = 17
cols = 13


def get_recharging_points(fileName):
    file_pointer = open(fileName, "r")
    recharging_points = []
    for lines in file_pointer:
        recharging_points.append(int(float(lines.strip())))
    return recharging_points


def construct_graph_recharging_points(recharging_points, graph):
    for nodes in recharging_points:
        graph.add_node(nodes)
    for node1 in recharging_points:
        for node2 in recharging_points:
            if(node1 == node2):
                continue
            add1 = index_to_points(node1)
            add2 = index_to_points(node2)
            distance = get_distance_between_grids(
                add1[0], add1[1], add2[0], add2[1])
            if(distance <= fp):
                graph.add_edge(node1, node2, weight=distance)


def get_nearest_recharging_station(recharging_points, cust_nodes):
    nearest_dictionary = {}
    for cust_address in cust_nodes:
        min_distance = 100000000000
        nearest_node = recharging_points[0]
        flag = 0
        for points in recharging_points:
            add1 = index_to_points(cust_address)
            add2 = index_to_points(points)
            distance = get_distance_between_grids(
                add1[0], add1[1], add2[0], add2[1])
            if(distance < min_distance and distance < fd):
                flag = 1
                min_distance = distance
                nearest_node = points
        if(flag):
            nearest_dictionary[cust_address] = nearest_node
    return nearest_dictionary


def get_minimum_distance(graph, start, end, nearest_dictionary):
    recharging1 = nearest_dictionary[start]
    recharging2 = nearest_dictionary[end]
    start_point = index_to_points(start)
    end_point = index_to_points(end)
    recharging1_point = index_to_points(recharging1)
    recharging2_point = index_to_points(recharging2)
    if(recharging1 == recharging2):
        return get_distance_between_grids(start_point[0], start_point[1], end_point[0], end_point[1])
    distance1 = get_distance_between_grids(
        start_point[0], start_point[1], recharging1_point[0], recharging1_point[1])
    distance2 = get_distance_between_grids(
        end_point[0], end_point[1], recharging2_point[0], recharging2_point[1])
    return distance1 + distance2 + nx.dijkstra_path_length(graph, recharging1, recharging2)


def get_customer_nodes(fileName):
    file_pointer = open(fileName, "r")
    customer_nodes = []
    for lines in file_pointer:
        words = [int(float(word.strip())) for word in lines.split(",")]
        customer_nodes.append(words[0])
    return customer_nodes


def get_min(time_drones):
    min_value = time_drones[0]
    min_index = 0
    for i in range(len(time_drones)):
        if(time_drones[i] < min_value):
            min_value = time_drones[i]
            min_index = i
    return min_index


if __name__ == "__main__":
    recharging_points = get_recharging_points("recharging_points.txt")
    graph = nx.Graph()
    construct_graph_recharging_points(recharging_points, graph)
    customer_nodes = get_customer_nodes("customer_demands.csv")
    nearest_recharging_station = get_nearest_recharging_station(
        recharging_points, customer_nodes)
    data = pd.read_csv("instance.csv")
    print(data.columns)
    data = data.sort_values(by=['arrival_time'], ascending=True)
    print(data)
    warehouse_number = 122
    total_distance = 0
    # print(data)
    for i in range(len(data)):
        customer_address = int(float(data.loc[i, "customer_address"]))
        rest_address = int(float(data.loc[i, "rest_address"]))
        #print(data.loc[i, "rest_address"])
        total_distance += get_minimum_distance(
            graph, warehouse_number, rest_address, nearest_recharging_station)
        total_distance += get_minimum_distance(
            graph, rest_address, customer_address, nearest_recharging_station)
        total_distance += get_minimum_distance(
            graph, customer_address, warehouse_number, nearest_recharging_station)
    print(total_distance)

    current_order = 0
    number_drones = 3000
    speed_drones = 1
    free_time = [0]*number_drones
    drone_location = [recharging_points[0]]*number_drones
    arrival_time = [0]*number_drones
    while(current_order < len(data)):
        total_distance = 0
        next_free_drone = get_min(free_time)
        customer_address = int(
            float(data.loc[current_order, "customer_address"]))
        rest_address = int(float(data.loc[current_order, "rest_address"]))
        for i in range(number_drones):
            arrival_time[i] = free_time[i] - free_time[next_free_drone]
            #add1 = index_to_points(rest_address)
            #add2 = index_to_points(nearest_recharging_station[drone_location[i]])
            arrival_time[i] += get_minimum_distance(
                graph, drone_location[i], rest_address, nearest_recharging_station)

        #print(data.loc[i, "rest_address"])
        next_free_drone = get_min(arrival_time)
        total_distance += get_minimum_distance(
            graph, drone_location[next_free_drone], rest_address, nearest_recharging_station)
        total_distance += get_minimum_distance(
            graph, rest_address, customer_address, nearest_recharging_station)
        total_distance += get_minimum_distance(
            graph, customer_address, nearest_recharging_station[customer_address], nearest_recharging_station)
        free_time[next_free_drone] += total_distance/speed_drones
        drone_location[next_free_drone] = nearest_recharging_station[customer_address]
        current_order += 1

    print(max(free_time))
