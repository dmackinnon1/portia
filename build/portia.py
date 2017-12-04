import random
#
# Functions for generating Portia Casket puzzles and solutions.
# run script to generate json files for all puzzle types
#-------------------

# A range of possible 'pointers' to caskets - all possible +/- values on n integers
# used by generateAllPuzzlesPortia1, generateAllPuzzlesPortia2, generateAllPuzzlesPortia3
# portia 1, portia 2, portia 3
def casketPointers(n):
    return [i+1 for i in range(n)] + [-1*(i+1) for i in range(n)]

# generates array of casket lables
# used in portia 1, portia 2, portia 3
def caskets(n):
    return [i+1 for i in range(n)]

# A truth sequence records how many of the statements
# are true if the portrait is in a given position.
# this initializes the sequence.
# used by truthForPointers, portia 1
def initialTruthSequence(n):
    return [0 for i in range(n)]

# this computes the truth sequence for
# a given list of casket pointers
# the truth sequence for a pointerSequence:
# for each position in the truth sequence,
# it is the count of how many pointers
# are true if the portrait is in that position.
# used in checkForPortia1, portia 1
def truthForPointers(pointerSequence):
    n = len(pointerSequence)
    c = caskets(n)
    truthSequence = initialTruthSequence(n)
    for i in c:
        for j in pointerSequence:
            truthSequence[i-1] += truthAtPointer(i,j)
    return truthSequence

# used by truthForPointers
def truthAtPointer(p, pointer):
    if p == pointer :
        return 1
    if pointer < 0:
        if p != -1*pointer:
            return 1        
    return 0

# used by checkForPortia3, portia 3
def truthSequence(p, pointers):
    return [truthAtPointer(p, i) for i in pointers]
    

# in portia2, we want to know how many true statements
# are on each casket for a given position
# used by checkForPortia2, portia 2
def truthForPointers2(pointerSequence1, pointerSequence2):
    n = len(pointerSequence1)
    c = caskets(n)
    truthVector = []   
    for i in c:
        truthAti = []
        for j in range(n):
            truthCount = truthAtPointer(i, pointerSequence1[j])
            truthCount += truthAtPointer(i, pointerSequence2[j])
            truthAti.append(truthCount)
        truthVector.append(truthAti)
    return truthVector

# used by noPermutationInList, portia 2
def isPermutation(v1, v2):
    count = 0;
    for i in v1:
        if i in v2:
            count += 1
    return count == len(v1)        

# used by portia 2 to ensure that the truth distributions
# are unique. ie. we can't have a puzzle with truths (1, 0, 2) and (2, 1, 0)
# used in checkForPortia2, portia 2
def noPermutationInList(d, list):
    for c in list:
        if isPermutation(d,c):
            return False 
    return True

# Looks for distinct truth counts within truth sequence.
# used in portia 1 for evaluating/generating solvable puzzles.
# used by checkForPortia1, portia 1
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


# For a given set of statement pointers, generates all possible portia 1 puzzles
# A valid portia 1 puzzle is one with a unique truth count among all puzzles with the same
# statement pointers. At most 3 valid statements are available, but there could be none.
# used by generateAllPuzzlesPortia1, portia 1
def checkForPortia1(pointers):
    t = truthForPointers(pointers)
    d = whichDistinct(t)
    results = []
    if len(d) == 0:
        return results
    for i in d:
        p = []
        p.append(pointers)
        p.append(t[i-1])
        p.append(i)
        p.append(positionalTruth(t[i-1],t))
        results.append(p)    
    return results

# Checks a truth count against other possible truth counts
# Used in portia 1 to be able to make assertions like 'at least one is true'
# used by checkForPortia1, portia 1
def positionalTruth(c, t): 
    if c == min(t): return "min" 
    if c == max(t): return "max"
    return "mid"


# In portia 3, we need to ensure that the 
# location of the portrait is either directly mentioned
# or that the remaining cakets are ruled out.
# This method checks for a given location of the portrait (i) that one of those
# conditions hold.
# used by pointerList portia 3 
def hasPointer(i, pointers) :
    for j in pointers:
        if i == j : return True
        if i == -1*j : return True
    a = []
    for j in pointers:
        a.append(abs(j))
    if len(set(a)) >1 : return True
    return False; 

# generates list of locations where a given pointer list
# will generate a valid puzzle according to portia 3 requirements
# used by checkForPortia3 portia 3
def pointerList(pointers) :
    n = len(pointers)
    c = caskets(n)
    results = []
    for i in c:
        if hasPointer(i, pointers):
            results.append(i)
    return results

# Will generate valid portia 3 puzzle definitions based on a
# given pointer sequence.
# first it generates all valid sets of first statements
# then for each it generates a valid sets of 'bellini cellini' statmeents
# using a simple belini-cellini statement topology
# used by generateAllPuzzlesPortia3 portia 3    
def checkForPortia3(pointers):
    l = pointerList(pointers)
    results = []
    if len(l) == 0:
        return results
    for i in l:
        for j in negateOnePerSequence(belliniCellini1(len(pointers))):
            p = []
            p.append([pointers, j])
            p.append(truthSequence(i, pointers))
            p.append(i)
            results.append(p)    
    return results

# Generates solvavble portia2 puzzles from a given input of casket pointers
# will return an empty list if no puzzles are possible, or a list of 
# puzzle lists. Each solution generates a truth array - valid puzzles correspond to 
# unique truth distributions.
# used by generateAllPuzzlesPortia2 portia 2
def checkForPortia2(casketTuple):
    casketSet1 = casketTuple[0]
    casketSet2 = casketTuple[1]
    solutionList = []
    t = truthForPointers2(casketSet1, casketSet2)
    for i in range(len(t)) :
        remaining = list(t)
        remaining.remove(t[i])
        if noPermutationInList(t[i],remaining):
            solutionList.append(i)
    results = []    
    for i in solutionList:
        p = []
        p.append(casketTuple)
        p.append(t[i])
        p.append(i+1)
        results.append(p)
    return results

# formats portia 1 puzzles for output
# used by generateAllPuzzlesPortia3 portia 1
def json(puzzleDef, counter):
    result  = "{\"caskets\": "
    result += str(puzzleDef[0])
    result += ", \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2])
    result += ", \"position\": \"" + puzzleDef[3] +"\"" 
    result += ", \"id\": " + "\"portia1-" + str(counter)+ "\"}"        
    return result

# formats portia 2 puzzles for output
# used by generateAllPuzzlesPortia2 portia 2
def json2(puzzleDef, counter):
    result  = "{\"caskets\": ["
    result += str(puzzleDef[0][0])
    result += ", "
    result += str(puzzleDef[0][1])
    result += "], \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2]) 
    result += ", \"id\": " + "\"portia2-" + str(counter)+ "\"}"
    return result

# formats portia 3 puzzles for output
# used by generateAllPuzzlesPortia3 portia 3
def json3(puzzleDef, counter):
    result  = "{\"caskets\": "
    result += str(puzzleDef[0])
    result += ", \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2])
    result += ", \"id\": " + "\"portia3-" + str(counter)+ "\"}"        
    return result

# recursively generates all sequences of length n using elements from
# the provided list. Used in all portias to generate the list of 'casket pointers'
# which correspond to the core statements.
# used by: allNoMatchSequencePairs, generateAllPuzzlesPortia3, generateAllPuzzlesPortia1
#   portia 1, portia 2, portia 3
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

# helper function for allSequences
# used by: allSequences, portia 1, portia 2, portia 3
def appendTo(elements, listOfLists):    
    newList = []
    for i in elements:
        for l in listOfLists:
            nl = list (l)
            nl.append(i)
            newList.append(nl)
    return newList

# generates all pairs of sequences of n elements that
# do not have the same element in the same position.
# Portia 2 uses this to ensure that there are not duplicate statements
# on the same casket.
# used by: generateAllPuzzlesPortia2 porita 2
def allNoMatchSequencePairs(n, elements): 
    pairs = []
    sequences = allSequences(n, elements)
    decreasing = list(sequences)
    for s in sequences :
        decreasing.remove(s)
        for t in decreasing :            
            if noMatch(s,t):
                pairs.append((s,t))
    return pairs

# used by: allNoMatchSequencePairs, portia 2
def noMatch(l1, l2):
    result = True
    for i in range(len(l1)) :
        if l1[i] == l2[i] :
            result = False 
    return result

# returns a 'derranged cycle' on n elements
# a permutation of (1, 2, ... n) such that no element is in its 
# original position, and the permutation is a cycle.
# Used to create a simple 'bellini/cellini' network of statements that will
# either be 'sympathy/antipathy' statements or 'accusation/affirmation' statements
# used by: portia 3
def belliniCellini1(n): 
    c = caskets(n)
    result = []
    cp = c[1:len(c)]
    for j in cp:
        result.append([j])
    for i in cp:
        remainders = c[:]
        newResult = []
        for k in result:
            remainderk = removeAll(remainders,k)
            remainderk = removeIfPresent(remainderk, i)
            if len(remainderk) == 0:
                newResult.append(k)
            for r in remainderk: 
                p = k[:]
                p.append(r)
                newResult.append(p)
        result = newResult[:]
    final = []
    for i in result:
        if len(i) == n:
            final.append(i)
    return final


# For each input, return a set of sequences the same as the input, except that
# in each returned, -1* the corresponding element in the input.
# Used to select one statement pointer as a 'sympathy/antipathy' statement
# While the others remain 'accusation/affiermation' statements
# used by: portia 3
def negateOnePerSequence(sequences):
    result = []
    for s in sequences:
        for i in range(len(s)):
            r = s[:]
            r[i] = -1*r[i]
            result.append(r)
    return result;

# utility function - remove all of one collection from another
# used by: belliniCellini1 in portia3
def removeAll(p,d):
    q = p[:]
    for i in d:
        removeIfPresent(q,i)
    return q    

# used by: removeAll in portia 3
def removeIfPresent(p,i):
    if i in p: p.remove(i)
    return p

# will generate all puzzles on n caskets for Portia I                          
def generateAllPuzzlesPortia1(n):
    cp = casketPointers(n)
    allPossible = allSequences(n, cp)
    counter = 0
    result = "[\n"
    first = True
    for i in allPossible:
        results = checkForPortia1(i)
        for j in results:
            if not first:
                result += ","
                result += "\n"
            first = False
            result += "\t"
            counter += 1
            result += json(j, counter)
    result += "\n]"
    print("generated " + str(counter) + " puzzles")
    return result;


# will generate all puzzles on n caskets for Portia II                          
def generateAllPuzzlesPortia2(n):
    cp = casketPointers(n)
    allPossible = allNoMatchSequencePairs(n, cp)
    counter = 0
    result = "[\n"
    first = True
    for i in allPossible:
        results = checkForPortia2(i)
        for j in results:
            if not first:
                result += ","
                result += "\n"
            first = False
            result += "\t"
            counter += 1
            result += json2(j, counter)
    result += "\n]"
    print("generated " + str(counter) + " puzzles")
    return result;


# will generate all puzzles on n caskets for Portia III                         
def generateAllPuzzlesPortia3(n):
    cp = casketPointers(n)
    allPossible = allSequences(n, cp)
    counter = 0
    result = "[\n"
    first = True
    for i in allPossible:
        results = checkForPortia3(i)  
        for j in results:
            if not first:
                result += ","
                result += "\n"
            first = False
            result += "\t"
            counter += 1
            result += json3(j, counter)
    result += "\n]"
    print("generated " + str(counter) + " puzzles")
    return result;

#
# Puzzle Generator
#
print('-------------------------------------------')
print('Generating Portia I data.')
print(' --- creating file ../data/portia1.json')
f = open("../data/portia1.json","w")
f.write(generateAllPuzzlesPortia1(3))
f.close()
print(' --- completed writing out Portia I data.')
print('-------------------------------------------')
print("Generating Portia II data.")
print(' --- creating file ../data/portia2.json')
f = open("../data/portia2.json","w")
f.write(generateAllPuzzlesPortia2(3))
f.close()
print(' --- completed writing out Portia II data.')
print('-------------------------------------------')
print("Generating Portia III data.")
print(' --- creating file ../data/portia3.json')
f = open("../data/portia3.json","w")
f.write(generateAllPuzzlesPortia3(3))
f.close()
print(' --- completed writing out Portia III data.')
print('-------------------------------------------')
