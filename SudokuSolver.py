# Headers and imports
import time
from SolveFunctions import *

# Retrieve sudoku grid from user
# Expects numbers 1-9, or x/X when there is nothing in that space
# Should check that no columns or rows have repeated numbers
# Only applicable for 9x9 grid
rows=[]
parsedTable=[]

"""
#region Retrieve input and check for validity
# Retrieve input from user, currently assumes "good" values
print("Begin entering the values found in the 9x9 Sudoku puzzle")
print("If there is a blank space, please type x or X in its place")
for currentRow in range(9):
    rows.append(input("Enter values for row " + str((currentRow+1)) + ": "))

# Parse user input into list of lists
# ie:
# [1,2,3,4,5,6,7,8,9],  #ROW 1
# [2,1,3,6,5,4,7,8,9],  #ROW 2 etc..
# Currently stored as:
# [123456789,213654789,...]
for currentRow in range(9):
    parsedTable.append(split(rows[currentRow]))

# Validate data given by user
# Check rows and columns for repeats
# Likely O(N^3) time complexity
# May be worthwhile to either skip this step or reconfigure the algorithm

repeatFlag = 0 # Flag for determining of a row has duplicate numbers
innerRow = 0

# Navigate through each set, and each element in the set to check for duplicates
for outerRow in range(len(parsedTable)): # ->[1,2,3,4,5,6,7,8,9]<-, [2,1,3,6,5,4,7,8,9], etc...
    innerRow = 0
    while innerRow < len(parsedTable[outerRow]): # [->1<-,2,3,4,5,6,7,8,9]
        numCompare = innerRow + 1

        while numCompare < len(parsedTable[outerRow]): # [->1<-,*2*,3,4,5,6,7,8,9]
            if parsedTable[outerRow][innerRow] == parsedTable[outerRow][numCompare]:
                repeatFlag = 1
                break
            numCompare = numCompare + 1

        if repeatFlag:
            break
        innerRow = innerRow + 1

    if repeatFlag:
        break

# Navigate through each column to check for duplicates 
    # im too lazy to do this right now, later problem
#endregion
"""

testPuzzle =[
            ['x', '6', 'x', '1', 'x', '4', 'x', '5', 'x'],
            ['x', 'x', '8', '3', 'x', '5', '6', 'x', 'x'],
            ['2', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '1'],
            ['8', 'x', 'x', '4', 'x', '7', 'x', 'x', '6'],
            ['x', 'x', '6', 'x', 'x', 'x', '3', 'x', 'x'],
            ['7', 'x', 'x', '9', 'x', '1', 'x', 'x', '4'],
            ['5', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '2'],
            ['x', 'x', '7', '2', 'x', '6', '9', 'x', 'x'],
            ['x', '4', 'x', '5', 'x', '8', 'x', '7', 'x']
            ]

for i in range(9):
    for j in range(9):
        if testPuzzle[i][j].isdigit():
            testPuzzle[i][j] = int(testPuzzle[i][j])

# Generate solutions at each box
'''
0,0: 0,1,2,3
0,1: 1

'''
allSolutions = [ # Matrix of lists of all working numbers for solutions
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]]
]
#tik = time.perf_counter()

for row in range(9):
    for column in range(9):
        if (testPuzzle[row][column] == 'x'):
            allSolutions[row][column] = usableNumbers(testPuzzle,row,column)
onePossibility = 1 # Tracks cells with only one option, assumes it starts with at least one, doesn't really matter will just waste time if not possible

solution = iteratePuzzle(testPuzzle,allSolutions,0)

for i in range(9):
    for j in range(9):
        if (solution[i][j] == 'x'):
            print(f"At {i}, {j}")
            print(usableNumbers(solution,i,j))

for i in range(9):
    print(solution[i])








'''
while (onePossibility >= 1):
    print("Iteration[" + str(iteration) + "]: Solving...")
    onePossibility = 0 # reset posibilities flag

    # Solve all boxes with only one possibility
    for row in range(9):
        for column in range(9):
            if (len(allSolutions[row][column]) == 1 and testPuzzle[row][column] == 'x'):
                testPuzzle[row][column] = allSolutions[row][column][0] # add into test puzzle
                allSolutions[row][column] = [] # blank out solutions for this section
    
    # Recreate solutions at each point
    for row in range(9):
        for column in range(9):
            if (testPuzzle[row][column] == 'x'):
                allSolutions[row][column] = usableNumbers(testPuzzle,row,column) # re-calculate "usable" numbers
                if (len(usableNumbers(testPuzzle,row,column)) == 1): # Determine if any have only one solution
                    onePossibility += 1

    iteration += 1

# Check completion (maybe we got lucky)
for i in range(9):
    vFlag = checkBox(testPuzzle,i+1)
while (vFlag): # Continually solve until vFlag goes down
    # Guessing becomes necessary here
    print("Iteration[" + str(iteration) + "]: Solving...")
    onePossibility = 0
    # Solve all boxes with only one possibility
    for row in range(9):
        for column in range(9):
            if (len(allSolutions[row][column]) == 2 and testPuzzle[row][column] == 'x'):
                testPuzzle[row][column] = allSolutions[row][column][0] # add into test puzzle, pick first
                allSolutions[row][column] = [] # blank out solutions
    
    # Recreate solutions at each point
    for row in range(9):
        for column in range(9):
            if (testPuzzle[row][column] == 'x'):
                allSolutions[row][column] = usableNumbers(testPuzzle,row,column)
                if (len(usableNumbers(testPuzzle,row,column)) == 1):
                    onePossibility += 1
    iteration += 1
for i in range(9):
    for j in range(9):
        print(i,j,usableNumbers(testPuzzle,i,j))

tok = time.perf_counter()
print("\n\nDONE! Solved in " + str(iteration) + " iterations.")
print(f"Duration: {tok-tik:0.4f} seconds")
for i in range(9):

    print(testPuzzle[i])
'''