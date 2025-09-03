########################################
#   Ho Ho Home: the Santa Maze Game 
#   (mazeGenerationAndSolution.py)
#   By: Sarah Chen (sarahc2)
########################################
#   Maze Generation & Solution
########################################
import random

def generate_maze_dict(n):
    maze_dict = {}
    last_point = (0, 0)
    new_point = (1, 0)
    generate_maze_dict_helper(n, maze_dict, last_point, new_point, 0)
    return maze_dict

def generate_maze_dict_helper(n, mazeDict, lastPoint, newPoint, index):
    # check if newPoint valid
    newX, newY = newPoint
    if ((newX < 0) or (newX > n-1) or (newY < 0) or (newY > n-1)
        or (is_point_in_dict(mazeDict, newPoint) == True) 
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
        if (generate_maze_dict_helper(n, mazeDict, newPoint, 
                                    nextPoint, index+1) == True):
            return True
    
    # if recursion doesn't work, undo move
    return generate_maze_dict_helper(n, mazeDict, lastPoint, newPoint, index)

def is_point_in_dict(mazeDict, point):
    for coordinate in mazeDict:
        if point in mazeDict[coordinate]:
            return True
    return False

def maze_solver(n, mazeDict, startCell, endCell):
    flippedDict = flipMazeDict(mazeDict)
    solution = [startCell]
    lastPoint = mazeDict[startCell][0]
    maze_solver_helper(n, mazeDict, solution, lastPoint, endCell)
    if (len(solution) == 1):
        maze_solver_helper(n, flippedDict, solution, lastPoint, endCell)
    return flippedDict, solution

def maze_solver_in_two_parts(n, mazeDict, startCell, endCell):
    flippedDict, solution = maze_solver(n, mazeDict, (0,0), (n-1,n-1))
    intermediateCell = (n-1, n-1)

    def getFirstConnectedCell(cell, graph):
        try:
            return graph[cell][0]
        except KeyError:
            for point in graph:
                if cell in graph[point]:
                    return point
        raise ValueError(f"No connected cell found for {cell} in graph")

    def solvePath(cell, graph, flippedGraph):
        path = [cell]
        lastPoint = getFirstConnectedCell(cell, graph)
        maze_solver_given_sol(n, graph, path, lastPoint, intermediateCell, solution)
        if len(path) == 1:
            lastPoint = getFirstConnectedCell(cell, flippedGraph)
            maze_solver_given_sol(n, flippedGraph, path, lastPoint, intermediateCell, solution)
        return path

    firstSol = solvePath(startCell, mazeDict, flippedDict)
    secondSol = solvePath(endCell, mazeDict, flippedDict)

    # Combine the two paths
    finalSol = []
    for i, f in enumerate(firstSol):
        if f in secondSol:
            j = secondSol.index(f)
            finalSol.extend(firstSol[:i])
            secondPart = secondSol[:j+1]
            secondPart.reverse()
            finalSol.extend(secondPart)
            break

    # Trim extra points beyond endCell
    if endCell in finalSol:
        idx = finalSol.index(endCell)
        finalSol = finalSol[:idx+1]

    return finalSol


def maze_solver_helper(n, mazeDict, solution, lastPoint, endCell):
    _ , _ = lastPoint

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
        if maze_solver_helper(n, mazeDict, solution, connection, endCell) == True:
            return True

    # if recursion doesn't work
    solution.pop()
    return False

def maze_solver_given_sol(n, dictionary, solution, lastPoint, endCell, givenSol):
    _ , _ = lastPoint

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
        if maze_solver_given_sol(n, dictionary, solution, connection, givenSol, endCell) == True:
            return True

    # if recursion doesn't work
    solution.pop()
    return False

def get_maze_solution_connections(n, mazeDict, startCell, endCell):
    solution = maze_solver_in_two_parts(n, mazeDict, startCell, endCell)
    connDict = {}

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
    flippedDict = {}

    for key in mazeDict:
        for point in mazeDict[key]:
            flippedDict[point] = [key]

    return flippedDict