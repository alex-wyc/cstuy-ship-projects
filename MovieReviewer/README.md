#Movie Reviewer
This program seeks to understand the intricacies behind meanings of movie
reviews in a variety of fashions, using Bayes Classifier, Support Vector Machine
and Decision Tree.

##Compile Data
Train:
```
./bayesClassifierTrain.py
./SVMTrain.py
./DecisionTreeTrain.py
```

##Test Results
To get the results of each of the methods and the combined method, we used
files SVMTest.py and bayesTest.py. Or to see the combined result of all
three, simply run movieReviewTest.py.

If you want to see these in action fo single files, simply run SVM.py,
bayesClassifier.py or movieReviewer.py and they will prompt you for file
location.

##Tools Used:
- nltk: a python library that does natural language processing
- scikit-learn: a python library that does machine learning algorithms

##Sources Cited:
[Cornell Movie Review Data] (http://www.cs.cornell.edu/people/pabo/movie-review-data/)

[Stanford Movie Review Data] (http://ai.stanford.edu/~amaas/data/sentiment/)
