def recursion(test1):
    oldtest1= test1
    print(oldtest1)
    if (test1 < 0): 
        return -1
    elif (test1 < 2):
        return 1
    else:
        return test1 * recursion(test1-1)


print(recursion(5))
    
