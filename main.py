########################################
#   Ho Ho Home: the Santa Maze Game
#   (main.py)
#   By: Sarah Chen (sarahc2)
########################################
#   Combine gameScreens and mazeModes
########################################
#
#   Citations: 
#   1)  incorporated subclassing ModalApp and Mode idea from
#       https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
#
########################################
from gameScreens import *
from mazeModes import *

class MyApp(ModalApp):
    def app_started(self):
        # from gameScreens
        self.titleScreen = TitleScreen()
        self.backgroundScreen = BackgroundScreen()
        self.instructionsScreen = InstructionsScreen()
        self.sleighScreen = SleighScreen()
        self.finalScreen = FinalScreen()

        # from mazeModes
        self.maze = Maze()
        self.radiusMode = RadiusMode()
        self.grinchMode = GrinchMode()
        self.presents = 100
        self.finalPresents = 100
        self.timeSec = 0
        self.timeMin = 0

        self.timerMode = True
        self.timer_delay = 10

        self.set_active_mode(self.titleScreen)

    def timer_fired(self):
        self._active_mode.timer_fired()

MyApp(width=1000, height=800)