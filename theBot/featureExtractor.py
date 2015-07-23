#!/usr/bin/python

import nltk
import os
import operator

outputGood = open('PosKeywords.txt', 'w')
outputBad = open('NegKeywords.txt', 'w')
freqDict = {}

def featureExtractor(document, increment):
    documentWords = set(document);
    for word in documentWords:
        if word in freqDict:
            freqDict[word][0] += increment
            freqDict[word][1] += 1
        else:
            freqDict[word] = [increment, 1]

def asciify(text):
    return "".join([i for i in list(text) if isAlphanumeric(i)])

def isAlphanumeric(char):
    order = ord(char)
    return (order >= 48 and order <= 57) or (order >= 65 and order <= 90) or (order >= 97 and order <= 122) or order == 9 or order == 32

files = os.listdir('./train/pos')
total = float(len(files))
done = 0

for i in files:
    f = asciify(open('./train/pos/' + i, 'r').read()).split()
    featureExtractor(f, 1)
    done += 1
    if (done / total > 1. / 10):
        os.system("echo -n '='")
        done = 0

files = os.listdir('./train/neg')
assert total == float(len(files))
done = 0

for i in files:
    f = asciify(open('./train/neg/' + i, 'r').read()).split()
    featureExtractor(f, -1)
    done += 1
    if (done / total > 1. / 10):
        os.system("echo -n '='")
        done = 0

for i in freqDict.keys():
    if int(freqDict[i][1]) < 20:
        del freqDict[i]
    else:
        freqDict[i] = int(freqDict[i][0])

sortedDict = sorted(freqDict.items(), key = operator.itemgetter(1))

#print sortedDict

for i in sortedDict:
    if i[1] > 0:
        outputGood.write("%s\n" % (str(i[0]).strip(' ')))
    elif i[1] < 0:
        outputBad.write("%s\n" % (str(i[0]).strip(' ')))

outputGood.close()
outputBad.close()
