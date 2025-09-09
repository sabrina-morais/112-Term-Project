import pytest
from unittest.mock import MagicMock, patch
import main

@pytest.fixture
def app():
    # Mock Tk e _the_root antes da criação do app
    with patch("cmu_112_graphics.Tk", new=MagicMock()), \
         patch("cmu_112_graphics.App._the_root", new_callable=MagicMock):
        # Inicializa sem autorun
        app = main.MyApp(width=500, height=400, autorun=False)
        yield app

def test_app_initializes_with_expected_attributes():
    app = main.MyApp(width=500, height=400, autorun=False)
    app._app_started_wrapper()  # inicializa as telas e modos

    assert hasattr(app, "titleScreen")
    assert hasattr(app, "backgroundScreen")
    assert hasattr(app, "instructionsScreen")
    assert hasattr(app, "sleighScreen")
    assert hasattr(app, "finalScreen")

    assert hasattr(app, "maze")
    assert hasattr(app, "radiusMode")
    assert hasattr(app, "grinchMode")

    assert app.presents == 100
    assert app.finalPresents == 100
    assert app.timeSec == 0
    assert app.timeMin == 0
    assert app.timerMode is True
    assert app.timer_delay == 10
