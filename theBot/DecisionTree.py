import nltk
from sklearn import tree

att = open('foo.txt').read()

numLines = 0

l = att.split('\n')
numLines = len(l)
attributes = [[]]

for element in l:
    temp = element.split(',')
    temp2 = []
    for s in temp:
        temp2.append(int(s))
    attributes.append(temp2)

samples = []
x = 0
while (x < numLines/2):
    samples[x] = -1
    x = x + 1
x = 0
while (x < numLines):
    samples[x] = 1
    x = x + 1

clf = tree.DecisionTreeClassifier()
clf = clf.fit(attributes,samples)
