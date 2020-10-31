#!/usr/bin/env python3

from itertools import combinations
import subprocess
from math import floor
import os
import sys, getopt


inputfile = sys.argv[1]
script_dir = os.path.dirname(__file__)
filePath = os.path.join(script_dir, "instances/" + inputfile)
resultPath = os.path.join(script_dir, "result.cnf")
solPath = os.path.join(script_dir, "sol.txt")


def map3to1(order,a,b,c):

    leftMultiplier  = order**2
    midMultiplier   = order
    rightMultiplier = 1
    correction      = leftMultiplier + midMultiplier

    return (a*leftMultiplier + b*midMultiplier + c*rightMultiplier) - correction

def map1to3(order,val,a,b):
    leftMultiplier  = order**2
    midMultiplier   = order
    rightMultiplier = 1
    correction      = leftMultiplier + midMultiplier

    return int((val + correction - (a*leftMultiplier + b*midMultiplier)) / rightMultiplier)




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
                    clause = '-' + str(map3to1(order,i,val[k-1],j))
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
                clause = str(map3to1(order,k,i,j))
                clauses.append(clause)
            clauses.append('0')
    return clauses



def checkSolution(lines,order):
    encodedVals = []
    decodedVals = []
    for line in lines:
        words = line.split()
        if words[0] == 'v':
            for word in words[1:]:
                if int(word) > 0:
                    encodedVals.append(word)

    index = 0
    a = 0
    b = 0
    for i in range(0,len(encodedVals)):
        a = floor(i/order) + 1
        b = (i % order) + 1
        decodedVals.append(map1to3(order,int(encodedVals[i]),a,b))

    return decodedVals

A = propertyA()
B = propertyB()
C = propertyC()
D = propertyD()
E = propertyE()
F = propertyF()
finalClauses = fixedCellClauses + A + B + C + D + E + F

numClauses = finalClauses.count('0')
numVars = map3to1(order,order,order,order)

f = open(resultPath, 'w')
f.write('p cnf ' + str(numVars) + ' ' + str(numClauses) + '\n' )
for clause in finalClauses:
    f.write(clause)
    if clause == '0':
        f.write('\n')
    else:
        f.write(' ')
f.close()

command = 'picosat/picosat result.cnf > sol.txt'
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
process.wait()

sol = open(solPath, 'r')
lines = sol.readlines()
sol.close()

solution = checkSolution(lines,order)
print(solution)




