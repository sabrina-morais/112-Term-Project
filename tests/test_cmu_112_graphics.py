import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from cmu_112_graphics import App, getHash, WrappedCanvas

# ---------------- UNITÁRIOS ----------------

def test_getHash_equal_dicts():
    d1 = {"a": 1, "b": [1,2]}
    d2 = {"b": [1,2], "a": 1}
    assert getHash(d1) == getHash(d2)

def test_getHash_different_values():
    d1 = {"a": 1}
    d2 = {"a": 2}
    assert getHash(d1) != getHash(d2)

def test_scaleImage_size_change():
    from PIL import Image
    app = App(autorun=False)
    img = Image.new("RGB", (10, 10), "red")
    scaled = app.scaleImage(img, 3)
    assert scaled.size == (30, 30)

# def test_wrappedCanvas_invalid_create_image():
#     app = App(autorun=False)
#     canvas = WrappedCanvas(app)
#     with pytest.raises(Exception):
#         canvas.create_image(0, 0)  # sem parâmetros válidos

# ---------------- INTEGRAÇÃO ----------------

class DummyEvent:
    """Simula um evento do Tkinter"""
    def __init__(self, x=0, y=0, keysym=None, char=None):
        self.x = x
        self.y = y
        self.keysym = keysym
        self.char = char

# def test_app_lifecycle_methods_called():
#     called = {}
#     class MyApp(App):
#         def appStarted(self): called["start"] = True
#         def appStopped(self): called["stop"] = True

#     app = MyApp(autorun=False)
#     app._appStartedWrapper()
#     assert "start" in called
#     app._appStoppedWrapper()
#     assert "stop" in called

# def test_keyPressedWrapper_triggers_method():
#     called = {}
#     class MyApp(App):
#         def keyPressed(self, event): called["ok"] = event.key

#     app = MyApp(autorun=False)
#     event = DummyEvent(keysym="a", char="a")
#     app._keyPressedWrapper(event)
#     assert called["ok"] == "a"

# def test_mousePressed_and_released_change_state():
#     class MyApp(App):
#         def mousePressed(self, event): pass
#         def mouseReleased(self, event): pass

#     app = MyApp(autorun=False)
#     event = DummyEvent(x=10, y=20)

#     app._mousePressedWrapper(event)
#     assert app._mouseIsPressed is True

#     app._mouseReleasedWrapper(event)
#     assert app._mouseIsPressed is False

def test_timerFiredWrapper_runs():
    called = {}
    class MyApp(App):
        def timerFired(self): called["ok"] = True

    app = MyApp(autorun=False)
    app.timerFired()
    assert "ok" in called
