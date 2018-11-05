from __future__ import division
from collections import Counter
from matplotlib import pyplot as plt
import math
import random

def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find approximate inverse using binary search"""
    
    # if not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)
    
    low_z, low_p = -10.0, 0            # normal_cdf(-10) is (very close to) 0
    hi_z,  hi_p  =  10.0, 1            # normal_cdf(10)  is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2     # consider the midpoint
        mid_p = normal_cdf(mid_z)      # and the cdf's value there
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint is still too high, search below it
            hi_z, hi_p = mid_z, mid_p
        else:
            break

    return mid_z

def normal_approximation_to_binomial(n, p):
    """finds mu and sigma corresponding to Binomial(n,p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma

#the normal cdf _is_ the probability the variable is below a threshold
normal_probability_below = normal_cdf

#it's above the threshold if it's not below the threshold
def normal_probability_above(lo, mu=0, sigma=1):
    return 1 - normal_cdf(lo, mu, sigma)

#it's beween if it's less than hi, but no less than lo
def normal_probability_between(lo, hi, mu=0, sigma=1):
    return normal_cdf(hi,mu,sigma) - normal_cdf(lo,mu,sigma)

#it's outside if it's not between
def normal_probability_outside(lo, hi, mu=0, sigma=1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)

def normal_upper_bound(probabiliy, mu=0, sigma=1):
    """return the z for which P(Z <= z) = probability"""
    return inverse_normal_cdf(probabiliy, mu, sigma)

def normal_lower_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z >= z) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)

def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """returns the symmetric (about the mean) bounds
    that contain specified probability"""
    tail_probability = (1 - probability) / 2

    #upper bound should have tail_probability above it
    upper_bound = normal_lower_bound(tail_probability,mu,sigma)

    #lower bound should have tail_probability below it
    lower_bound = normal_upper_bound(tail_probability,mu,sigma)

    return lower_bound, upper_bound

#let's say we flip a coin n=1000 times, if our hypothesis is true and the coin is fair, X should be
# distributed normally with a mean of 50% and an SD of 15.8

mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)

#set our significance to 5%
normal_two_sided_bounds(0.95, mu_0, sigma_0) # (469, 531)

#95% bounds based on assumption p = 0.5
lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)

#actual mu and sigma based on p = 0.55 (unfair coin)
mu_1, sigma_1 = normal_approximation_to_binomial(1000,0.55)

#a type 2 error means we fail to reject the null hypothesis
#which will happen when X is still inside our original interval
type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
power = 1 - type_2_probability

def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        #if x is greater than the mean, the tail is what's greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        #if x is less than the mean, the tail is what's less than x
            return 2 * normal_probability_below(x, mu, sigma)

#gives the p value for 530 heads
#two_sided_p_value(529.5, mu_0, sigma_0) == 0.062, can't reject null
#two_sided_p_value(531.5, mu_0, sigma_0) == 0.046, can reject null

# --- Confidence Intervals ---
p_hat = 540 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1-p_hat) / 1000)
normal_two_sided_bounds(0.95,mu,sigma) # [0.509, 0.570] "fair coin" does not lie in confidence interval

# --- Example - Analyzing Results of A/B Test
# Null hypothesis: P_A and P_B are the same
def estimated_parameters(N, n):
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma

def a_b_test_statistic(N_A, n_A, N_B, n_B):
    p_A, sigma_A = estimated_parameters(N_A,n_A)
    p_B, sigma_B = estimated_parameters(N_B,n_B)
    return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)

z = a_b_test_statistic(1000, 200, 1000, 180)    # -1.14
two_sided_p_value(z)    # 0.254, can't reject null hypothesis

z = a_b_test_statistic(1000, 200, 1000, 150)    # -2.94
two_sided_p_value(z)    # 0.003, can reject null hypothesis





