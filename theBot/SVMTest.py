#!/usr/bin/python

import SVM
from sklearn.externals import joblib
import os
from sys import argv

os.system("echo -n 'loading keywords...\t\t'")
SVM.loadModule(argv[1])
SVM.loadWords(argv[1])
os.system("echo -n '[done]\n'")

os.system("echo -n 'testing files:\n[00%'")
files = os.listdir('./test/pos')[:3000]
total = float(len(files)) * 2
done = 0
progress = 0
correct = 0

for i in files:
    f = SVM.asciify(open('./test/pos/' + i, 'r').read()).split()
    result = SVM.movieReviewer.predict(SVM.intersection(SVM.wordList, f))[0]
    if result > 0:
        correct += 1
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        #os.system("echo -n '\b\b\b=%2d%%'" % progress)

files = os.listdir('./test/neg')[:3000]

for i in files:
    f = SVM.asciify(open('./test/neg/' + i, 'r').read()).split()
    result = SVM.movieReviewer.predict(SVM.intersection(SVM.wordList, f))[0]
    if result < 0:
        correct += 1
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        os.system("echo -n '\b\b\b=%2d%%'" % progress)
os.system("echo -n '\b\b\b\b]    \t[done]\n'")

print "Result: %.2f%% accurate!" % (correct * 100 / total)
