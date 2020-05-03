import sys
import time

def printVector(vector):
    outputFile = open('justToCheckResults.txt','w')
    for node in vector:
        outputFile.write(str(node)+'\n')

def orderVector(vector,numberOfRecords):
    vector.sort(key= lambda value : value[1])

    numberOfSlices = int(len(vector)/68)
    #print('number of slices',numberOfSlices)
    lastSliceLenth = numberOfRecords - numberOfSlices*68
    #print('last slice\'s length',lastSliceLenth)

    for i in range(1,numberOfSlices):
        if i == numberOfSlices:
            vector[i*68:numberOfRecords].sort(key= lambda value : value[3]) 
        else:
            subVector = vector[68*(i-1):68*i]
            subVector.sort(key= lambda value : value[3])
            vector[68*(i-1):68*i] = subVector
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

def isParentNode(value):
    if value == 0:
        return True
    elif value == 1:
        return False


fileName = sys.argv[1]
#outputFileName = sys.argv[2]
rectanglesDictionary = {}
unorderedList = {}
numberOfRecords = 0
vector = []

with open(fileName) as rectanglesFile:
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
            #print('everything is gonna be allright',len(vector))

outputFile = open('newRTree.txt','w')
print('tree height:',level)
rootNode = len(rTree) - 1
outputFile.write(str(rootNode)+'\n'+str(level)+'\n')

rootValue = rTree[rootNode]
treeNodesCounter = 0
nextLevelNodes = []
visitedNodes = []

while len(rootValue) != 0:
    for node in rootValue:
        
        if node[0] not in visitedNodes:
            visitedNodes.append(node[0])
            nodeId = node[0]
            vector = rTree[nodeId]
            numberOfChildren = len(vector)
            header = str(nodeId)+','+str(numberOfChildren)
            outputFile.write(header)
            nodeToString = ''
            for childNode in vector:
                nodeToString += ',({0},<{1}>,<{2}>,<{3}>,<{4}>)'.format(*childNode)
                nextLevelNodes.append(childNode)
            treeNodesCounter += 1
            outputFile.write(nodeToString + '\n')
            
            
            if treeNodesCounter == len(rootValue):
                rootValue = nextLevelNodes
                nextLevelNodes = []
                treeNodesCounter = 0
                #printVector(rootValue)
        else:
            rootValue = []
            break

queryVector = []
with open('query_rectangles.txt') as rectanglesFile:
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

startTime = time.time()

for queryRectangle in queryVector:

    rootValue = rTree[rootNode]
    rootValueCurrentPos = 0
    nodesThatIntersect = []
    #visitedNodes = []
    resultsVector = []
    results.write('\n QueryRectangle:'+str(queryRectangle)+'\n\n')
    while len(rootValue) != 0:
        for node in rootValue: 
            nodeId = node[0]
            if node[5] == 0:
                #visitedNodes.append(nodeId)
                if intersects(queryRectangle,node):
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
                if intersects(queryRectangle,node):
                    resultsVector.append(node)
                    #results.write(str(node)+'\n')
                rootValueCurrentPos += 1
                if len(rootValue) == rootValueCurrentPos:
                    resultsVector.sort(key= lambda value : value[0])
                    for value in resultsVector:
                        results.write(str(value)+'\n')
                    rootValue = []
    #print('number of nodes Visited:',len(visitedNodes))

endTime = time.time()
results.close()
print('execution Time of intersect Query:',endTime-startTime)

results = open('nonLinearInsideQuery.txt','w')

startTime = time.time()

for queryRectangle in queryVector:

    rootValue = rTree[rootNode]
    rootValueCurrentPos = 0
    nodesThatIntersect = []
    #visitedNodes = []
    resultsVector = []
    results.write('\n QueryRectangle:'+str(queryRectangle)+'\n\n')
    while len(rootValue) != 0:
        for node in rootValue: 
            nodeId = node[0]
            if node[5]==0:
                #visitedNodes.append(nodeId)
                if intersects(node,queryRectangle):
                    nodeValue = rTree[nodeId]
                    for value in nodeValue:
                        nodesThatIntersect.append(value)
                rootValueCurrentPos += 1
                if rootValueCurrentPos == len(rootValue):
                    rootValue = nodesThatIntersect
                    nodesThatIntersect = []
                    rootValueCurrentPos = 0
            else:
                #visitedNodes.append(nodeId)
                if inside(node,queryRectangle):
                    resultsVector.append(node)
                    #results.write(str(node)+'\n')
                rootValueCurrentPos += 1
                if len(rootValue) == rootValueCurrentPos:
                    resultsVector.sort(key= lambda value : value[0])
                    for value in resultsVector:
                        results.write(str(value)+'\n')
                    rootValue = []
    #print('number of nodes Visited:',len(visitedNodes))

endTime = time.time()
results.close()
print('execution Time of inside Query:',endTime-startTime)


results = open('nonLinearContainmentQuery.txt','w')

startTime = time.time()

for queryRectangle in queryVector:

    rootValue = rTree[rootNode]
    rootValueCurrentPos = 0
    nodesThatIntersect = []
    #visitedNodes = []
    resultsVector = []
    results.write('\n QueryRectangle:'+str(queryRectangle)+'\n\n')
    while len(rootValue) != 0:
        for node in rootValue: 
            nodeId = node[0]
            if node[5] == 0:
                #visitedNodes.append(nodeId)
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
                #visitedNodes.append(nodeId)
                if inside(queryRectangle,node) and nodeId in visitedNodes:
                    resultsVector.append(node)
                    #results.write(str(node)+'\n')
                rootValueCurrentPos += 1
                if len(rootValue) == rootValueCurrentPos:
                    resultsVector.sort(key= lambda value : value[0])
                    for value in resultsVector:
                        results.write(str(value)+'\n')
                    rootValue = []
    #print('number of nodes Visited:',len(visitedNodes))

endTime = time.time()

print('execution Time of Containment Query:',endTime-startTime)