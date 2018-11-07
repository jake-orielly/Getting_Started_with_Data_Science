from __future__ import division
from collections import Counter
from matplotlib import pyplot as plt
import functions as fnc
import math, random

def correlation_matrix(data):
    """returns the num_columns x num_columns matrix whose (i,j)th entry is the correlation between cloumns i and j of data"""

    _, num_columns = fnc.shape(data)

    def matrix_entry(i, j):
        return fnc.correlation(fnc.get_col(data,i), fnc.get_col(data,j))

    return make_matrix(num_columns, num_columns, matrix_entry)

def make_scatterplot_matrix():
    #first, generate some data
    num_points = 100
    
    def random_row():
        row = [None, None, None, None]
        row[0] = fnc.random_normal()
        row[1] = -5 * row[0] + fnc.random_normal()
        row[2] = row[0] + row[1] + 5 * fnc.random_normal()
        row[3] = 6 if row[2] > -2 else 0
        return row
    random.seed(0)
    data = [random_row()
            for _ in range(num_points)]

    _, num_columns = fnc.shape(data)
    fig, ax = plt.subplots(num_columns, num_columns)

    for i in range(num_columns):
        for j in range(num_columns):
            #scatter column_j on the x-axis vs column_i on the y
            if i != j: ax[i][j].scatter(fnc.getCol(data,j), fnc.getCol(data,i))

            #unless i == j, in which case show series name
            else: ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                                    xycoords='axes fraction',
                                    ha="center", va="center")

            #then hide axis labels except left and bottom charts
            if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
            if j > 0: ax[i][j].yaxis.set_visible(False)

    #fix bottom right and top left axis labels, whose charts only have text
    ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    ax[0][0].set_ylim(ax[0][1].get_ylim())

    plt.show()

make_scatterplot_matrix()
