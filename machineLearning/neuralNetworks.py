from __future__ import division
import functions as fnc
import math

def step_function(x):
    return 1 if x >= 0 else 0

def perceptron_output(weights, bias, x):
    """returns 1 if the perceptron 'fires', 0 if not"""
    calculation = fnc.dot(weights, x) + bias
    return step_function(calculation)

#print(perceptron_output([2,2],-3,[1,1])) # AND operator as perceptron
#print(perceptron_output([2,2],-1,[0,0])) # OR
#print(perceptron_output([-2],1,[1])) # NOT

def sigmoid(t):
    return 1 / (1 + math.exp(-t))

def neuron_output(weights, inputs):
    return sigmoid(fnc.dot(weights, inputs))

def feed_forward(neural_network, input_vector):
    """takes in a neural network (reprsented as a list of lists of lists of weights)
        and returns the output from forward-propogatin the input"""

    outputs = []

    #process one layer at a time
    for layer in neural_network:
        input_with_bias = input_vector + [1]    #add a bias input
        output = [neuron_output(neuron, input_with_bias) #compute the output
                  for neuron in layer] #for each neuron
        outputs.append(output) #and remember it

        #then the input to the next layer is the output of this one
        input_vector = output

    return outputs

xor_network= [# hidden layer
              [[20, 20, -30], # 'and' neuron
               [20, 20, -10]], # 'or' neuron
              # output layer
              [[-60, 60, -30]]] # second input but not first input layer

for x in [0, 1]:
    for y in [0, 1]:
        print(x, y, feed_forward(xor_network,[x,y])[-1])

