#!/usr/bin/python

import bayesClassifier
import os
import sys

total = 0
done = 0
accurate = 0
keywordList = {}

bayesClassifier.loadData()

files = os.listdir('./test/pos')

# comment this line to increase sample size
files = files[:1000]

total = len(files)

progress = 0

for i in files:
    done += 1
    if ((done * 100 / float(total)) > (progress + 10)):
        progress += 10
        os.system("echo -n '='")
    f = bayesClassifier.asciify(open('./test/pos/' + i, 'r').read())
    if bayesClassifier.percentPositive(f) > 0.5:
        accurate += 1

files = os.listdir('./test/neg')

# comment this line to increase sample size
files = files[:1000]

total += len(files)

negTotal = len(files)

progress = 0

done = 0

for i in files:
    done += 1
    if ((done * 100 / float(negTotal)) > (progress + 10)):
        progress += 10
        os.system("echo -n '='")
    f = bayesClassifier.asciify(open('./test/neg/' + i, 'r').read())
    if bayesClassifier.percentPositive(f) < 0.5:
        accurate += 1

print "test result on positive test data: %.2f" % (float(accurate) * 100 / total)


