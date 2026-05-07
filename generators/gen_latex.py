import json
import latex_utils as lu

colours = ['lead', 'silver', 'gold']
truthCounts =["There are no true statements on the caskets.","Only one of the caskets has a true statement.","There are two caskets with true statements.","All caskets have true statements."]

def textForPointer(pointer, currentIndex):
    #selfNegative = ["The portrait is not in this casket.", "The portrait is not in here.","This casket is empty."];
    #selfPositive = ["The portrait is in this casket.", "The portrait is in here.","This casket has the portriat."]
    p = pointer;
    negative = False
    if pointer < 0:
        p = -1*pointer
        negative = True

    if p == currentIndex:
        if negative:
            return "The portrait is not here"
        else:
            return "The portrait is here"
    if negative:
        return "The portrait is not in the " + colours[p-1] + " casket"
    else:
        return "The portrait is in the " + colours[p-1] + " casket"

def portiaICasketText(pointerArray):
    text = []
    for j in range(len(pointerArray)):
        text.append(textForPointer(pointerArray[j],j+1))
    return text

with open('../data/portia1.json') as f:
    all_portia1 = json.load(f)
    print(all_portia1)

def writePuzzle(puzzleNumber,inputList):
    puzzle= all_portia1[puzzleNumber]
    statements = portiaICasketText(puzzle['caskets'])
    solution = "Solution: The portrait is in the " + colours[puzzle['solution']-1] + " casket."

    tabular = lu.LTabular("ccc")
    titleRow = lu.LRow(len(colours))
    titleRow.addAll(colours)
    topRow = lu.LRow(len(statements))
    topRow.addAll(statements)
    tabular.add(titleRow)
    tabular.add(topRow)

    latex = truthCounts[puzzle['truths']]
    latex = latex + '\n'
    latex = latex + tabular.build()
    latex = latex + '\n'
    latex = latex + solution
    fileLocation = "latex_files/puzzle_"+ str(puzzleNumber) + ".tex"
    inputList.append("\\input{"+fileLocation+"}\n")
    file = open("../"+ fileLocation,"w")
    file.write(latex)
    file.close()

def generatePortia1():
    inputs = []
    for p in range(12):
        writePuzzle(p,inputs)
    inputString = ""
    for i in inputs:
        inputString += i

    file = open("../latex_files/portia1.tex","w")
    file.write(inputString)
    file.close()

generatePortia1()
