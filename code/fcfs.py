def get_recharging_points(fileName):
    file_pointer = open(fileName, "r")
    recharging_points = []
    for lines in file_pointer:
        recharging_points.append(int(float(lines.strip())))
    return recharging_points
