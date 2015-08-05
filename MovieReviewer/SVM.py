#!/usr/bin/python

from sklearn import svm
from sklearn.externals import joblib
import os
from sys import argv
from nltk import pos_tag as pt

wordList = []
movieReviewer = None

def loadModule(mode):
    global movieReviewer
    try:
        movieReviewer = joblib.load("./SVM/movieReviewer%s.svm" % mode)
    except:
        import SVMTrain
        movieReviewer = joblib.load("./SVM/movieReviewer%s.svm" % mode)

def loadWords(mode):
    global wordList
    if mode == 'U':
        wordList = open('./SVM/PosKeywords.txt', 'r').read().split()
        wordList += open('./SVM/NegKeywords.txt', 'r').read().split()
        return wordList
    elif mode == 'A':
        wordList = open('adjKeywords.txt', 'r').read().split('\n')[:-1]
        result = []
        for i in wordList:
            result.append(i.split()[0])
        wordList = result[:1000] + result[-1000:]
    elif mode == 'P':
        wordList = open('PosKeywords.txt', 'r').read().split('\n')[:-1]
        result = []
        for i in wordList:
            result.append(eval("".join(i.split()[:-1])))
        wordList = result[:1000] + result[-1000:]

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
    loadModule(argv[1])
    os.system("echo -n 'loading keywords...\t\t'")
    wordList = loadWords(argv[1])
    os.system("echo -n '[done]\n'")

    review = asciify(open(raw_input("Please enter the review location: "), 'r').read()).split()
    if argv[1] == 'P':
        review = pt(review)
    X = intersection(wordList, review)
    result = movieReviewer.predict(X)[0]

    if (result > 0):
        print "Good movie!"
        #print result
    else:
        print "BAD movie!"
        #print result
