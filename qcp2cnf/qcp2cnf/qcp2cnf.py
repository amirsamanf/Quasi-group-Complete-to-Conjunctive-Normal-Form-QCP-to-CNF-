
from itertools import combinations

filePath = 'C:\\Users\\Amirsaman\\Documents\\CMPT417\\Assignment1\\instances\\q_10_01.qcp'
resultPath = 'C:\\Users\\Amirsaman\\Documents\\CMPT417\\Assignment1\\instances\\result.cnf'


def map3to1(order,a,b,c):

    leftMultiplier  = order**2
    midMultiplier   = order
    rightMultiplier = 1
    correction      = leftMultiplier + midMultiplier

    return (a*leftMultiplier + b*midMultiplier + c*rightMultiplier) - correction



file = open(filePath, 'r')
lines = file.readlines()


row = 0
order = ""
fixedCellClauses = []
propertyDependentClauses = []
for line in lines:
    # Determine order
    if row == 0:
        order = line.split(' ')[1]
           
    else:
        words = line.split()
        
        col = 1
        for word in words:
            if word != '.':
                clause = str(map3to1(int(order),row,col,int(word)))
                fixedCellClauses.append(clause)
                fixedCellClauses.append('0')
            col += 1
    row += 1

order = int(order)

def propertyA():
    clauses = []
    for i in range(1,order+1):
        for j in range(1,order+1):
            for k in range(1,order+1):
                clause = str(map3to1(order,i,j,k))
                clauses.append(clause)
            clauses.append('0')
    return clauses
    

def propertyB():
    clauses = []
    nums = range(1,order+1)
    comb = list(combinations(nums, 2))
    combNum = 0
    for i in range(1,order+1):
        for j in range(1,order+1):
            val = comb[combNum]
            for val in comb:
                for k in range(1,3):
                    clause = '-' + str(map3to1(order,i,j,val[k-1]))
                    clauses.append(clause)
                clauses.append('0')
        combNum += 1
    return clauses



def propertyC():
    clauses = []
    nums = range(1,order+1)
    comb = list(combinations(nums, 2))
    combNum = 0
    for i in range(1,order+1):
        for j in range(1,order+1):
            val = comb[combNum]
            for val in comb:
                for k in range(1,3):
                    lause = '-' + str(map3to1(order,i,val[k-1],j))
                    clauses.append(clause)
                clauses.append('0')
        combNum += 1
    return clauses


def propertyD():
    clauses = []
    nums = range(1,order+1)
    comb = list(combinations(nums, 2))
    combNum = 0
    for i in range(1,order+1):
        for j in range(1,order+1):
            val = comb[combNum]
            for val in comb:
                for k in range(1,3):
                    clause = '-' + str(map3to1(order,val[k-1],i,j))
                    clauses.append(clause)
                clauses.append('0')
        combNum += 1
    return clauses


def propertyE():
    clauses = []
    for i in range(1,order+1):
        for j in range(1,order+1):
            for k in range(1,order+1):
                clause = str(map3to1(order,i,k,j))
                clauses.append(clause)
            clauses.append('0')
    return clauses


def propertyF():
    clauses = []
    for i in range(1,order+1):
        for j in range(1,order+1):
            for k in range(1,order+1):
                clause = str(order,map3to1(k,i,j))
                clauses.append(clause)
            clauses.append('0')
    return clauses


A = propertyA()
B = propertyB()
C = propertyC()
D = propertyD()
#E = propertyE()
#F = propertyF()
finalClauses = fixedCellClauses + A + C + D

numClauses = finalClauses.count('0')
numVars = map3to1(order,order,order,order)

with open(resultPath, "w") as f:
    f.write('p cnf ' + str(numVars) + ' ' + str(numClauses) + '\n' )
    for clause in finalClauses:
        f.write(clause)
        if clause == '0':
            f.write('\n')
        else:
            f.write(' ')






