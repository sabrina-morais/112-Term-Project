import pytest
from unittest.mock import MagicMock, patch

import main


def test_app_initializes_with_expected_attributes():
    app = main.MyApp(width=500, height=400)

    # Verifica atributos vindos das telas
    assert hasattr(app, "titleScreen")
    assert hasattr(app, "backgroundScreen")
    assert hasattr(app, "instructionsScreen")
    assert hasattr(app, "sleighScreen")
    assert hasattr(app, "finalScreen")

    # Verifica atributos vindos dos modos de maze
    assert hasattr(app, "maze")
    assert hasattr(app, "radiusMode")
    assert hasattr(app, "grinchMode")

    # Verifica variáveis iniciais
    assert app.presents == 100
    assert app.finalPresents == 100
    assert app.timeSec == 0
    assert app.timeMin == 0
    assert app.timerMode is True
    assert app.timer_delay == 10


def test_app_starts_with_title_screen_active():
    app = main.MyApp(width=500, height=400)
    # O modo ativo deve ser a tela de título
    assert isinstance(app._active_mode, type(app.titleScreen))


def test_timer_fired_delegates_to_active_mode():
    app = main.MyApp(width=500, height=400)

    # Substitui o modo ativo por um mock
    fake_mode = MagicMock()
    app._active_mode = fake_mode

    app.timer_fired()

    fake_mode.timer_fired.assert_called_once()
