from __future__ import division
import functions as fnc
import matplotlib
import matplotlib.pyplot as plt
import math, random

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

"""for x in [0, 1]:
    for y in [0, 1]:
        print(x, y, feed_forward(xor_network,[x,y])[-1])"""

def backpropagate(network, input_vector, targets):
    hidden_outputs, outputs = feed_forward(network, input_vector)

    # the output * (1 - output) is from the derivative of sigmoid
    output_deltas = [output * (1 - output) * (output - target)
                     for output, target in zip(outputs, targets)]

    # adjust weights for output layer, one neuron at a time
    for i, output_neuron in enumerate(network[-1]):
        # focus on the ith output layer neuron
        for j, hidden_output in enumerate(hidden_outputs + [1]):
            # adjust the jth weight based on both this neuron's delta and jth input
            output_neuron[j] -= output_deltas[i] * hidden_output

    #back-propagate errors to hidden layer
    hidden_deltas = [hidden_output * (1 - hidden_output) *
                     fnc.dot(output_deltas, [n[i] for n in output_layer])
                     for i, hidden_output in enumerate(hidden_outputs)]

    #adjust weights for hidden layer, one neuron at a time
    for i, hidden_neuron in enumerate(network[0]):
        for j, input in enumerate(input_vector + [1]):
            hidden_neuron[j] -= hidden_deltas[i] * input

# --- Defeating a single digit "captcha" ---
# each "digit" is reprsented by a 5x5 of "on" or "off" pixels
raw_digits = [
              """11111
                  1...1
                  1...1
                  1...1
                  11111""",
              
              """..1..
                  ..1..
                  ..1..
                  ..1..
                  ..1..""",
              
              """11111
                  ....1
                  11111
                  1....
                  11111""",
              
              """11111
                  ....1
                  11111
                  ....1
                  11111""",
              
              """1...1
                  1...1
                  11111
                  ....1
                  ....1""",
              
              """11111
                  1....
                  11111
                  ....1
                  11111""",
              
              """11111
                  1....
                  11111
                  1...1
                  11111""",
              
              """11111
                  ....1
                  ....1
                  ....1
                  ....1""",
              
              """11111
                  1...1
                  11111
                  1...1
                  11111""",
              
              """11111
                  1...1
                  11111
                  ....1
                  11111"""]     
                      
def make_digit(raw_digit):
  return [1 if c == '1' else 0
          for row in raw_digit.split("\n")
          for c in row.strip()]
      
inputs = map(make_digit, raw_digits)

targets = [[1 if i == j else 0 for i in range(10)]
          for j in range(10)]

input_size = 25
num_hidden = 5 # we'll have 5 neurons in the hidden layer
output_size = 10 # we'll need 10 ouputs
random.seed(0)
#each hidden neuron has one weight per input, plus a bias weight
hidden_layer = [[random.random() for __ in range(input_size+1)]
                for __ in range(num_hidden)]

#each output neuron has one weight per hidden neuron plus a bias weight
output_layer = [[random.random() for __ in range(num_hidden + 1)]
                for __ in range(output_size)]

#the network starts out with random weights
network = [hidden_layer, output_layer]

#we then train with our backpropogation algorithm
for __ in range(10000):
    for input_vector, target_vector in zip(inputs, targets):
        backpropagate(network, input_vector, target_vector)

def predict(input):
    return feed_forward(network, input)[-1]

#print(predict(inputs[7])) #Neural network says, it's very probably a 7

weights = network[0][0] #first neuron in hidden layer
abs_weight = map(abs, weights)  #darkness only depends on absolute value

grid = [abs_weight[row:(row+5)]    #turn the weights into a 5x5 grid
        for row in range(0,25,5)]   #[weights[0:5], ..., weights[20:25]]

ax = plt.gca()

ax.imshow(grid, #same as plt.imshow
          cmap=matplotlib.cm.binary,    #use white-black color scale
          interpolation='none') #plot blocks as blocks

def patch(x, y, hatch, color):
    """return a matplotlib 'patch' object with specified location, crosshatch patern, and color"""
    return matplotlib.patches.Rectangle((x - 0.5, y - 0.5), 1, 1,
                                 hatch=hatch, fill=False, color=color)

#cross-hatch the negative weights
for i in range(5):
    for j in range(5):
        if weights[5*i + j] < 0:
            #add black and white hatches so visible whether dark or light
            ax.add_patch(patch(j, i, '/', 'white'))
            ax.add_patch(patch(j, i, '\\', 'black'))

plt.show()



