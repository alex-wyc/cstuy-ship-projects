#!/usr/bin/python

from sklearn import svm
from sklearn.externals import joblib
import os
from sys import argv

wordList = []

try:
    movieReviewer = joblib.load("movieReviewer.svm")
except:
    import SVMTrain
    movieReviewer = joblib.load("movieReviewer.svm")

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

if __name__ == '__main__':
    review = asciify(open(raw_input("Please enter the review location: "), 'r').read()).split()
    X = intersection(wordList, review)
    result = movieReviewer.predict(X)[0]

    if (result > 0):
        print "Good movie!"
        #print result
    else:
        print "BAD movie!"
        #print result
