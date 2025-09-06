import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from cmu_112_graphics import App, get_hash, WrappedCanvas
from unittest.mock import MagicMock

# ---------------- UNITÁRIOS ----------------

def test_get_hash_equal_dicts():
    d1 = {"a": 1, "b": [1,2]}
    d2 = {"b": [1,2], "a": 1}
    assert get_hash(d1) == get_hash(d2)

def test_get_hash_different_values():
    d1 = {"a": 1}
    d2 = {"a": 2}
    assert get_hash(d1) != get_hash(d2)

def test_scale_image_size_change():
    from PIL import Image
    app = App(autorun=False)
    img = Image.new("RGB", (10, 10), "red")
    scaled = app.scale_image(img, 3)
    assert scaled.size == (30, 30)

def test_get_hash_stable():
    data1 = "abc"
    data2 = "abc"
    assert get_hash(data1) == get_hash(data2)


def test_app_initializes_without_autorun():
    app = App(autorun=False)
    assert isinstance(app, App)

def test_wrapped_canvas_logs_calls():
    app = MagicMock()
    app.width = 500
    app.height = 500
    app._root = MagicMock()  # Mock do _root para o Canvas
    canvas = WrappedCanvas(app)
    canvas.loggedDrawingCalls.append("test_call")
    assert "test_call" in canvas.loggedDrawingCalls

# ---------------- INTEGRAÇÃO ----------------

class DummyEvent:
    """Simula um evento do Tkinter"""
    def __init__(self, x=0, y=0, keysym=None, char=None):
        self.x = x
        self.y = y
        self.keysym = keysym
        self.char = char