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

class Maze(Mode):
    def appStarted(mode):
        # maze display
        mode.n = 10 # 38+ has MVC Violation
        mode.mazeDict = generateMazeDict(mode.n)
        mode.solution, mode.connDict = getMazeSolutionConnections(mode.n, mode.mazeDict, (0,0), (mode.n-1,mode.n-1))
        mode.cellWidth = mode.width / mode.n
        mode.cellHeight = mode.height / mode.n
        mode.lineWidth = mode.height / (mode.n * 10)
        mode.lineMargin = mode.lineWidth * 2 / 5
        mode.showSolution = False
        mode.visibilityR = 17
        mode.mazeFontSize = int(min(mode.cellWidth, mode.cellHeight) / 3)

        # presents and candycane
        mode.presentsGathered = False
        mode.presentsCellX = random.randrange(mode.n)
        mode.presentsCellY = random.randrange(mode.n)
        mode.presents = mode.loadImage('presents.png')
        mode.presentsResized = mode.scaleImage(mode.presents, mode.cellWidth / 2000)
        mode.candycaneCellX = random.randrange(mode.n)
        mode.candycaneCellY = random.randrange(mode.n)
        mode.candycane = mode.loadImage('candycane.png')
        mode.candycaneResized = mode.scaleImage(mode.candycane, mode.cellWidth / 2000)

        # sleigh
        mode.dotX = mode.cellWidth + mode.cellWidth / 2
        mode.dotY = mode.cellHeight / 2
        mode.dotR = min(mode.cellWidth, mode.cellHeight) / 10
        mode.dotStepSize = mode.dotR / 2
        mode.sleigh1 = mode.loadImage('sleigh1.png')
        mode.sleigh1Resized = mode.scaleImage(mode.sleigh1, mode.cellWidth / 2000)
        mode.sleigh2 = mode.loadImage('sleigh2.png')
        mode.sleigh2Resized = mode.scaleImage(mode.sleigh2, mode.cellWidth / 2000)
        mode.sleigh3 = mode.loadImage('sleigh3.png')
        mode.sleigh3Resized = mode.scaleImage(mode.sleigh3, mode.cellWidth / 2000)

        # grinch
        mode.grinchX = mode.width - mode.cellWidth / 2
        mode.grinchY = mode.cellHeight / 2
        mode.grinchR = min(mode.cellWidth, mode.cellHeight) / 10
        mode.grinch = mode.loadImage('grinch.png')
        mode.grinchResized = mode.scaleImage(mode.grinch, mode.cellWidth / 2000)
        mode.canGrinchMove = True

        # north pole and chimney
        mode.northPole = mode.loadImage('northPole.png')
        mode.northPoleResized = mode.scaleImage(mode.northPole, mode.cellWidth / 2500)
        mode.chimney = mode.loadImage('chimney.png')
        mode.chimneyResized = mode.scaleImage(mode.chimney, mode.cellWidth / 2000)
        
    def restartMaze(mode):
        # maze display
        mode.mazeDict = generateMazeDict(mode.n)
        mode.solution, mode.connDict = getMazeSolutionConnections(mode.n, mode.mazeDict, (0,0), (mode.n-1,mode.n-1))
        mode.cellWidth = mode.width / mode.n
        mode.cellHeight = mode.height / mode.n
        mode.lineWidth = mode.height / (mode.n * 10)
        mode.lineMargin = mode.lineWidth * 2 / 5
        mode.showSolution = False
        mode.visibilityR = 17
        mode.mazeFontSize = int(min(mode.cellWidth, mode.cellHeight) / 3)
        mode.app.timeMin = 0
        mode.app.timeSec = 0
        if (mode.app._activeMode == mode.app.maze):
            mode.app.presents = 0
        else:
            mode.app.presents = 100

        # presents and candycane
        mode.presentsGathered = False
        mode.presentsCellX = random.randrange(mode.n)
        mode.presentsCellY = random.randrange(mode.n)
        mode.presentsResized = mode.scaleImage(mode.presents, mode.cellWidth / 2000)
        mode.candycaneCellX = random.randrange(mode.n)
        mode.candycaneCellY = random.randrange(mode.n)
        mode.candycaneResized = mode.scaleImage(mode.candycane, mode.cellWidth / 2000)

        # sleigh
        mode.dotX = mode.cellWidth + mode.cellWidth / 2
        mode.dotY = mode.cellHeight / 2
        mode.dotR = min(mode.cellWidth, mode.cellHeight) / 10
        mode.dotStepSize = mode.dotR / 2
        mode.sleigh1Resized = mode.scaleImage(mode.sleigh1, mode.cellWidth / 2000)
        mode.sleigh2Resized = mode.scaleImage(mode.sleigh2, mode.cellWidth / 2000)
        mode.sleigh3Resized = mode.scaleImage(mode.sleigh3, mode.cellWidth / 2000)

        # grinch
        mode.grinchX = mode.width - mode.cellWidth / 2
        mode.grinchY = mode.cellHeight / 2
        mode.grinchR = min(mode.cellWidth, mode.cellHeight) / 3
        mode.grinchResized = mode.scaleImage(mode.grinch, mode.cellWidth / 2000)
        mode.canGrinchMove = True

        # north pole and chimney
        mode.northPoleResized = mode.scaleImage(mode.northPole, mode.cellWidth / 2500)
        mode.chimneyResized = mode.scaleImage(mode.chimney, mode.cellWidth / 2000)

    def timerFired(mode):
        GrinchMode.checkSleighGrinchIntersect(mode)

    def keyPressed(mode, event):
        if (event.key == 'Space'):
            mode.showSolution = not mode.showSolution
        elif (event.key == 'r'):
            Maze.restartMaze(mode)
        elif (event.key == 'Up'):
            possibleMoves = Maze.getPossibleMoves(mode)
            if (mode.dotY > mode.dotStepSize) and ('Up' in possibleMoves):
                mode.dotY -= mode.dotStepSize
                Maze.checkIfMazeSolved(mode)
        elif (event.key == 'Down'):
            possibleMoves = Maze.getPossibleMoves(mode)
            if ((mode.dotY < mode.height - mode.dotStepSize) 
                and ('Down' in possibleMoves)):
                mode.dotY += mode.dotStepSize
                Maze.checkIfMazeSolved(mode)
        elif (event.key == 'Left'):
            possibleMoves = Maze.getPossibleMoves(mode)
            if (mode.dotX > mode.dotStepSize) and ('Left' in possibleMoves):
                mode.dotX -= mode.dotStepSize
                Maze.checkIfMazeSolved(mode)
        elif (event.key == 'Right'):
            possibleMoves = Maze.getPossibleMoves(mode)
            if ((mode.dotX < mode.width - mode.dotStepSize) 
                and ('Right' in possibleMoves)):
                mode.dotX += mode.dotStepSize
                Maze.checkIfMazeSolved(mode)
        elif (event.key == 'b'):
            mode.visibilityR += 3
        elif (event.key == 's'):
            if (mode.visibilityR > 0):
                mode.visibilityR -= 3
        elif (event.key == 'e'):
            Maze.resetTimer(mode)
            mode.app.finalPresents = mode.app.presents
            Maze.restartMaze(mode)
            mode.app.setActiveMode(mode.app.finalScreen)
        elif (event.key == '1'):
            mode.n = 5
            Maze.restartMaze(mode)
        elif (event.key == '2'):
            mode.n = 10
            Maze.restartMaze(mode)
        elif (event.key == '3'):
            mode.n = 15
            Maze.restartMaze(mode)
        elif (event.key == '4'):
            mode.n = 20
            Maze.restartMaze(mode)
        elif (event.key == '5'):
            mode.n = 25
            Maze.restartMaze(mode)
        elif (event.key == '6'):
            mode.n = 30
            Maze.restartMaze(mode)
        elif (event.key == '7'):
            mode.n = 35
            Maze.restartMaze(mode)
        elif (event.key == '8'):
            Maze.restartMaze(mode)
            mode.app.setActiveMode(mode.app.maze)
        elif (event.key == '9'):
            Maze.restartMaze(mode)
            mode.app.timerMode = True
            mode.app.setActiveMode(mode.app.radiusMode)
        elif (event.key == '0'):
            Maze.restartMaze(mode)
            mode.app.timerMode = True
            mode.app.setActiveMode(mode.app.grinchMode)

    def checkIfMazeSolved(mode):
        cellX, cellY = Maze.getCell(mode, mode.dotX, mode.dotY)
        if ((cellX, cellY) == (mode.n - 1, mode.n - 1)):
            Maze.resetTimer(mode)
            mode.app.finalPresents = mode.app.presents
            Maze.restartMaze(mode)
            mode.app.setActiveMode(mode.app.finalScreen)

    def resetTimer(mode):
        mode.app.timerMode = False
        mode.app.timeSec = 0
        mode.app.timeMin = 0
    
    def getPossibleMoves(mode):
        # center and radius of dot
        cx, cy, r = mode.dotX, mode.dotY, mode.dotR
        
        # left, right, top, and bottom of dot
        dotx0, dotx1, doty0, doty1 = cx-r, cx+r, cy-r, cy+r
        midX = (dotx0 + dotx1) / 2
        midY = (doty0 + doty1) / 2

        # cell that center, top, bottom, left, and right of dot is in
        centerX, centerY = Maze.getCell(mode, cx, cy)
        cellOfCenter = (centerX, centerY)
        aboveX, aboveY = Maze.getCell(mode, midX, doty0)
        cellOfTop = (aboveX, aboveY)
        belowX, belowY = Maze.getCell(mode, midX, doty1)
        cellOfBottom = (belowX, belowY)
        leftX, leftY = Maze.getCell(mode, dotx0, midY)
        cellOfLeft = (leftX, leftY)
        rightX, rightY = Maze.getCell(mode, dotx1, midY)
        cellOfRight = (rightX, rightY)

        # bounds of cell that center of dot is in
        centerx0, centerx1, centery0, centery1 = Maze.getCellBounds(mode, centerX, centerY)

        possibleMoves = set()

        # check if dot can move within cell
        if (doty0 - mode.dotStepSize > centery0 + (mode.lineWidth * 2 / 3)):
            possibleMoves.add('Up')
        if (doty1 + mode.dotStepSize < centery1 - (mode.lineWidth * 2 / 3)):
            possibleMoves.add('Down')
        if (dotx0 - mode.dotStepSize > centerx0 + (mode.lineWidth * 2 / 3)):
            possibleMoves.add('Left')
        if (dotx1 + mode.dotStepSize < centerx1 - (mode.lineWidth * 2 / 3)):
            possibleMoves.add('Right')

        # cells above, below, left, and right of center cell
        cellAbove = (centerX, centerY-1)
        cellBelow = (centerX, centerY+1)
        cellLeft = (centerX-1, centerY)
        cellRight = (centerX+1, centerY)

        # check if dot can move to next cell
        if ((cellAbove in mode.connDict[cellOfLeft]) 
            and (cellAbove in mode.connDict[cellOfRight])):
            possibleMoves.add('Up')
        if ((cellBelow in mode.connDict[cellOfLeft]) 
            and (cellBelow in mode.connDict[cellOfRight])):
            possibleMoves.add('Down')
        if ((cellLeft in mode.connDict[cellOfTop]) 
            and (cellLeft in mode.connDict[cellOfBottom])):
            possibleMoves.add('Left')
        if ((cellRight in mode.connDict[cellOfTop]) 
            and (cellRight in mode.connDict[cellOfBottom])):
            possibleMoves.add('Right')

        return possibleMoves

    def getCell(mode, cx, cy):
        cellX = cx // mode.cellWidth
        cellY = cy // mode.cellHeight
        return int(cellX), int(cellY)

    def getCellBounds(mode, x, y):
        x0 = x * mode.cellWidth
        x1 = x * mode.cellWidth + mode.cellWidth
        y0 = y * mode.cellHeight
        y1 = y * mode.cellHeight + mode.cellHeight
        return x0, x1, y0, y1

    def drawAboveLine(mode, canvas, point):
        x, y = point
        x1 = x * mode.cellWidth - mode.lineMargin
        x2 = x * mode.cellWidth + mode.cellWidth + mode.lineMargin
        y1 = y * mode.cellHeight
        canvas.create_line(x1, y1, x2, y1, width=mode.lineWidth)

    def drawBelowLine(mode, canvas, point):
        x, y = point
        x1 = x * mode.cellWidth - mode.lineMargin
        x2 = x * mode.cellWidth + mode.cellWidth + mode.lineMargin
        y1 = y * mode.cellHeight + mode.cellHeight
        canvas.create_line(x1, y1, x2, y1, width=mode.lineWidth)

    def drawLeftLine(mode, canvas, point):
        x, y = point
        x1 = x * mode.cellWidth
        y1 = y * mode.cellHeight - mode.lineMargin
        y2 = y * mode.cellHeight + mode.cellHeight + mode.lineMargin
        canvas.create_line(x1, y1, x1, y2, width=mode.lineWidth)

    def drawRightLine(mode, canvas, point):
        x, y = point
        x1 = x * mode.cellWidth + mode.cellWidth
        y1 = y * mode.cellHeight - mode.lineMargin
        y2 = y * mode.cellHeight + mode.cellHeight + mode.lineMargin
        canvas.create_line(x1, y1, x1, y2, width=mode.lineWidth)

    def indicateSolution(mode, canvas, point):
        x, y = point        
        cx = x * mode.cellWidth + mode.cellWidth / 2
        cy = y * mode.cellHeight + mode.cellHeight / 2
        r = min(mode.cellWidth, mode.cellHeight) / 10
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='black')

    def highlight(mode, canvas, point):
        x, y = point
        x1 = x * mode.cellWidth
        x2 = x * mode.cellWidth + mode.cellWidth
        y1 = y * mode.cellHeight
        y2 = y * mode.cellHeight + mode.cellHeight
        canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='aliceblue')

        if (mode.showSolution == True):
            for point in mode.solution:
                Maze.indicateSolution(mode, canvas, point)

        for point in mode.connDict:
            x, y = point
            abovePoint = (x, y-1)
            belowPoint = (x, y+1)
            leftPoint = (x-1, y)
            rightPoint = (x+1, y)
            if (abovePoint not in mode.connDict[point]):
                Maze.drawAboveLine(mode, canvas, point)
            if (belowPoint not in mode.connDict[point]):
                Maze.drawBelowLine(mode, canvas, point)
            if (leftPoint not in mode.connDict[point]):
                Maze.drawLeftLine(mode, canvas, point)
            if (rightPoint not in mode.connDict[point]):
                Maze.drawRightLine(mode, canvas, point)
        
        # presents
        if (mode.presentsGathered == False):
            presentsX = mode.presentsCellX * mode.cellWidth + mode.cellWidth / 2
            presentsY = mode.presentsCellY * mode.cellHeight + mode.cellHeight / 2
            canvas.create_image(presentsX, presentsY, 
                        image=ImageTk.PhotoImage(mode.presentsResized))

        # sleigh
        canvas.create_oval(mode.dotX - mode.dotR, mode.dotY - mode.dotR,
                        mode.dotX + mode.dotR, mode.dotY + mode.dotR, 
                        fill='white', outline='')
        canvas.create_image(mode.dotX, mode.dotY, 
                        image=ImageTk.PhotoImage(mode.sleigh1Resized))

        # north pole, chimney
        canvas.create_image(mode.cellWidth / 2, mode.cellHeight / 2, 
                        image=ImageTk.PhotoImage(mode.northPoleResized))
        canvas.create_image(mode.width - mode.cellWidth / 2, 
                        mode.height - mode.cellHeight / 2,
                        image=ImageTk.PhotoImage(mode.chimneyResized))

class RadiusMode(Maze):
    def timerFired(mode):
        mode.app.timeSec += 0.03
        if (mode.app.timeSec >= 60):
            mode.app.timeMin += 1
            if (mode.app.presents >= 10):
                mode.app.presents -= 10
        mode.app.timeSec %= 60

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        canvas.create_oval(mode.dotX - mode.dotR * mode.visibilityR, 
                        mode.dotY - mode.dotR * mode.visibilityR,
                        mode.dotX + mode.dotR * mode.visibilityR, 
                        mode.dotY + mode.dotR * mode.visibilityR, 
                        fill='aliceblue')

        if (mode.showSolution == True):
            for point in mode.solution:
                Maze.indicateSolution(mode, canvas, point)

        for point in mode.connDict:
            x, y = point
            abovePoint = (x, y-1)
            belowPoint = (x, y+1)
            leftPoint = (x-1, y)
            rightPoint = (x+1, y)
            if abovePoint not in mode.connDict[point]:
                Maze.drawAboveLine(mode, canvas, point)
            if belowPoint not in mode.connDict[point]:
                Maze.drawBelowLine(mode, canvas, point)
            if leftPoint not in mode.connDict[point]:
                Maze.drawLeftLine(mode, canvas, point)
            if rightPoint not in mode.connDict[point]:
                Maze.drawRightLine(mode, canvas, point)

        # sleigh
        canvas.create_oval(mode.dotX - mode.dotR, mode.dotY - mode.dotR,
                        mode.dotX + mode.dotR, mode.dotY + mode.dotR, 
                        fill='white', outline='')
        canvas.create_image(mode.dotX, mode.dotY, 
                        image=ImageTk.PhotoImage(mode.sleigh2Resized))

        # time, presents label
        canvas.create_text(mode.width - 20, 20, fill='green', 
                        text=f'Time: {mode.app.timeMin}m {int(mode.app.timeSec)}s',
                        anchor='ne',
                        font='Baloo 40')
        canvas.create_text(mode.width - 20, 60, fill='green', 
                        text=f'Presents: {mode.app.presents}',
                        anchor='ne',
                        font='Baloo 40')

        # north pole, chimney
        canvas.create_image(mode.cellWidth / 2, mode.cellHeight / 2, 
                        image=ImageTk.PhotoImage(mode.northPoleResized))
        canvas.create_image(mode.width - mode.cellWidth / 2, 
                        mode.height - mode.cellHeight / 2,
                        image=ImageTk.PhotoImage(mode.chimneyResized))

class GrinchMode(Maze):
    def timerFired(mode):
        mode.app.timeSec += 0.03
        if (mode.app.timeSec >= 60):
            mode.app.timeMin += 1
            if (mode.app.presents >= 10):
                mode.app.presents -= 10
        mode.app.timeSec %= 60
        
        GrinchMode.checkSleighGrinchIntersect(mode)
        if (mode.canGrinchMove == True):
            GrinchMode.moveGrinch(mode)

    def checkSleighGrinchIntersect(mode):
        sleighX, sleighY = Maze.getCell(mode, mode.dotX, mode.dotY)
        grinchX, grinchY = Maze.getCell(mode, mode.grinchX, mode.grinchY)
        # sleigh and grinch
        if ((sleighX, sleighY) == (grinchX, grinchY)) and (mode.app.presents > 0):
            mode.app.presents -= 0.1
        # sleigh and presents
        if ((sleighX, sleighY) == (mode.presentsCellX, mode.presentsCellY)
            and (mode.presentsGathered == False)):
            mode.app.presents += 10
            mode.presentsGathered = True
        # grinch and candycane
        grinchCellX, grinchCellY = Maze.getCell(mode, mode.grinchX, mode.grinchY)
        if ((grinchCellX, grinchCellY) == (mode.candycaneCellX, mode.candycaneCellY)):
            mode.canGrinchMove = False

    def moveGrinch(mode):
        sleighX, sleighY = Maze.getCell(mode, mode.dotX, mode.dotY)
        grinchCellX, grinchCellY = Maze.getCell(mode, mode.grinchX, mode.grinchY)
        grinchR, grinchB = Maze.getCell(mode, mode.grinchX + mode.grinchR, mode.grinchY + mode.grinchR)
        grinchL, grinchT = Maze.getCell(mode, mode.grinchX - mode.grinchR, mode.grinchY - mode.grinchR)
        grinchSol, grinchConn = getMazeSolutionConnections(mode.n, mode.mazeDict, (grinchCellX, grinchCellY), (sleighX, sleighY))
        try:
            if (len(grinchSol) >= 5) and (grinchSol[0] == grinchSol[3]):
                newCellX, newCellY = grinchSol[4]
            else:
                newCellX, newCellY = grinchSol[1]
        except:
            newCellX, newCellY = grinchSol[0]

        # find coordinates of grinchCellX, grinchCellY, newCellX, newCellY
        grinchCellXCoord = grinchCellX * mode.cellWidth + mode.cellWidth / 2
        grinchCellYCoord = grinchCellY * mode.cellHeight + mode.cellHeight / 2
        newCellXCoord = newCellX * mode.cellWidth + mode.cellWidth / 2
        newCellYCoord = newCellY * mode.cellHeight + mode.cellHeight / 2

        # move grinch to center of cell or to center of next cell
        if (grinchCellX + 1 == newCellX):
            if (grinchCellXCoord-1 < mode.grinchX <= newCellXCoord+1):
                GrinchMode.moveGrinchTowardsPoint(mode, newCellXCoord, newCellYCoord)
            else:
                GrinchMode.moveGrinchTowardsPoint(mode, grinchCellXCoord, grinchCellYCoord)
        elif (grinchCellX - 1 == newCellX):
            if (newCellXCoord-1 <= mode.grinchX < grinchCellXCoord+1):
                GrinchMode.moveGrinchTowardsPoint(mode, newCellXCoord, newCellYCoord)
            else:
                GrinchMode.moveGrinchTowardsPoint(mode, grinchCellXCoord, grinchCellYCoord)
        elif (grinchCellY + 1 == newCellY):
            if (grinchCellYCoord-1 < mode.grinchY <= newCellYCoord+1):
                GrinchMode.moveGrinchTowardsPoint(mode, newCellXCoord, newCellYCoord)
            else:
                GrinchMode.moveGrinchTowardsPoint(mode, grinchCellXCoord, grinchCellYCoord)
        elif (grinchCellY - 1 == newCellY):
            if (newCellYCoord-1 <= mode.grinchY < grinchCellYCoord+1):
                GrinchMode.moveGrinchTowardsPoint(mode, newCellXCoord, newCellYCoord)
            else:
                GrinchMode.moveGrinchTowardsPoint(mode, grinchCellXCoord, grinchCellYCoord)
        
    def moveGrinchTowardsPoint(mode, x, y):
        if (mode.grinchX > x):
            mode.grinchX -= 1
        elif (mode.grinchX < x):
            mode.grinchX += 1
        if (mode.grinchY > y):
            mode.grinchY -= 1
        elif (mode.grinchY < y):
            mode.grinchY += 1

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='aliceblue')

        if (mode.showSolution == True):
            for point in mode.solution:
                Maze.indicateSolution(mode, canvas, point)

        for point in mode.connDict:
            x, y = point
            abovePoint = (x, y-1)
            belowPoint = (x, y+1)
            leftPoint = (x-1, y)
            rightPoint = (x+1, y)
            if abovePoint not in mode.connDict[point]:
                Maze.drawAboveLine(mode, canvas, point)
            if belowPoint not in mode.connDict[point]:
                Maze.drawBelowLine(mode, canvas, point)
            if leftPoint not in mode.connDict[point]:
                Maze.drawLeftLine(mode, canvas, point)
            if rightPoint not in mode.connDict[point]:
                Maze.drawRightLine(mode, canvas, point)
        
        # presents and candycane
        if (mode.presentsGathered == False):
            presentsX = mode.presentsCellX * mode.cellWidth + mode.cellWidth / 2
            presentsY = mode.presentsCellY * mode.cellHeight + mode.cellHeight / 2
            canvas.create_image(presentsX, presentsY, 
                        image=ImageTk.PhotoImage(mode.presentsResized))
        candycaneX = mode.candycaneCellX * mode.cellWidth + mode.cellWidth / 2
        candycaneY = mode.candycaneCellY * mode.cellHeight + mode.cellHeight / 2
        canvas.create_image(candycaneX, candycaneY, 
                        image=ImageTk.PhotoImage(mode.candycaneResized))

        # sleigh
        canvas.create_oval(mode.dotX - mode.dotR, mode.dotY - mode.dotR,
                        mode.dotX + mode.dotR, mode.dotY + mode.dotR, 
                        fill='white', outline='')
        canvas.create_image(mode.dotX, mode.dotY, 
                        image=ImageTk.PhotoImage(mode.sleigh3Resized))

        # grinch
        canvas.create_oval(mode.grinchX - mode.grinchR, mode.grinchY - mode.grinchR,
                        mode.grinchX + mode.grinchR, mode.grinchY + mode.grinchR,
                        fill='white', outline='')
        canvas.create_image(mode.grinchX, mode.grinchY, 
                        image=ImageTk.PhotoImage(mode.grinchResized))

        # time, presents label
        canvas.create_text(mode.width - 20, 20, fill='green', 
                        text=f'Time: {mode.app.timeMin}m {int(mode.app.timeSec)}s',
                        anchor='ne',
                        font='Baloo 40')
        canvas.create_text(mode.width - 20, 60, fill='green', 
                        text=f'Presents: {int(mode.app.presents)}',
                        anchor='ne',
                        font='Baloo 40')

        # north pole, chimney
        canvas.create_image(mode.cellWidth / 2, mode.cellHeight / 2, 
                        image=ImageTk.PhotoImage(mode.northPoleResized))
        canvas.create_image(mode.width - mode.cellWidth / 2, 
                        mode.height - mode.cellHeight / 2,
                        image=ImageTk.PhotoImage(mode.chimneyResized))
