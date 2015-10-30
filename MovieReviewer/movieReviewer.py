#!/usr/bin/python
#!C:\Python27\python

import SVM
import bayesClassifier
from sklearn import tree
from sklearn.externals import joblib


Tree = joblib.load("DT/movieReview.dt")

def rate(review):
    review = SVM.asciify(review)

    inputData = []

    # 1st element = bayes with unigram
    bayesClassifier.loadData('U')
    inputData.append(bayesClassifier.percentPositive(review))
    # bayes with adjective
    bayesClassifier.loadData('A')
    inputData.append(bayesClassifier.percentPositive(review))
    # bayes with POS
    bayesClassifier.loadData('P')
    bayesClassifier.partOfSpeech = True
    inputData.append(bayesClassifier.percentPositive(review))

    # SVM with unigram
    review = review.split()
    SVM.loadModule('U')
    SVM.loadWords('U')
    X = SVM.intersection(SVM.wordList, review)
    # SVM with adjective
    inputData.append(SVM.movieReviewer.predict(X)[0])
    SVM.loadModule('A')
    SVM.loadWords('A')
    X = SVM.intersection(SVM.wordList, review)
    inputData.append(SVM.movieReviewer.predict(X)[0])

    return Tree.predict(inputData)[0]

if __name__ == '__main__':
    reviewLoc = raw_input("Please enter a route to the review: ")
    review = open(reviewLoc, 'r').read()
    rating = rate(review)
    if rating < 0:
        print "BAD movie!"
    else:
        print "GOOD movie!"
