########################################
#   Ho Ho Home: the Santa Maze Game
#   (gameScreens.py)
#   By: Sarah Chen (sarahc2)
########################################
#   Game Screens
########################################
#
#   Citations: 
#   1)  incorporated subclassing ModalApp and Mode idea from
#       https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
#   2)  used rgbString function from
#       https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors 
#   3)  snowfall idea from Rachel Wilson
#
########################################
from cmu_112_graphics import *
import random

BACKGROUND_IMAGE_PATH = 'background.png'
TITULO_FONTE = 'Baloo 60'
TITULO_FONTE2 = 'Baloo 20'
TITULO_FONTE3 = 'Baloo 30'
TITULO_FONTE4 = 'GB18030Bitmap 11 bold'

class TitleScreen(Mode):
    def app_started(mode):
        mode.darkGreen = TitleScreen.rgbString(52, 102, 51)
        mode.green = TitleScreen.rgbString(89, 156, 93)
        mode.buttonColor = mode.green
        mode.buttonTextColor = 'white'
        mode.snow = []
        mode.snowR = 17
        mode.count = 0
        mode.title = mode.loadImage('title.png')
        mode.titleResized = mode.scaleImage(mode.title, 0.4)
        mode.background = mode.loadImage(BACKGROUND_IMAGE_PATH)
        mode.backgroundResized = mode.scaleImage(mode.background, 0.5)

    def rgbString(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def mouse_pressed(mode, event):
        if ((mode.width/2-150 <= event.x <= mode.width/2+150) 
            and (mode.height*2/3-50 <= event.y <= mode.height*2/3+50)):
            mode.app.setActiveMode(mode.app.backgroundScreen)
            mode.homeButtonColor = mode.green
    
    def mouse_moved(mode, event):
        if ((mode.width/2-150 <= event.x <= mode.width/2+150) 
            and (mode.height*2/3-50 <= event.y <= mode.height*2/3+50)
            and (mode.buttonColor != 'dark green')):
            mode.buttonColor = mode.darkGreen
        elif (((event.x < mode.width/2-150) 
            or (event.x > mode.width/2+150) 
            or (event.y < mode.height*2/3-50) 
            or (event.y > mode.height*2/3+50))
            and (mode.buttonColor != 'dark green')):
            mode.buttonColor = mode.green

    def timer_fired(mode):
        mode.count += 1
        if (mode.count == 20):
            randomX = random.randrange(mode.width)
            mode.snow.append(FallingSnow(randomX, 0))
            mode.count = 0

        for snowball in mode.snow:
            snowball.fall()

    def redraw_all(mode, canvas):
        # background
        canvas.create_image(mode.width/2, mode.height/2, 
                            image=ImageTk.PhotoImage(mode.backgroundResized))
        # snow
        for snowball in mode.snow:
            snowX, snowY = snowball.x, snowball.y
            canvas.create_oval(snowX-mode.snowR, snowY-mode.snowR, 
                            snowX+mode.snowR, snowY+mode.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_image(mode.width/2+30, mode.height/3, 
                            image=ImageTk.PhotoImage(mode.titleResized))
        canvas.create_text(mode.width/2, mode.height/3+80,
                            fill='firebrick4',
                            text='the Santa Maze Game', 
                            font='Baloo 50')
        # 'Let's Begin' button
        canvas.create_rectangle(mode.width/2-150, mode.height*2/3-50,
                            mode.width/2+150, mode.height*2/3+50,
                            fill=mode.buttonColor, outline='')
        canvas.create_text(mode.width/2, mode.height*2/3,
                            fill=mode.buttonTextColor,
                            text='Let\'s Begin', 
                            font='Baloo 45')

class FallingSnow(Mode):
    def __init__(mode, x, y):
        mode.x = x
        mode.y = y

    def fall(mode):
        mode.y += 3

class BackgroundScreen(Mode):
    def app_started(mode):
        mode.snow = []
        mode.snowR = 20
        mode.count = 0
        mode.titleColor = 'gold'
        mode.darkGreen = TitleScreen.rgbString(52, 102, 51)
        mode.green = TitleScreen.rgbString(89, 156, 93)
        mode.homeButtonColor = mode.nextButtonColor = mode.green
        mode.homeButtonTextColor = mode.nextButtonTextColor = 'white'
        mode.backgroundText = '''It's the last few hours of Christmas Eve, and 
there are only a couple more presents left to be 
delivered. Unfortunately, Santa’s reindeer just 
contracted a novel XMAS-20 virus that can only 
affect reindeer (don’t worry, all of them are 
showing positive signs of recovery), and they 
can’t help Santa deliver the last 100 presents! 
Even though Rudolf told him the fastest way, 
Santa immediately forgot and must now figure out 
his way to town on his own. Help Santa redeem his 
bad memory by following the instructions on the 
next slide, and prove to the world that Santa 
still has what it takes to deliver presents to 
every last kid!'''
        mode.background = mode.loadImage(BACKGROUND_IMAGE_PATH)
        mode.backgroundResized = mode.scaleImage(mode.background, 0.5)

    def timer_fired(mode):
        mode.count += 1
        if (mode.count == 20):
            randomX = random.randrange(mode.width)
            mode.snow.append(FallingSnow(randomX, 0))
            mode.count = 0

        for snowball in mode.snow:
            snowball.fall()

    def mouse_pressed(mode, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            mode.app.setActiveMode(mode.app.titleScreen)
            mode.homeButtonColor = mode.green
        elif ((mode.width-150 <= event.x <= mode.width-50) 
            and (50 <= event.y <= 100)):
            mode.app.setActiveMode(mode.app.instructionsScreen)
            mode.nextButtonColor = mode.green
    
    def mouse_moved(mode, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            mode.homeButtonColor = mode.darkGreen
        elif ((mode.width-150 <= event.x <= mode.width-50) 
            and (50 <= event.y <= 100)):
            mode.nextButtonColor = mode.darkGreen
        elif (((event.x < 50) or ((event.x > 150) 
            and (event.x < mode.width-150)) or (event.x > mode.width-50))
            or ((event.y < 50) or (event.y > 100))):
            mode.homeButtonColor = mode.nextButtonColor = mode.green

    def redraw_all(mode, canvas):
        # background
        canvas.create_image(mode.width/2, mode.height/2, 
                            image=ImageTk.PhotoImage(mode.backgroundResized))
        # snow
        for snowball in mode.snow:
            snowX, snowY = snowball.x, snowball.y
            canvas.create_oval(snowX-mode.snowR, snowY-mode.snowR, 
                            snowX+mode.snowR, snowY+mode.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(mode.width/2, mode.height/10,
                            fill=mode.titleColor,
                            text='Background', 
                            font=TITULO_FONTE)
        # 'Home' button
        canvas.create_rectangle(50, 50, 150, 100,
                            fill=mode.homeButtonColor,
                            outline='')
        canvas.create_text(100, 75,
                            fill=mode.homeButtonTextColor,
                            text='Home', 
                            font=TITULO_FONTE2)
        # 'Next' button
        canvas.create_rectangle(mode.width-50, 50, mode.width-150, 100,
                            fill=mode.nextButtonColor,
                            outline='')
        canvas.create_text(mode.width-100, 75,
                            fill=mode.nextButtonTextColor,
                            text='Next', 
                            font=TITULO_FONTE2)
        # background text
        canvas.create_text(mode.width/2, mode.height/2-50,
                            fill='gold',
                            text=mode.backgroundText, 
                            font='GB18030Bitmap 15')

class InstructionsScreen(BackgroundScreen):
    def app_started(mode):
        mode.snow = []
        mode.snowR = 20
        mode.count = 0
        mode.titleColor = 'gold'
        mode.darkGreen = TitleScreen.rgbString(52, 102, 51)
        mode.green = TitleScreen.rgbString(89, 156, 93)
        mode.backButtonColor = mode.nextButtonColor = mode.green
        mode.backButtonTextColor = mode.nextButtonTextColor = 'white'
        mode.instructionsText = '''Navigate Santa's sleigh through the maze by using the 'Up', 'Down', 
'Left', and 'Right' arrow keys and get him from the North Pole to 
the first chimney in town as fast as you can. Every extra minute 
you take, Santa will lose 10 presents from his initial 100!

Hints:
- If the Grinch finds Santa, he will be sure to steal as many 
  presents as he can so long as Santa's sleigh is in his reach. 
  Though Santa's sleigh moves faster than the Grinch, the Grinch 
  can cut corners by moving diagonally.
- Press the ‘Space’ bar to “call a telephone line back to the 
  knowledgable reindeer” who will reveal Santa’s ideal route 
  through a series of dots.
- Press keys '1' through '7' to regenerate the maze. A higher 
  number implies a higher maze complexity.
- Press the 'r' key to restart the maze.
- Santa may be able to "find extra presents" using Sled 1 or 3.
- Grinches get stuck on melted candy canes!

Proceed to the next page to choose Santa’s sleigh and begin. 
Hurry - you’re running out of time!'''
        mode.background = mode.loadImage(BACKGROUND_IMAGE_PATH)
        mode.backgroundResized = mode.scaleImage(mode.background, 0.5)

    def timer_fired(mode):
        mode.count += 1
        if (mode.count == 20):
            randomX = random.randrange(mode.width)
            mode.snow.append(FallingSnow(randomX, 0))
            mode.count = 0

        for snowball in mode.snow:
            snowball.fall()

    def mouse_pressed(mode, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            mode.app.setActiveMode(mode.app.backgroundScreen)
            mode.backButtonColor = mode.green
        elif ((mode.width-150 <= event.x <= mode.width-50) 
            and (50 <= event.y <= 100)):
            mode.app.setActiveMode(mode.app.sleighScreen)
            mode.nextButtonColor = mode.green
    
    def mouse_moved(mode, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            mode.backButtonColor = mode.darkGreen
        elif ((mode.width-150 <= event.x <= mode.width-50) 
            and (50 <= event.y <= 100)):
            mode.nextButtonColor = mode.darkGreen
        elif (((event.x < 50) or ((event.x > 150) 
            and (event.x < mode.width-150)) or (event.x > mode.width-50))
            or ((event.y < 50) or (event.y > 100))):
            mode.backButtonColor = mode.nextButtonColor = mode.green

    def redraw_all(mode, canvas):
        # background
        canvas.create_image(mode.width/2, mode.height/2, 
                            image=ImageTk.PhotoImage(mode.backgroundResized))
        # snow
        for snowball in mode.snow:
            snowX, snowY = snowball.x, snowball.y
            canvas.create_oval(snowX-mode.snowR, snowY-mode.snowR, 
                            snowX+mode.snowR, snowY+mode.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(mode.width/2, mode.height/10,
                            fill=mode.titleColor,
                            text='Instructions', 
                            font=TITULO_FONTE)
        # 'Back' button
        canvas.create_rectangle(50, 50, 150, 100,
                            fill=mode.backButtonColor,
                            outline='')
        canvas.create_text(100, 75,
                            fill=mode.backButtonTextColor,
                            text='Back', 
                            font=TITULO_FONTE2)
        # 'Next' button
        canvas.create_rectangle(mode.width-50, 50, mode.width-150, 100,
                            fill=mode.nextButtonColor,
                            outline='')
        canvas.create_text(mode.width-100, 75,
                            fill=mode.nextButtonTextColor,
                            text='Next', 
                            font=TITULO_FONTE2)
        # instructions text
        canvas.create_text(mode.width/2, mode.height/2-40,
                            fill='gold',
                            text=mode.instructionsText, 
                            font='GB18030Bitmap 12')

class SleighScreen(BackgroundScreen):
    def app_started(mode):
        mode.snow = []
        mode.snowR = 20
        mode.count = 0
        mode.titleColor = 'gold'
        mode.darkGreen = TitleScreen.rgbString(52, 102, 51)
        mode.green = TitleScreen.rgbString(89, 156, 93)
        mode.backButtonColor = mode.nextButtonColor = mode.green
        mode.backButtonTextColor = mode.nextButtonTextColor = 'white'
        mode.mode1ButtonColor = mode.mode2ButtonColor = mode.mode3ButtonColor = mode.green
        mode.mode1ButtonTextColor = mode.mode2ButtonTextColor = mode.mode3ButtonTextColor = 'white'
        mode.mode1Title = '''                Sleigh 1:
No Presents, Just Vibes'''
        mode.mode1Text = '''Santa accidentally forgot 
all his presents back at the North 
Pole. He has decided to cut his 
losses and just vibe his way to 
town (no timer). Fortunately, this 
means that Santa has nothing the 
Grinch wants, so the Grinch will 
stay home this Eve. Though the 
kids will be left empty-handed, 
sometimes Santa just needs to 
prioritize his own self care. 
Hopefully he can come up with a 
good excuse on the way though…'''
        mode.mode2Title = '''         Sleigh 2:
Will Pay To Take'''
        mode.mode2Text = '''Santa Will Pay you To Take 
this sleigh. Pros: not even the 
Grinch can be bothered by this 
sleigh, so he will not be chasing 
after Santa. Cons: Absolutely no 
visibility. Cannot see anything.
Note that Santa is smart enough
to take a flashlight with this 
sleigh. Turn up his flashlight and
make his visibility range Bigger 
by pressing the 'b' key. Make 
his visibility range Smaller by 
pressing the 's' key.'''
        mode.mode3Title = '''              Sleigh 3:
2021 Christmas Corvette'''
        mode.mode3Text = '''Santa is now “that car guy,” 
and has finally invested in the 
shiniest! newest! cleanest! 2021 
Christmas Corvette. This sleigh of 
beauty has the highest visibility 
known to all car dudes (i.e. she, 
the car, can see the whole maze); 
However, Santa needs to be careful 
if he chooses this sleigh - not only 
because he’s a bad driver and 
doesn’t want to scrape her, but 
also because she’ll attract …the 
Grinch! (who will steal his presents)'''
        mode.sleigh1 = mode.loadImage('sleigh1.png')
        mode.sleigh1Resized = mode.scaleImage(mode.sleigh1, 0.1)
        mode.sleigh2 = mode.loadImage('sleigh2.png')
        mode.sleigh2Resized = mode.scaleImage(mode.sleigh2, 0.1)
        mode.sleigh3 = mode.loadImage('sleigh3.png')
        mode.sleigh3Resized = mode.scaleImage(mode.sleigh3, 0.1)
        mode.background = mode.loadImage(BACKGROUND_IMAGE_PATH)
        mode.backgroundResized = mode.scaleImage(mode.background, 0.5)

    def timer_fired(mode):
        mode.count += 1
        if (mode.count == 20):
            randomX = random.randrange(mode.width)
            mode.snow.append(FallingSnow(randomX, 0))
            mode.count = 0

        for snowball in mode.snow:
            snowball.fall()

    def mouse_moved(mode, event):
        # 'Back' and 'Home' button toggle
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            mode.backButtonColor = mode.darkGreen
        elif ((mode.width-150 <= event.x <= mode.width-50) 
            and (50 <= event.y <= 100)):
            mode.nextButtonColor = mode.darkGreen
        elif (event.x < 50 or (event.x > 150 and event.x < mode.width-150) 
            or event.x > mode.width-50 or event.y < 50 or event.y > 100):
            mode.backButtonColor = mode.nextButtonColor = mode.green
        # 'Play Sleigh 1' button toggle
        if ((mode.width/6-80 <= event.x <= mode.width/6+80) 
            and (mode.height*9/10-40 <= event.y <= mode.height*9/10+40)):
            mode.mode1ButtonColor = mode.darkGreen
        elif ((event.x < mode.width/4-80) or (event.x > mode.width/4+80)
            or (event.y < mode.height*9/10-40) 
            or (event.y < mode.height*9/10+40)):
            mode.mode1ButtonColor = mode.green
        # 'Play Sleigh 2' button toggle
        if ((mode.width/2-80 <= event.x <= mode.width/2+80) 
            and (mode.height*9/10-40 <= event.y <= mode.height*9/10+40)):
            mode.mode2ButtonColor = mode.darkGreen
        elif ((event.x < mode.width/2-80) or (event.x > mode.width/2+80)
            or (event.y < mode.height*9/10-40) 
            or (event.y < mode.height*9/10+40)):
            mode.mode2ButtonColor = mode.green
        # 'Play Sleigh 3' button toggle
        if ((mode.width*5/6-80 <= event.x <= mode.width*5/6+80) 
            and (mode.height*9/10-40 <= event.y <= mode.height*9/10+40)):
            mode.mode3ButtonColor = mode.darkGreen
        elif ((event.x < mode.width*3/4-80) or (event.x > mode.width*3/4+80)
            or (event.y < mode.height*9/10-40) 
            or (event.y < mode.height*9/10+40)):
            mode.mode3ButtonColor = mode.green

    def mouse_pressed(mode, event):
        # 'Back' button
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            mode.app.setActiveMode(mode.app.instructionsScreen)
            mode.backButtonColor = mode.green
        # 'Home' button
        elif ((mode.width-150 <= event.x <= mode.width-50) 
            and (50 <= event.y <= 100)):
            mode.app.setActiveMode(mode.app.titleScreen)
            mode.nextButtonColor = mode.green
        # 'Play Sleigh 1' button
        elif ((mode.width/6-80 <= event.x <= mode.width/6+80) 
            and (mode.height*9/10-40 <= event.y <= mode.height*9/10+40)):
            mode.app.timeSec = 0
            mode.app.timeMin = 0
            mode.app.setActiveMode(mode.app.maze) 
            mode.mode1ButtonColor = mode.green
        # 'Play Sleigh 2' button
        elif ((mode.width/2-80 <= event.x <= mode.width/2+80) 
            and (mode.height*9/10-40 <= event.y <= mode.height*9/10+40)):
            mode.app.presents = 100
            mode.app.setActiveMode(mode.app.radiusMode) 
            mode.mode2ButtonColor = mode.green
        # 'Play Sleigh 3' button
        elif ((mode.width*5/6-80 <= event.x <= mode.width*5/6+80) 
            and (mode.height*9/10-40 <= event.y <= mode.height*9/10+40)):
            mode.app.presents = 100
            mode.app.setActiveMode(mode.app.grinchMode) 
            mode.mode3ButtonColor = mode.green

    def redraw_all(mode, canvas):
        # background
        canvas.create_image(mode.width/2, mode.height/2, 
                            image=ImageTk.PhotoImage(mode.backgroundResized))
        # snow
        for snowball in mode.snow:
            snowX, snowY = snowball.x, snowball.y
            canvas.create_oval(snowX-mode.snowR, snowY-mode.snowR, 
                            snowX+mode.snowR, snowY+mode.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(mode.width/2, mode.height/10,
                            fill=mode.titleColor,
                            text='Choose Your Sleigh', 
                            font=TITULO_FONTE)
        # 'Back' button
        canvas.create_rectangle(50, 50, 150, 100,
                            fill=mode.backButtonColor,
                            outline='')
        canvas.create_text(100, 75,
                            fill=mode.backButtonTextColor,
                            text='Back', 
                            font=TITULO_FONTE2)
        # 'Home' button
        canvas.create_rectangle(mode.width-50, 50, mode.width-150, 100,
                            fill=mode.nextButtonColor,
                            outline='')
        canvas.create_text(mode.width-100, 75,
                            fill=mode.nextButtonTextColor,
                            text='Home', 
                            font=TITULO_FONTE2)
        # Sleigh 1
        canvas.create_rectangle(mode.width/6-150, mode.height/2-20, 
                            mode.width/6+130, mode.height/2+260,
                            fill='white',
                            outline='')
        canvas.create_rectangle(mode.width/6-80, mode.height*9/10-40, 
                            mode.width/6+80, mode.height*9/10+40,
                            fill=mode.mode1ButtonColor,
                            outline='')
        canvas.create_text(mode.width/6, mode.height*9/10,
                            fill=mode.mode1ButtonTextColor,
                            text='Sleigh 1', 
                            font=TITULO_FONTE3)
        canvas.create_text(mode.width/6, mode.height/5,
                            fill='gold',
                            text=mode.mode1Title, 
                            font=TITULO_FONTE3)
        canvas.create_text(mode.width/6, mode.height*3/5+40,
                            fill='black',
                            text=mode.mode1Text, 
                            font=TITULO_FONTE4)
        canvas.create_image(mode.width/6, mode.height*2/5-25, 
                            image=ImageTk.PhotoImage(mode.sleigh1Resized))
        # Sleigh 2
        canvas.create_rectangle(mode.width/2-150, mode.height/2-20, 
                            mode.width/2+130, mode.height/2+260,
                            fill='white',
                            outline='')
        canvas.create_rectangle(mode.width/2-80, mode.height*9/10-40, 
                            mode.width/2+80, mode.height*9/10+40,
                            fill=mode.mode2ButtonColor,
                            outline='')
        canvas.create_text(mode.width/2, mode.height*9/10,
                            fill=mode.mode2ButtonTextColor,
                            text='Sleigh 2', 
                            font=TITULO_FONTE3)
        canvas.create_text(mode.width/2, mode.height/5,
                            fill='gold',
                            text=mode.mode2Title, 
                            font=TITULO_FONTE3)
        canvas.create_text(mode.width/2, mode.height*3/5+40,
                            fill='black',
                            text=mode.mode2Text, 
                            font=TITULO_FONTE4)
        canvas.create_image(mode.width/2, mode.height*2/5-25, 
                            image=ImageTk.PhotoImage(mode.sleigh2Resized))
        # Sleigh 3
        canvas.create_rectangle(mode.width*5/6-160, mode.height/2-20, 
                            mode.width*5/6+140, mode.height/2+260,
                            fill='white',
                            outline='')
        canvas.create_rectangle(mode.width*5/6-80, mode.height*9/10-40, 
                            mode.width*5/6+80, mode.height*9/10+40,
                            fill=mode.mode3ButtonColor,
                            outline='')
        canvas.create_text(mode.width*5/6, mode.height*9/10,
                            fill=mode.mode3ButtonTextColor,
                            text='Sleigh 3', 
                            font=TITULO_FONTE3)
        canvas.create_text(mode.width*5/6, mode.height/5,
                            fill='gold',
                            text=mode.mode3Title, 
                            font=TITULO_FONTE3)
        canvas.create_text(mode.width*5/6, mode.height*3/5+40,
                            fill='black',
                            text=mode.mode3Text, 
                            font=TITULO_FONTE4)
        canvas.create_image(mode.width*5/6, mode.height*2/5-25, 
                            image=ImageTk.PhotoImage(mode.sleigh3Resized))

class FinalScreen(SleighScreen):
    def app_started(mode):
        mode.snow = []
        mode.snowR = 20
        mode.count = 0
        mode.titleColor = 'gold'
        mode.darkGreen = TitleScreen.rgbString(52, 102, 51)
        mode.green = TitleScreen.rgbString(89, 156, 93)
        mode.playAgainButtonColor = mode.green
        mode.playAgainButtonTextColor = 'white'
        mode.homeButtonColor = mode.green
        mode.homeButtonTextColor = 'white'
        mode.background = mode.loadImage(BACKGROUND_IMAGE_PATH)
        mode.backgroundResized = mode.scaleImage(mode.background, 0.5)

    def timer_fired(mode):
        mode.count += 1
        if (mode.count == 20):
            randomX = random.randrange(mode.width)
            mode.snow.append(FallingSnow(randomX, 0))
            mode.count = 0

        for snowball in mode.snow:
            snowball.fall()

    def mouse_moved(mode, event):
        if ((mode.width/2-200 <= event.x <= mode.width/2+200) 
            and (mode.height*7/10-50 <= event.y <= mode.height*7/10+50)):
            mode.playAgainButtonColor = mode.darkGreen
        elif ((event.x < mode.width/2-200) or (event.x > mode.width/2+200)
            or (event.y < mode.height*7/10-50) 
            or (event.y > mode.height*7/10+50)):
            mode.playAgainButtonColor = mode.green
        if ((mode.width/2-50 <= event.x <= mode.width/2+50) 
            and (mode.height*9/10-25 <= event.y <= mode.height*9/10+25)):
            mode.homeButtonColor = mode.darkGreen
        elif ((event.x < mode.width/2-50) or (event.x > mode.width/2+50)
            or (event.y < mode.height*9/10-25) 
            or (event.y > mode.height*9/10+25)):
            mode.homeButtonColor = mode.green

    def mouse_pressed(mode, event):
        # 'Play Again' button
        if ((mode.width/2-200 <= event.x <= mode.width/2+200) 
            and (mode.height*7/10-50 <= event.y <= mode.height*7/10+50)):
            mode.app.presents = 0
            mode.app.setActiveMode(mode.app.sleighScreen)
            mode.playAgainButtonColor = mode.green
        # 'Home' button
        elif ((mode.width/2-50 <= event.x <= mode.width/2+50) 
            and (mode.height*9/10-25 <= event.y <= mode.height*9/10+25)):
            mode.app.presents = 0
            mode.app.setActiveMode(mode.app.titleScreen)
            mode.homeButtonColor = mode.green

    def redraw_all(mode, canvas):
        # background
        canvas.create_image(mode.width/2, mode.height/2, 
                            image=ImageTk.PhotoImage(mode.backgroundResized))
        # snow
        for snowball in mode.snow:
            snowX, snowY = snowball.x, snowball.y
            canvas.create_oval(snowX-mode.snowR, snowY-mode.snowR, 
                            snowX+mode.snowR, snowY+mode.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(mode.width/2, mode.height*3/10,
                            fill=mode.titleColor,
                            text='Congrats!', 
                            font='Baloo 90')
        canvas.create_text(mode.width/2, mode.height*4/10,
                            fill=mode.titleColor,
                            text=f'You successfully delivered {int(mode.app.finalPresents)} presents.', 
                            font='Baloo 40')
        # 'Play Again' button
        canvas.create_rectangle(mode.width/2-200, mode.height*7/10-50, 
                            mode.width/2+200, mode.height*7/10+50,
                            fill=mode.playAgainButtonColor,
                            outline='')
        canvas.create_text(mode.width/2, mode.height*7/10,
                            fill=mode.playAgainButtonTextColor,
                            text='Play Again', 
                            font='Baloo 40')
        # 'Home' button
        canvas.create_rectangle(mode.width/2-50, mode.height*9/10-25, 
                            mode.width/2+50, mode.height*9/10+25,
                            fill=mode.homeButtonColor,
                            outline='')
        canvas.create_text(mode.width/2, mode.height*9/10,
                            fill=mode.homeButtonTextColor,
                            text='Home', 
                            font=TITULO_FONTE2)