#!/usr/bin/python
#!C:\Python27\python

import nltk
import math

review = "review goes here!!!"

posKeywordList = {}
negKeywordList = {}

def loadData():
    f = open("PosKeywords.txt", 'r').read().split('\n')[:-1]
    for i in f:
        data = i.split()
        posKeywordList[data[0]] = float(data[1])

    f = open("NegKeywords.txt", 'r').read().split('\n')[:-1]
    for i in f:
        data = i.split()
        negKeywordList[data[0]] = float(data[1])

def intersection(list1, list2):
    return list(set(list1) & set(list2))

def percentPositive(review):
    tokens = nltk.pos_tag(nltk.word_tokenize(review))
    posWordList = intersection((w[0] for w in tokens), posKeywordList.keys())
    negWordList = intersection((w[0] for w in tokens), negKeywordList.keys())
    
    exp = 0
    for k in posWordList:
        exp += math.log(1 - posKeywordList[k]) - math.log(posKeywordList[k])
    for k in negWordList:
        exp -= math.log(1 - negKeywordList[k]) - math.log(negKeywordList[k])
    return 1 / (1 + math.exp(exp))

def asciify(text):
    return ''.join([i for i in text if ord(i) < 128])

if __name__ == '__main__':
    loadData()
    reviewLoc = raw_input("Please enter a route to the review: ")
    review = asciify(open(reviewLoc, 'r').read())
    print "%.2f%% of a great movie." % (percentPositive(review) * 100)
