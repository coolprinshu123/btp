'''
from scipy.stats import poisson
mean_level_1 = 100
mean_level_2 = 60
mean_level_3 = 25
num_rest_level_1= 100
num_rest_level_2= 200
num_rest_level_3= 150

num_orders_level_1 = poisson.rvs(mean_level_1, size=num_rest_level_1)
num_orders_level_2 = poisson.rvs(mean_level_2, size=num_rest_level_2)
num_orders_level_3 = poisson.rvs(mean_level_3, size=num_rest_level_3)

'''

import pandas as pd
import random
import math
import statistics
import matplotlib.pyplot as plt
from main import calculate_distance
sector_distance = 2
rows = 17
cols = 13
lat_min = 28.5285736999
lon_min = 77.0439512
lat_max = 28.7446158
lon_max = 77.3899722
customer_order_file = open("customer_demands.csv", "r")
total_customers = 0
customer_numbers = []
for lines in customer_order_file:
    words = [int(float(word.strip())) for word in lines.split(",")]
    customer_numbers.append(words[1])
    total_customers += words[1]

output_file = open("instance.csv", "w+")
output_file.write(
    "order_id,customer_address,rest_id,rest_lat,rest_long,rest_address,arrival_time\n")
order_id = 0


def generate_num_orders(_lambda, _num_events, rest_id, rest_lat, rest_long):
    #_lambda = 5
    #_num_events = 100
    global order_id
    global output_file
    global customer_numbers
    global total_customers
    global rows
    global cols
    global lat_min
    global lon_min
    global sector_distance
    len_index = math.ceil(calculate_distance(
        lat_min, lon_min, rest_lat, lon_min)/sector_distance)
    bre_index = math.ceil(calculate_distance(
        lat_min, lon_min, lat_min, rest_long)/sector_distance)
    rest_index = len_index*cols+bre_index
    print("index : ", rest_index, " ", len_index, bre_index)
    _event_num = []
    _inter_event_times = []
    _event_times = []
    _event_time = 0
    print('EVENT_NUM,INTER_EVENT_T,EVENT_T')

    for i in range(_num_events):
        customer_id = random.randint(1, total_customers)
        customers_now = 0
        customer_address = 0
        for i in range(len(customer_numbers)):
            customers_now += customer_numbers[i]
            if(customers_now > customer_id):
                customer_address = i-1
                break
        instance = []
        instance.append(order_id)
        instance.append(customer_address)
        instance.append(rest_id)
        instance.append(rest_lat)
        instance.append(rest_long)
        instance.append(rest_index)
        _event_num.append(i)
        # Get a random probability value from the uniform distribution's PDF
        n = random.random()

        # Generate the inter-event time from the exponential distribution's CDF using the Inverse-CDF technique
        _inter_event_time = -math.log(1.0 - n) / _lambda
        _inter_event_times.append(_inter_event_time)

        # Add the inter-event time to the running sum to get the next absolute event time
        _event_time = _event_time + _inter_event_time
        _event_times.append(_event_time)
        instance.append(_event_time)
        for items in instance:
            output_file.write(str(items)+",")
        output_file.write("\n")
        order_id += 1
        # print it all out
        #print(str(i) + ',' + str(_inter_event_time) + ',' + str(_event_time))
    '''
	#plot the inter-event times
	fig = plt.figure()
	fig.suptitle('Times between consecutive events in a simulated Poisson process')
	plot, = plt.plot(_event_num, _inter_event_times, 'bo-', label='Inter-event time')
	plt.legend(handles=[plot])
	plt.xlabel('Index of event')
	plt.ylabel('Time')
	plt.show()


	#plot the absolute event times
	fig = plt.figure()
	fig.suptitle('Absolute times of consecutive events in a simulated Poisson process')
	plot, = plt.plot(_event_num, _event_times, 'bo-', label='Absolute time of event')
	plt.legend(handles=[plot])
	plt.xlabel('Index of event')
	plt.ylabel('Time')
	plt.show()
	'''

    _interval_nums = []
    _num_events_in_interval = []
    _interval_num = 1
    _num_events = 0

    print('INTERVAL_NUM,NUM_EVENTS')

    for i in range(len(_event_times)):
        _event_time = _event_times[i]
        if _event_time <= _interval_num:
            _num_events += 1
        else:
            _interval_nums.append(_interval_num)
            _num_events_in_interval.append(_num_events)

            print(str(_interval_num) + ',' + str(_num_events))

            _interval_num += 1

            _num_events = 1

    # print the mean number of events per unit time
    print(statistics.mean(_num_events_in_interval))
    '''
	#plot the number of events in consecutive intervals
	fig = plt.figure()
	fig.suptitle('Number of events occurring in consecutive intervals in a simulated Poisson process')
	plt.bar(_interval_nums, _num_events_in_interval)
	plt.xlabel('Index of interval')
	plt.ylabel('Number of events')
	plt.show()### function to search tripadvisor ratings parsing the google search results page ###
	'''


'''num_rest_level_1 = 100
num_rest_level_2 = 200
num_rest_level_3 = 150
'''


def generate_instances(_lambda, _num_arrivals, rest_id, rest_lat, rest_long, time_slot):
    global order_id
    global output_file
    global customer_numbers
    global total_customers
    global rows
    global cols
    global lat_min
    global lon_min
    global sector_distance
    len_index = math.ceil(calculate_distance(
        lat_min, lon_min, rest_lat, lon_min)/sector_distance)
    bre_index = math.ceil(calculate_distance(
        lat_min, lon_min, lat_min, rest_long)/sector_distance)
    rest_index = len_index*cols+bre_index
    _arrival_time = 0
    for i in range(_num_arrivals):
        customer_id = random.randint(1, total_customers)
        customers_now = 0
        customer_address = 0
        for i in range(len(customer_numbers)):
            customers_now += customer_numbers[i]
            if(customers_now > customer_id):
                customer_address = i
                break
        instance = []
        instance.append(order_id)
        instance.append(customer_address)
        instance.append(rest_id)
        instance.append(rest_lat)
        instance.append(rest_long)
        instance.append(rest_index)
        # Get the next probability value from Uniform(0,1)
        p = random.random()

        # Plug it into the inverse of the CDF of Exponential(_lamnbda)
        _inter_arrival_time = -math.log(1.0 - p)/_lambda

        # Add the inter-arrival time to the running sum
        _arrival_time = _arrival_time + _inter_arrival_time
        if(_arrival_time*time_slot > time_slot):
            break
        # print it all out
        instance.append(_arrival_time*time_slot)
        count = 0
        for items in instance:
            count += 1
            if(count != len(instance)):
                output_file.write(str(items)+",")
            else:
                output_file.write(str(items))
        output_file.write("\n")
        order_id += 1
        print(str(p)+','+str(_inter_arrival_time)+','+str(_arrival_time))


avg_orders_per_quaterly_hour_level_1 = 10
avg_orders_per_quaterly_hour_level_2 = 5
avg_orders_per_quaterly_hour_level_3 = 4
total_slots = 1
time_slot = 15
#num_orders_level_1 = poisson.rvs(mean_level_1, size=num_rest_level_1)
#num_orders_level_2 = poisson.rvs(mean_level_2, size=num_rest_level_2)
#num_orders_level_3 = poisson.rvs(mean_level_3, size=num_rest_level_3)
file_rest = pd.read_csv("zomato.csv")
file_rest = file_rest.head(1000)
print(file_rest.columns)
for i in range(len(file_rest)):
    rating_val = float(file_rest.loc[i, "rating"])
    rest_lat = float(file_rest.loc[i, "lat"])
    rest_lon = float(file_rest.loc[i, "lon"])
    if(rest_lat < lat_min or rest_lat > lat_max or rest_lon < lon_min or rest_lon > lon_max):
        continue
    if(rating_val >= 4):
        generate_instances(avg_orders_per_quaterly_hour_level_1,
                           avg_orders_per_quaterly_hour_level_1*total_slots, i+1, rest_lat, rest_lon, time_slot)
    elif(rating_val >= 3):
        generate_instances(avg_orders_per_quaterly_hour_level_2,
                           avg_orders_per_quaterly_hour_level_2*total_slots, i+1, rest_lat, rest_lon, time_slot)
    else:
        generate_instances(avg_orders_per_quaterly_hour_level_3,
                           avg_orders_per_quaterly_hour_level_3*total_slots, i+1, rest_lat, rest_lon, time_slot)

'''
for i in range(num_rest_level_1):
	generate_num_orders(avg_orders_per_quaterly_hour_level_1, avg_orders_per_quaterly_hour_level_1*total_slots)
for i in range(num_rest_level_2):
	generate_num_orders(avg_orders_per_quaterly_hour_level_2, avg_orders_per_quaterly_hour_level_2*total_slots)
for i in range(num_rest_level_3):
	generate_num_orders(avg_orders_per_quaterly_hour_level_3, avg_orders_per_quaterly_hour_level_3*total_slots)

restaurants = [{u"name":u"Anglow",u"location":u"Delhi"}]
GetTripadvisorRatingsFromGoogleSearch(restaurants)
'''
