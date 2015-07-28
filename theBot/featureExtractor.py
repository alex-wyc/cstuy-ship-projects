#!/usr/bin/python

import nltk
import os
import operator

output = open('PosKeywords.txt', 'w')
freqDict = {}

def bayesTheorem(pOfGood, pOfWord, pOfWordAssumingGood):
    return (pOfWordAssumingGood * pOfGood) / pOfWord

def featureExtractor(document, increment):
    documentWords = set(document);
    for word in documentWords:
        if word in freqDict:
            freqDict[word][0] += increment
            freqDict[word][1] += 1
        else:
            freqDict[word] = [increment, 1]

def asciify(text):
    return "".join([i for i in text if ord(i) < 128])

files = os.listdir('./train/pos')
total = float(len(files))
done = 0
testing = 0
for i in files:
    f = nltk.pos_tag(asciify(open('./train/pos/' + i, 'r').read()).split())
    featureExtractor(f, 1)
    done += 1
    if (done / total > 1. / 10):
        os.system("echo -n '='")
        testing += done
        done = 0
    if(testing == total):
        os.system("echo -n 'test'")
    
os.system("echo -n 'abc'")

files = os.listdir('./train/neg')
assert total == float(len(files))
done = 0

for i in files:
    f = nltk.pos_tag(asciify(open('./train/neg/' + i, 'r').read()).split())
    featureExtractor(f, 0)
    done += 1
    if (done / total > 1. / 10):
        os.system("echo -n '='")
        done = 0

for i in freqDict.keys():
    if int(freqDict[i][1]) > 15:
        freqDict[i] = bayesTheorem(0.5, freqDict[i][1] / (2 * total), freqDict[i][0] / total)
    else:
        del freqDict[i]

sortedDict = sorted(freqDict.items(), key = operator.itemgetter(1))

for i in sortedDict:
    if i[1] > 0:
        output.write("%s\t\t%.4f\n" % (str(i[0]).strip(' '),i[1]))

output.close()
