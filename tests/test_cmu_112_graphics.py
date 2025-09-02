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

# ---------------- INTEGRAÇÃO ----------------

class DummyEvent:
    """Simula um evento do Tkinter"""
    def __init__(self, x=0, y=0, keysym=None, char=None):
        self.x = x
        self.y = y
        self.keysym = keysym
        self.char = char


def test_timerFiredWrapper_runs():
    called = {}
    class MyApp(App):
        def timerFired(self): called["ok"] = True

    app = MyApp(autorun=False)
    app.timerFired()
    assert "ok" in called
