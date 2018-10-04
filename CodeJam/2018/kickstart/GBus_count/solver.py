## This is a problem solver written by Le Zhang
## For CodeJam kickstart problem GBus count
## It took 40 mins for code writing and going through both small&large test cases
## RUN:
##    python solver.py inputFile outputFile

import sys


def getContent(path):
    ret = []
    content_file = open(path, 'r')

    with open(path, 'r') as fp:
       line = fp.readline()
       while line:
           ret.append(line)
           line = fp.readline()
    return ret


def parseQuestion(content):
    numBuses = int(content[0])
    busList = map(int, content[1].split())
    numCities = int(content[2])
    cityList = []
    for n in xrange(numCities):
        cityList.append(int(content[3+n]))

    return numBuses, busList, cityList


def countSrvBus(busList, city):
    bl = list(busList)
    cnt = 0
    flag = 1
    while bl:
        num = bl.pop()
        if len(bl)%2 == 1 and city <= num:
            flag = -1
        elif len(bl)%2 == 0 and flag == -1 and city >= num:
            cnt += 1
            flag = 1
        else:
            flag = 0
            continue
    return cnt


path = str(sys.argv[1])
content = getContent(path)

numCase = int(content[0])

content = content[1:]

f = open(sys.argv[2], "w")

for num in xrange(numCase):
    numBuses, busList, cityList = parseQuestion(content)

    content = content[4+len(cityList):]
    sol = []
    for c in cityList:
        sol.append(countSrvBus(busList, c))

    pstr = 'Case #'+str(num+1)+':'
    for s in sol:
        pstr += ' '
        pstr += str(s)
    print pstr
    f.write(pstr+'\n')
