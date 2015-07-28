#!/usr/bin/python

from sklearn import svm
from sklearn.externals import joblib
import os
from sys import argv

X = []
y = []
wordList = []

def loadWords(mode):
    if mode == 'U':
        wordList = open('PosKeywords.txt', 'r').read().split()
        wordList += open('NegKeywords.txt', 'r').read().split()
        return wordList

os.system("echo -n 'loading keywords...\t\t'")
wordList = loadWords(argv[1])
os.system("echo -n '[done]\n'")

def asciify(text):
    return "".join([i for i in list(text) if isAlphanumeric(i)])

def isAlphanumeric(char):
    order = ord(char)
    return (order >= 48 and order <= 57) or (order >= 65 and order <= 90) or (order >= 97 and order <= 122) or order == 9 or order == 32

def intersection(keywords, text):
    resultVec = []
    textSet = set(text)
    for i in keywords:
        if i in textSet:
            resultVec.append(1)
        else:
            resultVec.append(0)
    return resultVec

os.system("echo -n 'loading training files:\n[05%'")
files = os.listdir('../train/pos')[:3000]
total = float(len(files)) * 2
done = 0
progress = 0

for i in files:
    f = asciify(open('../train/pos/' + i, 'r').read()).split()
    X.append(intersection(wordList, f))
    y.append(1)
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        os.system("echo -n '\b\b\b=%d%%'" % progress)

files = os.listdir('../train/neg')[:3000]

for i in files:
    f = asciify(open('../train/neg/' + i, 'r').read()).split()
    X.append(intersection(wordList, f))
    y.append(-1)
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        os.system("echo -n '\b\b\b=%d%%'" % progress)
os.system("echo -n '\b\b\b\b]    \t[done]\n'")
print("Training...")
movieReviewer = svm.SVC()
movieReviewer.fit(X, y)

joblib.dump(movieReviewer, "movieReviewer.svm")
print("Training complete! The trained machine is saved at \"movieReviewer.svm\"")
