import numpy as np

# Евклидова мера близости
def Euclidean_measure(node1, node2):
    evk = Minkowski_measure(2, node1, node2)
    return evk


# Расстояние городских кварталов
def City_block_distance(node1, node2):
    city = Minkowski_measure(1, node1, node2)
    return city


# Косинусная мера близости
def Cosine_measure(node1, node2):
    sumMulty = 0
    for elem in range(len(node1)):
        sumMulty += node1[elem] * node2[elem]
    
    sum1 = 0
    for elem in range(len(node1)):
        sum1 += pow(node1[elem], 2)
    sum1 = pow(sum1, 1/2)
    
    sum2 = 0
    for elem in range(len(node2)):
        sum2 += pow(node2[elem], 2)
    sum2 = pow(sum2, 1/2)
    
    return (sumMulty / (sum1 * sum2))


# Расстояние Чебышева
def Chebyshev_measure(node1, node2):
    distance = []
    for elem in range(len(node1)):
        cur_dist = abs(node1[elem] - node2[elem])
        distance.append(cur_dist)
    
    return max(distance)


# Расстояние Минковского
def Minkowski_measure(p, node1, node2):
    sumMink = 0
    for elem in range(len(node1)):
        curDiff = abs(node1[elem] - node2[elem])
        sumMink += pow(curDiff, p)
    
    return pow(sumMink, 1/p)


# Древесная мера
def get_path_to_root(tree, node):
    for cur_node in tree:
        if "Name" in cur_node and cur_node["Name"] == node.name:
            path = cur_node["parent"]
    return path

def Tree_measure(tree, node1, node2):
    path1 = get_path_to_root(tree, node1)
    path2 = get_path_to_root(tree, node2)
    
    print("path1 = ", path1)
    print("path2 = ", path2)

    if (type(path1[0]) is list and type(path2[0]) is not list):
        common1 = sum(1 for i in path1[0] if i in path2)
        common2 = sum(1 for i in path1[1] if i in path2)
        
        distance1 = len(path1[0]) + len(path2) - 2 * common1
        distance2 = len(path1[1]) + len(path2) - 2 * common2
        distance = max(distance1, distance2)

        print("Distance = ", distance)

    if (type(path2[0]) is list):
        print(True)

    #common = sum(1 for i in path1 if i in path2)
    #print("common = ", common)

    #distance = len(path1) + len(path2) - 2 * common
    #print("distance = ", distance)


    return


def get_correlation_matix(data, metric):
    matrix = []
    n = data.shape[0]

    for i in range(n):
        cur_vector = []
        for j in range(n):
            if (metric == Minkowski_measure):
                measure = metric(0.5, data.values.tolist()[i], data.values.tolist()[j])
            else:
                measure = metric(data.values.tolist()[i], data.values.tolist()[j])
            cur_vector.append(measure)
        matrix.append(np.array(cur_vector))

    matrix = np.array(matrix)
    return matrix
