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
from cmu_112_graphics import App, runApp, Mode, ModalApp
from PIL import Image, ImageTk
import random

BACKGROUND_IMAGE_PATH = 'background.png'
TITULO_FONTE = 'Baloo 60'
TITULO_FONTE2 = 'Baloo 20'
TITULO_FONTE3 = 'Baloo 30'
TITULO_FONTE4 = 'GB18030Bitmap 11 bold'

class TitleScreen(Mode):
    def app_started(self):
        self.darkGreen = TitleScreen.rgbString(52, 102, 51)
        self.green = TitleScreen.rgbString(89, 156, 93)
        self.buttonColor = self.green
        self.buttonTextColor = 'white'
        self.snow = []
        self.snowR = 17
        self.count = 0
        self.title = self.load_image('title.png')
        self.titleResized = self.scale_image(self.title, 0.4)
        self.background = self.load_image(BACKGROUND_IMAGE_PATH)
        self.backgroundResized = self.scale_image(self.background, 0.5)

    def rgbString(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def mouse_pressed(self, event):
        if ((self.width/2-150 <= event.x <= self.width/2+150) 
            and (self.height*2/3-50 <= event.y <= self.height*2/3+50)):
            self.app.set_active_mode(self.app.backgroundScreen)
            self.homeButtonColor = self.green
    
    def mouse_moved(self, event):
        if ((self.width/2-150 <= event.x <= self.width/2+150) 
            and (self.height*2/3-50 <= event.y <= self.height*2/3+50)
            and (self.buttonColor != 'dark green')):
            self.buttonColor = self.darkGreen
        elif (((event.x < self.width/2-150) 
            or (event.x > self.width/2+150) 
            or (event.y < self.height*2/3-50) 
            or (event.y > self.height*2/3+50))
            and (self.buttonColor != 'dark green')):
            self.buttonColor = self.green

    def timer_fired(self):
        self.count += 1
        if (self.count == 20):
            random_x = random.randrange(self.width)
            self.snow.append(FallingSnow(random_x, 0))
            self.count = 0

        for snowball in self.snow:
            snowball.fall()

    def redraw_all(self, canvas):
        # background
        canvas.create_image(self.width/2, self.height/2, 
                            image=ImageTk.PhotoImage(self.backgroundResized))
        # snow
        for snowball in self.snow:
            snow_x, snow_y = snowball.x, snowball.y
            canvas.create_oval(snow_x-self.snowR, snow_y-self.snowR, 
                            snow_x+self.snowR, snow_y+self.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_image(self.width/2+30, self.height/3, 
                            image=ImageTk.PhotoImage(self.titleResized))
        canvas.create_text(self.width/2, self.height/3+80,
                            fill='firebrick4',
                            text='the Santa Maze Game', 
                            font='Baloo 50')
        # 'Let's Begin' button
        canvas.create_rectangle(self.width/2-150, self.height*2/3-50,
                            self.width/2+150, self.height*2/3+50,
                            fill=self.buttonColor, outline='')
        canvas.create_text(self.width/2, self.height*2/3,
                            fill=self.buttonTextColor,
                            text='Let\'s Begin', 
                            font='Baloo 45')

class FallingSnow(Mode):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def fall(self):
        self.y += 3

class BackgroundScreen(Mode):
    def app_started(self):
        self.snow = []
        self.snowR = 20
        self.count = 0
        self.titleColor = 'gold'
        self.darkGreen = TitleScreen.rgbString(52, 102, 51)
        self.green = TitleScreen.rgbString(89, 156, 93)
        self.homeButtonColor = self.nextButtonColor = self.green
        self.homeButtonTextColor = self.nextButtonTextColor = 'white'
        self.backgroundText = '''It's the last few hours of Christmas Eve, and 
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
        self.background = self.load_image(BACKGROUND_IMAGE_PATH)
        self.backgroundResized = self.scale_image(self.background, 0.5)

    def timer_fired(self):
        self.count += 1
        if (self.count == 20):
            random_x = random.randrange(self.width)
            self.snow.append(FallingSnow(random_x, 0))
            self.count = 0

        for snowball in self.snow:
            snowball.fall()

    def mouse_pressed(self, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            self.app.set_active_mode(self.app.titleScreen)
            self.homeButtonColor = self.green
        elif ((self.width-150 <= event.x <= self.width-50) 
            and (50 <= event.y <= 100)):
            self.app.set_active_mode(self.app.instructionsScreen)
            self.nextButtonColor = self.green
    
    def mouse_moved(self, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            self.homeButtonColor = self.darkGreen
        elif ((self.width-150 <= event.x <= self.width-50) 
            and (50 <= event.y <= 100)):
            self.nextButtonColor = self.darkGreen
        elif (((event.x < 50) or ((event.x > 150) 
            and (event.x < self.width-150)) or (event.x > self.width-50))
            or ((event.y < 50) or (event.y > 100))):
            self.homeButtonColor = self.nextButtonColor = self.green

    def redraw_all(self, canvas):
        # background
        canvas.create_image(self.width/2, self.height/2, 
                            image=ImageTk.PhotoImage(self.backgroundResized))
        # snow
        for snowball in self.snow:
            snow_x, snow_y = snowball.x, snowball.y
            canvas.create_oval(snow_x-self.snowR, snow_y-self.snowR, 
                            snow_x+self.snowR, snow_y+self.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(self.width/2, self.height/10,
                            fill=self.titleColor,
                            text='Background', 
                            font=TITULO_FONTE)
        # 'Home' button
        canvas.create_rectangle(50, 50, 150, 100,
                            fill=self.homeButtonColor,
                            outline='')
        canvas.create_text(100, 75,
                            fill=self.homeButtonTextColor,
                            text='Home', 
                            font=TITULO_FONTE2)
        # 'Next' button
        canvas.create_rectangle(self.width-50, 50, self.width-150, 100,
                            fill=self.nextButtonColor,
                            outline='')
        canvas.create_text(self.width-100, 75,
                            fill=self.nextButtonTextColor,
                            text='Next', 
                            font=TITULO_FONTE2)
        # background text
        canvas.create_text(self.width/2, self.height/2-50,
                            fill='gold',
                            text=self.backgroundText, 
                            font='GB18030Bitmap 15')

class InstructionsScreen(BackgroundScreen):
    def app_started(self):
        self.snow = []
        self.snowR = 20
        self.count = 0
        self.titleColor = 'gold'
        self.darkGreen = TitleScreen.rgbString(52, 102, 51)
        self.green = TitleScreen.rgbString(89, 156, 93)
        self.backButtonColor = self.nextButtonColor = self.green
        self.backButtonTextColor = self.nextButtonTextColor = 'white'
        self.instructionsText = '''Navigate Santa's sleigh through the maze by using the 'Up', 'Down', 
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
        self.background = self.load_image(BACKGROUND_IMAGE_PATH)
        self.backgroundResized = self.scale_image(self.background, 0.5)

    def timer_fired(self):
        self.count += 1
        if (self.count == 20):
            random_x = random.randrange(self.width)
            self.snow.append(FallingSnow(random_x, 0))
            self.count = 0

        for snowball in self.snow:
            snowball.fall()

    def mouse_pressed(self, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            self.app.set_active_mode(self.app.backgroundScreen)
            self.backButtonColor = self.green
        elif ((self.width-150 <= event.x <= self.width-50) 
            and (50 <= event.y <= 100)):
            self.app.set_active_mode(self.app.sleighScreen)
            self.nextButtonColor = self.green
    
    def mouse_moved(self, event):
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            self.backButtonColor = self.darkGreen
        elif ((self.width-150 <= event.x <= self.width-50) 
            and (50 <= event.y <= 100)):
            self.nextButtonColor = self.darkGreen
        elif (((event.x < 50) or ((event.x > 150) 
            and (event.x < self.width-150)) or (event.x > self.width-50))
            or ((event.y < 50) or (event.y > 100))):
            self.backButtonColor = self.nextButtonColor = self.green

    def redraw_all(self, canvas):
        # background
        canvas.create_image(self.width/2, self.height/2, 
                            image=ImageTk.PhotoImage(self.backgroundResized))
        # snow
        for snowball in self.snow:
            snow_x, snow_y = snowball.x, snowball.y
            canvas.create_oval(snow_x-self.snowR, snow_y-self.snowR, 
                            snow_x+self.snowR, snow_y+self.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(self.width/2, self.height/10,
                            fill=self.titleColor,
                            text='Instructions', 
                            font=TITULO_FONTE)
        # 'Back' button
        canvas.create_rectangle(50, 50, 150, 100,
                            fill=self.backButtonColor,
                            outline='')
        canvas.create_text(100, 75,
                            fill=self.backButtonTextColor,
                            text='Back', 
                            font=TITULO_FONTE2)
        # 'Next' button
        canvas.create_rectangle(self.width-50, 50, self.width-150, 100,
                            fill=self.nextButtonColor,
                            outline='')
        canvas.create_text(self.width-100, 75,
                            fill=self.nextButtonTextColor,
                            text='Next', 
                            font=TITULO_FONTE2)
        # instructions text
        canvas.create_text(self.width/2, self.height/2-40,
                            fill='gold',
                            text=self.instructionsText, 
                            font='GB18030Bitmap 12')

class SleighScreen(BackgroundScreen):
    def app_started(self):
        self.snow = []
        self.snowR = 20
        self.count = 0
        self.titleColor = 'gold'
        self.darkGreen = TitleScreen.rgbString(52, 102, 51)
        self.green = TitleScreen.rgbString(89, 156, 93)
        self.backButtonColor = self.nextButtonColor = self.green
        self.backButtonTextColor = self.nextButtonTextColor = 'white'
        self.mode1ButtonColor = self.mode2ButtonColor = self.mode3ButtonColor = self.green
        self.mode1ButtonTextColor = self.mode2ButtonTextColor = self.mode3ButtonTextColor = 'white'
        self.mode1Title = '''                Sleigh 1:
No Presents, Just Vibes'''
        self.mode1Text = '''Santa accidentally forgot 
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
        self.mode2Title = '''         Sleigh 2:
Will Pay To Take'''
        self.mode2Text = '''Santa Will Pay you To Take 
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
        self.mode3Title = '''              Sleigh 3:
2021 Christmas Corvette'''
        self.mode3Text = '''Santa is now “that car guy,” 
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
        self.sleigh1 = self.load_image('sleigh1.png')
        self.sleigh1Resized = self.scale_image(self.sleigh1, 0.1)
        self.sleigh2 = self.load_image('sleigh2.png')
        self.sleigh2Resized = self.scale_image(self.sleigh2, 0.1)
        self.sleigh3 = self.load_image('sleigh3.png')
        self.sleigh3Resized = self.scale_image(self.sleigh3, 0.1)
        self.background = self.load_image(BACKGROUND_IMAGE_PATH)
        self.backgroundResized = self.scale_image(self.background, 0.5)

    def timer_fired(self):
        self.count += 1
        if (self.count == 20):
            random_x = random.randrange(self.width)
            self.snow.append(FallingSnow(random_x, 0))
            self.count = 0

        for snowball in self.snow:
            snowball.fall()
    
    def mouse_moved(self, event):
        buttons = [
            # nomeDoAtributo, x1, y1, x2, y2
            ("backButtonColor", 50, 50, 150, 100),
            ("nextButtonColor", self.width-150, 50, self.width-50, 100),
            ("mode1ButtonColor", self.width/6-80, self.height*9/10-40, self.width/6+80, self.height*9/10+40),
            ("mode2ButtonColor", self.width/2-80, self.height*9/10-40, self.width/2+80, self.height*9/10+40),
            ("mode3ButtonColor", self.width*5/6-80, self.height*9/10-40, self.width*5/6+80, self.height*9/10+40),
        ]

        for attr, x1, y1, x2, y2 in buttons:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                setattr(self, attr, self.darkGreen)
            else:
                setattr(self, attr, self.green)

    def mouse_pressed(self, event):
        # 'Back' button
        if ((50 <= event.x <= 150) and (50 <= event.y <= 100)):
            self.app.set_active_mode(self.app.instructionsScreen)
            self.backButtonColor = self.green
        # 'Home' button
        elif ((self.width-150 <= event.x <= self.width-50) 
            and (50 <= event.y <= 100)):
            self.app.set_active_mode(self.app.titleScreen)
            self.nextButtonColor = self.green
        # 'Play Sleigh 1' button
        elif ((self.width/6-80 <= event.x <= self.width/6+80) 
            and (self.height*9/10-40 <= event.y <= self.height*9/10+40)):
            self.app.timeSec = 0
            self.app.timeMin = 0
            self.app.set_active_mode(self.app.maze) 
            self.mode1ButtonColor = self.green
        # 'Play Sleigh 2' button
        elif ((self.width/2-80 <= event.x <= self.width/2+80) 
            and (self.height*9/10-40 <= event.y <= self.height*9/10+40)):
            self.app.presents = 100
            self.app.set_active_mode(self.app.radiusMode) 
            self.mode2ButtonColor = self.green
        # 'Play Sleigh 3' button
        elif ((self.width*5/6-80 <= event.x <= self.width*5/6+80) 
            and (self.height*9/10-40 <= event.y <= self.height*9/10+40)):
            self.app.presents = 100
            self.app.set_active_mode(self.app.grinchMode) 
            self.mode3ButtonColor = self.green

    def redraw_all(self, canvas):
        # background
        canvas.create_image(self.width/2, self.height/2, 
                            image=ImageTk.PhotoImage(self.backgroundResized))
        # snow
        for snowball in self.snow:
            snow_x, snow_y = snowball.x, snowball.y
            canvas.create_oval(snow_x-self.snowR, snow_y-self.snowR, 
                            snow_x+self.snowR, snow_y+self.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(self.width/2, self.height/10,
                            fill=self.titleColor,
                            text='Choose Your Sleigh', 
                            font=TITULO_FONTE)
        # 'Back' button
        canvas.create_rectangle(50, 50, 150, 100,
                            fill=self.backButtonColor,
                            outline='')
        canvas.create_text(100, 75,
                            fill=self.backButtonTextColor,
                            text='Back', 
                            font=TITULO_FONTE2)
        # 'Home' button
        canvas.create_rectangle(self.width-50, 50, self.width-150, 100,
                            fill=self.nextButtonColor,
                            outline='')
        canvas.create_text(self.width-100, 75,
                            fill=self.nextButtonTextColor,
                            text='Home', 
                            font=TITULO_FONTE2)
        # Sleigh 1
        canvas.create_rectangle(self.width/6-150, self.height/2-20, 
                            self.width/6+130, self.height/2+260,
                            fill='white',
                            outline='')
        canvas.create_rectangle(self.width/6-80, self.height*9/10-40, 
                            self.width/6+80, self.height*9/10+40,
                            fill=self.mode1ButtonColor,
                            outline='')
        canvas.create_text(self.width/6, self.height*9/10,
                            fill=self.mode1ButtonTextColor,
                            text='Sleigh 1', 
                            font=TITULO_FONTE3)
        canvas.create_text(self.width/6, self.height/5,
                            fill='gold',
                            text=self.mode1Title, 
                            font=TITULO_FONTE3)
        canvas.create_text(self.width/6, self.height*3/5+40,
                            fill='black',
                            text=self.mode1Text, 
                            font=TITULO_FONTE4)
        canvas.create_image(self.width/6, self.height*2/5-25, 
                            image=ImageTk.PhotoImage(self.sleigh1Resized))
        # Sleigh 2
        canvas.create_rectangle(self.width/2-150, self.height/2-20, 
                            self.width/2+130, self.height/2+260,
                            fill='white',
                            outline='')
        canvas.create_rectangle(self.width/2-80, self.height*9/10-40, 
                            self.width/2+80, self.height*9/10+40,
                            fill=self.mode2ButtonColor,
                            outline='')
        canvas.create_text(self.width/2, self.height*9/10,
                            fill=self.mode2ButtonTextColor,
                            text='Sleigh 2', 
                            font=TITULO_FONTE3)
        canvas.create_text(self.width/2, self.height/5,
                            fill='gold',
                            text=self.mode2Title, 
                            font=TITULO_FONTE3)
        canvas.create_text(self.width/2, self.height*3/5+40,
                            fill='black',
                            text=self.mode2Text, 
                            font=TITULO_FONTE4)
        canvas.create_image(self.width/2, self.height*2/5-25, 
                            image=ImageTk.PhotoImage(self.sleigh2Resized))
        # Sleigh 3
        canvas.create_rectangle(self.width*5/6-160, self.height/2-20, 
                            self.width*5/6+140, self.height/2+260,
                            fill='white',
                            outline='')
        canvas.create_rectangle(self.width*5/6-80, self.height*9/10-40, 
                            self.width*5/6+80, self.height*9/10+40,
                            fill=self.mode3ButtonColor,
                            outline='')
        canvas.create_text(self.width*5/6, self.height*9/10,
                            fill=self.mode3ButtonTextColor,
                            text='Sleigh 3', 
                            font=TITULO_FONTE3)
        canvas.create_text(self.width*5/6, self.height/5,
                            fill='gold',
                            text=self.mode3Title, 
                            font=TITULO_FONTE3)
        canvas.create_text(self.width*5/6, self.height*3/5+40,
                            fill='black',
                            text=self.mode3Text, 
                            font=TITULO_FONTE4)
        canvas.create_image(self.width*5/6, self.height*2/5-25, 
                            image=ImageTk.PhotoImage(self.sleigh3Resized))

class FinalScreen(SleighScreen):
    def app_started(self):
        self.snow = []
        self.snowR = 20
        self.count = 0
        self.titleColor = 'gold'
        self.darkGreen = TitleScreen.rgbString(52, 102, 51)
        self.green = TitleScreen.rgbString(89, 156, 93)
        self.playAgainButtonColor = self.green
        self.playAgainButtonTextColor = 'white'
        self.homeButtonColor = self.green
        self.homeButtonTextColor = 'white'
        self.background = self.load_image(BACKGROUND_IMAGE_PATH)
        self.backgroundResized = self.scale_image(self.background, 0.5)

    def timer_fired(self):
        self.count += 1
        if (self.count == 20):
            random_x = random.randrange(self.width)
            self.snow.append(FallingSnow(random_x, 0))
            self.count = 0

        for snowball in self.snow:
            snowball.fall()

    def mouse_moved(self, event):
        if ((self.width/2-200 <= event.x <= self.width/2+200) 
            and (self.height*7/10-50 <= event.y <= self.height*7/10+50)):
            self.playAgainButtonColor = self.darkGreen
        elif ((event.x < self.width/2-200) or (event.x > self.width/2+200)
            or (event.y < self.height*7/10-50) 
            or (event.y > self.height*7/10+50)):
            self.playAgainButtonColor = self.green
        if ((self.width/2-50 <= event.x <= self.width/2+50) 
            and (self.height*9/10-25 <= event.y <= self.height*9/10+25)):
            self.homeButtonColor = self.darkGreen
        elif ((event.x < self.width/2-50) or (event.x > self.width/2+50)
            or (event.y < self.height*9/10-25) 
            or (event.y > self.height*9/10+25)):
            self.homeButtonColor = self.green

    def mouse_pressed(self, event):
        # 'Play Again' button
        if ((self.width/2-200 <= event.x <= self.width/2+200) 
            and (self.height*7/10-50 <= event.y <= self.height*7/10+50)):
            self.app.presents = 0
            self.app.set_active_mode(self.app.sleighScreen)
            self.playAgainButtonColor = self.green
        # 'Home' button
        elif ((self.width/2-50 <= event.x <= self.width/2+50) 
            and (self.height*9/10-25 <= event.y <= self.height*9/10+25)):
            self.app.presents = 0
            self.app.set_active_mode(self.app.titleScreen)
            self.homeButtonColor = self.green

    def redraw_all(self, canvas):
        # background
        canvas.create_image(self.width/2, self.height/2, 
                            image=ImageTk.PhotoImage(self.backgroundResized))
        # snow
        for snowball in self.snow:
            snow_x, snow_y = snowball.x, snowball.y
            canvas.create_oval(snow_x-self.snowR, snow_y-self.snowR, 
                            snow_x+self.snowR, snow_y+self.snowR,
                            fill='white',
                            outline='')
        # title
        canvas.create_text(self.width/2, self.height*3/10,
                            fill=self.titleColor,
                            text='Congrats!', 
                            font='Baloo 90')
        canvas.create_text(self.width/2, self.height*4/10,
                            fill=self.titleColor,
                            text=f'You successfully delivered {int(self.app.finalPresents)} presents.', 
                            font='Baloo 40')
        # 'Play Again' button
        canvas.create_rectangle(self.width/2-200, self.height*7/10-50, 
                            self.width/2+200, self.height*7/10+50,
                            fill=self.playAgainButtonColor,
                            outline='')
        canvas.create_text(self.width/2, self.height*7/10,
                            fill=self.playAgainButtonTextColor,
                            text='Play Again', 
                            font='Baloo 40')
        # 'Home' button
        canvas.create_rectangle(self.width/2-50, self.height*9/10-25, 
                            self.width/2+50, self.height*9/10+25,
                            fill=self.homeButtonColor,
                            outline='')
        canvas.create_text(self.width/2, self.height*9/10,
                            fill=self.homeButtonTextColor,
                            text='Home', 
                            font=TITULO_FONTE2)