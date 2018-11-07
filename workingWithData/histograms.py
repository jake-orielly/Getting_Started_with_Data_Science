from __future__ import division
from collections import Counter
from matplotlib import pyplot as plt
import functions as cdf
import random, math

def bucketize(point, bucket_size):
    return bucket_size * math.floor(point/bucket_size)

def make_histogram(points, bucket_size):
    return Counter(bucketize(point, bucket_size) for point in points)

def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()

random.seed(0)

#uniform between -100 and 100
uniform = [200 * random.random() - 100 for _ in range(10000)]

#normal distribution with mean 0, standard deviation 57
normal = [57 * cdf.inverse_normal_cdf(random.random())
          for _ in range(10000)]

plot_histogram(uniform, 10, "Uniform Histogram")
plot_histogram(normal, 10, "Normal Histogram")
