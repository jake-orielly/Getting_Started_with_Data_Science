from __future__ import division
import math



def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i
               for v_i, w_i in zip(v,w))

def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v,v)

def vector_add(v, w, addon=1):
    """adds corresponding elements"""
    return [v_i + w_i*addon for v_i, w_i in zip(v,w)]

def vector_subtract(v,w):
    return vector_add(v, w, addon=-1)

def magnitude(v):
    return math.sqrt(sum_of_squares(v))

def distance(v, w):
    return magnitude(vector_subtract(v,w))

def mean(args):
    return sum(args)/len(args)
