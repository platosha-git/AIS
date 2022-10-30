from pandas_ods_reader import read_ods
from tabulate import tabulate
import numpy as np
import json

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def get_data_from_ods(ods_path):
    data = read_ods(ods_path, 1, headers=True)
    data.index = data.index + 1
    return data

def get_data_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data

def write_data_to_html(data, html_path):
    f = open(html_path, 'w')
    f.write(tabulate(data, headers="keys", tablefmt='html'))

def plot_matrices(matrix1, title1, matrix2, title2, \
                    matrix3, title3, matrix4, title4):
    n = matrix1.shape[0]

    plt.subplot(221)
    plt.imshow(matrix1)
    plt.title(title1)
    
    plt.colorbar()
    plt.xticks(np.arange(0, n, step=2))
    plt.yticks(np.arange(0, n, step=2))

    plt.subplot(222)
    plt.imshow(matrix2)
    plt.title(title2)
    
    plt.colorbar()
    plt.xticks(np.arange(0, n, step=2))
    plt.yticks(np.arange(0, n, step=2))

    plt.subplot(223)
    plt.imshow(matrix3)
    plt.title(title3)
    
    plt.colorbar()
    plt.xticks(np.arange(0, n, step=2))
    plt.yticks(np.arange(0, n, step=2))

    plt.subplot(224)
    plt.imshow(matrix4)
    plt.title(title4)
    
    plt.colorbar()
    plt.xticks(np.arange(0, n, step=2))
    plt.yticks(np.arange(0, n, step=2))
    
    
    plt.show()
