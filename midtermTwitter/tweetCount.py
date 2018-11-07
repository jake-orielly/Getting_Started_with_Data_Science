from collections import Counter
import matplotlib.pyplot as plt
import json

with open('../../../../../../../Volumes/jakesExternalDrive/tweets.txt','r') as f:
    #with open('tweets.txt','r') as f:
    file = f.read()
    file = file.split('\n\n')[:-1]
    count = 0
    time_counts = Counter(json.loads(item)['created_at'].split(' ')[3][:4] for item in file)

times = sorted(time_counts)
time_vals = [time_counts[time] for time in times]
plt.plot(times, time_vals)
plt.ylabel('# of tweets')
plt.title('That\'s a lot of tweets!')
plt.show()
