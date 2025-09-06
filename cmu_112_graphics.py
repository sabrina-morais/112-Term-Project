### taken from Carnegie Mellon University's 15-112 course website
### https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# cmu_112_graphics.py
# version 0.8.6

# Pre-release for CMU 15-112-f20

# Require Python 3.6 or later
import sys
if (sys.version_info[0] != 3) or (sys.version_info[1] < 6):
    raise RuntimeError('cmu_112_graphics.py requires Python version 3.6 or later.')

# Track version and file update timestamp
import datetime
MAJOR_VERSION = 0
MINOR_VERSION = 8.6 # version 0.8.6
LAST_UPDATED  = datetime.date(year=2020, month=2, day=24)

# Pending changes:
#   * Fix Windows-only bug: Position popup dialog box over app window (already works fine on Macs)
#   * Add documentation
#   * integrate sounds (probably from pyGame)
#   * Improved methodIsOverridden to TopLevelApp and ModalApp
#   * Save to animated gif and/or mp4 (with audio capture?)

# Deferred changes:
#   * replace/augment tkinter canvas with PIL/Pillow imageDraw (perhaps with our own fn names)
#   * use snake_case and CapWords

# Chages in v0.8.6
#   * f20

# Chages in v0.8.5
#   * Support load_image from Modes

# Chages in v0.8.3 + v0.8.4
#   * Use default empty Mode if none is provided
#   * Add KeyRelease event binding
#   * Drop user32.SetProcessDPIAware (caused window to be really tiny on some Windows machines)

# Changes in v0.8.1 + v0.8.2
#   * print version number and last-updated date on load
#   * restrict modifiers to just control key (was confusing with NumLock, etc)
#   * replace hasModifiers with 'control-' prefix, as in 'control-A'
#   * replace app._paused with app.paused, etc (use app._ for private variables)
#   * use improved ImageGrabber import for linux

# Changes in v0.8.0
#   * suppress more modifier keys (Super_L, Super_R, ...)
#   * raise exception on event.keysym or event.char + works with key = 'Enter'
#   * remove tryToInstall

# Changes in v0.7.4
#   * renamed drawAll back to redraw_all :-)

# Changes in v0.7.3
#   * Ignore mousepress-drag-release and defer configure events for drags in titlebar
#   * Extend deferredRedrawAll to 100ms with replace=True and do not draw while deferred
#     (together these hopefully fix Windows-only bug: file dialog makes window not moveable)
#   * changed size_changed to not take event (use app.width and app.height)

# Changes in v0.7.2
#   * Singleton App._the_root instance (hopefully fixes all those pesky Tkinter errors-on-exit)
#   * Use user32.SetProcessDPIAware to get resolution of screen grabs right on Windows-only (fine on Macs)
#   * Replaces showGraphics() with runApp(...), which is a veneer for App(...) [more intuitive for pre-OOP part of course]
#   * Fixes/updates images:
#       * disallows loading images in redraw_all (raises exception)
#       * eliminates cache from load_image
#       * eliminates app.getTkinterImage, so user now directly calls ImageTk.PhotoImage(image))
#       * also create_image allows magic pil_image=image instead of image=ImageTk.PhotoImage(app.image)

# Changes in v0.7.1
#   * Added keyboard shortcut:
#       * cmd/ctrl/alt-x: hard exit (uses os._exit() to exit shell without tkinter error messages)
#   * Fixed bug: shortcut keys stopped working after an MVC violation (or other exception)
#   * In app.save_snapshot(), add .png to path if missing
#   * Added: Print scripts to copy-paste into shell to install missing modules (more automated approaches proved too brittle)

# Changes in v0.7
#   * Added some image handling (requires PIL (retained) and pyscreenshot (later removed):
#       * app.load_image()       # loads PIL/Pillow image from file, with file dialog, or from URL (http or https)
#       * app.scale_image()      # scales a PIL/Pillow image
#       * app.getTkinterImage() # converts PIL/Pillow image to Tkinter PhotoImage for use in create_image(...)
#       * app.get_snapshot()     # get a snapshot of the canvas as a PIL/Pillow image
#       * app.save_snapshot()    # get and save a snapshot
#   * Added app._paused, app.togglePaused(), and paused highlighting (red outline around canvas when paused)
#   * Added keyboard shortcuts:
#       * cmd/ctrl/alt-s: save a snapshot
#       * cmd/ctrl/alt-p: pause/unpause
#       * cmd/ctrl/alt-q: quit

# Changes in v0.6:
#   * Added fn_prefix option to TopLevelApp (so multiple TopLevelApp's can be in one file)
#   * Added showGraphics(drawFn) (for graphics-only drawings before we introduce animations)

# Changes in v0.5:
#   * Added:
#       * app.winx and app.winy (and add winx,winy parameters to app.__init__, and sets these on configure events)
#       * app.set_size(width, height)
#       * app.set_position(x, y)
#       * app.quit()
#       * app.show_message(message)
#       * app.get_user_input(prompt)
#       * App.last_updated (instance of datetime.date)
#   * Show popup dialog box on all exceptions (not just for MVC violations)
#   * Draw (in canvas) "Exception!  App Stopped! (See console for details)" for any exception
#   * Replace callUserMethod() with more-general @_safe_method decorator (also handles exceptions outside user methods)
#   * Only include lines from user's code (and not our framework nor tkinter) in stack traces
#   * Require Python version (3.6 or greater)

# Changes in v0.4:
#   * Added __setattr__ to enforce Type 1A MVC Violations (setting app.x in redraw_all) with better stack trace
#   * Added app._deferred_redraw_all() (avoids resizing drawing/crashing bug on some platforms)
#   * Added deferredMethodCall() and app._after_id_map to generalize after_id handling
#   * Use (_ is None) instead of (_ == None)

# Changes in v0.3:
#   * Fixed "event not defined" bug in size_changed handlers.
#   * draw "MVC Violation" on Type 2 violation (calling draw methods outside redraw_all)

# Changes in v0.2:
#   * Handles another MVC violation (now detects drawing on canvas outside of redraw_all)
#   * App stops running when an exception occurs (in user code) (stops cascading errors)

# Changes in v0.1:
#   * OOPy + supports inheritance + supports multiple apps in one file + etc
#        * uses import instead of copy-paste-edit starter code + no "do not edit code below here!"
#        * no longer uses Struct (which was non-Pythonic and a confusing way to sort-of use OOP)
#   * Includes an early version of MVC violation handling (detects model changes in redraw_all)
#   * added events:
#       * app_started (no init-vs-__init__ confusion)
#       * app_stopped (for cleanup)
#       * key_released (well, sort of works) + mouse_released
#       * mouse_moved + mouse_dragged
#       * size_changed (when resizing window)
#   * improved key names (just use event.key instead of event.char and/or event.keysym + use names for 'Enter', 'Escape', ...)
#   * improved function names (renamed redraw_all to drawAll)
#   * improved (if not perfect) exiting without that irksome Tkinter error/bug
#   * app has a title in the titlebar (also shows window's dimensions)
#   * supports Modes and ModalApp (see ModalApp and Mode, and also see TestModalApp example)
#   * supports TopLevelApp (using top-level functions instead of subclasses and methods)
#   * supports version checking with App.major_version, App.minor_version, and App.version
#   * logs drawing calls to support autograding views (still must write that autograder, but this is a very helpful first step)

from tkinter import Tk, Canvas, Frame, Button, Label, Entry, ALL, BOTH, Event, YES
from tkinter import messagebox, simpledialog, filedialog
import inspect, copy, traceback
import sys, os
from io import BytesIO

def failed_import(import_name, install_name=None):
    install_name = install_name or import_name
    print('**********************************************************')
    print('** Cannot import ' + import_name + ' -- it seems you need to install ' + install_name)
    print('** This may result in limited functionality or even a runtime error.')
    print('**********************************************************')
    print()

try: from PIL import Image, ImageTk
except ModuleNotFoundError: failed_import('PIL', 'pillow')

if sys.platform.startswith('linux'):
    try: import pyscreenshot as ImageGrabber
    except ModuleNotFoundError: failed_import('pyscreenshot')
else:
    try: from PIL import ImageGrab as ImageGrabber
    except ModuleNotFoundError: pass # Our PIL warning is already printed above

try: import requests
except ModuleNotFoundError: failed_import('requests')

def get_hash(obj):
    # This is used to detect MVC violations in redraw_all
    # @TODO: Make this more robust and efficient
    try:
        return get_hash(obj.__dict__)
    except AttributeError:
        if isinstance(obj, list):
            return get_hash(tuple(get_hash(v) for v in obj))
        elif isinstance(obj, set):
            return get_hash(sorted(obj))
        elif isinstance(obj, dict):
            return get_hash(tuple(obj[key] for key in sorted(obj)))
        else:
            try:
                return hash(obj)
            except TypeError:
                return get_hash(repr(obj))

class WrappedCanvas(Canvas):
    # Enforces MVC: no drawing outside calls to redraw_all
    # Logs draw calls (for autograder) in canvas.loggedDrawingCalls
    def __init__(self, app):
        self.loggedDrawingCalls = [ ]
        self.log_drawing_calls = True
        self.inRedrawAll = False
        self.app = app
        super().__init__(app._root, width=app.width, height=app.height)

    def log(self, method_name, args, kwargs):
        if (not self.inRedrawAll):
            self.app._mvc_violation('you may not use the canvas (the view) outside of redraw_all')
        if (self.log_drawing_calls):
            self.loggedDrawingCalls.append((method_name, args, kwargs))

    def create_arc(self, *args, **kwargs): self.log('create_arc', args, kwargs); return super().create_arc(*args, **kwargs)
    def create_bitmap(self, *args, **kwargs): self.log('create_bitmap', args, kwargs); return super().create_bitmap(*args, **kwargs)
    def create_line(self, *args, **kwargs): self.log('create_line', args, kwargs); return super().create_line(*args, **kwargs)
    def create_oval(self, *args, **kwargs): self.log('create_oval', args, kwargs); return super().create_oval(*args, **kwargs)
    def create_polygon(self, *args, **kwargs): self.log('create_polygon', args, kwargs); return super().create_polygon(*args, **kwargs)
    def create_rectangle(self, *args, **kwargs): self.log('create_rectangle', args, kwargs); return super().create_rectangle(*args, **kwargs)
    def create_text(self, *args, **kwargs): self.log('create_text', args, kwargs); return super().create_text(*args, **kwargs)
    def create_window(self, *args, **kwargs): self.log('create_window', args, kwargs); return super().create_window(*args, **kwargs)

    def create_image(self, *args, **kwargs):
        self.log('create_image', args, kwargs)
        uses_image = 'image' in kwargs
        uses_pil_image = 'pil_image' in kwargs
        if ((not uses_image) and (not uses_pil_image)):
            raise ValueError('create_image requires an image to draw')
        elif (uses_image and uses_pil_image):
            raise ValueError('create_image cannot use both an image and a pil_image')
        elif (uses_pil_image):
            pil_image = kwargs['pil_image']
            del kwargs['pil_image']
            if (not isinstance(pil_image, Image.Image)):
                raise TypeError('create_image: pil_image value is not an instance of a PIL/Pillow image')
            image = ImageTk.PhotoImage(pil_image)
        else:
            image = kwargs['image']
            if (isinstance(image, Image.Image)):
                raise TypeError(
                    'create_image: image must not be an instance of a PIL/Pillow image\n'
                    'You perhaps meant to convert from PIL to Tkinter, like so:\n'
                    '     canvas.create_image(x, y, image=ImageTk.PhotoImage(image))'
                )
        kwargs['image'] = image
        return super().create_image(*args, **kwargs)

class App(object):
    major_version = MAJOR_VERSION
    minor_version = MINOR_VERSION
    version = f'{major_version}.{minor_version}'
    last_updated = LAST_UPDATED
    _the_root = None # singleton Tkinter root object

    ####################################
    # User Methods:
    ####################################
    def redraw_all(self, canvas): pass      # draw (view) the model in the canvas
    def app_started(self): pass           # initialize the model (app.xyz)
    def app_stopped(self): pass           # cleanup after app is done running
    def key_pressed(self, event): pass    # use event.key
    def key_released(self, event): pass   # use event.key
    def mouse_pressed(self, event): pass  # use event.x and event.y
    def mouse_released(self, event): pass # use event.x and event.y
    def mouse_moved(self, event): pass    # use event.x and event.y
    def mouse_dragged(self, event): pass  # use event.x and event.y
    def timer_fired(self): pass           # respond to timer events
    def size_changed(self): pass          # respond to window size changes

    ####################################
    # Implementation:
    ####################################

    def __init__(self, width=300, height=300, x=0, y=0, title=None, autorun=True, mvc_check=True, log_drawing_calls=True):
        self.winx, self.winy, self.width, self.height = x, y, width, height
        self.timer_delay = 100     # milliseconds
        self.mouse_moved_delay = 50 # ditto
        self._title = title
        self._mvc_check = mvc_check
        self._log_drawing_calls = log_drawing_calls
        self._running = self._paused = False
        self._mouse_pressed_outside_window = False
        if autorun: self.run()

    def set_size(self, width, height):
        self._root.geometry(f'{width}x{height}')

    def set_position(self, x, y):
        self._root.geometry(f'+{x}+{y}')

    def show_message(self, message):
        messagebox.showinfo('show_message', message, parent=self._root)

    def get_user_input(self, prompt):
        return simpledialog.askstring('get_user_input', prompt)

    def load_image(self, path=None):
        if (self._canvas.inRedrawAll):
            raise RuntimeError('Cannot call load_image in redraw_all')

        if (path is None):
            path = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title='Select file: ',
                filetypes=(('Image files','*.png *.gif *.jpg'),('all files','*.*'))
            )
            if (not path): 
                return None

        if (path.startswith('http')):
            response = requests.request('GET', path)  # path is a URL!
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(path)

        return image

    def scale_image(self, image, scale, antialias=False):
        # antialiasing is higher-quality but slower
        resample = Image.ANTIALIAS if antialias else Image.NEAREST
        return image.resize((round(image.width*scale), round(image.height*scale)), resample=resample)

    def get_snapshot(self):
        self._show_root_window()
        x0 = self._root.winfo_rootx() + self._canvas.winfo_x()
        y0 = self._root.winfo_rooty() + self._canvas.winfo_y()
        result = ImageGrabber.grab((x0,y0,x0+self.width,y0+self.height))
        return result

    def save_snapshot(self):
        path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Select file: ',filetypes = (('png files','*.png'),('all files','*.*')))
        if (path):
            # defer call to let filedialog close (and not grab those pixels)
            if (not path.endswith('.png')): path += '.png'
            self._deferred_method_call(after_id='save_snapshot', after_delay=0, after_fn=lambda:self.get_snapshot().save(path))

    def _toggle_paused(self):
        self._paused = not self._paused

    def quit(self):
        self._running = False
        self._root.quit() # break out of root.mainloop() without closing window!

    def __setattr__(self, attr, val):
        d = self.__dict__
        d[attr] = val
        canvas = d.get('_canvas', None)
        if (d.get('running', False) and
            d.get('mvc_check', False) and
            (canvas is not None) and
            canvas.inRedrawAll):
            self._mvc_violation(f'you may not change app.{attr} in the model while in redraw_all (the view)')

    def _print_user_traceback(self, exception, tb):
        stack = traceback.extract_tb(tb)
        lines = traceback.format_list(stack)
        in_redraw_all_wrapper = False
        print_lines = [ ]
        for line in lines:
            if (('"cmu_112_graphics.py"' not in line) and
                ('/cmu_112_graphics.py' not in line) and
                ('\\cmu_112_graphics.py' not in line) and
                ('/tkinter/' not in line) and
                ('\\tkinter\\' not in line)):
                print_lines.append(line)
            if ('redrawAllWrapper' in line):
                in_redraw_all_wrapper = True
        if (len(print_lines) == 0):
            # No user code in trace, so we have to use all the code (bummer),
            # but not if we are in a redrawAllWrapper...
            if in_redraw_all_wrapper:
                print_lines = ['    No traceback available. Error occurred in redraw_all.\n']
            else:
                print_lines = lines
        print('Traceback (most recent call last):')
        for line in print_lines: print(line, end='')
        print(f'Exception: {exception}')

    def _safe_method(app_method):
        def m(*args, **kwargs):
            app = args[0]
            try:
                return app_method(*args, **kwargs)
            except Exception as e:
                app._running = False
                app._print_user_traceback(e, sys.exc_info()[2])
                if ('_canvas' in app.__dict__):
                    app._canvas.inRedrawAll = True  # not really, but stops recursive MVC Violations!
                    app._canvas.create_rectangle(0, 0, app.width, app.height, fill=None, width=10, outline='red')
                    app._canvas.create_rectangle(10, app.height-50, app.width-10, app.height-10,
                                                fill='white', outline='red', width=4)
                    app._canvas.create_text(app.width/2, app.height-40, 
                                            text='Exception! App Stopped!', fill='red', font='Arial 12 bold')
                    app._canvas.create_text(app.width/2, app.height-20, 
                                            text='See console for details', fill='red', font='Arial 12 bold')
                    app._canvas.update()
                app.show_message('Exception: {}\nClick ok then see console for details.'.format(e))
        return m

    def _method_is_overridden(self, method_name):
        return (getattr(type(self), method_name) is not getattr(App, method_name))

    def _mvc_violation(self, err_msg):
        self._running = False
        raise RuntimeError('MVC Violation: ' + err_msg)

    @_safe_method
    def _redraw_all_wrapper(self):
        if (not self._running): return
        if ('deferredRedrawAll' in self._after_id_map): return # wait for pending call
        self._canvas.inRedrawAll = True
        self._canvas.delete(ALL)
        width,outline = (10,'red') if self._paused else (0,'white')
        self._canvas.create_rectangle(0, 0, self.width, self.height, fill='white', width=width, outline=outline)
        self._canvas.loggedDrawingCalls = [ ]
        self._canvas.log_drawing_calls = self._log_drawing_calls
        hash1 = get_hash(self) if self._mvc_check else None
        try:
            self.redraw_all(self._canvas)
            hash2 = get_hash(self) if self._mvc_check else None
            if (hash1 != hash2):
                self._mvc_violation('you may not change the app state (the model) in redraw_all (the view)')
        finally:
            self._canvas.inRedrawAll = False
        self._canvas.update()

    def _deferred_method_call(self, after_id, after_delay, after_fn, replace=False):
        current_id = self._after_id_map.get(after_id, None)  # renomeado de 'id'

        def after_fn_wrapper(after_fn=after_fn, after_id=after_id):
            self._after_id_map.pop(after_id, None)
            after_fn()

        if (current_id is None) or replace:
            if current_id:
                self._root.after_cancel(current_id)
            self._after_id_map[after_id] = self._root.after(after_delay, after_fn_wrapper)


    def _deferred_redraw_all(self):
        self._deferred_method_call(after_id='deferredRedrawAll', after_delay=100, after_fn=self._redraw_all_wrapper, replace=True)

    @_safe_method
    def _app_started_wrapper(self):
        self.app_started()
        self._redraw_all_wrapper()

    _key_name_map = { '\t':'Tab', '\n':'Enter', '\r':'Enter', '\b':'Backspace',
                   chr(127):'Delete', chr(27):'Escape', ' ':'Space' }

    @staticmethod
    def _use_event_key(attr):
        raise AttributeError(f'Use event.key instead of event.{attr}')

    @staticmethod
    def _get_event_key_info(event, keysym, char):
        key = c = char
        has_control_key = (event.state & 0x4 != 0)
        if ((c in [None, '']) or (len(c) > 1) or (ord(c) > 255)):
            key = keysym
            if (key.endswith('_L') or
                key.endswith('_R') or
                key.endswith('_Lock')):
                key = 'Modifier_Key'
        elif (c in App._key_name_map):
            key = App._key_name_map[c]
        elif ((len(c) == 1) and (1 <= ord(c) <= 26)):
            key = chr(ord('a')-1 + ord(c))
            has_control_key = True
        if has_control_key and (len(key) == 1):
            # don't add control- prefix to Enter, Tab, Escape, ...
            key = 'control-' + key
        return key

    class KeyEventWrapper(Event):
        def __init__(self, event):
            keysym, char = event.keysym, event.char
            del event.keysym
            del event.char
            for key in event.__dict__:
                if (not key.startswith('__')):
                    self.__dict__[key] = event.__dict__[key]
            self.key = App._get_event_key_info(event, keysym, char)
        keysym = property(lambda *args: App._use_event_key('keysym'),
                          lambda *args: App._use_event_key('keysym'))
        char =   property(lambda *args: App._use_event_key('char'),
                          lambda *args: App._use_event_key('char'))

    @_safe_method
    def _key_pressed_wrapper(self, event):
        event = App.KeyEventWrapper(event)
        if (event.key == 'control-s'):
            self.save_snapshot()
        elif (event.key == 'control-p'):
            self._toggle_paused()
            self._redraw_all_wrapper()
        elif (event.key == 'control-q'):
            self.quit()
        elif (event.key == 'control-x'):
            os._exit(0) # hard exit avoids tkinter error messages
        elif (self._running and
            (not self._paused) and
            self._method_is_overridden('key_pressed') and
            event.key != 'Modifier_Key'):

            self.key_pressed(event)
            self._redraw_all_wrapper()

    @_safe_method
    def _key_released_wrapper(self, event):
        if (not self._running) or self._paused or (not self._method_is_overridden('key_released')):
            return
        event = App.KeyEventWrapper(event)
        if event.key != 'Modifier_Key':
            self.key_released(event)
            self._redraw_all_wrapper()

    @_safe_method
    def _mouse_pressed_wrapper(self, event):
        if (not self._running) or self._paused: return
        if ((event.x < 0) or (event.x > self.width) or
            (event.y < 0) or (event.y > self.height)):
            self._mouse_pressed_outside_window = True
        else:
            self._mouse_pressed_outside_window = False
            self._mouse_is_pressed = True
            self._last_mouse_posn = (event.x, event.y)
            if (self._method_is_overridden('mouse_pressed')):
                self.mouse_pressed(event)
                self._redraw_all_wrapper()

    @_safe_method
    def _mouse_released_wrapper(self, event):
        if (not self._running) or self._paused: return
        self._mouse_is_pressed = False
        if self._mouse_pressed_outside_window:
            self._mouse_pressed_outside_window = False
            self._size_changed_wrapper()
        else:
            self._last_mouse_posn = (event.x, event.y)
            if (self._method_is_overridden('mouse_released')):
                self.mouse_released(event)
                self._redraw_all_wrapper()

    @_safe_method
    def _timer_fired_wrapper(self):
        if (not self._running) or (not self._method_is_overridden('timer_fired')): return
        if (not self._paused):
            self.timer_fired()
            self._redraw_all_wrapper()
        self._deferred_method_call(after_id='_timer_fired_wrapper', after_delay=self.timer_delay, after_fn=self._timer_fired_wrapper)

    @_safe_method
    def _size_changed_wrapper(self, event=None):
        if (not self._running): return
        if (event and ((event.width < 2) or (event.height < 2))): return
        if (self._mouse_pressed_outside_window): return
        self.width,self.height,self.winx,self.winy = [int(v) for v in self._root.winfo_geometry().replace('x','+').split('+')]
        if (self._last_window_dims is None):
            self._last_window_dims = (self.width, self.height, self.winx, self.winy)
        else:
            new_dims =(self.width, self.height, self.winx, self.winy)
            if (self._last_window_dims != new_dims):
                self._last_window_dims = new_dims
                self.update_title()
                self.size_changed()
                self._deferred_redraw_all() # avoid resize crashing on some platforms

    @_safe_method
    def _mouse_motion_wrapper(self):
        if (not self._running): return
        mouse_moved_exists = self._method_is_overridden('mouse_moved')
        mouse_dragged_exists = self._method_is_overridden('mouse_dragged')
        if ((not self._paused) and
            (not self._mouse_pressed_outside_window) and
            (((not self._mouse_is_pressed) and mouse_moved_exists) or
             (self._mouse_is_pressed and mouse_dragged_exists))):
            class MouseMotionEvent(object): pass
            event = MouseMotionEvent()
            root = self._root
            event.x = root.winfo_pointerx() - root.winfo_rootx()
            event.y = root.winfo_pointery() - root.winfo_rooty()
            if ((self._last_mouse_posn !=  (event.x, event.y)) and
                (event.x >= 0) and (event.x <= self.width) and
                (event.y >= 0) and (event.y <= self.height)):
                if (self._mouse_is_pressed): self.mouse_dragged(event)
                else: self.mouse_moved(event)
                self._last_mouse_posn = (event.x, event.y)
                self._redraw_all_wrapper()
        if (mouse_moved_exists or mouse_dragged_exists):
            self._deferred_method_call(after_id='mouseMotionWrapper', after_delay=self.mouse_moved_delay, after_fn=self._mouse_motion_wrapper)

    def update_title(self):
        self._title = self._title or type(self).__name__
        self._root.title(f'{self._title} ({self.width} x {self.height})')

    def get_quit_message(self):
        app_label = type(self).__name__
        if (self._title != app_label):
            if (self._title.startswith(app_label)):
                app_label = self._title
            else:
                app_label += f" '{self._title}'"
        return f"*** Closing {app_label}.  Bye! ***\n"

    def _show_root_window(self):
        root = self._root
        root.update(); root.deiconify(); root.lift(); root.focus()

    def _hide_root_window(self):
        root = self._root
        root.withdraw()

    @_safe_method
    def run(self):
        self._mouse_is_pressed = False
        self._last_mouse_posn = (-1, -1)
        self._last_window_dims= None # set in sizeChangedWrapper
        self._after_id_map = {}
        # create the singleton root window
        if (App._the_root is None):
            App._the_root = Tk()
            App._the_root.createcommand('exit', lambda: '') # when user enters cmd-q, ignore here (handled in key_pressed)
            App._the_root.protocol('WM_DELETE_WINDOW', lambda: App._the_root.app.quit()) # when user presses 'x' in title bar
            App._the_root.bind("<Button-1>", lambda event: App._the_root.app._mouse_pressed_wrapper(event))
            App._the_root.bind("<B1-ButtonRelease>", lambda event: App._the_root.app._mouse_released_wrapper(event))
            App._the_root.bind("<KeyPress>", lambda event: App._the_root.app._key_pressed_wrapper(event))
            App._the_root.bind("<KeyRelease>", lambda event: App._the_root.app._key_released_wrapper(event))
            App._the_root.bind("<Configure>", lambda event: App._the_root.app._size_changed_wrapper(event))
        else:
            App._the_root.canvas.destroy()
        self._root = root = App._the_root # singleton root!
        root.app = self
        root.geometry(f'{self.width}x{self.height}+{self.winx}+{self.winy}')
        self.update_title()
        # create the canvas
        root.canvas = self._canvas = WrappedCanvas(self)
        self._canvas.pack(fill=BOTH, expand=YES)
        # initialize, start the timer, and launch the app
        self._running = True
        self._paused = False
        self._app_started_wrapper()
        self._timer_fired_wrapper()
        self._mouse_motion_wrapper()
        self._show_root_window()
        root.mainloop()
        self._hide_root_window()
        self._running = False
        for after_id in self._after_id_map: self._root.after_cancel(self._after_id_map[after_id])
        self._after_id_map.clear() # for safety
        self.app_stopped()
        print(self.get_quit_message())

####################################
# TopLevelApp:
# (with top-level functions not subclassses and methods)
####################################

class TopLevelApp(App):
    _apps = {} # maps fn_prefix to app

    def __init__(self, fn_prefix='', **kwargs):
        if (fn_prefix in TopLevelApp._apps):
            print(f'Quitting previous version of {fn_prefix} TopLevelApp.')
            TopLevelApp._apps[fn_prefix].quit()
        if ((fn_prefix != '') and ('title' not in kwargs)):
            kwargs['title'] = f"TopLevelApp '{fn_prefix}'"
        TopLevelApp._apps[fn_prefix] = self
        self._fnPrefix = fn_prefix
        self._callersGlobals = inspect.stack()[1][0].f_globals
        super().__init__(**kwargs)

    def _callFn(self, fn, *args):
        fn = self._fnPrefix + fn
        if (fn in self._callersGlobals): self._callersGlobals[fn](*args)

    def redraw_all(self, canvas): self._callFn('redraw_all', self, canvas)
    def app_started(self): self._callFn('app_started', self)
    def app_stopped(self): self._callFn('app_stopped', self)
    def key_pressed(self, event): self._callFn('key_pressed', self, event)
    def key_released(self, event): self._callFn('key_released', self, event)
    def mouse_pressed(self, event): self._callFn('mouse_pressed', self, event)
    def mouse_released(self, event): self._callFn('mouse_released', self, event)
    def mouse_moved(self, event): self._callFn('mouse_moved', self, event)
    def mouse_dragged(self, event): self._callFn('mouse_dragged', self, event)
    def timer_fired(self): self._callFn('timer_fired', self)
    def size_changed(self): self._callFn('size_changed', self)

####################################
# ModalApp + Mode:
####################################

class ModalApp(App):
    def __init__(self, active_mode=None, **kwargs):
        self._running = False
        self._active_mode = None
        self.set_active_mode(active_mode)
        super().__init__(**kwargs)

    def set_active_mode(self, mode):
        if (mode is None): mode = Mode()  # default empty mode
        if (not isinstance(mode, Mode)):
            raise TypeError('active_mode must be a Mode instance!')
        if (mode.app not in [None, self]):
            raise ValueError('Modes cannot be added to two different apps!')

        if (self._active_mode != mode):
            mode.app = self
            if (self._active_mode is not None):
                self._active_mode.modeDeactivated()
            self._active_mode = mode
            if (self._running):
                self.start_active_mode()

    def start_active_mode(self):
        self._active_mode.width, self._active_mode.height = self.width, self.height
        if (not self._active_mode._appStartedCalled):
            self._active_mode.app_started() # called once per mode
            self._active_mode._appStartedCalled = True
        self._active_mode.modeActivated()  # called each time a mode is activated
        self._redraw_all_wrapper()

    def redraw_all(self, canvas):
        if (self._active_mode != None): self._active_mode.redraw_all(canvas)
    def app_started(self):
        if (self._active_mode != None): self.start_active_mode()
    def app_stopped(self):
        if (self._active_mode != None): self._active_mode.modeDeactivated()
    def key_pressed(self, event):
        if (self._active_mode != None): self._active_mode.key_pressed(event)
    def key_released(self, event):
        if (self._active_mode != None): self._active_mode.key_released(event)
    def mouse_pressed(self, event):
        if (self._active_mode != None): self._active_mode.mouse_pressed(event)
    def mouse_released(self, event):
        if (self._active_mode != None): self._active_mode.mouse_released(event)
    def mouse_moved(self, event):
        if (self._active_mode != None): self._active_mode.mouse_moved(event)
    def mouse_dragged(self, event):
        if (self._active_mode != None): self._active_mode.mouse_dragged(event)
    def timer_fired(self):
        if (self._active_mode != None): self._active_mode.timer_fired()
    def size_changed(self):
        if (self._active_mode != None):
            self._active_mode.width, self._active_mode.height = self.width, self.height
            self._active_mode.size_changed()

class Mode(App):
    def __init__(self, **kwargs):
        self.app = None
        self._appStartedCalled = False
        super().__init__(autorun=False, **kwargs)

    def modeActivated(self):
        # Este método é chamado quando o modo é ativado.
        # Mantido vazio para ser sobrescrito por subclasses.
        pass

    def modeDeactivated(self):
        # Este método é chamado quando o modo é desativado.
        # Mantido vazio para ser sobrescrito por subclasses.
        pass
    def load_image(self, path=None): return self.app.load_image(path)

####################################
# runApp()
####################################

runApp = TopLevelApp

print(f'Loaded cmu_112_graphics version {App.version} (last updated {App.last_updated})')

#Roda testes automatizado
if __name__ == '__main__':
    import subprocess
    import sys

    try:
        # Executa pytest em todos os arquivos da pasta tests/
        # -v : verbose, mostra detalhes de cada teste
        # --cov=. : gera relatório de cobertura de todo o projeto
        # --cov-report=term-missing : mostra no terminal quais linhas não foram testadas
        subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--cov=.", "--cov-report=term-missing", "tests/"],
            check=True
        )
    except FileNotFoundError:
        print("pytest não encontrado. Instale com 'pip install pytest pytest-cov' para rodar os testes.")
    except subprocess.CalledProcessError as e:
        print(f"Alguns testes falharam (código de saída {e.returncode}).")

