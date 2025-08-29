########################################
#   Ho Ho Home: the Santa Maze Game 
#   (mazeGenerationAndSolution.py)
#   By: Sarah Chen (sarahc2)
########################################
#   Maze Generation & Solution
########################################
import random

def generateMazeDict(n):
    mazeDict = {}
    lastPoint = (0,0)
    newPoint = (1,0)
    generateMazeDictHelper(n, mazeDict, lastPoint, newPoint, 0)
    return mazeDict

def generateMazeDictHelper(n, mazeDict, lastPoint, newPoint, index):
    # check if newPoint valid
    newX, newY = newPoint
    if ((newX < 0) or (newX > n-1) or (newY < 0) or (newY > n-1)
        or (isPointInDict(mazeDict, newPoint) == True) 
        or (newPoint == (0,0))):
        return False

    # set new point
    if lastPoint in mazeDict:
        mazeDict[lastPoint].append(newPoint)
    else:
        mazeDict[lastPoint] = [newPoint]

    # check if maze complete
    if (index == (n**2 - 2)):
        return True

    # run through moves & continue w recursion
    moves = [(1,0), (0,1), (-1,0), (0,-1)]
    random.shuffle(moves)
    for move in moves:
        dx, dy = move
        nextX = newX + dx
        nextY = newY + dy
        nextPoint = (nextX, nextY)
        if (generateMazeDictHelper(n, mazeDict, newPoint, 
                                    nextPoint, index+1) == True):
            return True
    
    # if recursion doesn't work, undo move
    return generateMazeDictHelper(n, mazeDict, lastPoint, newPoint, index)

def isPointInDict(mazeDict, point):
    for coordinate in mazeDict:
        if point in mazeDict[coordinate]:
            return True
    return False

def mazeSolver(n, mazeDict, startCell, endCell):
    flippedDict = flipMazeDict(mazeDict)
    solution = [startCell]
    lastPoint = mazeDict[startCell][0]
    mazeSolverHelper(n, mazeDict, solution, lastPoint, endCell)
    if (len(solution) == 1):
        mazeSolverHelper(n, flippedDict, solution, lastPoint, endCell)
    return flippedDict, solution

def mazeSolverInTwoParts(n, mazeDict, startCell, endCell):
    # get maze dictionary, flipped maze dictionary, and solution list from UL to BR
    flippedDict, solution = mazeSolver(n, mazeDict, (0,0), (n-1,n-1))

    # get BL cell
    intermediateCell = (n-1, n-1)

    # firstSol gets from startCell to BR
    firstSol = [startCell]
    try:
        firstLastPoint = mazeDict[startCell][0]
    except:
        for point in mazeDict:
            if startCell in mazeDict[point]:
                firstLastPoint = point
    mazeSolverGivenSol(n, mazeDict, firstSol, firstLastPoint, intermediateCell, solution)
    if (len(firstSol) == 1):
        try:
            firstLastPoint = flippedDict[startCell][0]
        except:
            for point in flippedDict:
                if startCell in flippedDict[point]:
                    firstLastPoint = point
        mazeSolverGivenSol(n, flippedDict, firstSol, firstLastPoint, intermediateCell, solution)

    # secondSol gets from endCell to BR
    secondSol = [endCell]
    try:
        secondLastPoint = mazeDict[endCell][0]
    except:
        for point in mazeDict:
            if endCell in mazeDict[point]:
                secondLastPoint = point
    mazeSolverGivenSol(n, mazeDict, secondSol, secondLastPoint, intermediateCell, solution)
    if (len(secondSol) == 1):
        try:
            secondLastPoint = flippedDict[endCell][0]
        except:
            for point in flippedDict:
                if endCell in flippedDict[point]:
                    secondLastPoint = point
        mazeSolverGivenSol(n, flippedDict, secondSol, secondLastPoint, intermediateCell, solution)

    # combine firstSol and secondSol to get finalSol
    finalSol = []
    for i in range(len(firstSol)):
        for j in range(len(secondSol)):
            if (firstSol[i] == secondSol[j]):
                firstHalf = firstSol[:i]
                secondHalf = secondSol[:j+1]
                secondHalf.reverse()
                finalSol.extend(firstHalf)
                finalSol.extend(secondHalf)
                break
        if len(finalSol) != 0:
            break

    # get rid of extras at end of finalSol
    for i in range(len(finalSol)):
        if (finalSol[i] == endCell):
            if (i == len(finalSol)-1):
                break
            finalSol = finalSol[:i+1]
            break

    return finalSol

def mazeSolverHelper(n, mazeDict, solution, lastPoint, endCell):
    lastX, lastY = lastPoint

    # set lastPoint
    solution.append(lastPoint)

    # check if reached bottom right coordinate
    if (lastPoint == endCell):
        return True

    # check if lastPoint valid
    if (lastPoint not in mazeDict):
        solution.pop()
        return False
    
    # recurse 
    for connection in mazeDict[lastPoint]:
        if mazeSolverHelper(n, mazeDict, solution, connection, endCell) == True:
            return True

    # if recursion doesn't work
    solution.pop()
    return False

def mazeSolverGivenSol(n, dictionary, solution, lastPoint, endCell, givenSol):
    lastX, lastY = lastPoint

    # set lastPoint
    solution.append(lastPoint)

    # check if reached solution
    for i in range(len(givenSol)):
        if (lastPoint == givenSol[i]):
            solution.extend(givenSol[i:])
            return True

    # check if lastPoint valid
    if (lastPoint not in dictionary):
        solution.pop()
        return False
    
    # recurse 
    for connection in dictionary[lastPoint]:
        if mazeSolverGivenSol(n, dictionary, solution, connection, givenSol, endCell) == True:
            return True

    # if recursion doesn't work
    solution.pop()
    return False

def getMazeSolutionConnections(n, mazeDict, startCell, endCell):
    solution = mazeSolverInTwoParts(n, mazeDict, startCell, endCell)
    connDict = dict()

    # create dictionary of all coordinates
    for x in range(n):
        for y in range(n):
            connDict[(x,y)] = []
    
    # map all coordinates to every point each is connected to
    for key in mazeDict:
        connDict[key] += mazeDict[key]
        for point in mazeDict[key]:
            connDict[point].append((key))

    return solution, connDict

def flipMazeDict(mazeDict):
    flippedDict = dict()

    for key in mazeDict:
        for point in mazeDict[key]:
            flippedDict[point] = [key]

    return flippedDict
