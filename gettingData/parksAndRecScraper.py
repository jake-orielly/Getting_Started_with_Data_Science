from bs4 import BeautifulSoup
import requests

# Prints all Parks and Rec episodes with more viewers than set min

url = "https://en.wikipedia.org/wiki/List_of_Parks_and_Recreation_episodes"
soup = BeautifulSoup(requests.get(url).text, 'html5lib')

minViewers = 4.9 #minimum US viewers in millions

def above_min(item):
    return float(item('td')[-1].text.split('[')[0]) >= minViewers

episodes = [tr
       for tr in soup('tr','vevent') if above_min(tr)]

pairs = [(curr('td')[1].text,curr('td')[-1].text.split('[')[0])
         for curr in episodes]

for pair in pairs:
    print ('Episode: ' + pair[0] + ' Viewers: ' + pair[1])
