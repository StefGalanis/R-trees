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
print('Block Size is: ',leafNodeSize)
numberOfLeafNodes = round(numberOfRecords/leafNodeSize)
print('the number of leaf nodes are:',numberOfLeafNodes)
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
parentNodeList = []
rTree = {}
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
                parentNodeList.append(parentNodeId)
                parentNodeCounter += 1
                nodeId += 2

            elif parentNodeCounter < leafNodeSize - 1 :
                #print('i got in and parent number is',parentNodeId)
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
                previousValue = rTree[parentNodeId]
                newValue = previousValue + parentsValue
                rTree[parentNodeId] = newValue 

                parentNodeCounter += 1
                nodeId += 1

            else :
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
                previousValue = rTree[parentNodeId]
                newValue = previousValue + parentsValue
                rTree[parentNodeId] = newValue 
                nodeId += 1
                parentNodeCounter = 0

            leafNodeValue = ''

#print(leafNodeValue)
if counter != 0 :
    xhigh = values [2]
    yhigh = values[4]
    rTree[nodeId] = leafNodeValue
    if parentNodeCounter == 0 :
        parentNodeId = nodeId + 1
                #print(parentNodeId)
        parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
        rTree[parentNodeId] = parentsValue
        parentNodeList.append(parentNodeId)
        parentNodeCounter += 1
        nodeId += 2

    elif parentNodeCounter < leafNodeSize - 1 :
                #print('i got in and parent number is',parentNodeId)
        parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
        previousValue = rTree[parentNodeId]
        newValue = previousValue + parentsValue
        rTree[parentNodeId] = newValue 

        parentNodeCounter += 1
        nodeId += 1

    else :
        parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
        previousValue = rTree[parentNodeId]
        newValue = previousValue + parentsValue
        rTree[parentNodeId] = newValue 
        nodeId += 1
        parentNodeCounter = 0


print('number of blocks generated: ',nodeId)
print(parentNodeList)
upperLayerParents = []
counter = 0
parentNodeId = nodeId
parentNodeCounter = 0
while len(parentNodeList) > leafNodeSize :
    parentListLength = len(parentNodeList)
    xlowList = []
    xhighList = []
    ylowList = []
    yhighList = []
    for node in parentNodeList:
        lines = rTree[node].split('\n')
        lines = lines[:-1]
        parentNodeList.remove(node)
        linecounter = 0
        if counter == 0 :

            for line in lines :
                values = line.split('\t')
                if linecounter == 0 :
                    xlow = values[1]
                    ylow = values[3]
                linecounter += 1
        counter += 1
        #print(counter,leafNodeSize)
        if counter == leafNodeSize or counter == parentListLength :
            
            for line in lines :
                values = line.split('\t')
                #print('i am in')
                if linecounter == len(lines)-1:
                    xhigh = values[2]
                    yhigh = values[4]
                linecounter += 1
        
    
        if counter == leafNodeSize or counter == parentListLength:
            counter = 0
            
            if parentNodeCounter == 0 :
                
                parentNodeId = nodeId + 1
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
                rTree[parentNodeId] = parentsValue
                upperLayerParents.append(parentNodeId)
                parentNodeCounter += 1
                nodeId += 2

            elif parentNodeCounter < leafNodeSize - 1 :
                #print('i got in and parent number is',parentNodeId)
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
                previousValue = rTree[parentNodeId]
                newValue = previousValue + parentsValue
                rTree[parentNodeId] = newValue 

                parentNodeCounter += 1
                nodeId += 1

            else :
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)
                previousValue = rTree[parentNodeId]
                newValue = previousValue + parentsValue
                rTree[parentNodeId] = newValue 
                nodeId += 1
                parentNodeCounter = 0

print(rTree[1],'\n',rTree[784])
#print(parentNodeList)
#print(rTree[parentNodeId])
#for node in parentNodeList:
#    print(rTree[node])
#print(parentNodeId)