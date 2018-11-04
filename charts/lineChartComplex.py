from matplotlib import pyplot as plt

variance = [1, 2, 4, 8, 16, 32, 64, 128, 256]
bias_squared = sorted(variance,reverse=True)
total_error = [x + y for x,y in zip(variance, bias_squared)]
xs = [i for i, _ in enumerate(variance)]

#multiple cause to plt.plot adds multiple series to same chart
plt.plot(xs, variance, 'g-', label='variance')  #green solid line
plt.plot(xs, bias_squared, 'r-.', label='bias^2')   #red dot-dashed line
plt.plot(xs, total_error, 'b:', label='total error')    #blue dotted line

#loc=9 means 'top center'
plt.legend(loc=9)
plt.xlabel('model complexity')
plt.title('The Bias Variance Tradeoff')
plt.show()
