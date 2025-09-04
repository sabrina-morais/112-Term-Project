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

def generate_maze_dict_helper(n, maze_dict, last_point, new_point, index):
    # check if new_point valid
    new_x, new_y = new_point
    if ((new_x < 0) or (new_x > n-1) or (new_y < 0) or (new_y > n-1)
        or (is_point_in_dict(maze_dict, new_point) == True) 
        or (new_point == (0,0))):
        return False

    # set new point
    if last_point in maze_dict:
        maze_dict[last_point].append(new_point)
    else:
        maze_dict[last_point] = [new_point]

    # check if maze complete
    if (index == (n**2 - 2)):
        return True

    # run through moves & continue w recursion
    moves = [(1,0), (0,1), (-1,0), (0,-1)]
    random.shuffle(moves)
    for move in moves:
        dx, dy = move
        next_x = new_x + dx
        next_y = new_y + dy
        next_point = (next_x, next_y)
        if (generate_maze_dict_helper(n, maze_dict, new_point, 
                                    next_point, index+1) == True):
            return True
    
    # if recursion doesn't work, undo move
    return generate_maze_dict_helper(n, maze_dict, last_point, new_point, index)

def is_point_in_dict(maze_dict, point):
    for coordinate in maze_dict:
        if point in maze_dict[coordinate]:
            return True
    return False

def maze_solver(n, maze_dict, start_cell, end_cell):
    flipped_dict = flip_maze_dict(maze_dict)
    solution = [start_cell]
    last_point = maze_dict[start_cell][0]
    maze_solver_helper(n, maze_dict, solution, last_point, end_cell)
    if (len(solution) == 1):
        maze_solver_helper(n, flipped_dict, solution, last_point, end_cell)
    return flipped_dict, solution

def maze_solver_in_two_parts(n, maze_dict, start_cell, end_cell):
    flipped_dict, solution = maze_solver(n, maze_dict, (0,0), (n-1,n-1))
    intermediate_cell = (n-1, n-1)

    def get_first_connected_cell(cell, graph):
        try:
            return graph[cell][0]
        except KeyError:
            for point in graph:
                if cell in graph[point]:
                    return point
        raise ValueError(f"No connected cell found for {cell} in graph")

    def solve_path(cell, graph, flipped_graph):
        path = [cell]
        last_point = get_first_connected_cell(cell, graph)
        maze_solver_given_sol(n, graph, path, last_point, intermediate_cell, solution)
        if len(path) == 1:
            last_point = get_first_connected_cell(cell, flipped_graph)
            maze_solver_given_sol(n, flipped_graph, path, last_point, intermediate_cell, solution)
        return path

    first_sol = solve_path(start_cell, maze_dict, flipped_dict)
    second_sol = solve_path(end_cell, maze_dict, flipped_dict)

    # Combine the two paths
    final_sol = []
    for i, f in enumerate(first_sol):
        if f in second_sol:
            j = second_sol.index(f)
            final_sol.extend(first_sol[:i])
            second_part = second_sol[:j+1]
            second_part.reverse()
            final_sol.extend(second_part)
            break

    # Trim extra points beyond end_cell
    if end_cell in final_sol:
        idx = final_sol.index(end_cell)
        final_sol = final_sol[:idx+1]

    return final_sol


def maze_solver_helper(n, maze_dict, solution, last_point, end_cell):
    _ , _ = last_point

    # set last_point
    solution.append(last_point)

    # check if reached bottom right coordinate
    if (last_point == end_cell):
        return True

    # check if last_point valid
    if (last_point not in maze_dict):
        solution.pop()
        return False
    
    # recurse 
    for connection in maze_dict[last_point]:
        if maze_solver_helper(n, maze_dict, solution, connection, end_cell) == True:
            return True

    # if recursion doesn't work
    solution.pop()
    return False

def maze_solver_given_sol(n, dictionary, solution, last_point, end_cell, given_sol):
    _ , _ = last_point

    # set last_point
    solution.append(last_point)

    # check if reached solution
    for i in range(len(given_sol)):
        if (last_point == given_sol[i]):
            solution.extend(given_sol[i:])
            return True

    # check if last_point valid
    if (last_point not in dictionary):
        solution.pop()
        return False
    
    # recurse 
    for connection in dictionary[last_point]:
        if maze_solver_given_sol(n, dictionary, solution, connection, given_sol, end_cell) == True:
            return True

    # if recursion doesn't work
    solution.pop()
    return False

def get_maze_solution_connections(n, maze_dict, start_cell, end_cell):
    solution = maze_solver_in_two_parts(n, maze_dict, start_cell, end_cell)
    conn_dict = {}

    # create dictionary of all coordinates
    for x in range(n):
        for y in range(n):
            conn_dict[(x,y)] = []
    
    # map all coordinates to every point each is connected to
    for key in maze_dict:
        conn_dict[key] += maze_dict[key]
        for point in maze_dict[key]:
            conn_dict[point].append((key))

    return solution, conn_dict

def flip_maze_dict(maze_dict):
    flipped_dict = {}

    for key in maze_dict:
        for point in maze_dict[key]:
            flipped_dict[point] = [key]

    return flipped_dict