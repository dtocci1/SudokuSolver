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