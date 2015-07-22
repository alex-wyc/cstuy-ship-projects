#!/usr/bin/python
#!C:\Python27\python

import nltk
import math

review = "review goes here!!!"

keywordList = {}

def loadData():
    f = open("PosKeywords.txt", 'r').read().split('\n')[:-1]
    for i in f:
        data = i.split()
        keywordList[eval(data[0] + data[1])] = float(data[2])

def intersection(list1, list2):
    return list(set(list1) & set(list2))

def percentPositive(review):
    tokens = nltk.pos_tag(nltk.word_tokenize(review))
    wordList = intersection(tokens, keywordList.keys())

    exp = 0
    for k in wordList:
        exp += math.log(1 - keywordList[k]) - math.log(keywordList[k])

    return 1 / (1 + math.exp(exp))

def asciify(text):
    return ''.join([i for i in text if ord(i) < 128])

if __name__ == '__main__':
    loadData()
    reviewLoc = raw_input("Please enter a route to the review: ")
    review = asciify(open(reviewLoc, 'r').read())
    print "%.2f%% of a great movie." % (percentPositive(review) * 100)
