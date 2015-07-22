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

for i in os.listdir('./train/pos'):
    f = nltk.pos_tag(asciify(open('./tokens/pos/' + i, 'r').read()).split())
    featureExtractor(f, 1)

for i in os.listdir('./train/neg'):
    f = nltk.pos_tag(asciify(open('./tokens/neg/' + i, 'r').read()).split())
    featureExtractor(f, 0)

for i in freqDict.keys():
    if int(freqDict[i][1]) > 15:
        freqDict[i] = bayesTheorem(0.5, freqDict[i][1] / 2000., freqDict[i][0] / 1000.)
    else:
        del freqDict[i]

sortedDict = sorted(freqDict.items(), key = operator.itemgetter(1))

for i in sortedDict:
    if i[1] > 0:
        output.write("%s \t\t %.4f\n" % (str(i[0]).strip(' '), i[1]))

output.close()
