import pytest
from unittest.mock import MagicMock, patch
import main

@pytest.fixture
def app():
    # Mock Tk para que nenhuma janela seja criada
    with patch("cmu_112_graphics.Tk", new=MagicMock()):
        # Mocka também o run() para não executar loop principal
        with patch.object(main.MyApp, "run", new=MagicMock()):
            app = main.MyApp(width=500, height=400, autorun=False)
            yield app

def test_app_initializes_with_expected_attributes(app):
    app._app_started_wrapper()
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

def test_app_starts_with_title_screen_active(app):
    app._app_started_wrapper()
    assert isinstance(app._active_mode, type(app.titleScreen))

def test_timer_fired_delegates_to_active_mode(app):
    app._app_started_wrapper()
    fake_mode = MagicMock()
    app._active_mode = fake_mode
    app.timer_fired()
    fake_mode.timer_fired.assert_called_once()
