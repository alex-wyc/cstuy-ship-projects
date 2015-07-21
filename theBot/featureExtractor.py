import nltk
import os
import operator

output = open('PosKeywords.txt', 'w')
freqDict = {}

def featureExtractor(document, increment):
    documentWords = set(document);
    for word in documentWords:
        if word in freqDict:
            freqDict[word][0] += increment
            freqDict[word][1] += 1
        else:
            freqDict[word] = [increment, 1]

for i in os.listdir('./tokens/pos'):
    f = open('./tokens/pos/' + i, 'r').read().split()
    featureExtractor(f, 1)

for i in os.listdir('./tokens/neg'):
    f = open('./tokens/neg/' + i, 'r').read().split()
    featureExtractor(f, 0)

for i in freqDict.keys():
    if int(freqDict[i][1]) > 13:
        freqDict[i] = [float(freqDict[i][0]) / 1000, freqDict[i][1] / 2000.]
    else:
        del freqDict[i]

sortedDict = sorted(freqDict.items(), key = operator.itemgetter(1))

for i in sortedDict:
    if i[1] > 0:
        output.write("%s \t\t %.4f \t\t %.4f\n" % (i[0], i[1][0], i[1][1]))

output.close()
