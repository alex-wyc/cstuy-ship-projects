#!/usr/bin/python

from SVM import asciify, intersection
from sklearn import svm
from sklearn.externals import joblib
import os
from sys import argv
from nltk import pos_tag as pt

wordList = []

try:
    movieReviewer = joblib.load("./SVM/movieReviewer%s.svm" % argv[1])
except:
    print "Please run SVMTrain.py first!"

os.system("echo -n 'loading keywords...\t\t'")
# argv = command line arguments, argv[1] = type of training to be done
# Possible arguments: -POS: part of speech, -U: unigrams, -A: adjectives
if argv[1] == '-POS':
    POSList = open('PosKeywords.txt', 'r').read().split("\n")
    for i in POSList:
        wordList.append("".join(i.split()[:-1]))

elif argv[1] == '-U':
    wordList = open("SVM/PosKeywords.txt", 'r').read().split()
    wordList += open("SVM/NegKeywords.txt", 'r').read().split()

elif argv[1] == 'A':
    AdjList = open('Adjectives.txt', 'r').read().split("\n")
    for i in AdjList:
        wordList.append("".join(i.split()[:-1]))
# this is so that it only takes in 1000 keywords.
os.system("echo -n '[done]\n'")

os.system("echo -n 'testing files:\n[00%'")
done = 0
progress = 0
correct = 0

files = os.listdir('./test/neg')[:2000]
total = float(len(files)) * 2

for i in files:
    f = asciify(open('./test/neg/' + i, 'r').read()).split()
    if argv[1] == '-POS' or argv[1] == '-U':
        f = pt(f)
    result = movieReviewer.predict(intersection(wordList, f))[0]
    if result < 0:
        correct += 1
    else:
        print result
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        os.system("echo -n '\b\b\b=%2d%%'" % progress)

files = os.listdir('./test/pos')[:2000]

for i in files:
    f = asciify(open('./test/pos/' + i, 'r').read()).split()
    if argv[1] == '-POS' or argv[1] == '-U':
        f = pt(f)
    result = movieReviewer.predict(intersection(wordList, f))[0]
    if result > 0:
        correct += 1
    else:
        print result
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        os.system("echo -n '\b\b\b=%2d%%'" % progress)

os.system("echo -n '\b\b\b\b]    \t[done]\n'")

print "Result: %.2f%% accurate!" % (correct * 100 / total)
