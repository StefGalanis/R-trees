import sys
import time
import math

def orderVector(vector,numberOfRecords):
    vector.sort(key= lambda value : value[1])
    blockSize = int(1024/36)
    numberOfLeaves = int(numberOfRecords/blockSize) + 1
    sliceSize = int(math.sqrt(numberOfLeaves)) + 1

    numberOfSlices = int(len(vector)/sliceSize)
    #print('number of slices',numberOfSlices)
    lastSliceLenth = numberOfRecords - numberOfSlices*sliceSize
    #print('last slice\'s length',lastSliceLenth)

    for i in range(1,numberOfSlices):
        if i == numberOfSlices:
            vector[i*sliceSize:numberOfRecords].sort(key= lambda value : value[3]) 
        else:
            subVector = vector[sliceSize*(i-1):sliceSize*i]
            subVector.sort(key= lambda value : value[3])
            vector[sliceSize*(i-1):sliceSize*i] = subVector
    return vector

def intersects(bValues,aValues) :
    
    if (bValues[1] < aValues[2] and bValues[2] > aValues[1] and bValues[4] > aValues[3] and bValues[3] < aValues[4]) :
        #print(bValues[0],' intersects with ',aValues[0])
        return True
    else:
        #print('some other relationship defines those two MBRs')
        return False

def inside(bValues,aValues) :

    if((bValues[4]<aValues[4] and bValues[1]>aValues[1]) and (bValues[2]<aValues[2] and bValues[3]>aValues[3])) :
        #print(bValues[0],'is inside of',aValues[0])
        return True
    else:
        #print('some other relationship defines those two MBRs')
        return False

rTreeFile = open('newRTree.txt')
vector = []
numberOfRecords = 0

with open('data_rectangles.txt') as rectanglesFile:
    for line in rectanglesFile:

        values = line.split('\t')

        objectId = int(values[0])
        xlow = float(values[1])
        xhigh = float(values[2])
        ylow = float(values[3])
        yhigh = float(values[4])
        vector.append((objectId,xlow,xhigh,ylow,yhigh,1))
        numberOfRecords += 1

vector = orderVector(vector,numberOfRecords)


rTree = []
nodeValue = []
xlow = []
xhigh = []
ylow = []
yhigh = []
parentVector = []
iterations = 0
numberOfRecordsRead = 0
parentNodeId = 0
sign = 0
level = 0
flag = 0

while len(vector) != 1 or sign == 0:

    if sign == 0:
        sign = 1

    for record in vector:
        
        xlow.append(record[1])
        xhigh.append(record[2])
        ylow.append(record[3])
        yhigh.append(record[4])
        nodeValue.append(record)

        numberOfRecordsRead += 1

        if numberOfRecordsRead == 28 or iterations == len(vector)-1:
            xlow.sort()
            xhigh.sort(reverse=True)
            ylow.sort()
            yhigh.sort(reverse=True)
            parentVector.append((parentNodeId,xlow[0],xhigh[0],ylow[0],yhigh[0],0))
            rTree.append(nodeValue)
            xlow = []
            xhigh = []
            ylow = []
            yhigh = []
            nodeValue = []
            parentNodeId += 1
            numberOfRecordsRead = 0

        iterations += 1

        if iterations == len(vector):
            numberOfRecords = len(parentVector)
            #print('numberOfrecords',numberOfRecords)
            vector = orderVector(parentVector,numberOfRecords)
            parentVector=[]
            numberOfRecordsRead = 0
            iterations = 0
            level += 1



queryFile = sys.argv[1]
queryVector = []
with open(queryFile) as rectanglesFile:
    for line in rectanglesFile:

        values = line.split('\t')

        objectId = int(values[0])
        xlow = float(values[1])
        xhigh = float(values[2])
        ylow = float(values[3])
        yhigh = float(values[4])
        queryVector.append((objectId,xlow,xhigh,ylow,yhigh))
        numberOfRecords += 1

results = open('nonLinearIntersectQuery.txt','w')

rootNode = len(rTree) - 1
startTime = time.time()
totalNumberOfVisitedNodes = 0
totalNumberOfResults = 0

for queryRectangle in queryVector:

    rootValue = rTree[rootNode]
    rootValueCurrentPos = 0
    nodesThatIntersect = []
    visitedNodes = []
    resultsVector = []
    results.write('\n QueryRectangle:'+str(queryRectangle)+'\n\n')
    while len(rootValue) != 0:
        for node in rootValue: 
            nodeId = node[0]
            if node[5] == 0:
                visitedNodes.append(nodeId)
                if inside(queryRectangle,node):
                    nodeValue = rTree[nodeId]
                    for value in nodeValue:
                        nodesThatIntersect.append(value)
                rootValueCurrentPos += 1
                if rootValueCurrentPos == len(rootValue):
                    rootValue = nodesThatIntersect
                    nodesThatIntersect = []
                    rootValueCurrentPos = 0
            else:
                visitedNodes.append(nodeId)
                if inside(queryRectangle,node) and nodeId in visitedNodes:
                    resultsVector.append(node)
                    #results.write(str(node)+'\n')
                rootValueCurrentPos += 1
                if len(rootValue) == rootValueCurrentPos:
                    resultsVector.sort(key= lambda value : value[0])
                    totalNumberOfResults += len(resultsVector)
                    for value in resultsVector:
                        results.write(str(value)+'\n')
                    rootValue = []
    totalNumberOfVisitedNodes += len(visitedNodes)
    print('Query Rectangle:',queryRectangle)
    print('number of nodes Visited:',len(visitedNodes))
    print('number of Results:',len(resultsVector))

endTime = time.time()
results.close()

print('execution Time of Containment Query:',endTime-startTime)
print('total number of Visited nodes for this query:',totalNumberOfVisitedNodes)
print('total number of results for this query:',totalNumberOfResults)