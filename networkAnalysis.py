from __future__ import division
import math, random, re
from collections import defaultdict, Counter, deque
from functions import dot, get_row, get_column, make_matrix, magnitude, scalar_multiply, shape, distance
from functools import partial

users = [
         { "id": 0, "name": "Hero" },
         { "id": 1, "name": "Dunn" },
         { "id": 2, "name": "Sue" },
         { "id": 3, "name": "Chi" },
         { "id": 4, "name": "Thor" },
         { "id": 5, "name": "Clive" },
         { "id": 6, "name": "Hicks" },
         { "id": 7, "name": "Devin" },
         { "id": 8, "name": "Kate" },
         { "id": 9, "name": "Klein" }
         ]

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

for user in users:
    user["friends"] = []

for i, j in friendships:
    #user[i] is the user whose id is i
    users[i]["friends"].append(users[j]) # add i as a friend of j
    users[j]["friends"].append(users[i]) # add j as a friend of i

def shortest_paths_from(from_user):
    # a dictionary from "user_id" to *all* shortest paths to that user
    shortest_paths_to = {from_user["id"]: [[]]}

    # a queue of (pervious user, next user) that we need to check
    # starts out with all pairs (from_user, friend_of_from_user)
    frontier = deque((from_user, friend)
                     for friend in from_user["friends"])

    # keep going until we empty the queue
    while frontier:
        prev_user, user = frontier.popleft() # remove first user in the queue
        user_id = user["id"]

        # because of the way we're adding to the queue
        # neccessarily we already know some shortest paths to prev_user
        paths_to_prev_user = shortest_paths_to[prev_user["id"]]
        new_paths_to_user = [path + [user_id] for path in paths_to_prev_user]

        # it's possible we already know the shortest path
        old_paths_to_user = shortest_paths_to.get(user_id, [])

        # what's the shortest path to here that we've seen so far?
        if old_paths_to_user:
            min_path_length = len(old_paths_to_user[0])
        else:
            min_path_length = float('inf')

        # only keep paths that aren't too long and are actually new
        new_paths_to_user = [path
                             for path in new_paths_to_user
                             if len(path) <= min_path_length
                             and path not in old_paths_to_user]

        shortest_paths_to[user_id] = old_paths_to_user + new_paths_to_user

        # add never-seen neighbors to the fronteir
        frontier.extend((user, friend)
                        for friend in user["friends"]
                        if friend["id"] not in shortest_paths_to)
    return shortest_paths_to

for user in users:
    user["shortest_paths"] = shortest_paths_from(user)

for user in users:
    user["betweenness_centrality"] = 0.0

for source in users:
    source_id = source["id"]
    for target_id, paths in source["shortest_paths"].iteritems():
        if source_id < target_id: # don't double count
            num_paths = len(paths) # how many shortest paths
            contrib = 1 / num_paths # contribution to centrality
            for path in paths:
                for id in path:
                    if id not in [source_id, target_id]:
                        users[id]["betweenness_centrality"] += contrib

def fareness(user):
    """the sum of the lengths of the shortest paths to each other user"""
    return sum(len(paths[0])
               for paths in user["shortest_paths"].values())

for user in users:
    user["closeness_centrality"] = 1 / fareness(user)

for user in users:
    print(user["betweenness_centrality"])

def matrix_product_entry(A,B,i,j):
    return dot(get_row(A,i), get_column(B,j))

def matrix_multiply(A, B):
    n1, k1 = shape(A)
    n2, k2 = shape(B)
    if k1 != n2:
        raise ArithmeticError("imcompatible shapes!")
    return make_matrix(n1, k2, partial(matrix_product_entry, A, B))

def vector_as_matrix(v):
    """returns the vector v (reprsented as a list) as a n x 1 matrix"""
    return [[v_i] for v_i in v]

def vector_from_matrix(v_as_matrix):
    """returns the n x 1 matrix as a list of values"""
    return [row[0] for row in v_as_matrix]

def matrix_operate(A, v):
    v_as_matrix = vector_as_matrix(v)
    product = matrix_multiply(A, v_as_matrix)
    return vector_from_matrix(product)
