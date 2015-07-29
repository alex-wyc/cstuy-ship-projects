import nltk
from sklearn import tree
from sklearn.externals import joblib

att = open('DATA.csv').read()

numLines = 0

l = att.split('\n')
numLines = len(l)
attributes = []

for element in l:
    temp = element.split(',')
    temp2 = []
    for s in temp:
        temp2.append(float(s))
    attributes.append(temp2)

samples = []
x = 0
while (x < numLines/2):
    samples[x] = 1
    x = x + 1
while (x < numLines):
    samples[x] = -1
    x = x + 1

clf = tree.DecisionTreeClassifier()
clf = clf.fit(attributes,samples)

joblib.dump(clf, "DT/movieReview.dt")
