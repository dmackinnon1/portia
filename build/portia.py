import random
#
# Functions for generating Portia Casket puzzles and solutions.
# run script to generate portia_data.json
#

#-------------------------
# a range of possible 'pointers' to caskets
def casketPointers(n):
    pointers = []
    for i in range(n):
        pointers.append(i+1)
        pointers.append(-1*(i+1))
    return pointers

# generates a random puzzle statement, might not be valid
def randomCasketSequence(n):
    cp = casketPointers(n)
    pointerSequence =[]
    for i in range(n):
        pointerSequence.append(random.choice(cp))
    return pointerSequence

# array of casket labels
def caskets(n):
    c = []
    for i in range(n):
        c.append(i+1)
    return c

# A truth sequence records how many of the statements
# are true if the portrait is in a given position.
# this initializes the sequence.
def initialTruthSequence(n):
    t = []
    for i in range(n):
        t.append(0)
    return t

# this computes the truth sequence for
# a given list of casket pointers
def truthForPointers(pointerSequence):
    n = len(pointerSequence)
    c = caskets(n)
    truthSequence = initialTruthSequence(n)
    for i in c:
        for j in pointerSequence:
            if  i == j :
                truthSequence[i-1] = truthSequence[i-1] +1
            if j < 0 :
                if i != -1*j:
                    truthSequence[i-1] = truthSequence[i-1] +1   
    return truthSequence

# checks to see of all truth counts
# are distinct
def allDistinct(truthSequence):
    reduced = set(truthSequence)
    return len(reduced) == len(truthSequence)

# checks to see which truth counts
# are distinct
def whichDistinct(truthSequence):
    distinct = []
    position = 0
    for i in truthSequence:       
        position += 1
        current = i
        count = 0
        for j in truthSequence:
            if i == j:
                count +=1
        if count == 1 :
            distinct.append(position)
    return distinct

def printCasketStatements(caskets):
    output = ""
    for i in caskets:
        if i > 0:
            output += "[the portrait is in "
            output += str(i)
            output += "]"
        if i < 0:
            output += "[the portrait is not in "
            output += str(-1*i)
            output += "]"
    print(output);

# a set of 3 tuples are returned
# the three tuples include 1 caskets, 2 #truths, 1 postion
def check(caskets):
    t = truthForPointers(caskets)
    d = whichDistinct(t)
    results = []
    if len(d) == 0:
        return results
    for i in d:
        p = []
        p.append(caskets)
        p.append(t[i-1])
        p.append(i)
        results.append(p)    
    return results

def printPuzzle(results):
    print("----- puzzle -----")
    caskets = results[0]
    truths = results[1]
    position = results[2]
    print("There are " + str(len(caskets)) + " caskets with these inscriptions:")
    printCasketStatements(caskets)
    print("There are exactly " + str(truths) + " true inscriptions.")
    print("   solution: The portrait is in  casket " + str(position))

def json(puzzleDef):
    result  = "{\"caskets\": "
    result += str(puzzleDef[0])
    result += ", \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2]) + "}"
    return result
    
# generates all sequences of length n using elements from
# the provided list
def allSequences(n, elements):
    if n == 0 :
        return [];
    if n == 1 :
        sequences = []
        for i in elements :
            temp = []
            temp.append(i)
            sequences.append(temp)
        return sequences
    return appendTo(elements, allSequences(n-1,elements))

def appendTo(elements, listOfLists):    
    newList = []
    for i in elements:
        for l in listOfLists:
            nl = list (l)
            nl.append(i)
            newList.append(nl)
    return newList

# will generate all puzzles on n caskets                           
def generateAllPuzzles(n):
    cp = casketPointers(n)
    allPossible = allSequences(n, cp)
    counter = 0
    result = "[\n"
    first = True
    for i in allPossible:
        results = check(i)
        counter += len(results)
        for j in results:
            if not first:
                result += ","
                result += "\n"
            first = False
            result += "\t"
            result += json(j)
    result += "\n]"
    print("generated " + str(counter) + " puzzles")
    return result;

#
# using the puzzle generator
#
print('Generating Portia I data.')
print(' --- creating file ../data/portia1.json')
f = open("../data/portia1.json","w")
f.write(generateAllPuzzles(3))
f.close()
print(' --- completed writing out Portia I data.')
