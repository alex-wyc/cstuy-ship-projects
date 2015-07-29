#!/usr/bin/python
#!C:\Python27\python

import nltk
import math
from sys import argv

review = "review goes here!!!"

posKeywordList = {}

def loadData(mode):
    if mode == 'U':
        f = open("Keywords.txt", 'r').read().split('\n')[:-1]
    elif mode == 'A':
        f = open("adjKeywords.txt", 'r').read().split('\n')[:-1]
    elif mode == 'P':
        f = open("PosKeywords.txt", 'r').read().split('\n')[:-1]


    for i in f:
        data = i.split()
        if mode == 'P':
            posKeywordList[eval("".join(data[:-1]))] = float(data[-1])
        else:
            posKeywordList[data[0]] = float(data[1])

def asciify(text):
    return "".join([i for i in list(text) if isAlphanumeric(i)])

def isAlphanumeric(char):
    order = ord(char)
    return (order >= 48 and order <= 57) or (order >= 65 and order <= 90) or (order >= 97 and order <= 122) or order == 9 or order == 32

def intersection(list1, list2):
    return list(set(list1) & set(list2))

def percentPositive(review):
    tokens = asciify(review).split()
    if argv[1] == 'P':
        tokens = nltk.pos_tag(tokens)
    posWordList = intersection(tokens, posKeywordList.keys())
    exp = 0
    for k in posWordList:
        exp += math.log(1 - posKeywordList[k]) - math.log(posKeywordList[k])
    return 1 / (1 + math.exp(exp))

def asciify(text):
    return ''.join([i for i in text if ord(i) < 128])

if __name__ == '__main__':
    loadData(argv[1])
    reviewLoc = raw_input("Please enter a route to the review: ")
    review = asciify(open(reviewLoc, 'r').read())
    print "%.2f%% of a great movie." % (percentPositive(review) * 100)
