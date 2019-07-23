"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont, QMovie, QPainter, QPalette, QImage, QBrush, qRgba
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, \
    QVBoxLayout, QTabWidget, QRadioButton, QHBoxLayout, QGroupBox

import Server
import random
import sys

####################################################################################
# needs to be installed (https://www.pygame.org/docs/ref/mixer.html)
####################################################################################
import pygame


# music playlist for game
playlist = {
    "Track 1": "sounds/beautiful-flute-ringtone.mp3",
    "Track 2": "sounds/Bahubali Flute Ringtone 2019.mp3",
    "Track 3": "sounds/japanese_zen_1.mp3",
    "Track 4": "sounds/japanese_zen_2.mp3",
    "Track 5": "sounds/Beautiful Japanese Music - Cherry Blossoms.mp3",
    "Track 6": "sounds/Beautiful Japanese Music - Kitsune Woods.mp3",
    "Track 7": "sounds/IntroTheme.mp3"
}

# Japanese_zen_1.mp3 & Japanese_zen_2 ( downloaded from
# https://www.zedge.net/find/ringtones/japanese%20bamboo%20flute) Japanese Music - Cherry Blossoms & Japanese Music -
# Kitsune Woods (downloaded from https://archive.org/details/BeautifulJapaneseMusicZenGarden/Beautiful+Japanese+Music
# +-+Kitsune+Woods.mp3)



# background library
backgrounds = {
    "BlueForest": "textures/Background/Forest.jpg",
    "Gate": "textures/Background/Gate.jpg",
    "ForestTempel": "textures/Background/ForestTempel.jpg",
    "NightRoad": "textures/Background/NightRoad.jpg",
    "RedForest": "textures/Background/RedForest.jpg",
    "Shrine": "textures/Background/Shrine.jpg",
    "Tempel": "textures/Background/Tempel.jpg",
}


# default settings
CurFloor = "White Stone"
CurWall = "Metall wall"
CurSpell = "Spellcard1"
CurCol = "Wall Collision   On"


# initialize the music mixer
pygame.mixer.init()


####################################################################################
# creating start screen
####################################################################################

class Game (QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(800, 336)
        Server.center(self)
        self.setWindowTitle("Welcome")

        self.enter = QPushButton("enter", self)
        self.enter.move(360,280)
        self.enter.resize(80, 25)
        self.enter.clicked.connect(self.gameMenu)
        self.enter.setStyleSheet("background-color: rgb(240,255,255); font: bold 15px; color: black;")

        # create background animated gif
        self.movie = QMovie("textures/Background/Red.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        # select the music track
        pygame.mixer.music.load(playlist["Track 5"])
        # loops the music
        pygame.mixer.music.play(-1, 0.0)

        self.show()


    def gameMenu(self):
        self.startM = start_Menu()
        self.movie.stop()
        self.close()

    def paintEvent(self, event):
        # after every changed image, refresh the background with the currentPixmap
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)


####################################################################################
# creating start Menu
####################################################################################

class start_Menu(QWidget):

    WIDTH = 500
    HEIGHT = 666

    XPosStart = 70
    YPosStart = 60

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Start Menu')
        Server.center(self)

        # switch to gameboard
        self.button1 = QPushButton('Start Game', self)
        self.button1.move(self.XPosStart, self.YPosStart)
        self.button1.clicked.connect(self.startGame)

        # switch to options
        self.button2 = QPushButton('Options', self)
        self.button2.clicked.connect(self.Options)
        self.button2.move(self.XPosStart, 2 * self.YPosStart)

        # switch to howtoplay
        self.button3 = QPushButton('How to Play', self)
        self.button3.clicked.connect(self.How2Play)
        self.button3.move(self.XPosStart, 3 * self.YPosStart)

        # switch to credits
        self.button4 = QPushButton('Credits', self)
        self.button4.clicked.connect(self.Credits)
        self.button4.move(self.XPosStart, 4 * self.YPosStart)

        # quite game
        self.button5 = QPushButton('Quit', self)
        self.button5.clicked.connect(self.close)
        self.button5.move(self.XPosStart, 5 * self.YPosStart)

        #create animated background
        self.movie = QMovie('textures/Background/Red2.gif')
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        # start new music in loop
        pygame.mixer.music.load(playlist["Track 6"])
        pygame.mixer.music.play(-1, 0.0)

        self.show()


    def paintEvent(self, event):

        # after every changed image, refresh the background with the currentPixmap
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def Instance(self):
        self.gBoard = Server.SpielFeld()
        return self.gBoard

    def startGame(self):
        self.Instance().start()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(playlist["Track 7"])
        pygame.mixer.music.play(-1, 0.0)
        self.close()

    def Options(self):
        self.opt = OptionField()
        self.close()

    def How2Play(self):
        self.instructions = How2PlayText()
        self.close()

    def Credits(self):
        self.authors = CreditText()
        self.close()

    def closeEvent(self, event):
        self.close()

    def Back2Menu(self):
        self.sMenu = start_Menu()
        self.close()


####################################################################################
# creating options
####################################################################################

class OptionField(QWidget):
    def __init__(self):
        super().__init__()

        self.background = QLabel(self)
        # randomly change background after every enter
        self.image = self.ImageChange()
        self.background.setPixmap(self.image)

        self.InitUI()

    def InitUI(self):
        self.resize(800, 500)
        self.setWindowTitle('Options')
        Server.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200, 450)

        self.table_widget = TableWidget(self)
        QtGui.QGuiApplication.processEvents()
        self.table_widget.move(380, 100)
        self.table_widget.resize(470,350)

        # for use, if tab_widget is not shown transparent)
        #self.table_widget.setStyleSheet('background-color: transparent;')
        # transparent as rgb color number
        #self.table_widget.setStyleSheet('background-color: rgb(255, 255, 255);')

        pygame.mixer.music.load(playlist["Track 5"])
        pygame.mixer.music.play(-1, 0.0)

        self.show()

    def Back2Menu(self):
            start_Menu.Back2Menu(self)

    def ImageChange(self):
        themes = list(backgrounds.keys())
        return QPixmap(backgrounds[random.choice(themes)])


####################################################################################
# creating contents for tabs
####################################################################################

class TableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Game")
        self.tabs.addTab(self.tab2, "Graphic")

        # Create game tab
        self.tab1.layout = QHBoxLayout()

        self.gameG = Spellcards()
        self.bulG = BulletCol()

        # add new content to tab1
        self.tab1.layout.addWidget(self.bulG)
        self.tab1.layout.addWidget(self.gameG)

        self.tab1.setLayout(self.tab1.layout)


        # create content grafic tab
        self.tab2.layout = QHBoxLayout()

        # add wallG to tab3
        self.wallG = wallTexture()
        self.tab2.layout.addWidget(self.wallG)


        # add floorG to tab3
        self.floorG = floorTexture()
        self.tab2.layout.addWidget(self.floorG)

        # add all layouts to tab3
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


####################################################################################
# tab Game: Spellcard option
####################################################################################

class Spellcards(QWidget):
    def __init__(self):
        super().__init__()

        # set layout for Spellbox
        self.gameG = QGroupBox(self)

        # set button layout
        self.button_layout1 = QVBoxLayout()

        # create buttons
        self.Spell1 = QRadioButton("Spellcard1")
        self.Spell2 = QRadioButton("Spellcard2")
        self.Spell3 = QRadioButton("Spellcard3")
        self.Spell4 = QRadioButton("Spellcard4")
        self.Spell5 = QRadioButton("Spellcard5")
        self.Spell6 = QRadioButton("Spellcard6")
        self.Spell7 = QRadioButton("Spellcard7")
        self.Spell8 = QRadioButton("All Spellcards")

        self.btn = QPushButton("Select")
        self.btn.setStyleSheet('background-color: white')

        self.currentRBtn = self.Spell1

        # set texture choice
        self.label = QLabel(self)

        # change style of lettering
        self.style = QFont()
        self.style.setBold(True)
        self.label.setFont(self.style)

        self.chk_RBtn()

        self.iniUt()

    def iniUt(self):

        self.gameG.setTitle("Spellcard Selection")

        # add buttons to button layout
        self.button_layout1.addWidget(self.Spell1)
        self.button_layout1.addWidget(self.Spell2)
        self.button_layout1.addWidget(self.Spell3)
        self.button_layout1.addWidget(self.Spell4)
        self.button_layout1.addWidget(self.Spell5)
        self.button_layout1.addWidget(self.Spell6)
        self.button_layout1.addWidget(self.Spell7)
        self.button_layout1.addWidget(self.Spell8)
        self.button_layout1.addWidget(self.btn)
        self.button_layout1.addWidget(self.label)

        # add button layout to Spellbox
        self.gameG.setLayout(self.button_layout1)

        # set Spellbox semi transparent rgba(255, 255, 255, 0.8)
        self.gameG.setStyleSheet('background-color: rgba(255, 255, 255, 0.5);')

        # click buttons
        self.Spell1.clicked.connect(lambda: self.currBtn_clk(self.Spell1))
        self.Spell2.clicked.connect(lambda: self.currBtn_clk(self.Spell2))
        self.Spell3.clicked.connect(lambda: self.currBtn_clk(self.Spell3))
        self.Spell4.clicked.connect(lambda: self.currBtn_clk(self.Spell4))
        self.Spell5.clicked.connect(lambda: self.currBtn_clk(self.Spell5))
        self.Spell6.clicked.connect(lambda: self.currBtn_clk(self.Spell6))
        self.Spell7.clicked.connect(lambda: self.currBtn_clk(self.Spell7))
        self.Spell8.clicked.connect(lambda: self.currBtn_clk(self.Spell8))


        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))


    # show new setting, after returing to options
    def chk_RBtn(self):
        global CurSpell

        self.Spell2.setChecked(False)
        self.Spell3.setChecked(False)
        self.Spell4.setChecked(False)
        self.Spell5.setChecked(False)
        self.Spell6.setChecked(False)
        self.Spell7.setChecked(False)
        self.Spell8.setChecked(False)

        if CurSpell == "Spellcard1":
            self.Spell1.setChecked(True)

        elif CurSpell == "Spellcard2":
            self.Spell2.setChecked(True)

        elif CurSpell == "Spellcard3":
            self.Spell3.setChecked(True)

        elif CurSpell == "Spellcard4":
            self.Spell4.setChecked(True)

        elif CurSpell == "Spellcard5":
            self.Spell5.setChecked(True)

        elif CurSpell == "Spellcard6":
            self.Spell6.setChecked(True)

        elif CurSpell == "Spellcard7":
            self.Spell7.setChecked(True)

        elif CurSpell == "AllSpellcards":
            self.Spell8.setChecked(True)

        else:
            self.Spell1.setChecked(True)

        self.label.setText('currently used\n' + CurSpell)
        self.label.update()


    def currBtn_clk(self, button):
        self.currentRBtn = button

    def btn_clk(self, button):
        global CurSpell
        print(button.text() + ' clicked')

        if button == self.Spell1:
            Server.spellcard = "Spellcard1"
            CurSpell = "Spellcard1"

        elif button == self.Spell2:
            Server.spellcard = "Spellcard2"
            CurSpell = "Spellcard2"

        elif button == self.Spell3:
            Server.spellcard = "Spellcard3"
            CurSpell = "Spellcard3"

        elif button == self.Spell4:
            Server.spellcard = "Spellcard4"
            CurSpell = "Spellcard4"

        elif button == self.Spell5:
            Server.spellcard = "Spellcard5"
            CurSpell = "Spellcard5"

        elif button == self.Spell6:
            Server.spellcard = "Spellcard6"
            CurSpell = "Spellcard6"

        elif button == self.Spell7:
            Server.spellcard = "Spellcard7"
            CurSpell = "Spellcard7"

        elif button == self.Spell8:
            Server.spellcard = "AllSpellcards"
            CurSpell = "AllSpellcards"

        else:
            pass

        self.label.setText("You selected: \n" + button.text())
        QtGui.QGuiApplication.processEvents()


####################################################################################
# tab Game: bullet - wall collision setting
####################################################################################

class BulletCol(QWidget):
    def __init__(self):
        super().__init__()

        # set wall texture layout
        self.bulG = QGroupBox(self)

        # set button layout
        self.button_layout1 = QVBoxLayout()

        # create buttons
        self.BulTrue = QRadioButton("Wall Collision   On")
        self.BulFalse = QRadioButton("Wall Collision   Off")

        self.btn = QPushButton("Select")
        self.btn.setStyleSheet('background-color: white')

        self.currentRBtn = self.BulTrue

        self.label = QLabel(self)

        # change style of lettering
        self.style = QFont()
        self.style.setBold(True)
        self.label.setFont(self.style)

        self.chk_RBtn()

        self.iniUt()

    def iniUt(self):

        self.bulG.setTitle("Bullet - Wall Collision")

        self.button_layout1.addWidget(self.BulTrue)
        self.button_layout1.addWidget(self.BulFalse)
        self.button_layout1.addWidget(self.btn)
        self.button_layout1.addWidget(self.label)


        # add button layout in wall layout
        self.bulG.setLayout(self.button_layout1)

        # set Bullet setting semi-transparent
        self.bulG.setStyleSheet('background-color: rgba(255, 255, 255, 0.5);')

        # click buttons
        self.BulTrue.clicked.connect(lambda: self.currBtn_clk(self.BulTrue))
        self.BulFalse.clicked.connect(lambda: self.currBtn_clk(self.BulFalse))


        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))


    # show new setting, after returing to options
    def chk_RBtn(self):
        global CurCol

        print('Here: ' + CurCol)
        self.BulFalse.setChecked(False)
        self.BulTrue.setChecked(False)

        if CurCol == "Wall Collision   On":
            self.BulTrue.setChecked(True)

        elif CurCol == "Wall Collision   Off":
            self.BulFalse.setChecked(True)
            print('now why?')

        else:
            self.BulTrue.setChecked(True)

        self.label.setText('currently used\n' + CurCol)
        self.label.update()


    def currBtn_clk(self, button):
        self.currentRBtn = button


    def btn_clk(self, button):
        global CurCol
        print(button.text() + ' clicked')

        if button == self.BulTrue:
            Server.BulCollision = True
            CurCol = "Wall Collision   On"

        elif button == self.BulFalse:
            Server.BulCollision = False
            CurCol = "Wall Collision   Off"

        else:
            pass

        self.label.setText("You selected: \n" + button.text())
        QtGui.QGuiApplication.processEvents()



####################################################################################
# tab Graphic: wall texture choice
####################################################################################

class wallTexture(QWidget):
    def __init__(self):
        super().__init__()

        # set wall texture layout
        self.wallG = QGroupBox(self)

        # set button layout
        self.button_layout1 = QVBoxLayout()

        # create buttons
        self.texture1 = QRadioButton("Metall wall")
        self.texture2 = QRadioButton("Metall Bar")
        self.texture3 = QRadioButton("Mosaik wall")
        self.texture4 = QRadioButton("Metall Fence")
        self.texture5 = QRadioButton("Rusty Bar")

        self.btn = QPushButton("Select")
        self.btn.setStyleSheet('background-color: white')

        self.currentRBtn = self.texture1

        self.label = QLabel(self)

        # change style of lettering
        self.style = QFont()
        self.style.setBold(True)
        self.label.setFont(self.style)

        self.chk_RBtn()

        self.iniUt()

    def iniUt(self):

        self.wallG.setTitle("Texture Wall")

        # adjust icons on buttons
        self.texture1.setIcon(QIcon(Server.wallTextures["Metall wall"]))
        self.texture2.setIcon(QIcon(Server.wallTextures["Metall Bar"]))
        self.texture3.setIcon(QIcon(Server.wallTextures["Mosaik wall"]))
        self.texture4.setIcon(QIcon(Server.wallTextures["Metall Fence"]))
        self.texture5.setIcon(QIcon(Server.wallTextures["Rusty Bar"]))

        self.button_layout1.addWidget(self.texture1)
        self.button_layout1.addWidget(self.texture2)
        self.button_layout1.addWidget(self.texture3)
        self.button_layout1.addWidget(self.texture4)
        self.button_layout1.addWidget(self.texture5)
        
        self.button_layout1.addWidget(self.btn)
        self.button_layout1.addWidget(self.label)

        # add button layout in wall layout
        self.wallG.setLayout(self.button_layout1)

        # set wall texture box semi-transparent
        self.wallG.setStyleSheet('background-color: rgba(255, 255, 255, 0.5);')

        # click buttons
        self.texture1.clicked.connect(lambda: self.currBtn_clk(self.texture1))
        self.texture2.clicked.connect(lambda: self.currBtn_clk(self.texture2))
        self.texture3.clicked.connect(lambda: self.currBtn_clk(self.texture3))
        self.texture4.clicked.connect(lambda: self.currBtn_clk(self.texture4))
        self.texture5.clicked.connect(lambda: self.currBtn_clk(self.texture5))


        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))


    # show new setting, after returing to options
    def chk_RBtn(self):
        global CurWall

        self.texture2.setChecked(False)
        self.texture3.setChecked(False)
        self.texture4.setChecked(False)
        self.texture5.setChecked(False)

        if CurWall == "Metall wall":
            self.texture1.setChecked(True)


        elif CurWall == "Metall Bar":
            self.texture2.setChecked(True)

        elif CurWall == "Mosaik wall":
            self.texture3.setChecked(True)

        elif CurWall == "Metall Fence":
            self.texture4.setChecked(True)

        elif CurWall == "Rusty Bar":
            self.texture5.setChecked(True)

        else:
            self.texture1.setChecked(True)

        self.label.setText('currently used\n' + CurWall)
        self.label.update()


    def currBtn_clk(self, button):
        self.currentRBtn = button


    def btn_clk(self, button):
        global CurWall
        print(button.text() + ' clicked')

        if button == self.texture1:
            Server.wtexture = "Metall wall"
            CurWall = "Metall wall"

        elif button == self.texture2:
            Server.wtexture = "Metall Bar"
            CurWall = "Metall Bar"

        elif button == self.texture3:
            Server.wtexture = "Mosaik wall"
            CurWall = "Mosaik wall"

        elif button == self.texture4:
            Server.wtexture = "Metall Fence"
            CurWall = "Metall Fence"

        elif button == self.texture5:
            Server.wtexture = "Rusty Bar"
            CurWall = "Rusty Bar"
            
        else:
            pass

        self.label.setText("You selected: \n" + button.text())
        QtGui.QGuiApplication.processEvents()



####################################################################################
# tab Graphic: floor texture choice
####################################################################################

class floorTexture(QWidget):

    def __init__(self):
        super().__init__()

        # set floor texture layout
        self.floorG = QGroupBox(self)

        # set button layout
        self.button_layout2 = QVBoxLayout()

        # create floor texture buttons
        self.texture1 = QRadioButton("White Stone")
        self.texture2 = QRadioButton("Brown Stone")
        self.texture3 = QRadioButton("Dirt")
        self.texture4 = QRadioButton("Dirt (Moving)")
        self.texture5 = QRadioButton("Pattern (Moving)")
        self.texture6 = QRadioButton("Sakura (Moving)")
        self.texture7 = QRadioButton("Water (Moving)")
        # create selector
        self.btn = QPushButton("Select")
        self.btn.setStyleSheet('background-color: white')

        self.currentRBtn = self.texture1

        # set texture choice
        self.label = QLabel(self)

        # change style of lettering
        self.style = QFont()
        self.style.setBold(True)
        self.label.setFont(self.style)

        self.chk_RBtn()

        self.iniUt()

    def iniUt(self):

        self.floorG.setTitle("Texture Floor")

        # title cant be set bold
        #self.setStyleSheet('QGroupBox:title {color: blue;}')
        # alternatives, but not really efficient
        #self.floorG.setStyleSheet("font-weight: bold;")
        #self.setStyleSheet("font-weight: bold;")

        # add button icons
        self.texture1.setIcon(QIcon(Server.floorTextures["White Stone"]))
        self.texture2.setIcon(QIcon(Server.floorTextures["Brown Stone"]))
        self.texture3.setIcon(QIcon(Server.floorTextures["Dirt"]))
        self.texture4.setIcon(QIcon(Server.floorTextures["Background Dirt"]))
        self.texture5.setIcon(QIcon(Server.floorTextures["Background Pattern"]))
        self.texture6.setIcon(QIcon(Server.floorTextures["Background Sakura"]))
        self.texture7.setIcon(QIcon(Server.floorTextures["Background Water"]))

        # clicked buttons
        self.texture1.clicked.connect(lambda: self.currBtn_clk(self.texture1))
        self.texture2.clicked.connect(lambda: self.currBtn_clk(self.texture2))
        self.texture3.clicked.connect(lambda: self.currBtn_clk(self.texture3))
        self.texture4.clicked.connect(lambda: self.currBtn_clk(self.texture4))
        self.texture5.clicked.connect(lambda: self.currBtn_clk(self.texture5))
        self.texture6.clicked.connect(lambda: self.currBtn_clk(self.texture6))
        self.texture7.clicked.connect(lambda: self.currBtn_clk(self.texture7))



        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))


        # add buttons to layout
        self.button_layout2.addWidget(self.texture1)
        self.button_layout2.addWidget(self.texture2)
        self.button_layout2.addWidget(self.texture3)
        self.button_layout2.addWidget(self.texture4)
        self.button_layout2.addWidget(self.texture5)
        self.button_layout2.addWidget(self.texture6)
        self.button_layout2.addWidget(self.texture7)

        self.button_layout2.addWidget(self.btn)
        self.button_layout2.addWidget(self.label)

        # add button layout in floor layout
        self.floorG.setLayout(self.button_layout2)

        #set floor textures box semi-transparent
        self.floorG.setStyleSheet('background-color: rgba(255, 255, 255, 0.5);')


    # show new setting, after returing to options
    def chk_RBtn(self):
        global CurFloor

        self.texture1.setChecked(False)
        self.texture2.setChecked(False)
        self.texture3.setChecked(False)
        self.texture4.setChecked(False)
        self.texture5.setChecked(False)
        self.texture6.setChecked(False)

        if CurFloor == "White Stone":
            self.texture1.setChecked(True)

        elif CurFloor == "Brown Stone":
            self.texture2.setChecked(True)

        elif CurFloor == "Dirt":
            self.texture3.setChecked(True)

        elif CurFloor == "Background Dirt":
            self.texture4.setChecked(True)

        elif CurFloor == "Background Pattern":
            self.texture5.setChecked(True)

        elif CurFloor == "Background Sakura":
            self.texture6.setChecked(True)

        elif CurFloor == "Background Water":
            self.texture7.setChecked(True)

        else:
            self.texture1.setChecked(True)

        self.label.setText('currently used\n' + CurFloor)


    def currBtn_clk(self, button):
        self.currentRBtn = button


    def btn_clk(self, button):
        global CurFloor

        if button == self.texture1:
            Server.ftexture = "White Stone"
            CurFloor = "White Stone"

        elif button == self.texture2:
            Server.ftexture = "Brown Stone"
            CurFloor = "Brown Stone"

        elif button == self.texture3:
            Server.ftexture = "Dirt"
            CurFloor = "Dirt"
            
        if button == self.texture4:
            Server.ftexture = "Background Dirt"
            CurFloor = "Background Dirt"

        elif button == self.texture5:
            Server.ftexture = "Background Pattern"
            CurFloor = "Background Pattern"

        elif button == self.texture6:
            Server.ftexture = "Background Sakura"
            CurFloor = "Background Sakura"

        elif button == self.texture7:
            Server.ftexture = "Background Water"
            CurFloor = "Background Water"

        else:
            pass

        self.label.setText("You selected: \n" + button.text())


####################################################################################
# creating credit window
####################################################################################

class CreditText(QWidget):

    def __init__(self):
        super(CreditText, self).__init__()

        self.label = QLabel(self)
        self.image = QPixmap('textures/Background/CreditBackground.jpg')
        self.label.setPixmap(self.image)

        self.back = QPushButton('back', self)

        self.initUI()

    def initUI(self):
        self.resize(self.image.width(), self.image.height())
        self.setWindowTitle('Credits')
        Server.center(self)

        self.back.clicked.connect(self.Back2Menu)
        self.back.move(350,330)

        pygame.mixer.music.load(playlist["Track 6"])
        pygame.mixer.music.play(-1, 0.0)

        self.show()

    def Back2Menu(self):
            start_Menu.Back2Menu(self)



####################################################################################
# creating instruction window
####################################################################################


class How2PlayText(QWidget):

    def __init__(self):
        super(How2PlayText, self).__init__()

        self.background = QLabel(self)
        self.image = QPixmap("textures/Background/Test.jpg")
        self.background.setPixmap(self.image)


        self.title = QLabel("INSTRUCTIONS", self)
        self.title.setStyleSheet("color: Black; font: bold; font-size: 30px")
        self.title.move(self.image.width()/2 - self.title.width(), 20)

        self.text1 = QLabel("Hello and welcome to our little project! Today you are part of a world "
                          "full of new adventures and great experiences. But you know,\nevery new beginning comes with some "
                          "instructions. So before starting the game, lets rule down some basic understanding of the\ngameplay."
                            " Maybe you already took a turn into the settings, there you can select some spellcards and so on. These "
                           "spellcards can help\nyou to cast some special abilities. So try some!\n \nDown below you can see the "
                           "game keys for the selection of only one random spellcard. Just press key L for activating the spell.\nWith the "
                           "key Q you can halt then velocity of your character and maybe let it take a look around. The"
                           " others are self-explanatory.", self)
        self.text1.setStyleSheet("background-color: transparent; color: black; font-size: 15px; font: bold")
        self.text1.move(150, self.title.height() + 50)

        self.keyboard1 = QLabel(self)
        self.image1 = QPixmap("textures/Instructions/keyboard1.jpg")
        self.keyboard1.setPixmap(self.image1)
        self.keyboard1.move(self.image.width()/2 - self.image1.width()/2, self.text1.height() + 200)


        self.initUI()

    def initUI(self):
        self.resize(self.image.width(), self.image.height())
        self.setWindowTitle('How to Play')
        Server.center(self)

        self.back = QPushButton("Back", self)
        self.back.clicked.connect(self.back2Menu)
        self.back.move(20, self.image.height() - self.back.height() - 20)

        self.next = QPushButton("Next", self)
        self.next.clicked.connect(self.nextPage1)
        self.next.move(self.image.width() - self.next.width() + 20,  self.image.height() - self.next.height() - 20)

        self.show()

    def back2Menu(self):
        start_Menu.Back2Menu(self)

    def nextPage1(self):
        self.nextP = NextPage1()
        self.close()
        

class NextPage1(QWidget):

    def __init__(self):
        super(NextPage1, self).__init__()

        self.background = QLabel(self)
        self.image = QPixmap("textures/Background/Test.jpg")
        self.background.setPixmap(self.image)

        self.title = QLabel("INSTRUCTIONS", self)
        self.title.setStyleSheet("color: Black; font: bold; font-size: 30px")
        self.title.move(self.image.width() / 2 - self.title.width(), 20)


        self.text2 = QLabel(self)
        self.text2.setText("But humans are a little greedy and so why not give you the ability to choose all spellcards. With this "
                           "possibility in the \noption settings, you can use all spells. Down below you can see the game keys for "
                           "selecting all spellcards.\nPress any key from 1 to 7 to activate one of the special abilities.")
        self.text2.setStyleSheet("background-color: transparent; color: black; font-size: 15px; font: bold")
        self.text2.move(200, self.title.height() + 100)

        self.keyboard2 = QLabel(self)
        self.image2 = QPixmap("textures/Instructions/keyboard2.jpg")
        self.keyboard2.setPixmap(self.image2)
        self.keyboard2.move(self.image.width() / 2 - self.image2.width() / 2, self.text2.height() + 200)

        self.selection = QLabel(self)
        self.image3 = QPixmap("textures/Instructions/spellSelection.png")
        self.selection.setPixmap(self.image3)
        self.selection.move(20, 20)

        self.initUI()

    def initUI(self):
        self.resize(self.image.width(), self.image.height())
        self.setWindowTitle('How to Play')
        Server.center(self)

        self.back = QPushButton("Back", self)
        self.back.clicked.connect(self.back2H2P)
        self.back.move(20, self.image.height() - self.back.height() - 20)

        self.next = QPushButton("Next", self)
        self.next.clicked.connect(self.nextPage2)
        self.next.move(self.image.width() - self.next.width() + 20,  self.image.height() - self.next.height() - 20)

        self.show()

    def back2H2P(self):
        self.h2P = How2PlayText()
        self.close()

    def nextPage2(self):
        self.nextP = NextPage2()
        self.close()


class NextPage2(QWidget):

    def __init__(self):
        super(NextPage2, self).__init__()

        self.background = QLabel(self)
        self.image = QPixmap("textures/Background/Test.jpg")
        self.background.setPixmap(self.image)


        self.title = QLabel("INSTRUCTIONS", self)
        self.title.setStyleSheet("color: Black; font: bold; font-size: 30px")
        self.title.move(self.image.width() / 2 - self.title.width(), 20)

        self.text3 = QLabel("Additionally, we have some specials hidden in the game. As you can see on the left side, "
                            "we have a little\nhelping hand in form of a Bomb.\n \nBe assured, the bomb will not hurt you in "
                            "any way. Instead it gives you an shield against the attacks of your enemies. ", self)
        self.text3.setStyleSheet("color: black; font: bold; font-size: 15px;")
        self.text3.move(200,100)

        self.bomb = QLabel(self)
        self.bomb.setPixmap(QPixmap("textures/bomb.jpg"))
        self.bomb.move(150, 100)

        self.robo_alive = QLabel(self)
        self.robo_alive.setPixmap(QPixmap("textures/Robots/Robot01.png"))
        self.robo_alive.move(150, 250)

        self.robo_ememy = QLabel(self)
        self.robo_ememy.setPixmap(QPixmap("textures/Robots/Robot02.png"))
        self.robo_ememy.move(150, 300)

        self.robo_immun = QLabel(self)
        self.robo_immun.setPixmap(QPixmap("textures/Robots/Robot_In.png"))
        self.robo_immun.move(150, 350)

        self.robo_dead = QLabel(self)
        self.robo_dead.setPixmap(QPixmap("textures/Robots/Robot_Dead.png"))
        self.robo_dead.move(150, 400)

        self.text4 = QLabel("Now let's introduce the most important characters in this game. On the left side, you can see "
                            "the robot ninjas.\n \nThe green ninja represents our hero, which you can control with the "
                            "keyboard. The details are mentioned beforehand,\ntake a look if not sure anymore.\n \n"
                            "The red one, represents the enemy of our hero. So be careful of it. Make sure to shoot it or"
                            "run away.\n \nAs we mentioned before, you can be saved for a certain amount of time against your"
                            "enemies with the help\nof the bomb or after you are killed. The yellow color represents a golden "
                            "shield around you.\n \nEven the best will be shoot, so after being hit by a bullet your color will change "
                            "to grey.\nBut be assured, your hero will be revived after a certain amount of time.", self)
        self.text4.setStyleSheet("color: black; font: bold; font-size: 15px;")
        self.text4.move(200, 250)

        self.endMess = QLabel("HAVE FUN AND ENJOY!!", self)
        self.endMess.setStyleSheet("color: black; font: bold; font-size: 30px;")
        self.endMess.move(self.image.width() / 2 - self.endMess.width()/2 - self.endMess.width(), 600)
        self.initUI()


    def initUI(self):
        self.resize(self.image.width(), self.image.height())
        self.setWindowTitle('How to Play')
        Server.center(self)

        self.back = QPushButton("Back", self)
        self.back.clicked.connect(self.back2Page1)
        self.back.move(20, self.image.height() - self.back.height() - 20)

        self.show()

    def back2Page1(self):
        self.page1 = NextPage1()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
