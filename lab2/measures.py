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


def get_correlation_matix(data, metric):
    matrix = []
    n = data.shape[0]

    for i in range(n):
        cur_vector = []
        for j in range(n):
            measure = metric(data.values.tolist()[i], data.values.tolist()[j])
            cur_vector.append(measure)
        matrix.append(np.array(cur_vector))

    matrix = np.array(matrix)
    return matrix
