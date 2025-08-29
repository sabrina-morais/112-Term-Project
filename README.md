# 15-112 Term Project

Hello and welcome to Ho Ho Home: the Santa Maze Game!

This project was created by Sarah Chen for my CMU 15-112 Fall 2020 Term Project. It contains roughly 1400 lines of python code.

Game Description

Players will begin by being given the Christmas-themed background story and 
instructions. From there, players will choose a sled based on what features 
of the game they want to play with and then enter the sled’s respective mode. 
Though each mode has different features (e.g. compromised visibility or a 
pathfinding Grinch), the ultimate goal for each is still the same - solve the 
maze as quickly and accurately as possible. Players lose 10 presents every 
minute it takes them to solve the maze, and the final screen will display how 
many presents out of 100 they were able to deliver. A "telephone line" can be 
called where the solution path is revealed through a series of dots.

How to run
1) Make sure PIL/Pillow is installed. Refer to the following link if not:
    https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#installingModules
2) Download the code into one folder.
3) Make sure the following files are in the same folder.
    - main.py
    - gameScreens.py
    - mazeModes.py
    - mazeGeneration.py
    - cmu_112_graphics.py
4) Save the following images into the same folder as your Python code:
    - sleigh1.png
    - sleigh2.png
    - sleigh3.png
    - northPole.png
    - chimney.png
    - grinch.png
    - presents.png
    - candycane.png
    - title.png
    - background.png
5) Run the following file in an editor (e.g. VSCode):
    - main.py

Libraries Needed
- PIL/Pillow

Shortcuts
- When in any of the 3 Game Modes, pressing the '8', '9', and '0' key will take 
  the player directly to Sled 1, Sled 2, and Sled 3's modes.
- The 'Space' key will reveal the maze solution path.
- The 'r' key regenerates the maze and restarts the game mode.
- The 'e' key automatically ends the game.
