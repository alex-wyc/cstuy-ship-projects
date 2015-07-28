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
    if freqDict[i][1] < 20:
        del freqDict[i]
    else:
        freqDict[i].append(bayesTheorem(0.5, freqDict[i][1] / (2 * total), (freqDict[i][1] - (freqDict[i][1] - abs(freqDict[i][0]))/2) / total))

sortedDict = sorted(freqDict.items(), key = lambda x: x[1][0])

sortedDict = sortedDict[:500] + sortedDict[-500:]

for i in sortedDict:
    if float(i[1][0]) > 0:
        outputGood.write("%s \t\t %.4f\n" % (str(i[0]).strip(' '), i[1][2]))
    elif float(i[1][0]) < 0:
        outputBad.write("%s \t\t %.4f\n" % (str(i[0]).strip(' '), i[1][2]))

sortedDict = sorted(freqDict.items(), key = operator.itemgetter(1))

output.close()
