import sys
import math

fileName = sys.argv[1]
rectanglesDictionary = {}
unorderedList = {}
numberOfRecords = 0

with open(fileName) as rectanglesFile:
    for line in rectanglesFile:
        values = line.split('\t')
        objectId = values[0]
        xlow = values[1]
        coordinates = ''
        for i in range(1,len(values)):
            if i < len(values)-1:
                coordinates += values[i] + '\t'
            else :
                coordinates += values[i].replace('\n','') + '\n'
        rectanglesDictionary[objectId] = coordinates
        unorderedList[objectId] = float(xlow)
        numberOfRecords += 1

orderedList = {k: v for k, v in sorted(unorderedList.items(), key=lambda item: item[1])}

outputFile = open('xlowOrderedFile.txt','w')

for key in orderedList:
    coordinates = rectanglesDictionary[key]
    outputFile.write(key + '\t' + coordinates)

outputFile.close()
leafNodeSize = int(1024/36)
numberOfLeafNodes = round(numberOfRecords/leafNodeSize)
print(numberOfLeafNodes)
partitionSize = round(math.sqrt(numberOfLeafNodes))
print('Partition Size:' + str(partitionSize) + '\t Number of Records:' + str(numberOfRecords))
counter = 0
tempDictionary = {}
bulkDataFile = open('bulkDataFile.txt','w')

with open('xlowOrderedFile.txt') as inputFile: 
    for line in inputFile:
        if counter == partitionSize:
            orderedList = {k: v for k, v in sorted(tempDictionary.items(), key=lambda item: item[1])}
            counter = 0
            tempDictionary = {}
            for key in orderedList:
                coordinates = rectanglesDictionary[key]
                bulkDataFile.write(key + '\t' + coordinates)   
        values = line.split('\t')
        objectId = values[0]
        ylow = values[3]
        tempDictionary[objectId] = float(ylow)
        counter += 1

orderedList = {k: v for k, v in sorted(tempDictionary.items(), key=lambda item: item[1])}
for key in orderedList:
    coordinates = rectanglesDictionary[key]
    bulkDataFile.write(key + '\t' + coordinates)

bulkDataFile.close()

nodeId = 0
counter = 0
parentNodeCounter = 0
rTree = {}
tempList = []
leafNodeValue = ''

with open('bulkDataFile.txt') as inputFile:
    for line in inputFile :

        values = line.split('\t')
        objectId = values[0]

        if counter == 0 :
            xlow = values[1]
            ylow = values[3]
        leafNodeValue += line
        counter += 1
        #print(nodeId)


        if counter == leafNodeSize:
            counter = 0
            xhigh = values [2]
            yhigh = values[4]
            rTree[nodeId] = leafNodeValue

            if parentNodeCounter == 0 :
                parentNodeId = nodeId + 1
                #print(parentNodeId)
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
                rTree[parentNodeId] = parentsValue

                parentNodeCounter += 1
                nodeId += 2

            elif parentNodeCounter < leafNodeSize :
                #print('i got in and parent number is',parentNodeId)
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
                previousValue = rTree[parentNodeId]
                newValue = previousValue + parentsValue
                rTree[parentNodeId] = newValue 

                parentNodeCounter += 1
                nodeId += 1

            else :

                parentNodeCounter = 0
                nodeId += 1

            leafNodeValue = ''

print(rTree[parentNodeId])
print(parentNodeId)