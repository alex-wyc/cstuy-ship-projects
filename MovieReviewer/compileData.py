bayesU = open("bayesU.txt", 'r').read().split('\n')
bayesA = open("bayesA.txt", 'r').read().split('\n')
bayesP = open("bayesP.txt", 'r').read().split('\n')
SVMA = open("SVMA.txt", 'r').read().split('\n')
SVMU = open("SVMU.txt", 'r').read().split('\n')

output = open("DATA.csv", 'w')

for i in range(0, len(bayesU)):
    output.write("%s,%s,%s,%s,%s\n" % (bayesU[i], bayesA[i], bayesP[i], SVMU[i], SVMA[i]))

output.close()
