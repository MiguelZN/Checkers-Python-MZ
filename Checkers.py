from tkinter import *
from PIL import ImageTk,Image
import shelve, time, random, threading, functools,platform,os
from enum import Enum
import simpleaudio as sa

#Current issues:
#MAC:
#1) when leaving current game causes issues (duplicate tabs)
#2) changing the color of board does not work but works on windows
#3) buttonclick.wav does not work with simpleaudio library but works with windows winsound
#4) Return to current game from within game makes a duplicate 'Game Options tab'

#Works when you restart a new game from the current game mode

#operating systems is: 'windows' or 'other' for mac,linux,etc
if('window' in platform.system().lower()):
    OS = 'windows'
    import winsound
else:
    OS = 'other'

SL = "" #contains the slash direction either '\' for windows or '/' for mac,linux,etc
if(OS=='windows'):
    SL = '\\'
else:
    SL = '/'


#PATHS:
PWD_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
IMAGE_DIR = PWD_PATH+SL+'images'
SOUND_DIR = PWD_PATH+SL+'sounds'

# print(IMAGE_DIR)
# print(SOUND_DIR)


def playSound(soundfile:str):
    if (OS == 'windows'):
        winsound.PlaySound(
            SOUND_DIR + SL + soundfile,
            winsound.SND_FILENAME + winsound.SND_ASYNC)

    else:
        ''
        wave_obj = sa.WaveObject.from_wave_file(SOUND_DIR + SL + soundfile)
        play_obj = wave_obj.play()

class checkerpiece():
    def __init__(self, player, selected, row, column, crowned):
        self.__playerowned = player
        self.__isSelected = False
        self.__row = row
        self.__column = column
        self.crowned = crowned #representing that the checkerpiece is not crowned yet
        self.movement = ""
        self.setMovement()

    def setMovement(self):
        if ( self.crowned == True):
            self.movement = "both"
        if ((self.__playerowned=="p1" or self.__playerowned =="cpu") and self.crowned == False):
            self.movement = "down"
        elif((self.__playerowned=="p2" or self.__playerowned=="player") and self.crowned == False):
            self.movement = "up"

    def getCrowned(self):
        return self.crowned
    def Crown(self, iscrowned):
        self.crowned = iscrowned
    def Movement(self, movement):
        self.movement = movement
    def getPlayer(self):
        return self.__playerowned
    def setPlayer(self, player):
        self.__playerowned = player
    def getRow(self):
        return self.__row
    def setRow(self, row):
        self.__row = row
    def getColumn(self):
        return self.__column
    def setColumn(self, column):
        self.__column = column
    def getSelected(self):
        return self.__isSelected

    def unSelect(self):
        self.__isSelected = False

    def Select(self):
        self.__isSelected = True
    def __str__(self):
        return "Row:"+str(self.__row)+" | Column:"+str(self.__column)+" | Player:" + str(self.__playerowned)
#----------------------------------------------------------------------------------------------------------------------------
class Board():
    def createboard(self, rows, columns):
        board = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(checkerpiece(player="E", row=i, column=j, selected = False, crowned= False))
            board.append(row)
        return board

    def addPlayers(self, player1, player2):
        #creates the top
        for i in range(1,len(self.__board),2):
            self.__board[0][i] = checkerpiece(player= player1, row= 0, column= i, selected = False, crowned= False)
        for i in range(0, len(self.__board), 2):
            self.__board[1][i] = checkerpiece(player= player1, row= 1, column= i, selected = False, crowned = False)
        for i in range(1,len(self.__board),2):
            self.__board[2][i] = checkerpiece(player= player1, row= 2, column= i, selected = False, crowned = False)
        #creates the bottom
        for i in range(0, len(self.__board), 2):
            self.__board[len(self.__board) - 3][i] = checkerpiece(player=player2, row=len(self.__board) - 3, column=i, selected = False, crowned = False)
        for i in range(1,len(self.__board),2):
            self.__board[len(self.__board)-2][i] = checkerpiece(player= player2, row= len(self.__board)-2, column= i, selected = False, crowned = False)
        for i in range(0, len(self.__board), 2):
            self.__board[len(self.__board)-1][i] = checkerpiece(player= player2, row= len(self.__board)-1, column= i, selected= False, crowned = False)

    def __init__(self, size, player1, player2):
        self.__board = self.createboard(size, size)
        self.player1 = player1
        self.player2 = player2
        self.addPlayers(player1, player2) # adds the players to the game
        self.__numberofrows = size
        self.__numberofcolumns = size
        self.__sizeofboard = size
        self.isGameUnderway = "None"

    def getPlayer1(self):
        return self.player1
    def getPlayer2(self):
        return self.player2

    def getBoard(self):
        return self.__board

    #prints out checker at specified row/column
    def printChecker(self, row, column):
        print(self.__board[row][column])
    def __str__(self):
        for i in range(self.__sizeofboard):
            for j in range(self.__sizeofboard):
                print(self.__board[i][j])
#----------------------------------------------------------------------------------------------------------------------------
class selected():
    def __init__(self, selectedrow, selectedcolumn):
        self.selectedrow = selectedrow
        self.selectedcolumn = selectedcolumn
    def getRow(self):
        return self.selectedrow
    def getColumn(self):
        return self.selectedcolumn
    def setNewPosn(self, row, column):
        self.selectedrow = row
        self.selectedcolumn = column
#----------------------------------------------------------------------------------------------------------------------------
class CheckersBoardGUI(Frame):
    #This creates the board and appends the colors of the tiles
    def createBoard(self, color1, color2):
        for i in range (len(self.board.getBoard())):
            row = []
            for j in range (len(self.board.getBoard())):
                if (i % 2) == 0 and (j % 2) == 0:
                    row.append(Button(self, width=4, height=2, bg=color1))
                elif (i%2)==0 or (j%2)==0:
                    row.append(Button(self, width = 4, height = 2, bg = color2))
                else:
                    row.append(Button(self,width =4, height=2, bg = color1))
            self.buttonlist.append(row)
        self.showboard(self.buttonlist)
    #This grids all of the buttons to the root and sets the images of the checkers
    def showboard(self, buttonlist):
        for i in range (len(self.board.getBoard())):
            for j in range(len(self.board.getBoard())):
                buttonlist[i][j].grid(row = i, column = j)
                if self.board.getBoard()[i][j].getPlayer()== self.board.getPlayer1() and self.board.getBoard()[i][j].getCrowned()==False:
                    buttonlist[i][j].config(image = self.BLACKCHECKER, height = 35, width =32)


                elif self.board.getBoard()[i][j].getPlayer()==self.board.getPlayer2() and self.board.getBoard()[i][j].getCrowned()==False:
                    buttonlist[i][j].config(image = self.REDCHECKER, height = 35, width = 32)

                elif self.board.getBoard()[i][j].getPlayer()==self.board.getPlayer2() and self.board.getBoard()[i][j].getCrowned()==True:
                    buttonlist[i][j].config(image = self.REDKING, height = 35, width = 32)

                elif self.board.getBoard()[i][j].getPlayer()==self.board.getPlayer1() and self.board.getBoard()[i][j].getCrowned()==True:
                    buttonlist[i][j].config(image = self.BLACKKING, height = 35, width = 32)

                elif self.board.getBoard()[i][j].getPlayer()=="E":
                    buttonlist[i][j].config(image=self.TRANSPARENT, height=35, width=32)

    def __init__(self, root, size, board1color, board2color, board):
        super().__init__(root)
        RedChecker = Image.open(IMAGE_DIR+SL+"redchecker.png")
        RedChecker.thumbnail((30, 30))
        self.REDCHECKER = ImageTk.PhotoImage(RedChecker)

        RedKing = Image.open(IMAGE_DIR+SL+"redking2.png")
        RedKing.thumbnail((30, 30))
        self.REDKING = ImageTk.PhotoImage(RedKing)

        BlackChecker = Image.open(IMAGE_DIR+SL+"blackchecker2.png")
        BlackChecker.thumbnail((30, 30))
        self.BLACKCHECKER = ImageTk.PhotoImage(BlackChecker)

        BlackKing = Image.open(IMAGE_DIR+SL+"blackking2.png")
        BlackKing.thumbnail((30, 30))
        self.BLACKKING = ImageTk.PhotoImage(BlackKing)

        SelectedChecker = Image.open(IMAGE_DIR+SL+"selectedchecker.png")
        SelectedChecker.thumbnail((30, 30))
        self.SELECTEDCHECKER = ImageTk.PhotoImage(SelectedChecker)

        Transparent = Image.open(IMAGE_DIR+SL+"transparent.png")
        SelectedChecker.thumbnail((30, 30))
        self.TRANSPARENT = ImageTk.PhotoImage(Transparent)

        self.size = size
        self.board = board
        self.buttonlist = []
        self.color1 = board1color#color that checkers do not touch
        self.color2 = board2color #color that checkers touch
        self.createBoard(color1= self.color1, color2= self.color2)

    def hideAll(self, listofGUI):
        for i in listofGUI:
            i.grid_remove()
    def Hide(self):
        self.grid_remove()
    def Show(self):
        self.grid()
#----------------------------------------------------------------------------------------------------------------------------
class SettingsGUI(Frame):

    def __init__(self,root, gamewidth, gameheight):
        super().__init__(root, width = gamewidth, height = gameheight+100, bg = "navajowhite3")

        RedChecker = Image.open(IMAGE_DIR+SL+"redchecker.png")
        RedChecker.thumbnail((60, 60))
        self.REDCHECKER = ImageTk.PhotoImage(RedChecker)

        RedKing = Image.open(IMAGE_DIR+SL+"redking2.png")
        RedKing.thumbnail((60, 60))
        self.REDKING = ImageTk.PhotoImage(RedKing)

        BlackChecker = Image.open(IMAGE_DIR+SL+"blackchecker2.png")
        BlackChecker.thumbnail((60, 60))
        self.BLACKCHECKER = ImageTk.PhotoImage(BlackChecker)

        BlackKing = Image.open(IMAGE_DIR+SL+"blackking2.png")
        BlackKing.thumbnail((60, 60))
        self.BLACKKING = ImageTk.PhotoImage(BlackKing)

        SelectedChecker = Image.open(IMAGE_DIR+SL+"selectedchecker.png")
        SelectedChecker.thumbnail((60, 60))
        self.SELECTEDCHECKER = ImageTk.PhotoImage(SelectedChecker)

        self.halfscreenx = int(gamewidth/2)
        self.halfscreeny = int(gameheight/2)


        self.buttonwidth = int(gamewidth/10)
        self.buttonheight = int(gameheight/90)

        self.color1relx = .15
        self.color2relx = .4
        self.Flashingx = .65





        self.Title = Label(self, text = "Settings", font = "none 30 bold")
        self.Title.place(relx = .5, rely=.1, anchor = CENTER)

        self.Options = Label(self, text="Options:", font="none 10 bold")
        self.Options.place(relx=self.Flashingx, rely=.2, anchor=CENTER)

        self.isFlashing = BooleanVar()
        self.isFlashing.set(True)

        self.Flashing = Checkbutton(self, text= "Flash?",variable = self.isFlashing)
        self.Flashing.place(relx = self.Flashingx, rely = .3, anchor =CENTER)


        self.BoardColor1 = Label(self, text = "BoardColor1:", font = "none 10 bold")
        self.BoardColor1.place(relx = self.color1relx, rely = .2, anchor = CENTER)

        self.colorvalue1 = StringVar()
        self.colorvalue1.set("saddle brown")

        self.Color1Radio1 = Radiobutton(self, text="Brown", value = "saddle brown", variable = self.colorvalue1)
        self.Color1Radio1.place(relx = self.color1relx, rely = .3, anchor = CENTER)
        self.Color1Radio2 = Radiobutton(self, text="Dark Gray", value="dark gray", variable=self.colorvalue1)
        self.Color1Radio2.place(relx=self.color1relx, rely=.4, anchor=CENTER)
        self.Color1Radio3 = Radiobutton(self, text="Blue", value="royal blue", variable=self.colorvalue1)
        self.Color1Radio3.place(relx=self.color1relx, rely=.5, anchor=CENTER)
        self.Color1Radio4= Radiobutton(self, text="Green", value="green3", variable=self.colorvalue1)
        self.Color1Radio4.place(relx=self.color1relx, rely=.6, anchor=CENTER)

        self.BoardColor2 = Label(self, text="BoardColor2:", font="none 10 bold")
        self.BoardColor2.place(relx=self.color2relx, rely=.2, anchor=CENTER)

        self.colorvalue2 = StringVar()
        self.colorvalue2.set("tan")

        self.Color2Radio1 = Radiobutton(self, text="Tan", value="tan", variable=self.colorvalue2)
        self.Color2Radio1.place(relx=self.color2relx, rely=.3, anchor=CENTER)

        self.Color2Radio2 = Radiobutton(self, text="Red", value="tomato", variable=self.colorvalue2)
        self.Color2Radio2.place(relx=self.color2relx, rely=.4, anchor=CENTER)

        self.Color2Radio3 = Radiobutton(self, text="Gold", value="yellow2", variable=self.colorvalue2)
        self.Color2Radio3.place(relx=self.color2relx, rely=.5, anchor=CENTER)

        self.Color2Radio4 = Radiobutton(self, text="White", value="snow", variable=self.colorvalue2)
        self.Color2Radio4.place(relx=self.color2relx, rely=.6, anchor=CENTER)

        self.Color1Radio1.select()
        self.Color2Radio1.select()

    def Hide(self):
        self.MAINMENUSELECTED = False
        self.grid_remove()

    def Show(self):
        self.MAINMENUSELECTED = True
        self.grid()
#----------------------------------------------------------------------------------------------------------------------------
class mainMenu(Frame):
    def __init__(self,root, gamewidth, gameheight, listofgui):
        super().__init__(root, width = gamewidth, height = gameheight+100, bg = "navajowhite3")

        RedChecker = Image.open(IMAGE_DIR+SL+"redchecker.png")
        RedChecker.thumbnail((60, 60))
        self.REDCHECKER = ImageTk.PhotoImage(RedChecker)

        RedKing = Image.open(IMAGE_DIR+SL+"redking2.png")
        RedKing.thumbnail((60, 60))
        self.REDKING = ImageTk.PhotoImage(RedKing)

        BlackChecker = Image.open(IMAGE_DIR+SL+"blackchecker2.png")
        BlackChecker.thumbnail((60, 60))
        self.BLACKCHECKER = ImageTk.PhotoImage(BlackChecker)

        BlackKing = Image.open(IMAGE_DIR+SL+"blackking2.png")
        BlackKing.thumbnail((60, 60))
        self.BLACKKING = ImageTk.PhotoImage(BlackKing)

        SelectedChecker = Image.open(IMAGE_DIR+SL+"selectedchecker.png")
        SelectedChecker.thumbnail((60, 60))
        self.SELECTEDCHECKER = ImageTk.PhotoImage(SelectedChecker)

        self.halfscreenx = int(gamewidth/2)
        self.halfscreeny = int(gameheight/2)
        self.guilist = listofgui

        self.MAINMENUSELECTED = True


        self.buttonwidth = int(gamewidth/10)
        self.buttonheight = int(gameheight/90)

        self.listofcheckerimages = [self.BLACKCHECKER,self.REDCHECKER,self.REDKING,self.BLACKKING, self.SELECTEDCHECKER]

        #IMAGES
        self.leftcimage = Label(self, image = random.choice(self.listofcheckerimages))
        self.leftcimage.place(relx= .15, rely=.15, anchor = CENTER)

        self.rightcimage = Label(self, image= random.choice(self.listofcheckerimages))
        self.rightcimage.place(relx=.85, rely=.15, anchor=CENTER)

        self.Title = Label(self, text = "CHECKERS", font = "none 28 bold italic")
        self.Author = Label(self, text= "Python Project- Miguel Zavala", font = "none 8 bold")
        #self.Title.pack(pady= 20)
        self.Title.place(relx = .5, rely=.1, anchor = CENTER)
        self.Author.place(relx=.5, rely=.19, anchor=CENTER)

        self.vsCPU = Button(self, text = "Player vs Computer", bg = "ivory2", height = self.buttonheight, width =self.buttonwidth)
        #self.vsCPU.pack(pady=10)
        self.vsCPU.place(relx = .5, rely= .35, anchor = CENTER)

        self.twoPlayer = Button(self, text = "Player vs Player", bg = "ivory2",height = self.buttonheight, width =self.buttonwidth)
        self.twoPlayer.place(relx= .5, rely = .5, anchor = CENTER)
        #self.twoPlayer.pack(pady=10)

        self.settings = Button(self, text="Settings", bg="ivory2", height=self.buttonheight,
                                width=self.buttonwidth)
        #self.settings.pack(pady=30)
        self.settings.place(relx=.5, rely=.65, anchor=CENTER)


    def updateTitleImages(self):
        if(self.MAINMENUSELECTED == True):
            self.leftcimage.config(image = random.choice(self.listofcheckerimages))
            self.rightcimage.config(image = random.choice(self.listofcheckerimages))


            playSound("checkermove2.wav")

            self.hideAll()


    def hideAll(self):
        self.MAINMENUSELECTED = True
        for i in self.guilist:
            i.grid_remove()
    def selectedTwoPlayer(self, gui):
        gui.grid()
        self.Hide()
    def Hide(self):
        self.MAINMENUSELECTED = False
        self.grid_remove()
    def Show(self):
        self.MAINMENUSELECTED = True
        self.grid()
#----------------------------------------------------------------------------------------------------------------------------
class infoGUI(Frame):
    def updatelabel(self, gametype, currentplayer):
        textcolorcpu = "black"
        textcolorplayer = "red"
        textcolorp1 = "black"
        textcolorp2 = "red"

        currentcolor = "gray"
        labelplayer ="None"


        if (gametype=="pvp"):
            #print("entered")
            if (currentplayer == "p1"):
                #print("entered2")
                labelplayer = "Player1"
                currentcolor = "black"
            elif(currentplayer=="p2"):
                labelplayer = "Player2"
                currentcolor = "red"
        elif (gametype == "cpu"):
            if (currentplayer == "cpu"):
                labelplayer = "Computer"
                currentcolor = "black"
            elif(currentplayer=="player"):
                labelplayer = "Player"
                currentcolor = "red"
        else:
            print("DID NOT SELECT PLAYER")

        self.labelinfo.config(text="Current Turn:\n" + labelplayer, fg=currentcolor)


        #self.labelinfo.place(relx = .5, rely= .5, anchor = CENTER)


#GOOD NOW
    def __init__(self,root, gametype, current):
        RedChecker = Image.open(IMAGE_DIR+SL+"redchecker.png")
        RedChecker.thumbnail((30, 30))
        self.REDCHECKER = ImageTk.PhotoImage(RedChecker)

        RedKing = Image.open(IMAGE_DIR+SL+"redking2.png")
        RedKing.thumbnail((30, 30))
        self.REDKING = ImageTk.PhotoImage(RedKing)

        BlackChecker = Image.open(IMAGE_DIR+SL+"blackchecker2.png")
        BlackChecker.thumbnail((30, 30))
        self.BLACKCHECKER = ImageTk.PhotoImage(BlackChecker)

        BlackKing = Image.open(IMAGE_DIR+SL+"blackking2.png")
        BlackKing.thumbnail((30, 30))
        self.BLACKKING = ImageTk.PhotoImage(BlackKing)

        SelectedChecker = Image.open(
            IMAGE_DIR+SL+"selectedchecker.png")
        SelectedChecker.thumbnail((30, 30))
        self.SELECTEDCHECKER = ImageTk.PhotoImage(SelectedChecker)

        Transparent = Image.open(
            IMAGE_DIR+SL+"transparent.png")
        SelectedChecker.thumbnail((30, 30))
        self.TRANSPARENT = ImageTk.PhotoImage(Transparent)

        self.textcolor = "gray"
        self.gametype = gametype
        self.currentturn = current

        #Handles the two gamemodes
        if gametype=="pvp":
            if (self.currentturn == "p1"):
                self.currentturn = "Player1"
                self.textcolor = "black"
            else:
                self.currentturn = "Player2"
                self.textcolor = "red"
        elif gametype == "cpu":
            if (current == "cpu"):
                self.currentturn = "Computer"
                self.textcolor = "black"
            else:
                self.currentturn = "Player"
                self.textcolor = "red"
        else:
            self.currentturn = "None"
            self.textcolor = "gray"

        super().__init__(root,width= 100, height = 350)

        self.labelinfo = Label(self, text = "Current Turn:\n"+self.currentturn, font = "none 10 bold", fg = self.textcolor, anchor = N)
        self.labelinfo.place(relx = .5, rely = .5, anchor =CENTER)


        #SHOWCASES HOW MUCH EACH PLAYER HAS TAKEN FROM THE OTHER PLAYER
        self.HoldTakenRed = Frame(self)
        self.numberTakenRed = Label(self.HoldTakenRed, text ="x0", font = "none 10 bold")
        self.HoldImageRed = Label(self.HoldTakenRed, image=self.REDCHECKER)
        self.numberTakenRed.grid(row= 0, column=0)
        self.HoldImageRed.grid(row=0, column=1)
        self.HoldTakenRed.place(relx = .5, rely =.2, anchor = CENTER)

        self.HoldTakenBlack = Frame(self)
        self.numberTakenBlack = Label(self.HoldTakenBlack, text="x0",font= "none 10 bold")
        self.HoldImageBlack = Label(self.HoldTakenBlack, image = self.BLACKCHECKER)
        self.numberTakenBlack.grid(row= 0, column = 0)
        self.HoldImageBlack.grid(row = 0, column = 1)
        self.HoldTakenBlack.place(relx=.5, rely=.8, anchor=CENTER)


    def updateLabels(self, amount1, amount2):
        self.numberTakenRed.config(text = "x"+str(amount1))
        self.numberTakenBlack.config(text = "x"+str(amount2))




class game():





    def PlayCPUTurn(self):
        if(self.isGameUnderway=="cpu" and self.current=="cpu"):
            #these go first
            prioritymoves = []

            self.board = self.cpuboard

            #these go second
            simplemoves = []
            #time.sleep(2)

            for i in range (len(self.board.getBoard())):
                for j in range(len(self.board.getBoard())):
                    boardlength = len(self.board.getBoard())-1

                    currenttile = self.board.getBoard()[i][j]
                    currenttilerow = currenttile.getRow()
                    currenttilecolumn = currenttile.getColumn()

                    print("ROW:"+str(currenttilerow))
                    print("COLUMN:"+str(currenttilecolumn))


                    onerowdown = currenttilerow+1
                    tworowsdown = currenttilerow+2

                    onerowup = currenttilerow-1
                    tworowsup = currenttilerow-2

                    onecolumnright = currenttilecolumn+1
                    twocolumnsright = currenttilecolumn+2

                    onecolumnleft = currenttilecolumn-1
                    twocolumnsleft = currenttilecolumn-2

                    crowned = currenttile.getCrowned()

                    bottomlefttile = ""
                    bottomleftexists = False
                    twodowntwolefttile = ""
                    twodowntwoleftexists = False

                    bottomrighttile = ""
                    bottomrightexists = False
                    twodowntworighttile = ""
                    twodowntworightexists = False

                    toplefttile = ""
                    topleftexists = False
                    twouptwolefttile = ""
                    twouptwoleftexists = False

                    toprighttile = ""
                    toprightexists = False
                    twouptworighttile = ""
                    twouptworightexists = False

                    howmanyplayersleft = self.CheckHowMany("left", i, j, "player",
                                                           self.cpuboard)
                    howmanyplayersright = self.CheckHowMany("right", i, j, "player",
                                                            self.cpuboard)
                    howmanyplayersabove = self.CheckHowMany("above", i, j, "player",
                                                            self.cpuboard)
                    howmanyplayersbelow = self.CheckHowMany("below", i, j, "player",
                                                            self.cpuboard)

                    print("playerright:" + str(howmanyplayersright))
                    print("playerleft:" + str(howmanyplayersleft))
                    print("playerabove:" + str(howmanyplayersabove))
                    print("playerbelow:" + str(howmanyplayersbelow))

                    #if the bottomleft tile exists
                    if(onerowdown<=boardlength and onecolumnleft>=0):
                        bottomlefttile = self.board.getBoard()[onerowdown][onecolumnleft]
                        bottomleftexists = True
                    #if the bottomright tile exists
                    if(onerowdown<=boardlength and onecolumnright<=boardlength):
                        bottomrighttile = self.board.getBoard()[onerowdown][onecolumnright]
                        bottomrightexists = True
                    if(tworowsdown<=boardlength and twocolumnsleft>=0):
                        twodowntwolefttile = self.board.getBoard()[tworowsdown][twocolumnsleft]
                        twodowntwoleftexists = True
                    if (tworowsdown <= boardlength and twocolumnsright<=boardlength):
                        twodowntworighttile = self.board.getBoard()[tworowsdown][twocolumnsright]
                        twodowntworightexists = True

                    if(onerowup>=0 and onecolumnleft>=0):
                        toplefttile = self.board.getBoard()[onerowup][onecolumnleft]
                        topleftexists = True
                    if(onerowup>=0 and onecolumnright<=boardlength):
                        toprighttile = self.board.getBoard()[onerowup][onecolumnright]
                        toprightexists = True
                    if(tworowsup>=0 and twocolumnsleft>=0):
                        twouptwolefttile = self.board.getBoard()[tworowsup][twocolumnsleft]
                        twouptwoleftexists = True
                    if(tworowsup>=0 and twocolumnsright<=boardlength):
                        twouptworighttile = self.board.getBoard()[tworowsup][twocolumnsright]
                        twouptworightexists = True



                    #Checks the non-crowned
                    if(currenttile.getPlayer()=="cpu" and crowned == False and onerowdown<=boardlength):
                        if(bottomleftexists):
                            #onerowdown, onecolumnleft
                            #adds a rowdown,left simple move
                            if(bottomlefttile.getPlayer()=="E"):
                                simplemoves.append([(onerowdown,onecolumnleft),(currenttilerow,currenttilecolumn),crowned])
                            if(bottomlefttile.getPlayer()=="player" and twodowntwoleftexists):
                                #adds a tworowsdown, twoleft priority move
                                if(twodowntwolefttile.getPlayer()=="E"):
                                    prioritymoves.append([(tworowsdown,twocolumnsleft),(currenttilerow,currenttilecolumn),(onerowdown,onecolumnleft),crowned])
                        if (bottomrightexists):
                            # onerowdown, onecolumnleft
                            # adds a rowdown,left simple move
                            if (bottomrighttile.getPlayer() == "E"):
                                simplemoves.append([(onerowdown, onecolumnright),(currenttilerow,currenttilecolumn),crowned])
                            if (bottomrighttile.getPlayer() == "player" and twodowntworightexists):
                                # adds a tworowsdown, tworight priority move
                                if (twodowntworighttile.getPlayer() == "E"):
                                    prioritymoves.append([(tworowsdown, twocolumnsright),(currenttilerow,currenttilecolumn),(onerowdown,onecolumnright),crowned])


                    #CROWNED MOVES
                    playeramountleft = self.CheckSingleUserAmount(self.cpuboard, "player")



                    playerthreshold = 4 #set to 0 to do all simple moves

                    if(crowned==True and onerowdown<=boardlength and currenttile.getPlayer()=="cpu"):
                        print("entered crowned bottom")
                        if (bottomleftexists):
                            # onerowdown, onecolumnleft
                            # adds a rowdown,left simple move

                            if (bottomlefttile.getPlayer() == "E" and howmanyplayersabove <= howmanyplayersbelow and howmanyplayersleft >= howmanyplayersright):
                                simplemoves.append(
                                    [(onerowdown, onecolumnleft), (currenttilerow, currenttilecolumn), crowned])
                            #if (bottomlefttile.getPlayer() == "E"):
                            #    simplemoves.append([(onerowdown, onecolumnleft),(currenttilerow,currenttilecolumn),crowned])





                            if (bottomlefttile.getPlayer() == "player" and twodowntwoleftexists):
                                # adds a tworowsdown, twoleft priority move
                                if (twodowntwolefttile.getPlayer() == "E"):
                                    prioritymoves.append([(tworowsdown, twocolumnsleft),(currenttilerow,currenttilecolumn),(onerowdown,onecolumnleft),crowned])
                        if (bottomrightexists):

                            if (bottomrighttile.getPlayer() == "E" and howmanyplayersabove <= howmanyplayersbelow and howmanyplayersleft <= howmanyplayersright):
                                simplemoves.append(
                                    [(onerowdown, onecolumnright), (currenttilerow, currenttilecolumn), crowned])
                            # onerowdown, onecolumnleft
                            # adds a rowdown,left simple move
                           # if (bottomrighttile.getPlayer() == "E"):
                           #     simplemoves.append([(onerowdown, onecolumnright),(currenttilerow,currenttilecolumn),crowned])

                            if (bottomrighttile.getPlayer() == "player" and twodowntworightexists):
                                # adds a tworowsdown, twoleft priority move
                                if (twodowntwolefttile.getPlayer() == "E"):
                                    prioritymoves.append([(tworowsdown, twocolumnsright),
                                                         (currenttilerow, currenttilecolumn),
                                                         (onerowdown, onecolumnright),crowned])


                    #CROWNED UPMOVES
                    if (crowned == True and onerowup >= 0 and currenttile.getPlayer()=="cpu"):
                        print("entered crowned top")
                        if(topleftexists):

                            print("entered topleftexists")
                            # SMART MOVEMENT
                            if(toplefttile.getPlayer()=="E" and howmanyplayersabove>=howmanyplayersbelow and howmanyplayersleft>=howmanyplayersright):
                                print("entered simplemove upleft")
                                simplemoves.append(
                                    [(onerowup, onecolumnleft), (currenttilerow, currenttilecolumn), crowned])
                            #elif (toplefttile.getPlayer()=="E"):
                            #    simplemoves.append(
                            #        [(onerowup, onecolumnleft), (currenttilerow, currenttilecolumn), crowned])

                            if(toplefttile.getPlayer()=="player" and twouptwoleftexists):
                                if(twouptwolefttile.getPlayer()=="E"):
                                    prioritymoves.append([(tworowsup,twocolumnsleft),(currenttilerow,currenttilecolumn),(onerowup,onecolumnleft),crowned])
                        if (toprightexists):
                            #SMART MOVEMENT
                            if (toprighttile.getPlayer() == "E" and howmanyplayersabove >= howmanyplayersbelow and howmanyplayersright>=howmanyplayersleft):
                                simplemoves.append(
                                    [(onerowup, onecolumnright), (currenttilerow, currenttilecolumn), crowned])
                            #elif (toprighttile.getPlayer() == "E" ):
                             #   simplemoves.append([(onerowup, onecolumnright),(currenttilerow,currenttilecolumn),crowned])


                            if (toprighttile.getPlayer() == "player" and twouptworightexists):
                                if (twouptworighttile.getPlayer() == "E"):
                                    prioritymoves.append([(tworowsup, twocolumnsright),(currenttilerow,currenttilecolumn),(onerowup,onecolumnright),crowned])

            self.prioritymoves = prioritymoves
            self.simplemoves = simplemoves


            cpuselected = ""
            #PRIORITY MOVE:
            if(len(prioritymoves)>0):
                prioritymove = random.choice(self.prioritymoves)
                cpuselected = prioritymove[0]
                currenttuple = prioritymove[1]
                playertile = prioritymove[2]


                self.selected.setNewPosn(cpuselected[0],cpuselected[1])
                self.board.getBoard()[currenttuple[0]][currenttuple[1]].setPlayer("E")
                self.board.getBoard()[currenttuple[0]][currenttuple[1]].Crown(False)
                self.board.getBoard()[currenttuple[0]][currenttuple[1]].movement = ""

                self.board.getBoard()[playertile[0]][playertile[1]].setPlayer("E")
                self.board.getBoard()[playertile[0]][playertile[1]].Crown(False)
                self.board.getBoard()[playertile[0]][playertile[1]].movement = ""

                self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].setPlayer("cpu")
                self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].Crown(prioritymove[3])

                if(prioritymove[3]==True):
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].movement = "both"
                else:
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].movement = "down"

                if (self.selected.getRow() == boardlength):
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].Crown(True)
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].movement="both"

                print("COMPUTERTILE")
                print(self.board.getBoard()[currenttuple[0]][currenttuple[1]].getPlayer())
                print(self.board.getBoard()[currenttuple[0]][currenttuple[1]].getCrowned())
                print(self.board.getBoard()[currenttuple[0]][currenttuple[1]].movement)
                print(topleftexists)
                print(toprightexists)

                self.newTurn()
            elif(len(simplemoves)>0):
                simplemove = random.choice(self.simplemoves)
                cpuselected = simplemove[0]
                currenttuple = simplemove[1]

                self.board.getBoard()[currenttuple[0]][currenttuple[1]].setPlayer("E")
                self.board.getBoard()[currenttuple[0]][currenttuple[1]].Crown(False)
                self.board.getBoard()[currenttuple[0]][currenttuple[1]].movement = "down"

                self.selected.setNewPosn(cpuselected[0],cpuselected[1])
                self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].setPlayer("cpu")
                self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].Crown(simplemove[2])

                if(simplemove[2]==False):
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].movement = "down"
                else:
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].movement = "both"

                if(self.selected.getRow()==boardlength):
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].Crown(True)
                    self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].movement= "both"

                self.newTurn()

            else:
                print("CPU SELECTION ERROR")



    def isValidMove(self, tuple):
        isValid  = False
        spotmovingto = self.board.getBoard()[tuple[0]][tuple[1]]
        currentspot = self.selected
        boardlength = len(self.board.getBoard())

        onerowdown = currentspot.getRow()+1# goingdown physically
        onerowup = currentspot.getRow()-1 #goingup physically
        onecolumnleft = currentspot.getColumn()-1 #goingleft physically
        onecolumnright = currentspot.getColumn()+1 #going right physically

        tworowsdown = currentspot.getRow()+2
        tworowsup = currentspot.getRow() - 2
        twocolumnsright = currentspot.getColumn()+2
        twocolumnsleft = currentspot.getColumn()-2

        movement = self.board.getBoard()[currentspot.getRow()][currentspot.getColumn()].movement
        iscrowned = self.board.getBoard()[currentspot.getRow()][currentspot.getColumn()].getCrowned()
        player = self.board.getBoard()[currentspot.getRow()][currentspot.getColumn()].getPlayer()

        #(self.board.getBoard()[onerowup][onecolumnleft].movement == "down" and spotmovingto.getRow() == tworowsup and spotmovingto.getColumn() == twocolumnleft)
        print(onerowdown)
        #(onerowdown<=boardlength and onerowup>=0 and onecolumnright <=boardlength and onecolumnleft>=0)


        if (self.board.getBoard()[tuple[0]][tuple[1]].getPlayer()== self.current):
            return True


        if((spotmovingto.getRow() == tworowsup or spotmovingto.getRow()== tworowsdown) and (spotmovingto.getColumn() ==twocolumnsright or spotmovingto.getColumn()==twocolumnsleft) and (self.board.getBoard()[spotmovingto.getRow()][spotmovingto.getColumn()].getPlayer()=="E")):
            print("ENTERED1")
            if(movement=="down"):
                if((spotmovingto.getColumn()==twocolumnsright and spotmovingto.getRow()==tworowsdown)and self.board.getBoard()[onerowdown][onecolumnright].getPlayer()!="E" \
                        and self.board.getBoard()[onerowdown][onecolumnright].getPlayer() != self.current):
                    self.board.getBoard()[onerowdown][onecolumnright].setPlayer("E")
                    self.board.getBoard()[onerowdown][onecolumnright].Crown(False)
                    isValid =True
                elif ((spotmovingto.getColumn() == twocolumnsleft and spotmovingto.getRow()==tworowsdown) and self.board.getBoard()[onerowdown][onecolumnleft].getPlayer() != self.current \
                      and self.board.getBoard()[onerowdown][onecolumnleft].getPlayer() != "E"):
                    self.board.getBoard()[onerowdown][onecolumnleft].setPlayer("E")
                    self.board.getBoard()[onerowdown][onecolumnleft].Crown(False)
                    isValid = True
            elif(movement=="up"):
                if ((spotmovingto.getColumn() == twocolumnsright and spotmovingto.getRow() == tworowsup) and self.board.getBoard()[onerowup][onecolumnright].getPlayer() != self.current \
                        and self.board.getBoard()[onerowup][onecolumnright].getPlayer() != "E"):
                    self.board.getBoard()[onerowup][onecolumnright].setPlayer("E")
                    self.board.getBoard()[onerowup][onecolumnright].Crown(False)
                    isValid = True
                elif ((spotmovingto.getColumn() == twocolumnsleft  and spotmovingto.getRow() == tworowsup) and self.board.getBoard()[onerowup][onecolumnleft].getPlayer() != self.current \
                      and self.board.getBoard()[onerowup][onecolumnleft].getPlayer() != "E"):
                    self.board.getBoard()[onerowup][onecolumnleft].setPlayer("E")
                    self.board.getBoard()[onerowup][onecolumnleft].Crown(False)
                    isValid = True
            #KING
            #elif(self.isGameUnderway=="cpu" and self.current=="player"):

            elif(movement == "both" or iscrowned==True or (player=="player" and currentspot.getRow()==0)):

                if(spotmovingto.getColumn() == twocolumnsright or spotmovingto.getColumn() == twocolumnsleft):
                    isValid = True
                    newrow = spotmovingto.getRow()
                    newcolumn = spotmovingto.getColumn()
                    currentrow = currentspot.getRow()
                    currentcolumn = currentspot.getColumn()

                    if(newrow<currentrow and newcolumn<currentcolumn):
                        self.board.getBoard()[onerowup][onecolumnleft].setPlayer("E")
                        self.board.getBoard()[onerowup][onecolumnleft].Crown(False)
                        self.board.getBoard()[onerowup][onecolumnleft].movement = ""
                    elif(newrow<currentrow and newcolumn>currentcolumn):
                        self.board.getBoard()[onerowup][onecolumnright].setPlayer("E")
                        self.board.getBoard()[onerowup][onecolumnright].Crown(False)
                        self.board.getBoard()[onerowup][onecolumnright].movement = ""
                    elif(newrow>currentrow and newcolumn<currentcolumn):
                        self.board.getBoard()[onerowdown][onecolumnleft].setPlayer("E")
                        self.board.getBoard()[onerowdown][onecolumnleft].Crown(False)
                        self.board.getBoard()[onerowdown][onecolumnleft].movement = ""
                    elif(newrow>currentrow and newcolumn>currentcolumn):
                        self.board.getBoard()[onerowdown][onecolumnright].setPlayer("E")
                        self.board.getBoard()[onerowdown][onecolumnright].Crown(False)
                        self.board.getBoard()[onerowdown][onecolumnright].movement=""



    #p2 (bottom player)
        if(movement=="up" and ((spotmovingto.getRow()== onerowup)and (spotmovingto.getColumn() == onecolumnleft or spotmovingto.getColumn() == onecolumnright))):
            isValid = True
            print("up isValid")

        elif (movement == "down" and ((spotmovingto.getRow() == onerowdown) and (
                spotmovingto.getColumn() == onecolumnleft or spotmovingto.getColumn() == onecolumnright))):
            isValid = True
            print("down isValid")

        elif ((currentspot.getRow==0 and self.board.getBoard()[currentspot.getRow()][currentspot.getColumn()])or(iscrowned or movement=="both") and ((spotmovingto.getRow()== onerowdown) or (spotmovingto.getRow() == onerowup))and ((spotmovingto.getColumn() == onecolumnleft) or (spotmovingto.getColumn() == onecolumnright))):
            isValid = True
        elif (self.selected.getRow()==-1):
            print("start")
            return True
        else:
            print(tuple[0], tuple[1])
            print(self.selected.getRow(), self.selected.getColumn())

        return isValid

    def checkWinner(self):
        user1pieces = 0
        user2pieces = 0
        for i in range(len(self.board.getBoard())):
            for j in range(len(self.board.getBoard())):
                if(self.board.getBoard()[i][j].getPlayer()=="p1"):
                    user1pieces+=1
                elif(self.board.getBoard()[i][j].getPlayer()=="p2"):
                    user2pieces+=1
        if (user1pieces>0 and user2pieces<=0):
            return "p1"
        elif(user2pieces>0 and user1pieces<=0):
            return "p2"
        else:
            return "None"

    def playturn(self, tuple):

        if (self.isValidMove(tuple) == True):
            self.makeselection(tuple)
            print("valid move")

        else:
            print("invalid move")
            print(self.isGameUnderway)
            print("CURRENT")
            print(self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].getPlayer())
            print(self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].getCrowned())
            print(self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].movement)
            print("MOVINGTO")
            print(self.board.getBoard()[tuple[0]][tuple[1]].getPlayer())
            print(self.board.getBoard()[tuple[0]][tuple[1]].getCrowned())
            print(self.board.getBoard()[tuple[0]][tuple[1]].movement)

            return None
    #tuple is (row,column): the button at tuple[0] ROW and tuple[1] COLUMN the user clicked
    def makeselection(self, tuple):

        #if its a valid move goes through the rest of the method else returns False and should stop the program
       #if((self.selectedchecker.movement=="up") and ((tuple[0] != self.selectedchecker.getRow()+1) and (tuple[1] !=  self.selectedchecker.getColumn()-1 or tuple[1] != self.selectedchecker.getColumn()+1)))
        if (self.selected.getRow() == tuple[0] and self.selected.getColumn()==tuple[1]):
            print("unselected tile")
            #sets the selected position to one which does not exist in the board
            self.selected.setNewPosn(-1,-1)

        #Means if the tile that the player selects is empty, and it's the current player's turn, place the tile in the place the player selected
        elif (self.board.getBoard()[tuple[0]][tuple[1]].getPlayer() == "E" and self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()].getPlayer()== self.current):

            currentrow = self.selected.getRow()  #the old row
            currentcolumn = self.selected.getColumn() #the old column

            #the New location where the user clicked at
            newrow = tuple[0]
            newcolumn = tuple[1]

            #currenttile attributes
            currentplayer = self.board.getBoard()[currentrow][currentcolumn].getPlayer()
            currentcrowned = self.board.getBoard()[currentrow][currentcolumn].getCrowned()

            #movement is determined on the creation of checkerpiece based on whether it is crowned or not and on which player it is
            currentplayer = self.current

            #sets the old checker location as a blank tile
            self.board.getBoard()[currentrow][currentcolumn] = checkerpiece("E",False,currentrow,currentcolumn, crowned= False)
            #print("CREATED")

            #if its a VALID MOVE DO (checks if it moved only by one row and :
            #Does not move checker only tells program where the selected disk should flash at****
            self.selected.setNewPosn(newrow,newcolumn)
            currentrow = newrow
            currentcolumn = newcolumn

            #----
            #METHODS BELOW MOVE THE CHECKER ON PROGRAMMED BOARD and LATER IT IS DRAWN
            #Crowns the player2 checker if it reaches the end of board
            if(currentrow == 0 and (currentplayer==self.player2 or currentplayer==self.computer)):
                self.board.getBoard()[currentrow][currentcolumn] = checkerpiece(currentplayer, True, currentrow, currentcolumn,
                                                                                True)
               # print("p2 was crowned")
                #print(self.board.getBoard()[currentrow][currentcolumn].movement)

            #Crowns the player1 checker if it reaches the end of board
            elif(currentrow == len(self.board.getBoard())-1 and (currentplayer==self.player1 or currentplayer==self.player)):
                self.board.getBoard()[currentrow][currentcolumn] = checkerpiece(currentplayer, True, currentrow,
                                                                                currentcolumn,True)
                #print("p1 was crowned")
                #print(self.board.getBoard()[currentrow][currentcolumn].movement)

            #Moves the crowned checker making sure it stays crowned
            elif(currentcrowned==True or self.board.getBoard()[currentrow][currentcolumn].getCrowned()==True):
                self.board.getBoard()[currentrow][currentcolumn] = checkerpiece(currentplayer, True, currentrow,
                                                                                currentcolumn,
                                                                                True)
                #print("moved Crowned checker")
                #print(self.board.getBoard()[currentrow][currentcolumn].movement)

            #Means: if the checker has not reached the end it can only move in one direction ("up"/"down") and it is not crowned
            else:
                self.board.getBoard()[currentrow][currentcolumn] = checkerpiece(currentplayer, True, currentrow, currentcolumn,
                                                                                False)
                #print("moved False checker")
                print(self.board.getBoard()[currentrow][currentcolumn].movement)
            #print(self.board.getBoard()[currentrow][currentcolumn].getCrowned())




            if(currentrow==0):
                self.board.getBoard()[currentrow][currentcolumn].Crown(True)

            self.newTurn()
            #self.CheckersBoardGUI.createBoard(self.CheckersBoardGUI.color1, self.CheckersBoardGUI.color2)

            #GOOD
        elif (self.board.getBoard()[tuple[0]][tuple[1]].getPlayer()== self.current):
            self.selected.setNewPosn(tuple[0],tuple[1])
            # PLACE isVALID METHOD HERE------------- Because if it's a valid move(available emtpy spot) it selects the position


        playSound("checkermove2.wav")

        #self.board.getBoard()[tuple[0]][tuple[1]].Select()
        #print("Selected: Row:"+str(self.selected.getRow())+",Column:"+str(self.selected.getColumn()))
        #place the sound here and the isVALID statement and what occurs if it is valid in this function

    def appendButtons(self):
        for i in range(len(self.board.getBoard())):
            for j in range(len(self.board.getBoard())):
                if (i % 2) == 0 and (j % 2) == 0:
                    None
                elif (i%2)==0 or (j%2)==0:

                    #functool.partial(function, itsarguments....) > lambda
                    self.CheckersBoardGUI.buttonlist[i][j].config(command = functools.partial(self.playturn, (i,j)))

                else:
                    None

    #Makes the selected tile blink yellow
    def placeSelection(self):
        if(self.SettingsGUI.isFlashing.get()==False):
            return None
        selectedchecker = self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()]
        if (self.selected.getRow()==-1) and (self.selected.getColumn()==-1):
            #print("none")
            return None
        if (True):
            selectedchecker.Select()
            self.CheckersBoardGUI.buttonlist[self.selected.getRow()][self.selected.getColumn()].config(
                image=self.CheckersBoardGUI.SELECTEDCHECKER)


    #sets the yellow selected tile to normal after tick
    def reUpdate(self):
        self.CheckersBoardGUI.createBoard(self.CheckersBoardGUI.color1, self.CheckersBoardGUI.color2)

        if (self.selected.getRow() == "") and (self.selected.getColumn() == ""):
            #print("none")
            return None

    def decidewhogoes(self, gametype):

        if(gametype == "pvp"):
            first = random.choice(("p1","p2"))
        elif(gametype == "cpu"):
            first = random.choice(("cpu","player"))
        return first

    def newTurn(self):
        if(self.isGameUnderway=="pvp"):
            if(self.current==self.player1):
                self.current = self.player2
            else:
                self.current = self.player1
        elif(self.isGameUnderway=="cpu"):
            if(self.current==self.computer):
                self.current=self.player
            else:
                self.current = self.computer

    def getSeconds(self):
        return self.gametime[0]

    def getMinutes(self):
        return self.gametime[1]

    def getHours(self):
        return self.gametime[2]

    def updateTime(self):
        self.timelabel.config(text ="Time:"+str(self.getSeconds())+"s,"+str(self.getMinutes())+"m,"+str(self.getHours())+"hr", font = "none 10 bold",fg="blue" )
        self.timelabel.pack(side=TOP, padx=10, pady=10, anchor=S)
        self.timelabel.pack_propagate(0)




    def __init__(self):
        #PVP
        self.player1 = "p1"
        self.player2 = "p2"
        self.pvpboard = Board(size=8, player1=self.player1, player2=self.player2)
        self.score1 = 0 #player1score
        self.p1obtained = 0
        self.p2obtained = 0
        self.isWinnerPvP = ""
        self.player1amount= self.CheckSingleUserAmount(self.pvpboard,self.player1)
        self.player2amount = self.CheckSingleUserAmount(self.pvpboard,self.player2)
        self.numberofgames = 0
        self.gametime = [0, 0, 0]  # seconds, minutes, hours
        self.size = 8 #size of board
        self.selectedPVP = selected(-1,-1)


        #CPU
        self.computer = "cpu"
        self.player = "player"

        #CPUMOVES
        self.prioritymoves = []
        self.simplemoves = []

        self.cpuboard = Board(size=8, player1=self.computer, player2=self.player)
        self.cpuobtained = 0
        self.playerobtained = 0
        self.cpuamount = self.CheckSingleUserAmount(self.cpuboard,self.computer)
        self.playeramount = self.CheckSingleUserAmount(self.cpuboard,self.player)
        self.isWinnerCpu = ""

        self.numberofgames = 0
        self.gametime = [0, 0, 0]  # seconds, minutes, hours
        self.size = 8  # size of board
        self.selectedCPU = selected(-1,-1)


        #NEUTRAL
        self.board = ""
        self.selected = "" #user has not selected anything yet
        self.current = ""
        self.selectedchecker = ""
        self.isGameUnderway= ""


        #sounds
        #winsound.PlaySound(r"C:\Users\Miguel\Desktop\EGGG\CISC108\FinishedProjects\Checkers\buttonclick.wav",winsound.SND_FILENAME)

        #GUI
        self.gameheight = 400
        self.gamewidth = 450
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.geometry(str(self.gamewidth)+"x"+str(self.gameheight))
        self.root.minsize(self.gamewidth,self.gameheight)
        self.root.maxsize(self.gamewidth,self.gameheight)
        self.root.title("Checkers - Miguel Zavala")
        self.root.iconbitmap(IMAGE_DIR+SL+"checkerslogo.ico")
        self.root.grid()

        self.optionsTab = Menu()
        self.gameOptionsTab = Menu()
        self.root.config(menu = self.optionsTab)

        self.subOptionsTab = Menu()
        self.optionsTab.add_cascade(menu = self.subOptionsTab, label = "Navigate")

        self.subOptionsTab.add_cascade(label = "Go to MainMenu", command = self.gotoMainMenu)
        self.subOptionsTab.add_cascade(label = "Go to Settings", command = self.SettingsSelected)

        self.infolabel = ""
        self.timelabel = Label(self.infolabel, text="Time:0s,0m,0hr", font="none 10 bold", fg="blue", wraplength=150,
                               width=13)

        self.SettingsGUI = SettingsGUI(self.root, self.gamewidth, self.gameheight)

        self.CheckersGUIPVP = CheckersGUI(self.root)
        self.CheckersGUICPU = CheckersGUI(self.root)

        self.board1color = self.SettingsGUI.colorvalue1.get()
        self.board2color = self.SettingsGUI.colorvalue2.get()

        self.CheckersBoardGUI = ""
        #self.CheckersBoardGUICPU = ""
        #self.CheckersBoardGUICPU = CheckersBoardGUI(self.CheckersGUICPU, size= self.size,board= self.board, board1color=self.board1color, board2color=self.board2color)
        #self.CheckersBoardGUICPU.grid(row=1, column=1, pady=20)







        self.guilist = [self.CheckersGUIPVP,self.CheckersGUICPU]

        self.mainMenu = mainMenu(self.root, self.gamewidth,self.gameheight, self.guilist)
        self.mainMenu.twoPlayer.config(command = self.TwoPlayerButtonSelected)
        self.mainMenu.settings.config(command = self.SettingsSelected)
        self.mainMenu.vsCPU.config(command = self.SelectedvsCPU)

        self.mainMenu.Show()

        #self.appendButtons()
        self.winner = ""

        self.run()

    def gotoMainMenu(self):
        playSound("checkermove2.wav")

        for i in self.guilist:
            i.grid_remove()
        self.mainMenu.Show()
        self.optionsTab.delete(2)
        self.optionsTab.delete(1)
    def ReturnToGame(self):
        self.optionsTab.delete(1)
        self.optionsTab.delete(2)
        if(self.isGameUnderway=="pvp"):
            self.createGameOptionsTab(self.createNewGame)
            self.mainMenu.Hide()
            self.SettingsGUI.Hide()
            self.CheckersGUICPU.Hide()
            self.updateColor(self.CheckersGUIPVP) #self.updateColor(("pvp"/"cpu"), self.CheckersGUIPVP/self.CheckersGUICPU)
            self.CheckersGUIPVP.Show()
        elif(self.isGameUnderway=="cpu"):
            self.createGameOptionsTab(self.createNewGame)
            self.mainMenu.Hide()
            self.SettingsGUI.Hide()
            self.CheckersGUIPVP.Hide()
            self.updateColor(self.CheckersGUICPU)  # self.updateColor(("pvp"/"cpu"), self.CheckersGUIPVP/self.CheckersGUICPU)
            self.CheckersGUICPU.Show()
        else:
            print("RETURN TO GAME ERROR")

    def TwoPlayerButtonSelected(self):
        self.selected = selected(-1, -1)
        self.createGameOptionsTab(self.createNewGame)

        playSound("checkermove.wav")

        if(self.subOptionsTab.index(3)==3):
            self.isGameUnderway = "pvp"
            self.board = self.pvpboard
            self.current = self.decidewhogoes("pvp")
            self.infolabel = infoGUI(self.CheckersGUIPVP, self.isGameUnderway, self.current)
            self.infolabel.grid(row=1, column=0, pady=10, padx=10)
            self.ReturnToGame()
            self.appendButtons()
            return None

        if(self.isGameUnderway=="" or self.isGameUnderway=="cpu"):
            self.player1 = "p1"
            self.player2 = "p2"
            self.board = self.pvpboard

            self.isGameUnderway = "pvp"
            self.numberofgames = 0
            self.gametime = [0, 0, 0]  # seconds, minutes, hours
            self.size = 8  # size of board
            self.selected = self.selectedPVP
            self.current = self.decidewhogoes("pvp")


            self.CheckersBoardGUI = CheckersBoardGUI(self.CheckersGUIPVP, size=self.size, board=self.board,
                                                     board1color=self.board1color, board2color=self.board2color)
            self.CheckersBoardGUI.grid(row=1, column=1, pady=20)

            self.subOptionsTab.add_cascade(label = "Return to Current Game", command = self.ReturnToGame)

            self.infolabel = infoGUI(self.CheckersGUIPVP, self.isGameUnderway, self.current)
            self.infolabel.grid(row=1, column=0, pady=10, padx=10)

            self.selectedchecker = self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()]

            self.appendButtons()
            self.winner = self.checkWinner()

            self.mainMenu.Hide()
            self.SettingsGUI.Hide()
            self.CheckersGUICPU.Hide()
            self.updateColor(self.CheckersGUIPVP)
            self.CheckersGUIPVP.Show()
        else:
            self.ReturnToGame()

    def SelectedvsCPU(self):
        self.selected = selected(-1, -1)
        self.createGameOptionsTab(self.createNewGame)

        playSound("checkermove.wav")

        #if a game has already started just recheck everything
        if (self.subOptionsTab.index(3) == 3):
            self.isGameUnderway = "cpu"
            self.board = self.cpuboard
            self.selected = self.selectedCPU
            self.current = self.decidewhogoes("cpu")
            self.infolabel = infoGUI(self.CheckersGUICPU, self.isGameUnderway, self.current)
            self.infolabel.grid(row=1, column=0, pady=10, padx=10)
            self.ReturnToGame()
            self.appendButtons()

            return None


        if(self.isGameUnderway=="" or self.isGameUnderway=="pvp"):
            self.isGameUnderway = "cpu"
            self.board = self.cpuboard
            self.numberofgames = 0
            self.gametime = [0, 0, 0]  # seconds, minutes, hours
            self.size = 8  # size of board
            self.selected = self.selectedCPU
            self.current = self.decidewhogoes("cpu")

            self.selectedchecker = self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()]

            self.CheckersBoardGUI = CheckersBoardGUI(self.CheckersGUICPU, size=self.size, board=self.board,
                                                     board1color=self.board1color, board2color=self.board2color)
            self.CheckersBoardGUI.grid(row=1, column=1, pady=20)

            self.subOptionsTab.add_cascade(label="Return to Current Game", command=self.ReturnToGame)

            self.infolabel = infoGUI(self.CheckersGUICPU, self.isGameUnderway, self.current)
            self.infolabel.grid(row=1, column=0, pady=10, padx=10)


            self.appendButtons()
            self.winner = self.checkWinner()

            self.mainMenu.Hide()
            self.SettingsGUI.Hide()
            self.CheckersGUIPVP.Hide()
            self.updateColor(self.CheckersGUICPU)
            self.CheckersGUICPU.Show()

        else:
            self.ReturnToGame()



    def SettingsSelected(self):
        self.mainMenu.Hide()
        self.CheckersGUIPVP.Hide()
        self.CheckersGUICPU.Hide()
        self.SettingsGUI.Show()
        self.optionsTab.delete(2)
        self.optionsTab.delete(1)

        playSound("checkermove.wav")


    def CheckSingleUserAmount(self, board, user):
        amount=0
        for i in range(len(board.getBoard())):
            for j in range(len(board.getBoard())):
                player = board.getBoard()[i][j].getPlayer()
                if(player ==user):
                    amount +=1
        return amount


    def CheckObtained(self):

        if(self.isGameUnderway=="pvp"):
            user1amount = 0
            user2amount = 0
            for i in range(len(self.board.getBoard())):
                for j in range(len(self.board.getBoard())):
                    player = self.board.getBoard()[i][j].getPlayer()

                    if (player == "p1"):
                        user1amount += 1
                    elif (player == "p2"):
                        user2amount += 1

            self.p1obtained = self.player1amount-user1amount
            self.p2obtained = self.player2amount-user2amount
            self.infolabel.updateLabels(self.p2obtained, self.p1obtained)

        elif (self.isGameUnderway == "cpu"):
            user1amount = 0
            user2amount = 0
            for i in range(len(self.board.getBoard())):
                for j in range(len(self.board.getBoard())):
                    player = self.board.getBoard()[i][j].getPlayer()

                    if (player == "cpu"):
                        user1amount += 1
                    elif (player == "player"):
                        user2amount += 1

            self.cpuobtained = self.cpuamount - user1amount
            self.playerobtained = self.playeramount - user2amount
            self.infolabel.updateLabels(self.playerobtained, self.cpuobtained)





    def createGameOptionsTab(self, game):
        gameOptions = Menu()

        self.optionsTab.add_cascade(menu = gameOptions, label = "Game Options")
        gameOptions.add_cascade(label = "Start New Game", command = game)
        gameOptions.add_cascade(label = "Skip Turn", command = self.SkipTurn)
        gameOptions.add_cascade(label = "re-Randomize Turn", command = self.RandomizeTurn)

    def RandomizeTurn(self):
        if(self.isGameUnderway=="pvp"):
            self.current=self.decidewhogoes("pvp")
        elif(self.isGameUnderway=="cpu"):
            self.current=self.decidewhogoes("cpu")
        self.infolabel.update()

        playSound("checkermove.wav")

    def SkipTurn(self):
        if(self.isGameUnderway=="cpu"):
            if(self.current=="cpu"):
                self.current="player"
            else:
                self.current= "cpu"

        elif(self.isGameUnderway=="pvp"):
            if(self.current=="p1"):
                self.current="p2"
            else:
                self.current="p1"

        playSound("checkermove.wav")
    #updates the color of the board
    def updateColor(self, gametype):
        #gametype is either CheckersBoardPVP or CehckersBoardCPU
        self.p1color = self.SettingsGUI.colorvalue1.get()
        self.p2color = self.SettingsGUI.colorvalue2.get()
        self.selectedchecker = self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()]

        self.CheckersBoardGUI = CheckersBoardGUI(gametype, size=self.size, board=self.board,
                                                 board1color=self.p1color, board2color=self.p2color)
        self.CheckersBoardGUI.grid(row=1, column=1, pady=20)

        self.appendButtons()
        self.winner = self.checkWinner()

        playSound("checkermove.wav")

    def createNewGame(self):

        if(self.isGameUnderway=="pvp"):
            self.player1 = "p1"
            self.player2 = "p2"
            self.isWinnerPvP= ""
            self.pvpboard = Board(size=self.size, player1=self.player1, player2=self.player2)
            self.board = self.pvpboard

            self.p1obtained = 0
            self.p2obtained = 0
            self.player1amount = self.CheckSingleUserAmount(self.pvpboard,self.player1)
            self.player2amount = self.CheckSingleUserAmount(self.pvpboard,self.player2)

            self.score2 = 0  # player2score
            self.numberofgames = 0
            self.gametime = [0, 0, 0]  # seconds, minutes, hours
            self.size = 8  # size of board
            self.p1color = self.SettingsGUI.colorvalue1.get()
            self.p2color = self.SettingsGUI.colorvalue2.get()
            self.selectedPVP = selected(-1, -1)  # user has not selected anything yet

            self.selected = self.selectedPVP

            self.current = self.decidewhogoes("pvp")
            self.selectedchecker = self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()]

            self.CheckersBoardGUI = CheckersBoardGUI(self.CheckersGUIPVP, size=self.size, board=self.board,
                                                     board1color=self.p1color, board2color=self.p2color)
            self.CheckersBoardGUI.grid(row=1, column=1, pady=20)

            self.isGameUnderway = "pvp"
            self.appendButtons()
            self.winner = self.checkWinner()

        elif(self.isGameUnderway=="cpu"):
            self.isGameUnderway = "cpu"
            self.isWinnerCpu = ""
            self.gametime = [0, 0, 0]  # seconds, minutes, hours
            self.size = 8  # size of board
            self.current = self.decidewhogoes("cpu")
            self.cpuboard = Board(size=self.size, player1=self.computer, player2=self.player)
            self.board = self.cpuboard
            self.cpuamount = self.CheckSingleUserAmount(self.cpuboard,self.computer)
            self.playeramount = self.CheckSingleUserAmount(self.cpuboard,self.player)
            self.cpuobtained= 0
            self.playerobtained = 0


            self.numberofgames = 0

            self.selectedCPU = selected(-1,-1)
            self.selected = self.selectedCPU

            self.selectedchecker = self.board.getBoard()[self.selected.getRow()][self.selected.getColumn()]

            self.CheckersBoardGUI = CheckersBoardGUI(self.CheckersGUICPU, size=self.size, board=self.board,
                                                     board1color=self.board1color, board2color=self.board2color)
            self.CheckersBoardGUI.grid(row=1, column=1, pady=20)


            self.infolabel = infoGUI(self.CheckersGUICPU, self.isGameUnderway, self.current)
            self.infolabel.grid(row=1, column=0, pady=10, padx=10)

            self.appendButtons()
            self.winner = self.checkWinner()

            self.mainMenu.Hide()
            self.SettingsGUI.Hide()
            self.CheckersGUIPVP.Hide()
            self.updateColor(self.CheckersGUICPU)
            self.CheckersGUICPU.Show()


    def printspecific(self,row,column):
        print(self.board.getBoard()[row][column].getPlayer())

        # current is a tuple (row,column)

    def CheckIfWinner(self):
        if(self.isGameUnderway=="pvp"):
            if self.CheckSingleUserAmount(self.pvpboard,self.player1)>0 and self.CheckSingleUserAmount(self.pvpboard,self.player2)<=0:
                self.infolabel.labelinfo.config(text = "Player1 Wins!", fg = "black")
                self.isWinnerPvP = "p1"
            elif self.CheckSingleUserAmount(self.pvpboard, self.player2) > 0 and self.CheckSingleUserAmount(self.pvpboard,self.player1) <= 0:
                self.infolabel.labelinfo.config(text="Player2 Wins!", fg = "red")
                self.isWinnerPvP = "p2"
        elif(self.isGameUnderway=="cpu"):
            if self.CheckSingleUserAmount(self.cpuboard,self.player)>0 and self.CheckSingleUserAmount(self.cpuboard,self.computer)<=0:
                self.infolabel.labelinfo.config(text = "Player Wins!", fg="red")
                self.isWinnerCpu = "player"
            elif self.CheckSingleUserAmount(self.cpuboard, self.computer) > 0 and self.CheckSingleUserAmount(self.cpuboard,self.player) <= 0:
                self.infolabel.labelinfo.config(text="Computer Wins!", fg = "black")
                self.isWinnerCpu = "cpu"


    def CheckHowMany(self, direction, row, column, player, board):
        currentrow = row
        currentcolumn = column
        amountofplayers = 0

        for i in range(len(board.getBoard())):
            for j in range(len(board.getBoard())):

                if (direction == "above" and board.getBoard()[i][j].getPlayer() == player and i < currentrow):
                    amountofplayers += 1
                elif (direction == "below" and board.getBoard()[i][j].getPlayer() == player and i > currentrow):
                    amountofplayers += 1
                elif (direction == "samerow" and board.getBoard()[i][j].getPlayer() == player and i == currentrow):
                    amountofplayers += 1
                elif (direction == "samecolumn" and board.getBoard()[i][
                    j].getPlayer() == player and j == currentcolumn):
                    amountofplayers += 1
                elif (direction == "left" and board.getBoard()[i][j].getPlayer() == player and j < currentcolumn):
                    amountofplayers += 1
                elif (direction == "right" and board.getBoard()[i][j].getPlayer() == player and j > currentcolumn):
                    amountofplayers += 1

        return amountofplayers



    def run(self):
        #thread1 = threading.Thread(target=self.placeSelection)
        #thread1.start()
        i = 0
        seconds = 0
        minutes = 0
        hours = 0

        while True:

            #controls the CPU'sturn, i%800==0 means that every 800 milliseconds play a computer turn
            if (self.isGameUnderway == "cpu" and i%800==0 and self.current=="cpu" and self.isWinnerCpu == ""):
                self.PlayCPUTurn()


                playSound("checkermove2.wav")


            #Every tick check how many pieces of the opposite player each player owns
            if(self.isGameUnderway!=""):
                self.CheckObtained()


            #TIME: keeps track of the time in-game,
            if(i == 1000):
                seconds +=1
                self.setTime(seconds,minutes,hours)
                i=0
            if(self.getSeconds()==60):
                seconds = 0
                minutes+=1
                self.setTime(seconds,minutes,hours)
            if(self.getMinutes()==60):
                minutes = 0
                hours+=1
                self.setTime(seconds,minutes,hours)


            if (self.isGameUnderway!=""):
                self.reUpdate()
            self.root.after(100)

            self.root.update_idletasks()
            self.root.update()
            self.root.after(100)

            if (self.isGameUnderway!=""):
                if(self.isGameUnderway=="pvp" and self.isWinnerPvP==""):
                    self.placeSelection()
                    self.infolabel.updatelabel(self.isGameUnderway,self.current)
                elif(self.isGameUnderway=="cpu" and self.isWinnerCpu==""):
                    self.placeSelection()
                    self.infolabel.updatelabel(self.isGameUnderway, self.current)

            #
            i+=200
            self.root.update()
            self.root.update_idletasks()

            if (self.getSeconds() % 2 == 0):
                ""
                self.mainMenu.updateTitleImages()

            self.CheckIfWinner()




    def setBoard(self, board):
        self.board = board
    def incrementscore1(self):
        self.score1 +=1
    def incrementscore2(self):
        self.score2 +=1
    def incrementnumberofgames(self):
        self.numberofgames+=1

    def setTime(self, seconds, minutes, hours):
        self.gametime[0]= seconds
        self.gametime[1]= minutes
        self.gametime[2]= hours

    def ShowBoard(self):
        self.CheckersBoardGUI.grid()

    def HideBoard(self):
        self.CheckersBoardGUI.grid_remove()





class CheckersGUI(Frame):
    def __init__(self,root):
        super().__init__(root)
    def Hide(self):
        self.grid_remove()
    def Show(self):
        self.grid()

game()

