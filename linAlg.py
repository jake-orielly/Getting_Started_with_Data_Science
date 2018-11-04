from __future__ import division
import math

v1 = [1,2]
v2 = [2,1]

# --- Vectors ---

def vector_add(v, w, addon=1):
    """adds corresponding elements"""
    return [v_i + w_i*addon for v_i, w_i in zip(v,w)]

def vector_subtract(v,w):
    return vector_add(v, w, addon=-1)

def vector_sum(vectors):
    return reduce(vector_add, vectors)

def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]

def vector_mean(vectors):
    """compute the vector whose ith element is the mean of the ith elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i
               for v_i, w_i in zip(v,w))

def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v,v)

def magnitude(v):
    return math.sqrt(sum_of_squares(v))

def squared_distance(v,w):
    """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_subtract(v, w))

def distance(v, w):
    return magnitude(vector_subtract(v,w))

# --- Matrices ---
A = [[1,2,3],
     [4,5,6]]


def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols

def getRow(A,i):
    return A[i]

def getCol(A,j):
    return [A_i[j]
            for A_i in A]

def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix whose (i,j)th entry is entry_fn(i, j)"""
    return [[entry_fn(i , j)
             for j in range(num_cols)]
            for i in range(num_rows)]

def is_diagonal(i,j):
    return 1 if i == j else 0

identity_matrix = make_matrix(5,5,is_diagonal)
