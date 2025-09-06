# tests/test_maze_generation_and_solution.py
import pytest
import random
from mazeGenerationAndSolution import (
    generate_maze_dict, generate_maze_dict_helper, is_point_in_dict,
    maze_solver, maze_solver_in_two_parts, get_maze_solution_connections,
    flip_maze_dict
)

# Fixar a seed para resultados determinísticos
random.seed(42)

# ------------------------
# Testes de geração de labirinto
# ------------------------
def test_generate_maze_dict_small():
    n = 3
    maze = generate_maze_dict(n)
    assert isinstance(maze, dict)
    assert (0,0) in maze
    for k, v in maze.items():
        for point in v:
            assert 0 <= point[0] < n
            assert 0 <= point[1] < n

def test_is_point_in_dict_true_and_false():
    maze = {(0,0): [(1,0)]}
    assert is_point_in_dict(maze, (1,0)) == True
    assert is_point_in_dict(maze, (2,2)) == False

def test_generate_maze_dict_helper_invalid_point():
    maze_dict = {}
    result = generate_maze_dict_helper(3, maze_dict, (0,0), (3,3), 0)
    assert result == False

# ------------------------
# Testes de flip de maze_dict
# ------------------------
def test_flip_maze_dict():
    maze = {(0,0): [(1,0)], (1,0): [(1,1)]}
    flipped = flip_maze_dict(maze)
    assert flipped[(1,0)] == [(0,0)]
    assert flipped[(1,1)] == [(1,0)]

# ------------------------
# Testes de solução de labirinto
# ------------------------
def test_maze_solver_and_in_two_parts():
    n = 3
    maze = generate_maze_dict(n)
    start_cell = (0,0)
    end_cell = (n-1,n-1)
    flipped, solution = maze_solver(n, maze, start_cell, end_cell)
    assert isinstance(flipped, dict)
    assert isinstance(solution, list)
    final_solution = maze_solver_in_two_parts(n, maze, start_cell, end_cell)
    assert final_solution[0] == start_cell
    assert final_solution[-1] == end_cell

# ------------------------
# Teste de conexões finais
# ------------------------
def test_get_maze_solution_connections():
    n = 3
    maze = generate_maze_dict(n)
    start_cell = (0,0)
    end_cell = (n-1,n-1)
    solution, conn_dict = get_maze_solution_connections(n, maze, start_cell, end_cell)
    assert isinstance(solution, list)
    assert isinstance(conn_dict, dict)
    for x in range(n):
        for y in range(n):
            assert (x,y) in conn_dict
            assert isinstance(conn_dict[(x,y)], list)
