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
    def app_started(app):
        # from gameScreens
        app.titleScreen = TitleScreen()
        app.backgroundScreen = BackgroundScreen()
        app.instructionsScreen = InstructionsScreen()
        app.sleighScreen = SleighScreen()
        app.finalScreen = FinalScreen()

        # from mazeModes
        app.maze = Maze()
        app.radiusMode = RadiusMode()
        app.grinchMode = GrinchMode()
        app.presents = 100
        app.finalPresents = 100
        app.timeSec = 0
        app.timeMin = 0

        app.timerMode = True
        app.timerDelay = 10

        app.setActiveMode(app.titleScreen)

    def timer_fired(app):
        app._activeMode.timer_fired()

MyApp(width=1000, height=800)