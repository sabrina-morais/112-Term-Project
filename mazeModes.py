########################################
#   Ho Ho Home: the Santa Maze Game
#   (mazeModes.py)
#   By: Sarah Chen (sarahc2)
########################################
#   Maze Modes
########################################
#
#   Citations: 
#   1)  incorporated subclassing ModalApp and Mode idea from
#       https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
#
########################################
from mazeGenerationAndSolution import *
from cmu_112_graphics import *
import random

TITULO_FONTE = 'Baloo 40'

class Maze(Mode):
    def app_started(self):
        # maze display
        self.n = 10 # 38+ has MVC Violation
        self.mazeDict = generate_maze_dict(self.n)
        self.solution, self.connDict = get_maze_solution_connections(self.n, self.mazeDict, (0,0), (self.n-1,self.n-1))
        self.cellWidth = self.width / self.n
        self.cellHeight = self.height / self.n
        self.lineWidth = self.height / (self.n * 10)
        self.lineMargin = self.lineWidth * 2 / 5
        self.showSolution = False
        self.visibilityR = 17
        self.mazeFontSize = int(min(self.cellWidth, self.cellHeight) / 3)

        # presents and candycane
        self.presentsGathered = False
        self.presentsCellX = random.randrange(self.n)
        self.presentsCellY = random.randrange(self.n)
        self.presents = self.load_image('presents.png')
        self.presentsResized = self.scale_image(self.presents, self.cellWidth / 2000)
        self.candycaneCellX = random.randrange(self.n)
        self.candycaneCellY = random.randrange(self.n)
        self.candycane = self.load_image('candycane.png')
        self.candycaneResized = self.scale_image(self.candycane, self.cellWidth / 2000)

        # sleigh
        self.dotX = self.cellWidth + self.cellWidth / 2
        self.dotY = self.cellHeight / 2
        self.dotR = min(self.cellWidth, self.cellHeight) / 10
        self.dotStepSize = self.dotR / 2
        self.sleigh1 = self.load_image('sleigh1.png')
        self.sleigh1Resized = self.scale_image(self.sleigh1, self.cellWidth / 2000)
        self.sleigh2 = self.load_image('sleigh2.png')
        self.sleigh2Resized = self.scale_image(self.sleigh2, self.cellWidth / 2000)
        self.sleigh3 = self.load_image('sleigh3.png')
        self.sleigh3Resized = self.scale_image(self.sleigh3, self.cellWidth / 2000)

        # grinch
        self.grinch_x = self.width - self.cellWidth / 2
        self.grinch_y = self.cellHeight / 2
        self.grinchR = min(self.cellWidth, self.cellHeight) / 10
        self.grinch = self.load_image('grinch.png')
        self.grinchResized = self.scale_image(self.grinch, self.cellWidth / 2000)
        self.canGrinchMove = True

        # north pole and chimney
        self.northPole = self.load_image('northPole.png')
        self.northPoleResized = self.scale_image(self.northPole, self.cellWidth / 2500)
        self.chimney = self.load_image('chimney.png')
        self.chimneyResized = self.scale_image(self.chimney, self.cellWidth / 2000)
        
    def restartMaze(self):
        # maze display
        self.mazeDict = generate_maze_dict(self.n)
        self.solution, self.connDict = get_maze_solution_connections(self.n, self.mazeDict, (0,0), (self.n-1,self.n-1))
        self.cellWidth = self.width / self.n
        self.cellHeight = self.height / self.n
        self.lineWidth = self.height / (self.n * 10)
        self.lineMargin = self.lineWidth * 2 / 5
        self.showSolution = False
        self.visibilityR = 17
        self.mazeFontSize = int(min(self.cellWidth, self.cellHeight) / 3)
        self.app.timeMin = 0
        self.app.timeSec = 0
        if (self.app._active_mode == self.app.maze):
            self.app.presents = 0
        else:
            self.app.presents = 100

        # presents and candycane
        self.presentsGathered = False
        self.presentsCellX = random.randrange(self.n)
        self.presentsCellY = random.randrange(self.n)
        self.presentsResized = self.scale_image(self.presents, self.cellWidth / 2000)
        self.candycaneCellX = random.randrange(self.n)
        self.candycaneCellY = random.randrange(self.n)
        self.candycaneResized = self.scale_image(self.candycane, self.cellWidth / 2000)

        # sleigh
        self.dotX = self.cellWidth + self.cellWidth / 2
        self.dotY = self.cellHeight / 2
        self.dotR = min(self.cellWidth, self.cellHeight) / 10
        self.dotStepSize = self.dotR / 2
        self.sleigh1Resized = self.scale_image(self.sleigh1, self.cellWidth / 2000)
        self.sleigh2Resized = self.scale_image(self.sleigh2, self.cellWidth / 2000)
        self.sleigh3Resized = self.scale_image(self.sleigh3, self.cellWidth / 2000)

        # grinch
        self.grinch_x = self.width - self.cellWidth / 2
        self.grinch_y = self.cellHeight / 2
        self.grinchR = min(self.cellWidth, self.cellHeight) / 3
        self.grinchResized = self.scale_image(self.grinch, self.cellWidth / 2000)
        self.canGrinchMove = True

        # north pole and chimney
        self.northPoleResized = self.scale_image(self.northPole, self.cellWidth / 2500)
        self.chimneyResized = self.scale_image(self.chimney, self.cellWidth / 2000)

    def timer_fired(self):
        GrinchMode.checkSleighGrinchIntersect(self)

    def key_pressed(self, event):
        if (event.key == 'Space'):
            self.showSolution = not self.showSolution
        elif (event.key == 'r'):
            Maze.restartMaze(self)
        elif (event.key == 'Up'):
            possible_moves = Maze.getPossibleMoves(self)
            if (self.dotY > self.dotStepSize) and ('Up' in possible_moves):
                self.dotY -= self.dotStepSize
                Maze.checkIfMazeSolved(self)
        elif (event.key == 'Down'):
            possible_moves = Maze.getPossibleMoves(self)
            if ((self.dotY < self.height - self.dotStepSize) 
                and ('Down' in possible_moves)):
                self.dotY += self.dotStepSize
                Maze.checkIfMazeSolved(self)
        elif (event.key == 'Left'):
            possible_moves = Maze.getPossibleMoves(self)
            if (self.dotX > self.dotStepSize) and ('Left' in possible_moves):
                self.dotX -= self.dotStepSize
                Maze.checkIfMazeSolved(self)
        elif (event.key == 'Right'):
            possible_moves = Maze.getPossibleMoves(self)
            if ((self.dotX < self.width - self.dotStepSize) 
                and ('Right' in possible_moves)):
                self.dotX += self.dotStepSize
                Maze.checkIfMazeSolved(self)
        elif (event.key == 'b'):
            self.visibilityR += 3
        elif (event.key == 's'):
            if (self.visibilityR > 0):
                self.visibilityR -= 3
        elif (event.key == 'e'):
            Maze.resetTimer(self)
            self.app.finalPresents = self.app.presents
            Maze.restartMaze(self)
            self.app.set_active_mode(self.app.finalScreen)
        elif (event.key == '1'):
            self.n = 5
            Maze.restartMaze(self)
        elif (event.key == '2'):
            self.n = 10
            Maze.restartMaze(self)
        elif (event.key == '3'):
            self.n = 15
            Maze.restartMaze(self)
        elif (event.key == '4'):
            self.n = 20
            Maze.restartMaze(self)
        elif (event.key == '5'):
            self.n = 25
            Maze.restartMaze(self)
        elif (event.key == '6'):
            self.n = 30
            Maze.restartMaze(self)
        elif (event.key == '7'):
            self.n = 35
            Maze.restartMaze(self)
        elif (event.key == '8'):
            Maze.restartMaze(self)
            self.app.set_active_mode(self.app.maze)
        elif (event.key == '9'):
            Maze.restartMaze(self)
            self.app.timerMode = True
            self.app.set_active_mode(self.app.radiusMode)
        elif (event.key == '0'):
            Maze.restartMaze(self)
            self.app.timerMode = True
            self.app.set_active_mode(self.app.grinchMode)

    def checkIfMazeSolved(self):
        cell_x, cell_y = Maze.getCell(self, self.dotX, self.dotY)
        if ((cell_x, cell_y) == (self.n - 1, self.n - 1)):
            Maze.resetTimer(self)
            self.app.finalPresents = self.app.presents
            Maze.restartMaze(self)
            self.app.set_active_mode(self.app.finalScreen)

    def resetTimer(self):
        self.app.timerMode = False
        self.app.timeSec = 0
        self.app.timeMin = 0
    
    def getPossibleMoves(self):
        # center and radius of dot
        cx, cy, r = self.dotX, self.dotY, self.dotR
        
        # left, right, top, and bottom of dot
        dotx0, dotx1, doty0, doty1 = cx-r, cx+r, cy-r, cy+r
        mid_x = (dotx0 + dotx1) / 2
        mid_y = (doty0 + doty1) / 2

        # cell that center, top, bottom, left, and right of dot is in
        center_x, center_y = Maze.getCell(self, cx, cy)
        above_x, above_y = Maze.getCell(self, mid_x, doty0)
        cell_of_top = (above_x, above_y)
        below_x, below_y = Maze.getCell(self, mid_x, doty1)
        cell_of_bottom = (below_x, below_y)
        left_x, left_y = Maze.getCell(self, dotx0, mid_y)
        cell_of_left = (left_x, left_y)
        right_x, right_y = Maze.getCell(self, dotx1, mid_y)
        cell_of_right = (right_x, right_y)

        # bounds of cell that center of dot is in
        centerx0, centerx1, centery0, centery1 = Maze.getCellBounds(self, center_x, center_y)

        possible_moves = set()

        # check if dot can move within cell
        if (doty0 - self.dotStepSize > centery0 + (self.lineWidth * 2 / 3)):
            possible_moves.add('Up')
        if (doty1 + self.dotStepSize < centery1 - (self.lineWidth * 2 / 3)):
            possible_moves.add('Down')
        if (dotx0 - self.dotStepSize > centerx0 + (self.lineWidth * 2 / 3)):
            possible_moves.add('Left')
        if (dotx1 + self.dotStepSize < centerx1 - (self.lineWidth * 2 / 3)):
            possible_moves.add('Right')

        # cells above, below, left, and right of center cell
        cell_above = (center_x, center_y-1)
        cell_below = (center_x, center_y+1)
        cell_left = (center_x-1, center_y)
        cell_right = (center_x+1, center_y)

        # check if dot can move to next cell
        if ((cell_above in self.connDict[cell_of_left]) 
            and (cell_above in self.connDict[cell_of_right])):
            possible_moves.add('Up')
        if ((cell_below in self.connDict[cell_of_left]) 
            and (cell_below in self.connDict[cell_of_right])):
            possible_moves.add('Down')
        if ((cell_left in self.connDict[cell_of_top]) 
            and (cell_left in self.connDict[cell_of_bottom])):
            possible_moves.add('Left')
        if ((cell_right in self.connDict[cell_of_top]) 
            and (cell_right in self.connDict[cell_of_bottom])):
            possible_moves.add('Right')

        return possible_moves

    def getCell(self, cx, cy):
        cell_x = cx // self.cellWidth
        cell_y = cy // self.cellHeight
        return int(cell_x), int(cell_y)

    def getCellBounds(self, x, y):
        x0 = x * self.cellWidth
        x1 = x * self.cellWidth + self.cellWidth
        y0 = y * self.cellHeight
        y1 = y * self.cellHeight + self.cellHeight
        return x0, x1, y0, y1

    def drawAboveLine(self, canvas, point):
        x, y = point
        x1 = x * self.cellWidth - self.lineMargin
        x2 = x * self.cellWidth + self.cellWidth + self.lineMargin
        y1 = y * self.cellHeight
        canvas.create_line(x1, y1, x2, y1, width=self.lineWidth)

    def drawBelowLine(self, canvas, point):
        x, y = point
        x1 = x * self.cellWidth - self.lineMargin
        x2 = x * self.cellWidth + self.cellWidth + self.lineMargin
        y1 = y * self.cellHeight + self.cellHeight
        canvas.create_line(x1, y1, x2, y1, width=self.lineWidth)

    def drawLeftLine(self, canvas, point):
        x, y = point
        x1 = x * self.cellWidth
        y1 = y * self.cellHeight - self.lineMargin
        y2 = y * self.cellHeight + self.cellHeight + self.lineMargin
        canvas.create_line(x1, y1, x1, y2, width=self.lineWidth)

    def drawRightLine(self, canvas, point):
        x, y = point
        x1 = x * self.cellWidth + self.cellWidth
        y1 = y * self.cellHeight - self.lineMargin
        y2 = y * self.cellHeight + self.cellHeight + self.lineMargin
        canvas.create_line(x1, y1, x1, y2, width=self.lineWidth)

    def indicateSolution(self, canvas, point):
        x, y = point        
        cx = x * self.cellWidth + self.cellWidth / 2
        cy = y * self.cellHeight + self.cellHeight / 2
        r = min(self.cellWidth, self.cellHeight) / 10
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='black')

    def highlight(self, canvas, point):
        x, y = point
        x1 = x * self.cellWidth
        x2 = x * self.cellWidth + self.cellWidth
        y1 = y * self.cellHeight
        y2 = y * self.cellHeight + self.cellHeight
        canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='')

    def redraw_all(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill='aliceblue')

        if (self.showSolution == True):
            for point in self.solution:
                Maze.indicateSolution(self, canvas, point)

        for point in self.connDict:
            x, y = point
            above_point = (x, y-1)
            below_point = (x, y+1)
            left_point = (x-1, y)
            right_point = (x+1, y)
            if (above_point not in self.connDict[point]):
                Maze.drawAboveLine(self, canvas, point)
            if (below_point not in self.connDict[point]):
                Maze.drawBelowLine(self, canvas, point)
            if (left_point not in self.connDict[point]):
                Maze.drawLeftLine(self, canvas, point)
            if (right_point not in self.connDict[point]):
                Maze.drawRightLine(self, canvas, point)
        
        # presents
        if (self.presentsGathered == False):
            presents_x = self.presentsCellX * self.cellWidth + self.cellWidth / 2
            presents_y = self.presentsCellY * self.cellHeight + self.cellHeight / 2
            canvas.create_image(presents_x, presents_y, 
                        image=ImageTk.PhotoImage(self.presentsResized))

        # sleigh
        canvas.create_oval(self.dotX - self.dotR, self.dotY - self.dotR,
                        self.dotX + self.dotR, self.dotY + self.dotR, 
                        fill='white', outline='')
        canvas.create_image(self.dotX, self.dotY, 
                        image=ImageTk.PhotoImage(self.sleigh1Resized))

        # north pole, chimney
        canvas.create_image(self.cellWidth / 2, self.cellHeight / 2, 
                        image=ImageTk.PhotoImage(self.northPoleResized))
        canvas.create_image(self.width - self.cellWidth / 2, 
                        self.height - self.cellHeight / 2,
                        image=ImageTk.PhotoImage(self.chimneyResized))

class RadiusMode(Maze):
    def timer_fired(self):
        self.app.timeSec += 0.03
        if (self.app.timeSec >= 60):
            self.app.timeMin += 1
            if (self.app.presents >= 10):
                self.app.presents -= 10
        self.app.timeSec %= 60

    def redraw_all(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill='black')
        canvas.create_oval(self.dotX - self.dotR * self.visibilityR, 
                        self.dotY - self.dotR * self.visibilityR,
                        self.dotX + self.dotR * self.visibilityR, 
                        self.dotY + self.dotR * self.visibilityR, 
                        fill='aliceblue')

        if (self.showSolution == True):
            for point in self.solution:
                Maze.indicateSolution(self, canvas, point)

        for point in self.connDict:
            x, y = point
            above_point = (x, y-1)
            below_point = (x, y+1)
            left_point = (x-1, y)
            right_point = (x+1, y)
            if above_point not in self.connDict[point]:
                Maze.drawAboveLine(self, canvas, point)
            if below_point not in self.connDict[point]:
                Maze.drawBelowLine(self, canvas, point)
            if left_point not in self.connDict[point]:
                Maze.drawLeftLine(self, canvas, point)
            if right_point not in self.connDict[point]:
                Maze.drawRightLine(self, canvas, point)

        # sleigh
        canvas.create_oval(self.dotX - self.dotR, self.dotY - self.dotR,
                        self.dotX + self.dotR, self.dotY + self.dotR, 
                        fill='white', outline='')
        canvas.create_image(self.dotX, self.dotY, 
                        image=ImageTk.PhotoImage(self.sleigh2Resized))

        # time, presents label
        canvas.create_text(self.width - 20, 20, fill='green', 
                        text=f'Time: {self.app.timeMin}m {int(self.app.timeSec)}s',
                        anchor='ne',
                        font=TITULO_FONTE)
        canvas.create_text(self.width - 20, 60, fill='green', 
                        text=f'Presents: {self.app.presents}',
                        anchor='ne',
                        font=TITULO_FONTE)

        # north pole, chimney
        canvas.create_image(self.cellWidth / 2, self.cellHeight / 2, 
                        image=ImageTk.PhotoImage(self.northPoleResized))
        canvas.create_image(self.width - self.cellWidth / 2, 
                        self.height - self.cellHeight / 2,
                        image=ImageTk.PhotoImage(self.chimneyResized))

class GrinchMode(Maze):
    def timer_fired(self):
        self.app.timeSec += 0.03
        if (self.app.timeSec >= 60):
            self.app.timeMin += 1
            if (self.app.presents >= 10):
                self.app.presents -= 10
        self.app.timeSec %= 60
        
        GrinchMode.checkSleighGrinchIntersect(self)
        if (self.canGrinchMove == True):
            GrinchMode.moveGrinch(self)

    def checkSleighGrinchIntersect(self):
        sleigh_x, sleigh_y = Maze.getCell(self, self.dotX, self.dotY)
        grinch_x, grinch_y = Maze.getCell(self, self.grinch_x, self.grinch_y)
        # sleigh and grinch
        if ((sleigh_x, sleigh_y) == (grinch_x, grinch_y)) and (self.app.presents > 0):
            self.app.presents -= 0.1
        # sleigh and presents
        if ((sleigh_x, sleigh_y) == (self.presentsCellX, self.presentsCellY)
            and (self.presentsGathered == False)):
            self.app.presents += 10
            self.presentsGathered = True
        # grinch and candycane
        grinch_cell_x, grinch_cell_y = Maze.getCell(self, self.grinch_x, self.grinch_y)
        if ((grinch_cell_x, grinch_cell_y) == (self.candycaneCellX, self.candycaneCellY)):
            self.canGrinchMove = False

    def moveGrinch(self):
        sleigh_x, sleigh_y = Maze.getCell(self, self.dotX, self.dotY)
        grinch_cell_x, grinch_cell_y = Maze.getCell(self, self.grinch_x, self.grinch_y)
        _ , _ = Maze.getCell(self, self.grinch_x + self.grinchR, self.grinch_y + self.grinchR)
        _ , _ = Maze.getCell(self, self.grinch_x - self.grinchR, self.grinch_y - self.grinchR)
        grinch_sol, _ = get_maze_solution_connections(self.n, self.mazeDict, (grinch_cell_x, grinch_cell_y), (sleigh_x, sleigh_y))
        try:
            if (len(grinch_sol) >= 5) and (grinch_sol[0] == grinch_sol[3]):
                new_cell_x, new_cell_y = grinch_sol[4]
            else:
                new_cell_x, new_cell_y = grinch_sol[1]
        except IndexError:
            new_cell_x, new_cell_y = grinch_cell_x, grinch_cell_y

        # find coordinates of grinch_cell_x, grinch_cell_y, new_cell_x, new_cell_y
        grinch_cell_x_coord = grinch_cell_x * self.cellWidth + self.cellWidth / 2
        grinch_cell_y_coord = grinch_cell_y * self.cellHeight + self.cellHeight / 2
        new_cell_x_coord = new_cell_x * self.cellWidth + self.cellWidth / 2
        new_cell_y_coord = new_cell_y * self.cellHeight + self.cellHeight / 2

        # move grinch to center of cell or to center of next cell
        if (grinch_cell_x + 1 == new_cell_x):
            if (grinch_cell_x_coord-1 < self.grinch_x <= new_cell_x_coord+1):
                GrinchMode.moveGrinchTowardsPoint(self, new_cell_x_coord, new_cell_y_coord)
            else:
                GrinchMode.moveGrinchTowardsPoint(self, grinch_cell_x_coord, grinch_cell_y_coord)
        elif (grinch_cell_x - 1 == new_cell_x):
            if (new_cell_x_coord-1 <= self.grinch_x < grinch_cell_x_coord+1):
                GrinchMode.moveGrinchTowardsPoint(self, new_cell_x_coord, new_cell_y_coord)
            else:
                GrinchMode.moveGrinchTowardsPoint(self, grinch_cell_x_coord, grinch_cell_y_coord)
        elif (grinch_cell_y + 1 == new_cell_y):
            if (grinch_cell_y_coord-1 < self.grinch_y <= new_cell_y_coord+1):
                GrinchMode.moveGrinchTowardsPoint(self, new_cell_x_coord, new_cell_y_coord)
            else:
                GrinchMode.moveGrinchTowardsPoint(self, grinch_cell_x_coord, grinch_cell_y_coord)
        elif (grinch_cell_y - 1 == new_cell_y):
            if (new_cell_y_coord-1 <= self.grinch_y < grinch_cell_y_coord+1):
                GrinchMode.moveGrinchTowardsPoint(self, new_cell_x_coord, new_cell_y_coord)
            else:
                GrinchMode.moveGrinchTowardsPoint(self, grinch_cell_x_coord, grinch_cell_y_coord)
        
    def moveGrinchTowardsPoint(self, x, y):
        if (self.grinch_x > x):
            self.grinch_x -= 1
        elif (self.grinch_x < x):
            self.grinch_x += 1
        if (self.grinch_y > y):
            self.grinch_y -= 1
        elif (self.grinch_y < y):
            self.grinch_y += 1

    def redraw_all(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill='aliceblue')

        if (self.showSolution == True):
            for point in self.solution:
                Maze.indicateSolution(self, canvas, point)

        for point in self.connDict:
            x, y = point
            above_point = (x, y-1)
            below_point = (x, y+1)
            left_point = (x-1, y)
            right_point = (x+1, y)
            if above_point not in self.connDict[point]:
                Maze.drawAboveLine(self, canvas, point)
            if below_point not in self.connDict[point]:
                Maze.drawBelowLine(self, canvas, point)
            if left_point not in self.connDict[point]:
                Maze.drawLeftLine(self, canvas, point)
            if right_point not in self.connDict[point]:
                Maze.drawRightLine(self, canvas, point)
        
        # presents and candycane
        if (self.presentsGathered == False):
            presents_x = self.presentsCellX * self.cellWidth + self.cellWidth / 2
            presents_y = self.presentsCellY * self.cellHeight + self.cellHeight / 2
            canvas.create_image(presents_x, presents_y, 
                        image=ImageTk.PhotoImage(self.presentsResized))
        candycane_x = self.candycaneCellX * self.cellWidth + self.cellWidth / 2
        candycane_y = self.candycaneCellY * self.cellHeight + self.cellHeight / 2
        canvas.create_image(candycane_x, candycane_y, 
                        image=ImageTk.PhotoImage(self.candycaneResized))

        # sleigh
        canvas.create_oval(self.dotX - self.dotR, self.dotY - self.dotR,
                        self.dotX + self.dotR, self.dotY + self.dotR, 
                        fill='white', outline='')
        canvas.create_image(self.dotX, self.dotY, 
                        image=ImageTk.PhotoImage(self.sleigh3Resized))

        # grinch
        canvas.create_oval(self.grinch_x - self.grinchR, self.grinch_y - self.grinchR,
                        self.grinch_x + self.grinchR, self.grinch_y + self.grinchR,
                        fill='white', outline='')
        canvas.create_image(self.grinch_x, self.grinch_y, 
                        image=ImageTk.PhotoImage(self.grinchResized))

        # time, presents label
        canvas.create_text(self.width - 20, 20, fill='green', 
                        text=f'Time: {self.app.timeMin}m {int(self.app.timeSec)}s',
                        anchor='ne',
                        font=TITULO_FONTE)
        canvas.create_text(self.width - 20, 60, fill='green', 
                        text=f'Presents: {int(self.app.presents)}',
                        anchor='ne',
                        font=TITULO_FONTE)

        # north pole, chimney
        canvas.create_image(self.cellWidth / 2, self.cellHeight / 2, 
                        image=ImageTk.PhotoImage(self.northPoleResized))
        canvas.create_image(self.width - self.cellWidth / 2, 
                        self.height - self.cellHeight / 2,
                        image=ImageTk.PhotoImage(self.chimneyResized))