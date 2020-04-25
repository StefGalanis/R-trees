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

xlowList = []
xhighList = []
ylowList = []
yhighList = []

nodeId = 0
counter = 0
parentNodeCounter = 0

parentNodeList = []
rTree = {}

leafNodeValue = ''
height = 1


with open('bulkDataFile.txt') as inputFile:

    for line in inputFile :

        values = line.split('\t')

        objectId = values[0]
        
        xlowList.append(values[1])
        ylowList.append(values[3])
        xhighList.append(values[2])
        yhighList.append(values[4])
        
        leafNodeValue += line

        counter += 1


        if counter == leafNodeSize:

            counter = 0

            xlowList.sort()
            xhighList.sort()
            ylowList.sort()
            yhighList.sort()

            xlow = xlowList[0]
            ylow = ylowList[0]
            xhigh = xhighList[-1]
            yhigh = yhighList[-1]

            if (nodeId == 0):
                print(xlow)

            xlowList = []
            xhighList = []
            ylowList = []
            yhighList = []

            rTree[nodeId] = leafNodeValue[:-1]

            if parentNodeCounter == 0 :
                parentNodeId = nodeId + 1
                parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)

                rTree[parentNodeId] = parentsValue
                parentNodeList.append(parentNodeId)

                parentNodeCounter += 1
                nodeId += 2

            elif parentNodeCounter < leafNodeSize - 1 :

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


if counter != 0 :

    xlow = xlowList[0]
    ylow = ylowList[0]
    xhigh = xhighList[-1]
    yhigh = yhighList[-1]

    rTree[nodeId] = leafNodeValue[:-1]

    if parentNodeCounter == 0 :

        parentNodeId = nodeId + 1
        parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh)

        rTree[parentNodeId] = parentsValue
        parentNodeList.append(parentNodeId)

        parentNodeCounter += 1
        nodeId += 2

    elif parentNodeCounter < leafNodeSize - 1 :

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

height += 1

print('number of blocks generated: ',nodeId)
print(parentNodeList)

upperLayerParents = []
counter = 0
nodeId -= 1

print(rTree[nodeId])
print('nodeid before loop:',nodeId)

parentNodeId = nodeId
parentNodeCounter = 0
parentNodeListLength = len(parentNodeList)

xlowList = []
xhighList = []
ylowList = []
yhighList = []

parentNodeXlow = []
parentNodeXhigh = []
parentNodeYlow = []
parentNodeYhigh = []

height += 1
testList = []

leafNodeValue = ''

for node in parentNodeList:

    lines = rTree[node].split('\n')
    lines = lines[:-1]
    #leafNodeValue += rTree[node]

    testList.append(node)

    for line in lines :
        values = line.split('\t')
        
        xhighList.append(float(values[2]))
        yhighList.append(float(values[4]))
        xlowList.append(float(values[1]))
        ylowList.append(float(values[3]))


        
    xhighList.sort()
    yhighList.sort()
    xlowList.sort()
    ylowList.sort()

    xlow = xlowList[0]
    ylow = ylowList[0]
    xhigh = xhighList[-1]
    yhigh = yhighList[-1]

    parentNodeXlow.append(xlow)
    parentNodeXhigh.append(xhigh)
    parentNodeYlow.append(ylow)
    parentNodeYhigh.append(yhigh)

    xlowList = []
    xhighList = []
    ylowList = []
    yhighList = []

    leafNodeValue += str(node) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh) + '\n'

    counter+=1
    parentNodeListLength -= 1
    
    if counter == leafNodeSize or parentNodeListLength == 0:
        
        #print(leafNodeValue)
        #sys.exit(1)
        rTree[nodeId] = leafNodeValue[:-1]

        leafNodeValue = ''
        counter = 0
        testList = []
        
        
        parentNodeXlow.sort()
        parentNodeXhigh.sort()
        parentNodeYlow.sort()
        parentNodeYhigh.sort()

        xlow = parentNodeXlow[0]
        ylow = parentNodeYlow[0]
        xhigh = parentNodeXhigh[-1]
        yhigh = parentNodeYhigh[-1]

        parentNodeXlow = []
        parentNodeXhigh = []
        parentNodeYlow = []
        parentNodeYhigh = []
        

        if parentNodeCounter == 0 :
            
            parentNodeId = nodeId + 1
            parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh) + '\n'

            rTree[parentNodeId] = parentsValue

            upperLayerParents.append(parentNodeId)

            parentNodeCounter += 1
            nodeId += 2

        elif parentNodeCounter < leafNodeSize - 1 :
            
            parentsValue = str(nodeId) + '\t' + str(xlow) + '\t' + str(xhigh) + '\t' + str(ylow) + '\t' + str(yhigh) +'\n'
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

height += 1
print(rTree[4678])
print(parentNodeList)
print(upperLayerParents)
print(parentNodeId)
#print(nodeId)
print(height)
print('This is the number of nodes that tree has:',len(rTree))

outputFile = open('R-tree.txt','w')

outputFile.write(str(parentNodeId)+'\n'+str(height)+'\n')

nodes = rTree[parentNodeId].split('\n')
print(nodes)
#print(rTree[4677])
nodes = nodes[:-1]

nodesToRemove = []
nextLevelNodes = []
treeNodesCounter = len(rTree)

while(len(nodes) != 0) :

    for node in nodes :
        
        values = node.split('\t')
        nodeId = int(values[0])
        
        treeNodesCounter -= 1

        if nodeId < len(rTree) and treeNodesCounter != 0:
            lines = rTree[nodeId].split('\n')
            if(lines[-1] == ''):
                lines = lines[:-1]
            numberOfRecords = len(lines)
            header = str(nodeId) + ',' + str(numberOfRecords)
            outputFile.write(header)
            nodeToString = ''
            for line in lines :
                nextLevelNodes.append(line)
                values = line.split('\t')
                nodeToString += ',({0},<{1}>,<{2}>,<{3}>,<{4}>)'.format(*values)
        else:
            nextLevelNodes = []
            #print(nodeId)
            nodeToString = ''
            break
        nodeToString += '\n'
        outputFile.write(nodeToString)
    nodes = nextLevelNodes
    nextLevelNodes = []
      




