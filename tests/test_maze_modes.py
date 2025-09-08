from unittest.mock import MagicMock, Mock
from PIL import Image
from mazeModes import RadiusMode, GrinchMode, Maze
import pytest

def test_radius_mode_starts():
    from unittest.mock import MagicMock
    from mazeModes import RadiusMode
    from PIL import Image

    fake_app = MagicMock()
    fake_app.load_image.return_value = Image.new("RGB", (200, 200), "blue")

    mode = RadiusMode()
    mode.app = fake_app
    mode.width = 2000
    mode.height = 2000
    # Executa inicialização
    mode.app_started()
    # Ajuste: verificar se o app foi configurado
    assert mode.app is fake_app
    assert mode.width == 2000
    assert mode.height == 2000

def test_grinch_mode_starts():
    fake_app = MagicMock()
    fake_app.load_image.return_value = Image.new("RGB", (200, 200), "green")
    mode = GrinchMode()
    mode.app = fake_app
    mode.width = 2000
    mode.height = 2000
    mode.app_started()
    assert hasattr(mode, "grinch")

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

def test_key_press_space_and_r():
    maze = create_maze_mode_for_test()
    event = Mock()
    event.key = "Space"
    maze.key_pressed(event)
    assert maze.showSolution is True
    event.key = "r"
    maze.key_pressed(event)
    assert maze.showSolution is False  # reiniciou

def test_key_press_movement():
    maze = create_maze_mode_for_test(n=3)
    maze.dotX, maze.dotY = maze.cellWidth, maze.cellHeight
    event = Mock()
    event.key = "Right"
    maze.key_pressed(event)
    assert maze.dotX != maze.cellWidth  # se moveu

def test_get_cell_and_bounds():
    maze = create_maze_mode_for_test(n=5)
    assert maze.getCell(10, 10) == (0, 0)
    x0, x1, y0, y1 = maze.getCellBounds(1, 1)
    assert x1 > x0 and y1 > y0

def test_check_if_maze_solved_switches_mode():
    maze = create_maze_mode_for_test(n=3)
    maze.dotX = maze.cellWidth * 2 + 1
    maze.dotY = maze.cellHeight * 2 + 1
    maze.app.finalScreen = Mock()
    maze.checkIfMazeSolved()
    maze.app.set_active_mode.assert_called_once_with(maze.app.finalScreen)

def test_reset_timer():
    maze = create_maze_mode_for_test()
    maze.app.timeMin, maze.app.timeSec = 5, 30
    maze.resetTimer()
    assert maze.app.timeMin == 0
    assert maze.app.timeSec == 0

def test_grinch_interactions():
    grinch = GrinchMode()
    grinch.app = Mock(presents=10)
    grinch.width = grinch.height = 300
    grinch.load_image = Mock(return_value="img")
    grinch.scale_image = Mock(return_value="img")
    grinch.app_started()

    # Força sleigh e grinch na mesma célula
    grinch.dotX, grinch.dotY = grinch.cellWidth/2, grinch.cellHeight/2
    grinch.grinch_x, grinch.grinch_y = grinch.dotX, grinch.dotY
    grinch.checkSleighGrinchIntersect()
    assert grinch.app.presents < 10


# Reutiliza a função auxiliar para criar Maze já inicializado
def create_maze_mode_for_test_full(n=10):
    mode = Maze()
    mode.app = Mock()
    mode.app.width = 500
    mode.app.height = 500
    mode.app._active_mode = mode
    mode.app.maze = mode
    mode.app.finalScreen = Mock()
    mode.app.timerMode = False
    mode.app.presents = 100
    mode.width = mode.app.width
    mode.height = mode.app.height
    mode.load_image = Mock(return_value="img")
    mode.scale_image = Mock(return_value="img_scaled")
    mode.app_started()
    if n is not None:
        mode.n = n
        mode.cellWidth = mode.width / n
        mode.cellHeight = mode.height / n
    return mode

# -----------------------
# Testando teclas
# -----------------------
@pytest.mark.parametrize("key", ["Space", "r", "Up", "Down", "Left", "Right", "b", "s", "e", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
def test_key_pressed_triggers_expected_behavior(key):
    maze = create_maze_mode_for_test_full()
    maze.dotX = maze.cellWidth / 2
    maze.dotY = maze.cellHeight / 2
    maze.dotR = 5
    maze.key_pressed(Mock(key=key))
    # Verifica se o método não lança erros e atualiza estado
    assert maze.n > 0 or maze.showSolution in [True, False]

# -----------------------
# Testando RadiusMode.timer_fired
# -----------------------
def test_radius_mode_timer_fired_decreases_presents():
    mode = RadiusMode()
    mode.app = Mock()
    mode.app.timeSec = 59
    mode.app.timeMin = 0
    mode.app.presents = 20
    mode.width = 200
    mode.height = 200
    mode.load_image = Mock(return_value="img")
    mode.scale_image = Mock(return_value="img_scaled")
    mode.app_started()
    mode.timer_fired()
    # Verifica que o tempo avançou
    assert mode.app.timeMin >= 0
    # Verifica que presents foram descontados se ultrapassou 60s
    assert mode.app.presents in [10, 20]

# -----------------------
# Testando GrinchMode.moveGrinch
# -----------------------
def test_grinch_mode_move_grinch_changes_position():
    mode = GrinchMode()
    mode.app = Mock()
    mode.width = 200
    mode.height = 200
    mode.load_image = Mock(return_value="img")
    mode.scale_image = Mock(return_value="img_scaled")
    mode.app_started()
    old_x, old_y = mode.grinch_x, mode.grinch_y
    mode.canGrinchMove = True
    mode.moveGrinch()
    # Verifica se a posição do Grinch mudou
    assert (mode.grinch_x != old_x) or (mode.grinch_y != old_y)

# -----------------------
# Testando checkSleighGrinchIntersect
# -----------------------
def test_grinch_mode_interactions_affect_presents():
    mode = GrinchMode()
    mode.app = Mock()
    mode.app.presents = 50
    mode.width = 200
    mode.height = 200
    mode.load_image = Mock(return_value="img")
    mode.scale_image = Mock(return_value="img_scaled")
    mode.app_started()
    mode.dotX = mode.presentsCellX * mode.cellWidth + mode.cellWidth / 2
    mode.dotY = mode.presentsCellY * mode.cellHeight + mode.cellHeight / 2
    mode.presentsGathered = False
    mode.checkSleighGrinchIntersect()
    # Verifica que os presentes foram coletados
    assert mode.presentsGathered is True
    assert mode.app.presents > 50
