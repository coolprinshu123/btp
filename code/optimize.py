from ortools.linear_solver import pywraplp
solver = pywraplp.Solver(
    'SolveRangeMIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)


def csv_to_dictionary(fileName, is_list=0):
    output_dictionary = {}
    fp = open(fileName, "r")
    for lines in fp:
        word = [int(float(word.strip())) for word in lines.split(",")]
        if is_list == 0:
            output_dictionary[word[0]] = word[1]
        else:
            output_dictionary[word[0]] = word[1:]
    return output_dictionary


customer_nodes = 221
y = {}
x = {}
p = 9
print(p)
service_demand_customer = csv_to_dictionary("customer_demands.csv")
N_k = csv_to_dictionary("n_k.csv", 1)
omega = csv_to_dictionary("omega.csv", 1)
m = customer_nodes
z = {}
warehouse_no = 122
for i in range(customer_nodes):
    y[i] = solver.IntVar(0, 1, 'y'+str(i))
    x[i] = solver.IntVar(0, 1, 'x'+str(i))

for i in range(customer_nodes):
    for j in range(customer_nodes):
        if i == j:
            continue
        elif j in omega[i]:
            z[(i, j)] = solver.IntVar(
                0, solver.infinity(), 'z'+str(i) + "_" + str(j))
        else:
            z[(i, j)] = solver.IntVar(0, 0, 'z'+str(i) + "_" + str(j))
solver.Add(solver.Sum([x[i] for i in range(customer_nodes)]) == p)
for key, nodesList in N_k.items():
    solver.Add(solver.Sum([x[j] for j in nodesList]) >= y[key])
for i in range(customer_nodes):
    solver.Add(solver.Sum([z[(i, j)]
                           for j in omega[i] if i != j]) <= (m-1)*x[i])
    if i != warehouse_no:
        solver.Add((solver.Sum([z[(i, j)] for j in omega[i] if i != j]) -
                    solver.Sum([z[(j, i)] for j in omega[i] if i != j])) >= x[i])
    if i == warehouse_no:
        solver.Add((solver.Sum([z[(i, j)] for j in omega[i] if i != j]) -
                    solver.Sum([z[(j, i)] for j in omega[i] if i != j])) <= x[i] - m)

solver.Maximize(solver.Sum([service_demand_customer[i] * y[i] for i in range(customer_nodes)]))
sol = solver.Solve()
recharging_points = []
recharging_points.append(warehouse_no)
print('Solution:')
print('Objective value =', solver.Objective().Value())
for i in range(customer_nodes):
    print('x', i, '=', x[i].solution_value())
    if x[i].solution_value() == 1.0:
        recharging_points.append(i)
        print("Found")
    print('y', i, '=', y[i].solution_value())
print('Objective value =', solver.Objective().Value())
print('\nAdvanced usage:')
print('Problem solved in %f milliseconds' % solver.wall_time())
print('Problem solved in %d iterations' % solver.iterations())
print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
output_recharging_file = open("recharging_points.txt", "w+")
for points in recharging_points:
    output_recharging_file.write(str(points) + "\n")
