import movieReviewer
from os import system, listdir

system('echo -n "[00%"')

files = listdir('./test/pos')[3000:3500]
total = float(len(files)) * 2
done = 0
progress = 0
correct = 0

for i in files:
    f = open('./test/pos/' + i, 'r').read()
    result = movieReviewer.rate(f)
    if result > 0:
        correct += 1
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        system("echo -n '\b\b\b=%2d%%'" % progress)

files = listdir('./test/neg')[3000:3500]

for i in files:
    f = open('./test/neg/' + i, 'r').read()

    result = movieReviewer.rate(f)
    if result < 0:
        correct += 1
    done += 1
    if (done / total * 100 >= progress + 5):
        progress += 5
        system("echo -n '\b\b\b=%2d%%'" % progress)
system("echo -n '\b\b\b\b]    \t[done]\n'")

print "Result: %.2f%% accurate!" % (correct * 100 / total)
