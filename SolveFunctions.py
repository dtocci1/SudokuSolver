# User-defined Functions
def split(word):
    return [char for char in word]
    
def checkBox(table, boxNumber):
    # Used to ensure each sudoku "box" uniquely uses 1-9
    # To quickly do this, summing the box should add up to 45
    if boxNumber <= 3:
        columnIndex = 3
    elif boxNumber <= 6:
        columnIndex = 6
    else:
        columnIndex =  9 

    rowIndex = int(((3 * boxNumber) / columnIndex) * 3)
    sum=0
    rI=rowIndex-3

    while rI < rowIndex:
        cI = columnIndex-3
        while cI < columnIndex:
            if (table[rI][cI] != 'x'):  
                sum = sum + table[rI][cI]
            cI = cI + 1
        rI = rI + 1

    if sum == 45: return 0
    else: return 1

def checkRow(table,row):
    # Used to ensure each sudoku row uniquely uses 1-9
    listAmount = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        if (table[row][i] != 'x' and table[row][i] != 'X'):
            listAmount[table[row][i]-1] += 1
            if 2 in listAmount:
                return 1
    return 0

def checkColumn(table,column):
    # Used to ensure each sudoku column uniquely uses 1-9
    listAmount = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        if (table[i][column] != 'x' and table[i][column] != 'X'):
            listAmount[table[i][column]-1] += 1
            if 2 in listAmount:
                return 1
    return 0

def missingFromRow(table, row):
    # Determine what numbers can be used (are missing) in this column
    usedNumbers = []
    missingNumbers = []
    for i in range(9):
        if (table[row][i] != 'x' and table[row][i] != 'X'):
            usedNumbers.append(table[row][i])
    for i in range(9):
        if(i+1 not in usedNumbers):
            missingNumbers.append(i+1)
    return missingNumbers

def missingFromColumn(table, column):
    # Determine what numbers can be used (are missing) in this column
    usedNumbers = []
    missingNumbers = []
    for i in range(9):
        if (table[i][column] != 'x' and table[i][column] != 'X'):
            usedNumbers.append(table[i][column])
    for i in range(9):
        if i+1 not in usedNumbers:
            missingNumbers.append(i+1)
    return missingNumbers

def missingFromBox(table,row,column):
    rm = 0 # row max
    cm = 0 # column max
    mB = [] # Missing numbers from "box" the coordinates are in
    usedNumbers=[] #tmp for storing missing numbers in box
    # Determine box
    # Some equation could probably replace this
    if (row <= 2): # First row of boxes
        rm = 3
        if (column <= 2): # First column
            cm = 3
        elif (column <= 5):
            cm = 6
        elif (column <= 8):
            cm = 9
    elif (row <= 5): # Second row of boxes
        rm = 6
        if (column <= 2):
            cm = 3
        elif (column <= 5):
            cm = 6
        elif (column <= 8): 
            cm = 9
    elif (row <= 8): # Third row of boxes
        rm = 9
        if (column <= 2):
            cm = 3
        elif (column <= 5):
            cm = 6
        elif (column <= 8) :
            cm = 9

    rI = rm - 3
    while rI < rm:
        cI = cm-3
        while cI < cm:
            if (table[rI][cI] != 'x' and table[rI][cI] != 'X'):
                usedNumbers.append(table[rI][cI]) # May be redundant variable
            cI = cI + 1
        rI = rI + 1
        
    for i in range(9): # MAKE THIS A FUNCTION, 3RD OR 4TH USE AT THIS POINT
        if(i+1 not in usedNumbers):
            mB.append(i+1)
    
    return mB

def usableNumbers(table,row,column):
    # Combines missingFromRow and missingFromColumn to determine numbers available for box
    if table[row][column] != 'x':
        return []
    mN =[] # All usable numbers for this coordinate, row column and box taken into account
    mC=[] # missing numbers in column
    mR=[] # missing numbers in row
    mB=[] # missing numbers in "box"
    mRC=[] # missing numbers in both
    mC = missingFromColumn(table, column)
    mR = missingFromRow(table, row)
    mB = missingFromBox(table,row,column)
    for i in range(min(len(mC), len(mR))):
        if (len(mC) < len(mR)):
            if mC[i] in mR:
                mRC.append(mC[i])
        else:
            if mR[i] in mC:
                mRC.append(mR[i])

    for i in range(min(len(mRC), len(mB))):
        if (len(mRC) < len(mB)):
            if mRC[i] in mB:
                mN.append(mRC[i])
        else:
            if mB[i] in mRC:
                mN.append(mB[i])
    return mN

def iteratePuzzle(table, solutions, depth):
    # Recursive function for solving the puzzle
    # minSolution refers to minimum number of solutions for each box
    # ie. if minSolution = 1, loop until no numbers have only one possibility
    possibilities = 1 # default to get into while loop
    newTable=table # table to be modified
    oldTable=table # unmodified version of previous stack table
    newSolutions=solutions
    oldSolutions=solutions # unmodified version of previous stack table
    iteration = 0
    broken=0
    recursion=1
    choice = 0
    tmpRC=[]
    bFlag=0 #prevents an edge case
    cFlag=0 #prevents logic issue
    #region Iterate through cells, solving cells with only one choice. Regenerate solution after
    while (possibilities >= 1): # While there are still solutions to iterate through (ie 1 or more cell has X possibilities)
        print(f"Solving iteration[{iteration}] at depth[{depth}]...")
        possibilities = 0
        for row in range(9):
            for column in range(9):
                if (len(oldSolutions[row][column]) == 1 and newTable[row][column] == 'x'): # If there is a cell with X possibilities and that cell is blank
                    newTable[row][column] = oldSolutions[row][column][0] # Plug in the "choice" into the new solution
                    newSolutions[row][column] = [] # blank out other solutions
        
        # Recreate solutions at each point
        for row in range(9):
            for column in range(9):
                if (newTable[row][column] == 'x'):
                    newSolutions[row][column] = usableNumbers(newTable,row,column) # re-calculate "usable" numbers
                    if (len(newSolutions[row][column]) == 1): # Determine if any have only one solution
                        possibilities += 1
                elif(newTable[row][column] != 'x'):
                    newSolutions[row][column] = [] # ensure solutions are wiped from solved boxes
        iteration+=1
    #endregion

    # Check if anything is unsolvable
    for row in range(9):
        for column in range(9):
            if (len(usableNumbers(newTable,row,column)) == 0 and newTable[row][column] == 'x'):
                broken=1
                break
        if(broken):
            break
    
    
    if (broken): # If there is any unsolvable point
        return oldTable # go up in the stack with the old table

    # Everything with one solution is solved
    # Check if we had to go back in stack

    # Guess on closest one with extra solution
    while (recursion == 1):        
        if (choice == 0):
            # Determine point where choice needs to be made
            for row in range(9):
                for column in range(9):
                    tmp = len(usableNumbers(newTable,row,column))
                    if (tmp == 2 and newTable[row][column] == 'x'):
                        bFlag = 1
                        break
                if (tmp == 2 and newTable[row][column] == 'x'):
                    break
            # Make a choice
            if(bFlag == 1):
                newTable[row][column] = usableNumbers(newTable,row,column)[choice]
                print(f"Making a choice at {row,column}, picking choice {choice}, value = {newTable[row][column]}")
                tmpRC=[row,column]
                bFlag = 0
                cFlag = 1

            # No choice could be made
            else:
                cFlag = 0
        elif ([row,column] == tmpRC): # Try another option
            newTable = oldTable # reset table
            newTable[row][column] = oldSolutions[row][column][choice] #pick new option
            # regenerate solutions
            for i in range(9):
                for j in range(9):
                    if (newTable[i][j] == 'x'):
                        newSolutions[i][j] = usableNumbers(newTable,i,j) # re-calculate "usable" numbers 
            print(f"Redoing a choice at {row,column}, picking choice {choice}, value = {newTable[row][column]}")
            cFlag = 1

        if (cFlag): #if a choice was made
            newTable = iteratePuzzle(newTable,newSolutions,depth+1) # *** RECURSION OCCURS HERE ***
        
        if (newTable == oldTable and cFlag == 1):
            tmp = len(oldSolutions[row][column])
            if(choice+1 < tmp):
                choice+=1
        else:
            # Check if puzzle is broken again
            for row in range(9):
                for column in range(9):
                    if (len(usableNumbers(newTable,row,column)) == 0 and newTable[row][column] == 'x'):
                        broken=1
                        break
                if(broken):
                    break
            if (broken):
                return oldTable
            else:
                recursion=0

    #region Old recursive solution
    '''
    # Check if we solved the puzzle
    for i in range(9):
        vFlag = checkBox(newTable,i+1)
        if (vFlag):
            break

    if (vFlag): # Puzzle is not solved :(
        # Not solved and there are no more possibilities
        # Check there are any "impossible" points
        for i in range(9):
            for j in range(9):
                if (len(newSolutions[i][j]) == 0 and newTable[i][j] == 'x'): # If there is a point not filled in with NO possibilities, break out
                    return oldTable

        # Determine where a minSolution+1 point lies and pick based on choice
        for row in range(9):
            for column in range(9):
                if (len(newSolutions[row][column]) == minSolution+1):
                    break
            if (len(newSolutions[row][column]) == minSolution+1):
                break
        # Guess at this singular point
        newTable[row][column] = newSolutions[row][column][choice]
        # Check if any one solutions appear
        newTable = iteratePuzzle(newTable,minSolution,choice,newSolutions,depth)
        if (newTable == oldTable): # We reached a point where nothing is possible
            if (choice < minSolution):
                choice = choice + 1
                newTable = iteratePuzzle(newTable,minSolution,choice,newSolutions,depth)

        # If they don't, try a the second choice
    '''
    #endregion


    return newTable
