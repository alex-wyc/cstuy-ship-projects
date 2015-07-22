#!/usr/bin/python

import bayesClassifier
import os
import sys

total = 0
done = 0
accurate = 0
keywordList = {}

# hack from stackoverflow to make animation pretty
def getTerminalWidth():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1])

width = getTerminalWidth()

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
        print "%d%% complete" % (progress)
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
        print "%d%% complete" % (progress)
    f = bayesClassifier.asciify(open('./test/neg/' + i, 'r').read())
    if bayesClassifier.percentPositive(f) < 0.5:
        accurate += 1

print "test result on positive test data: %.2f" % (float(accurate) * 100 / total)


