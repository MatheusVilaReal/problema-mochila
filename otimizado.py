from treelib.tree import Tree
from math import floor
from time import time

import backpack
import sys

currentNode = totalWeight = totalInterest = solutionInterest = counter = 0

Arvore = Tree(identifier = 0)
Arvore.create_node("Raiz", 0)

txt = backpack.getArgs(sys.argv, "i")

if(txt != 0):
    n = backpack.getN_manual(txt)
    items = backpack.getItems_manual(n, txt)
else:
    n = backpack.getN(sys.argv)
    items = backpack.getItems_rand(n)

filename = backpack.getArgs(sys.argv, "o")

if(filename):
    backpack.genTxt(items, filename)

solution = [0] * n

capacity = backpack.getCapacity(items)

for i in range(n):
    print("Itens[" + str(i+1) + "] =\tInteresse: ", items[i].interest, "\t| Peso: ", items[i].weight, "\t| Custo-benefício: ", items[i].interest/items[i].weight)

oldOrder = {items[i] : i for i in range(n)}

items.sort(reverse = True, key = backpack.Item.getBenefit)

print("\n$===================================$~SORT~$===================================$\n")

for i in range(n):
    print("Itens[" + str(i+1) + "] =\tInteresse: ", items[i].interest, "\t| Peso: ", items[i].weight, "\t| Custo-benefício: ", items[i].interest/items[i].weight)

print("\nCapacidade da mochila: ", capacity)

availableSpace = capacity

startTime = time()

while(True):
    for i in range(counter, n):

        Arvore.create_node("X" + str(Arvore.level(currentNode) + 1) + " = " + str(floor(availableSpace / items[i].weight)), Arvore.size(), currentNode, floor(availableSpace / items[i].weight))

        totalInterest += floor(availableSpace / items[i].weight) * items[i].interest
        totalWeight += floor(availableSpace / items[i].weight) * items[i].weight

        availableSpace %= items[i].weight

        currentNode = Arvore.size() - 1

    if(totalInterest > solutionInterest):

        solutionInterest = totalInterest

        solutionWeight = totalWeight

        nodeBuffer = currentNode

        while(nodeBuffer > 0):

            solution[Arvore.level(nodeBuffer) - 1] = Arvore[nodeBuffer].data
            nodeBuffer = Arvore[nodeBuffer].predecessor(0)

    counter = 1
    currentNode = Arvore[currentNode].predecessor(0)

    while(currentNode != 0 and not backpack.isBranchable(Arvore, items, currentNode, capacity, solutionInterest)):

        counter += 1
        currentNode = Arvore[currentNode].predecessor(0)
    
    if(currentNode == 0): break

    Arvore.create_node("X" + str(Arvore.level(Arvore[currentNode].predecessor(0)) + 1) + " = " + str(Arvore[currentNode].data - 1), Arvore.size(), Arvore[currentNode].predecessor(0), Arvore[currentNode].data - 1)

    currentNode = Arvore.size() - 1

    totalInterest = backpack.getInterestTilN(Arvore, items, currentNode)
    totalWeight = backpack.getWeightTilN(Arvore, items, currentNode)
    availableSpace = capacity - totalWeight

    counter = n - counter

elapsedTime = time() - startTime

print("Melhor solução: {solutionInterest} = {solution}\nPeso: {weight}/{capacity}".format(solutionInterest = solutionInterest, solution = solution, weight = solutionWeight, capacity = capacity))
print("Tempo decorrido: {time}s".format(time = elapsedTime))

filename = backpack.getArgs(sys.argv, "r")

if(filename):
    backpack.genCsv(filename, txt, n, elapsedTime, solutionInterest, solutionWeight, sys.argv, capacity, solution, items, oldOrder)

# if(n <= 10):
#     Arvore.show()