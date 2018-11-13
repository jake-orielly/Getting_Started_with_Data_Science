import functions as fnc
from matplotlib import pyplot as plt
import random

class KMeans:
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k  #number of clusters
        self.means = None   #means of clusters

    def classify(self,input):
            """return the index of the cluster closest to the input"""
            return min(range(self.k),
                       key=lambda i: fnc.squared_distance(input, self.means[i]))

    def train(self, inputs):
        #choose k random points as the initial means
        self.means = random.sample(inputs, self.k)
        assignments = None

        while True:
            #Find new assignments
            new_assignments = map(self.classify, inputs)

            #if no assignments have changed, we're done
            if assignments == new_assignments:
                return

            #otherwise keep the new assignments
            assignments = new_assignments

            #and compute new means based on the new assignments
            for i in range(self.k):
                #find all the points assigned to cluster i
                i_points = [p for p, a in zip(inputs, assignments) if a == i]

                #make sure i_points is not empty so don't divide by 0
                if i_points:
                    self.means[i] = fnc.vector_mean(i_points)

inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]

random.seed(0)
clusterer = KMeans(3)
clusterer.train(inputs)

plt.scatter(zip(*inputs)[0],zip(*inputs)[1])
plt.title('This data doesn\'t have labels')
ax = plt
for i in clusterer.means:
    ax.plot(i[0], i[1], "or")
plt.show()
