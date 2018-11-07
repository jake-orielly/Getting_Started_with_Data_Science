from collections import Counter
import matplotlib.pyplot as plt
import json, unicodedata, sys, io

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                    if unicodedata.category(unichr(i)).startswith('P'))

def remove_punctuation(text):
    return text.translate(tbl)

with open('../../../../../../../Volumes/jakesExternalDrive/tweets.txt','r') as f:
    #with open('tweets.txt','r') as f:
    file = f.read()
    file = file.split('\n\n')[:-1]

    counter = Counter(remove_punctuation(word.lower())       # lowercase words
                      for item in file
                      for word in json.loads(item)['text'].strip().split(' ')  # split on spaces
                      if remove_punctuation(word))


with io.open('common_words.txt','w',encoding='utf-8') as f:
    count = 1
    for word, word_count in counter.most_common(500):
        f.write((str(count) + ' : ' +str(word_count) + ' : ' + word + '\n'))
        count += 1

print('Done!')
