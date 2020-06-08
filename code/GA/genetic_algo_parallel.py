import networkx as nx
import pandas as pd
from main import get_distance_between_grids
import math
import random
import multiprocessing

class gene:
    order_drone_alloc = {}
    fitness = 0
    drone_order_alloc = {}
    fp = 8
    fd = 5
    rows = 17
    cols = 13
    recharging_points = None
    graph = None
    customer_nodes = None
    nearest_recharging_station = None
    warehouse_number = 122
    data = None
    fitness_value = None
    speed_drones = 50
    number_drones = 100000

    @classmethod
    def index_to_points(cls, index, rows=17, cols=13):
        y = math.floor(index / cols)
        x = index - (cols * y)
        return [x, y]

    @classmethod
    def get_recharging_points(cls, fileName):
        file_pointer = open(fileName, "r")
        recharging_points = []
        for lines in file_pointer:
            recharging_points.append(int(float(lines.strip())))
        return recharging_points

    @classmethod
    def construct_graph_recharging_points(cls, recharging_points, graph):
        for nodes in recharging_points:
            graph.add_node(nodes)
        for node1 in recharging_points:
            for node2 in recharging_points:
                if (node1 == node2):
                    continue
                add1 = cls.index_to_points(node1)
                add2 = cls.index_to_points(node2)
                distance = get_distance_between_grids(add1[0], add1[1], add2[0], add2[1])
                if (distance <= cls.fp):
                    graph.add_edge(node1, node2, weight=distance)

    @classmethod
    def get_nearest_recharging_station(cls, recharging_points, cust_nodes):
        nearest_dictionary = {}
        for cust_address in cust_nodes:
            min_distance = 1000
            nearest_node = recharging_points[0]
            flag = 0
            for points in recharging_points:
                add1 = cls.index_to_points(cust_address)
                add2 = cls.index_to_points(points)
                distance = get_distance_between_grids(
                    add1[0], add1[1], add2[0], add2[1])
                if distance < min_distance and distance < cls.fd:
                    flag = 1
                    min_distance = distance
                    nearest_node = points
            if (flag):
                nearest_dictionary[cust_address] = nearest_node
        return nearest_dictionary

    @classmethod
    def get_customer_nodes(cls, fileName):
        file_pointer = open(fileName, "r")
        customer_nodes = []
        for lines in file_pointer:
            words = [int(float(word.strip())) for word in lines.split(",")]
            customer_nodes.append(words[0])
        return customer_nodes

    @classmethod
    def get_min(cls, time_drones):
        min_value = time_drones[0]
        min_index = 0
        for i in range(len(time_drones)):
            if (time_drones[i] < min_value):
                min_value = time_drones[i]
                min_index = i
        return min_index

    @classmethod
    def Init(cls):
        if not cls.recharging_points:
            recharging_points = cls.get_recharging_points("../recharging_points.txt")
            cls.recharging_points = recharging_points
        if not cls.graph:
            graph = nx.Graph()
            cls.construct_graph_recharging_points(cls.recharging_points, graph)
            cls.graph = graph
        if not cls.customer_nodes:
            customer_nodes = cls.get_customer_nodes("../customer_demands.csv")
            cls.customer_nodes = customer_nodes
        if not cls.nearest_recharging_station:
            nearest_recharging_station = cls.get_nearest_recharging_station(cls.recharging_points, cls.customer_nodes)
            cls.nearest_recharging_station = nearest_recharging_station
        if not cls.data:
            data = pd.read_csv("../instance.csv")
            cls.data = data
            #print(data.columns)
            data = data.sort_values(by=['arrival_time'], ascending=True)
            #print(data)
            warehouse_number = cls.warehouse_number
            total_distance = 0

    def get_minimum_distance(self, graph, start, end, nearest_dictionary):
        recharging1 = nearest_dictionary[start]
        recharging2 = nearest_dictionary[end]
        start_point = self.index_to_point(start)
        end_point = self.index_to_point(end)
        recharging1_point = self.index_to_point(recharging1)
        recharging2_point = self.index_to_point(recharging2)
        if (recharging1 == recharging2):
            return get_distance_between_grids(start_point[0], start_point[1], end_point[0], end_point[1])
        distance1 = get_distance_between_grids(
            start_point[0], start_point[1], recharging1_point[0], recharging1_point[1])
        distance2 = get_distance_between_grids(
            end_point[0], end_point[1], recharging2_point[0], recharging2_point[1])
        return distance1 + distance2 + nx.dijkstra_path_length(graph, recharging1, recharging2)

    def index_to_point(self, index, rows=17, cols=13):
        y = math.floor(index / cols)
        x = index - (cols * y)
        return [x, y]

    def fitness(self):
        max_distance = 0
        for drone_id, orders_list in self.drone_order_alloc.items():
            total_distance = 0
            for order in orders_list:
                customer_address = int(float(self.data.loc[self.data['order_id'] == order, "customer_address"]))
                rest_address = int(float(self.data.loc[self.data['order_id'] == order, "rest_address"]))
                total_distance += self.get_minimum_distance(
                    self.graph, self.warehouse_number, rest_address, self.nearest_recharging_station)
                total_distance += self.get_minimum_distance(
                    self.graph, rest_address, customer_address, self.nearest_recharging_station)
                total_distance += self.get_minimum_distance(
                    self.graph, customer_address, self.warehouse_number, self.nearest_recharging_station)
            if total_distance > max_distance:
                max_distance = total_distance
        self.fitness_value = float(max_distance/self.speed_drones)

    def convert_drone_order(self):
        for order_id, drone_id in self.order_drone_alloc.items():
            if drone_id in self.drone_order_alloc.keys():
                self.drone_order_alloc[drone_id].append(order_id)
            else:
                self.drone_order_alloc[drone_id] = [order_id]
        self.fitness()

    def allocate_random_orders(self):
        for orderId in list(self.data['order_id']):
            self.order_drone_alloc[orderId] = random.randint(0,self.number_drones)
        self.convert_drone_order()

    def allocate_orders(self, order_drone_dict):
        self.order_drone_alloc = order_drone_dict
        self.convert_drone_order()
        

class genetic_algo:
    number_generation = 5
    current_population = []
    #new_generation = []
    number_population = 3
    crossover_percent = 0.3
    mutation_probability = 0.01
    def selection(self):
        self.current_population.sort(key=lambda x:x.fitness_value, reverse=False)
        return self.current_population[0:len(self.current_population)]

    def crossover(self,k, parents):
        parent1_idx = k % (len(parents))
        parent2_idx = (k+1) % (len(parents))
        parent1 = parents[parent1_idx]
        parent2 = parents[parent2_idx]
        mid = random.randint(0, len(parents[0].order_drone_alloc.keys()))
        offspring = {}
        count = 0
        for k,v in parent1.order_drone_alloc.items():
            if count == mid:
                break
            else :
                count+=1
                offspring[k] = v
        count = 0
        for k, v in parent2.order_drone_alloc.items():
            if count < mid:
                count+=1
                continue
            else:
                count += 1
                offspring[k] = v
        offspring = self.mutation(offspring)
        offspring_object = gene()
        offspring_object.allocate_orders(offspring)
        print(k)
        return offspring_object
    def crossover_util(self, parents):
        offspring_list = []
        pool= multiprocessing.Pool(processes = 4)
        result = pool.starmap(self.crossover, [(k,parents) for k in range(int((self.number_population*(self.number_population-1))/2))])
        return result
    def mutation(self, offspring):
        if (random.random() <= self.mutation_probability):
            key = random.choice(offspring.keys())
            offspring[key] = random.choice(offspring.values())
        return offspring

    def initialize_population(self):
        for i in range(self.number_population):
            print(i)
            chromosome = gene()
            chromosome.allocate_random_orders()
            self.current_population.append(chromosome)

    def runGA(self):
        gene.Init()
        self.initialize_population()
        for _ in range(self.number_generation):
            print("Iteration")
            selected_parents = self.selection()
            print("Selection Done.")
            self.current_population = self.crossover_util(selected_parents)
        self.current_population.sort(key=lambda x: x.fitness_value, reverse=False)
        print(self.current_population[0].fitness_value)

if __name__ == "__main__":
    genetic_algo_obj = genetic_algo()
    genetic_algo_obj.runGA()
    print("Result : ")

