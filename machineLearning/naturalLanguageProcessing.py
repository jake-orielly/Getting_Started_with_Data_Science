from __future__ import division
import matplotlib.pyplot as plt
import math, random, re, requests
from collections import defaultdict, Counter
from bs4 import BeautifulSoup

# --- A less pretty but more informative take on word clouds ---
def print_resume_data():
    data = [ ("big data", 100, 15), ("Hadoop", 95, 25), ("Python", 75, 50),
            ("R", 50, 40), ("machine learning", 80, 20), ("statistics", 20, 60),
            ("data science", 60, 70), ("analytics", 90, 3),
            ("team player", 85, 85), ("dynamic", 2, 90), ("synergies", 70, 0),
            ("actionable insights", 40, 30), ("think out of the box", 45, 10),
            ("self-starter", 30, 50), ("customer focus", 65, 15),
            ("thought leadership", 35, 35)]

    def text_size(total):
        """equals 8 if total is 0, 28 if total is 200"""
        return 8 + total / 200 * 20

    for word, job_pop, resume_pop in data:
        plt.text(job_pop, resume_pop, word,
                 ha='center', va='center',
                 size=text_size(job_pop + resume_pop))
    plt.xlabel("Popularity on Job Postings")
    plt.ylabel("Popularity on Resumes")
    plt.axis([0, 100, 0, 100])
    plt.xticks([])
    plt.yticks([])
    plt.show()

def fix_unicode(text):
    return text.replace(u"\u2019","'")

url = "https://www.oreilly.com/ideas/what-is-data-science"
html = requests.get(url).text
soup = BeautifulSoup(html, "html5lib")

content = soup.find("div", "article-body")
regex = r"[\w']+|[\.]"  # matches a word or a period

document = []

for paragraph in content("p"):
    words = re.findall(regex, fix_unicode(paragraph.text))
    document.extend(words)

bigrams = zip(document, document[1:])
transitions = defaultdict(list)

for prev, current in bigrams:
    transitions[prev].append(current)

def generate_using_bigrams():
    current = "."   # next word will be start of a sentence
    result = []
    while True:
        next_word_candidates = transitions[current] #bigrams (current, _)
        current = random.choice(next_word_candidates)   #choose one at random
        result.append(current)  #append it to the results
        if current == "." : return " ".join(result) # if "." we're done

#print(generate_using_bigrams())

trigrams = zip(document, document[1:], document[2:])
trigram_transitions = defaultdict(list)
starts = []

for prev, current, next in trigrams:
    if prev == ".":  # if the previous "word" was a period
        starts.append(current)  # then this is a start word

    trigram_transitions[(prev, current)].append(next)

def generate_using_trigrams():
    current = random.choice(starts) # choose a random starting word
    prev = "."  # and precede it with a "."
    result = [current]
    while True:
        next_word_candidates = trigram_transitions[(prev, current)]
        next_word = random.choice(next_word_candidates)

        prev, current = current, next_word
        result.append(current)

        if current == ".":
            return " ".join(result)

print(generate_using_trigrams())

