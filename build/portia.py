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
# the truth sequence for a pointerSequence:
# for each position in the truth sequence,
# it is the count of how many pointers
# are true if the portrait is in that position.
def truthForPointers(pointerSequence):
    n = len(pointerSequence)
    c = caskets(n)
    truthSequence = initialTruthSequence(n)
    for i in c:
        for j in pointerSequence:
            truthSequence[i-1] += truthAtPointer(i,j)
    return truthSequence

def truthAtPointer(p, pointer):
    if p == pointer :
        return 1
    if pointer < 0:
        if p != -1*pointer:
            return 1        
    return 0


def truthSequence(p, pointers):
	n = len(pointers)
	seq = []
	for i in pointers:
		seq.append(truthAtPointer(p, i))
	return seq

# checks to see of all truth counts
# are distinct
def allDistinct(truthSequence):
    reduced = set(truthSequence)
    return len(reduced) == len(truthSequence)

# in portia2, we want to know how many true statements
# are on each casket for a given position
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
    #print(truthVector)
    return truthVector

def isDerrangement(v1, v2):
    count = 0;
    for i in v1:
        if i in v2:
            count += 1
    return count == len(v1)        

def notDerrangementInList(d, list):
    for c in list:
        if isDerrangement(d,c):
            return False 
    return True

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

def positionalTruth(c, t): 
	if c == min(t): return "min" 
	if c == max(t): return "max"
	return "mid"

def hasPointer(i, pointers) :
	for j in pointers:
		if i == j : return True
		if i == -1*j : return True
	a = []
	for j in pointers:
		a.append(abs(j))
	if len(set(a)) >1 : return True
	return False; 

def pointerList(pointers) :
	n = len(pointers)
	c = caskets(n)
	results = []
	for i in c:
		if hasPointer(i, pointers):
			results.append(i)
	return results
		
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


def checkForPortia2(casketTuple):
    casketSet1 = casketTuple[0]
    casketSet2 = casketTuple[1]
    #print(casketTuple)
    solutionList = []
    t = truthForPointers2(casketSet1, casketSet2)
    for i in range(len(t)) :
        remaining = list(t)
        remaining.remove(t[i])
        if notDerrangementInList(t[i],remaining):
            solutionList.append(i)
    results = []    
    for i in solutionList:
        p = []
        p.append(casketTuple)
        p.append(t[i])
        p.append(i+1)
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

def json(puzzleDef, counter):
    result  = "{\"caskets\": "
    result += str(puzzleDef[0])
    result += ", \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2])
    result += ", \"position\": \"" + puzzleDef[3] +"\"" 
    result += ", \"id\": " + "\"portia1-" + str(counter)+ "\"}"        
    return result

def json2(puzzleDef, counter):
    result  = "{\"caskets\": ["
    result += str(puzzleDef[0][0])
    result += ", "
    result += str(puzzleDef[0][1])
    result += "], \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2]) 
    result += ", \"id\": " + "\"portia2-" + str(counter)+ "\"}"
    return result

def json3(puzzleDef, counter):
    result  = "{\"caskets\": "
    result += str(puzzleDef[0])
    result += ", \"truths\": " + str(puzzleDef[1])
    result += ", \"solution\": " + str(puzzleDef[2])
    result += ", \"id\": " + "\"portia3-" + str(counter)+ "\"}"        
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

def noMatch(l1, l2):
    result = True
    for i in range(len(l1)) :
        if l1[i] == l2[i] :
            result = False 
    return result

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

def negateOnePerSequence(sequences):
	result = []
	for s in sequences:
		for i in range(len(s)):
			r = s[:]
			r[i] = -1*r[i]
			result.append(r)
	return result;

def removeAll(p,d):
	q = p[:]
	for i in d:
		removeIfPresent(q,i)
	return q	

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
# using the puzzle generator
#
print('-------------------------------------')
print('Generating Portia I data.')
print(' --- creating file ../data/portia1.json')
f = open("../data/portia1.json","w")
f.write(generateAllPuzzlesPortia1(3))
f.close()
print(' --- completed writing out Portia I data.')
print('-------------------------------------')
print("Generating Portia II data.")
print(' --- creating file ../data/portia2.json')
f = open("../data/portia2.json","w")
f.write(generateAllPuzzlesPortia2(3))
f.close()
print(' --- completed writing out Portia II data.')
print('-------------------------------------')
print("Generating Portia III data.")
print(' --- creating file ../data/portia3.json')
f = open("../data/portia3.json","w")
f.write(generateAllPuzzlesPortia3(3))
f.close()
print(' --- completed writing out Portia III data.')
print('-------------------------------------')