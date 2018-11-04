from matplotlib import pyplot as plt

dogs = ['Koda','Nova','Willow','Winter']
cuteness = [6.5,9,8,4]

#bars are default width 0.8, so we'll add 0.1 to left coordinate to center them
xs = [i + 0.1 for i, _ in enumerate(dogs)]

plt.bar(xs,cuteness)
plt.ylabel('Cuteness')
plt.title('Some Cute Dogs')

#label x-axis with movie names at bar centers
plt.xticks([i + 0.1 for i, _ in enumerate(dogs)],dogs)

plt.show()