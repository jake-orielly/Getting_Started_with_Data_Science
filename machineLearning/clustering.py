import functions as fnc
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
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

# plot the clusters with red markers
clusterer = KMeans(3)
clusterer.train(inputs)

plt.scatter(zip(*inputs)[0],zip(*inputs)[1])
plt.title('Clustered based on vector means')
ax = plt
for i in clusterer.means:
    ax.plot(i[0], i[1], "or")
plt.show()

def squared_clustering_errors(inputs, k):
    """finds the total squared error from k-means clustering the inputs"""
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)

    return sum(fnc.squared_distance(input, means[cluster])
               for input, cluster in zip(inputs, assignments))

# now plot from 1 up to len(inputs) clusters

"""ks = range(1, len(inputs) + 1)
errors = [squared_clustering_errors(inputs, k) for k in ks]

plt.plot(ks, errors)
plt.xticks(ks)
plt.xlabel("k")
plt.ylabel("total squared error")
plt.title("Total Error vs. # of Clusters")
plt.show()"""

# use clustering to translate a picture into a small # of colors

"""path_to_png = r"./puppy.png"
img = mpimg.imread(path_to_png, 0);

pixels = [pixel for row in img for pixel in row]
clusterer = KMeans(5)
clusterer.train(pixels)

def recolor(pixel):
    cluster = clusterer.classify(pixel) # index of closest cluster
    return clusterer.means[cluster]

new_img = [[recolor(pixel) for pixel in row]
           for row in img]

plt.imshow(new_img)
plt.axis('off')
plt.show"""

# Bottom up clustering
def is_leaf(cluster):
    """a cluster is a leaf if it has length 1"""
    return len(cluster) == 1

def get_children(cluster):
    """returns the two children of this cluster if it's a merged cluster;
    raises an exception if this is a leaf cluster"""
    if is_leaf(cluster):
        raise TypeError("A leaf cluster has no children")
    else:
        return cluster[1]

def get_values(cluster):
    """returns the value in this cluster (if it's a leaf cluster)
        or all the values in the leaf clusters below it (if it's not)"""
    if is_leaf(cluster):
        return cluster
    else:
        return [value
                for child in get_children(cluster)
                for value in get_values(child)]

def cluster_distance(cluster1, cluster2, distance_agg=max):
    """compute all the pairwise distances between cluster1 and cluster2
        and appl distance_agg to the resulting list"""
    return distance_agg([fnc.distance(input1, input2)
                         for input1 in get_values(cluster1)
                         for input2 in get_values(cluster2)])

def get_merge_order(cluster):
    if is_leaf(cluster):
        return float('inf')
    else:
        return cluster[0] # merge_order is first element of the tuple

def bottom_up_cluster(inputs, distance_agg=max):
    # start with every input a leaf cluster / 1-tuple
    clusters = [(input,) for input in inputs]

    # as long as we have more than one cluster left...
    while len(clusters) > 1:
        # find the two closest clusters
        c1, c2 = min([(cluster1, cluster2)
                      for i, cluster1 in enumerate(clusters)
                      for cluster2 in clusters[:i]],
                      key=lambda(x, y): cluster_distance(x,y,distance_agg))

        # remove them from the list of clusters
        clusters = [c for c in clusters if c != c1 and c != c2]

        # merge them, using merge_order = # of clusters left
        merged_cluster = (len(clusters), [c1,c2])

        #and add their merge
        clusters.append(merged_cluster)

    return clusters[0]

base_cluster = bottom_up_cluster(inputs)

def generate_clusters(base_cluster, num_clusters):
    # start with a list with just the base cluster
    clusters = [base_cluster]

    # as long as we don't have enough clusters yet...
    while len(clusters) < num_clusters:
        #choose the last-merged of our clusters
        next_cluster = min(clusters, key=get_merge_order)
        # remove it from the list
        clusters = [c for c in clusters if c != next_cluster]
        # and add its children to the list (i.e., unmerge it)
        clusters.extend(get_children(next_cluster))
    
    return clusters

three_clusters = [get_values(cluster)
                  for cluster in generate_clusters(base_cluster, 3)]

for i, cluster, marker, color in zip([1,2,3],
                                     three_clusters,
                                     ['D','o','*'],
                                     ['r','g','b']):
    xs, ys = zip(*cluster)
    plt.scatter(xs, ys, color=color, marker=marker)

    #put a number at the mean of the cluster
    x,y = fnc.vector_mean(cluster)

    plt.plot(x,y, marker='$' + str(i) + '$', color='black')

plt.title("Bottom-Up Clusters Based on Max Distance")
plt.show()
