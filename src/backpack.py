from random import randint, seed
from os.path import exists

defaultN = 5

class Item():

    def __init__(self, interest, weight):
        
        self.interest = interest
        self.weight = weight

    def __hash__(self):
        return hash((self.interest, self.weight))

    def __eq__(self, other):
        return (self.interest, self.weight) == (other.interest, other.weight)

    def getBenefit(self):
            return self.interest/self.weight

def getItems_rand(n):

    items = []

    seed()

    for _ in range(n):
        items.append( Item(randint(1, n * 10), randint(1, n * 10)) )

    return items

def getItems_manual(n, filename):

    items = []

    file = open(filename)
    line = file.readline()

    for _ in range(n):
        
        line = file.readline()
        line = line.split(", ")

        items.append( Item(int(line[1]), int(line[0])) )

    file.close()

    return items

def getN(argv):

    n = int(getArgs(argv, "n"))

    if(n < 2):
        return defaultN

    return n

def getN_manual(filename):

    file = open(filename)

    n = file.readline().split(", ")

    file.close()

    return int(n[1])

def getWeightTilN(Tree, items, n):
    
    currentNode = n
    sum = 0

    while(currentNode > 0):

        sum += items[Tree.level(currentNode) - 1].weight * Tree[currentNode].data
        currentNode = Tree[currentNode].predecessor(Tree._identifier)

    return sum

def getInterestTilN(Tree, items, n):
    
    currentNode = n
    sum = 0

    while(currentNode > 0):

        sum += items[Tree.level(currentNode) - 1].interest * Tree[currentNode].data
        currentNode = Tree[currentNode].predecessor(Tree._identifier)

    return sum

def getCapacity(items):

    capacity = 0

    for i in range(len(items)):
        capacity += items[i].weight

    return capacity

def getLimit(Tree, items, currentNode, capacity):

    prevNode = Tree[currentNode].predecessor(Tree._identifier)

    index = Tree.level(currentNode) - 1
    
    newNodeInterest = items[index].interest * (Tree[currentNode].data - 1)
    newNodeWeight = items[index].weight * (Tree[currentNode].data - 1)

    S = getInterestTilN(Tree, items, prevNode) + newNodeInterest + items[index + 1].getBenefit() * (capacity - (getWeightTilN(Tree, items, prevNode) + newNodeWeight))

    return S

def isBranchable(Tree, items, currentNode, capacity, bestSolution):

    if(Tree[currentNode].data <= 0):
        return False
    
    elif(getLimit(Tree, items, currentNode, capacity) < bestSolution):
        return False

    return True

def genTxt(items, filename):

    if(not filename.endswith(".txt")):
        filename += ".txt"

    file = open(filename, "w")

    length = len(items)

    file.write("Tamanho, " + str(length) + "\n")

    for i in range(length):
        file.write(str(items[i].weight) + ", " + str(items[i].interest) + "\n")
    
    file.close()

def genCsv(filename, txt, n, time, totalInterest, totalWeight, argv, capacity, solution, items, oldOrder):

    if(not filename.endswith(".csv")):
        filename += ".csv"

    if(not exists(filename)):

        file = open(filename, "a+")
        file.write("Entrada,N° variáveis,Versão,Tempo (s),Peso,Interesse,Solução\n")
    else:
        file = open(filename, "a+")
    
    pversion = argv[0].split(".")

    if(txt == 0):
        file.write("N/A,")
    else:
        file.write("{txt},".format(txt = txt))

    file.write("{n},{pversion},{time},{totalWeight} / {capacity},{maxInterest},".format(n = n, time = time, maxInterest = totalInterest, totalWeight = totalWeight, pversion = pversion[0], capacity = capacity))

    for i in range(len(solution)):
        if(solution[i] > 0):
            file.write("[{i}] = {element} :: ".format(i = oldOrder[items[i]] + 1, element = solution[i]))

    file.write("\n")

    file.close()

def genCsvNoSort(filename, txt, n, time, totalInterest, totalWeight, argv, capacity, solution):

    if(not filename.endswith(".csv")):
        filename += ".csv"

    if(not exists(filename)):

        file = open(filename, "a+")
        file.write("Entrada,N° variáveis,Versão,Tempo (s),Peso,Interesse,Solução\n")
    else:
        file = open(filename, "a+")
    
    pversion = argv[0].split(".")

    if(txt == 0):
        file.write("N/A,")
    else:
        file.write("{txt},".format(txt = txt))

    file.write("{n},{pversion},{time},{totalWeight} / {capacity},{maxInterest},".format(n = n, time = time, maxInterest = totalInterest, totalWeight = totalWeight, pversion = pversion[0], capacity = capacity))

    for i in range(len(solution)):
        if(solution[i] > 0):
            file.write("[{i}] = {element} :: ".format(i = i + 1, element = solution[i]))

    file.write("\n")

    file.close()

def getArgs(argv, arg):

    argc = len(argv)

    for i in range(argc):
        if(argv[i].startswith("-")):
            if(argv[i].endswith(arg)):
                if(i + 1 < argc):
                    return argv[i + 1]
                
                else: 1

    return 0