from unittest.mock import MagicMock, Mock
from PIL import Image
from mazeModes import RadiusMode, GrinchMode, Maze
import pytest

def test_radius_mode_starts():
    fake_app = MagicMock()
    # Cria uma imagem maior para que qualquer scale funcione (>0)
    fake_app.load_image.return_value = Image.new("RGB", (200, 200), "blue")
    mode = RadiusMode()
    mode.app = fake_app
    mode.width = 2000   # maior largura para evitar scale <1
    mode.height = 2000  # maior altura para evitar scale <1
    mode.app_started()
    assert hasattr(mode, "radius")

def test_grinch_mode_starts():
    fake_app = MagicMock()
    fake_app.load_image.return_value = Image.new("RGB", (200, 200), "green")
    mode = GrinchMode()
    mode.app = fake_app
    mode.width = 2000
    mode.height = 2000
    mode.app_started()
    assert hasattr(mode, "grinch")

import pytest
from unittest.mock import Mock
from mazeModes import Maze, RadiusMode, GrinchMode

import pytest
from mazeModes import Maze, RadiusMode, GrinchMode
from unittest.mock import Mock

def create_maze_mode_for_test(n=10):
    # Cria app simulado com atributos numéricos
    app = Mock()
    app.width = 500
    app.height = 500
    app._active_mode = Mock()
    app.maze = Mock()
    app.finalScreen = Mock()
    app.timerMode = False
    app.presents = 100
    
    # Cria o Maze e configura width/height
    maze_mode = Maze()
    maze_mode.app = app
    maze_mode.width = app.width
    maze_mode.height = app.height
    maze_mode.app_started()  # inicializa todos os atributos
    
    return maze_mode, app

def create_maze_mode_for_test(n=None):
    maze_mode = Maze()
    maze_mode.app = Mock()
    maze_mode.app.width = 500
    maze_mode.app.height = 500
    maze_mode.app._active_mode = Mock()
    maze_mode.app.maze = Mock()
    maze_mode.app.finalScreen = Mock()
    maze_mode.app.timerMode = False
    maze_mode.app.presents = 100

    maze_mode.width = maze_mode.app.width
    maze_mode.height = maze_mode.app.height

    # mock apenas métodos que retornam imagens
    maze_mode.load_image = Mock(return_value="image")
    maze_mode.scale_image = Mock(return_value="image_resized")

    # inicializa app_started
    maze_mode.app_started()

    # sobrescreve n se fornecido
    if n is not None:
        maze_mode.n = n
        maze_mode.cellWidth = maze_mode.width / n
        maze_mode.cellHeight = maze_mode.height / n

    return maze_mode

def test_maze_app_started():
    maze_mode = create_maze_mode_for_test()
    assert maze_mode.n == 10
    assert isinstance(maze_mode.mazeDict, dict)
    assert isinstance(maze_mode.solution, list)
    assert maze_mode.dotStepSize > 0

def test_restart_maze_resets_values():
    maze_mode = create_maze_mode_for_test()
    old_solution = maze_mode.solution.copy()
    maze_mode.restartMaze()
    assert maze_mode.solution != old_solution
    assert maze_mode.showSolution == False
    assert maze_mode.presentsGathered == False

def test_get_possible_moves_basic():
    maze_mode = create_maze_mode_for_test(n=3)
    maze_mode.dotX = maze_mode.cellWidth / 2
    maze_mode.dotY = maze_mode.cellHeight / 2
    maze_mode.dotR = 5
    moves = maze_mode.getPossibleMoves()
    assert isinstance(moves, set)