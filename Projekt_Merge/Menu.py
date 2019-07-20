"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont, QMovie, QPainter
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, \
    QVBoxLayout, QTabWidget, QRadioButton, QHBoxLayout, QGridLayout, QGroupBox

import sys
import pygame # needs to be installed (https://www.pygame.org/docs/ref/mixer.html)
import Server

# initalize the music mixer
pygame.mixer.init()

playlist = {
    "Track 1": "sounds/beautiful-flute-ringtone.mp3",
    "Track 2": "sounds/Bahubali Flute Ringtone 2019.mp3",
    "Track 3": "sounds/japanese_zen_1.mp3",
    "Track 4": "sounds/japanese_zen_2.mp3",
    "Track 5": "sounds/Beautiful Japanese Music - Cherry Blossoms.mp3",
    "Track 6": 'sounds/Beautiful Japanese Music - Kitsune Woods.mp3'
}

# Japanese_zen_1.mp3 & Japanese_zen_2 ( downloaded from https://www.zedge.net/find/ringtones/japanese%20bamboo%20flute)
# Japanese Music - Cherry Blossoms & Japanese Music - Kitsune Woods (downloaded from https://archive.org/details/BeautifulJapaneseMusicZenGarden/Beautiful+Japanese+Music+-+Kitsune+Woods.mp3)


#default setting
CurFloor = "Brown floor "
CurWall = "Metall wall"
CurSpell = "Spellcard1"
CurCol = "Wall Collision   On"


class Game (QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.resize(800, 336)
        Server.center(self)
        self.setWindowTitle('Welcome')
        self.enter = QPushButton('enter', self)
        self.enter.move(360,280)
        self.enter.resize(80, 25)
        self.enter.clicked.connect(self.gameMenu)
        self.enter.setStyleSheet('background-color: rgb(240,255,255); font: bold 15px; color: black;')

        # create background animated gif
        self.movie = QMovie('textures/Background/Red.gif')
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        # select the music track
        pygame.mixer.music.load(playlist["Track 5"])
        # loops the music
        pygame.mixer.music.play(-1, 0.0)

        self.show()

    def gameMenu(self):
        self.startM = start_Menu()
        self.close()

    # reproduce movie
    def paintEvent(self, event):

        # https://wiki.python.org/moin/PyQt/Movie%20splash%20screen
        # after every changed image, refresh the background with the currentPixmap
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)



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

        # switch to manuel
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

    # reproduce movie
    def paintEvent(self, event):

        # https://wiki.python.org/moin/PyQt/Movie%20splash%20screen
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



class OptionField(QWidget):
    def __init__(self):
        super().__init__()

        self.background = QLabel(self)
        self.image = QPixmap('textures/Background/NightRoad.jpg')
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

        pygame.mixer.music.load(playlist["Track 4"])
        pygame.mixer.music.play(-1, 0.0)

        self.show()

    def Back2Menu(self):
            start_Menu.Back2Menu(self)



class TableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Game")
        self.tabs.addTab(self.tab3, "Grafik")

        # Create first tab
        self.tab1.layout = QHBoxLayout()

        self.gameG = Spellcards()
        self.bulG = BulletCol()

        # add new Boxes to tab1
        self.tab1.layout.addWidget(self.bulG)
        self.tab1.layout.addWidget(self.gameG)

        self.tab1.setLayout(self.tab1.layout)


        # create content grafic tab
        self.tab3.layout = QHBoxLayout()

        # add wallG to tab3
        self.wallG = wallTexture()
        self.tab3.layout.addWidget(self.wallG)


        # add floorG to tab3
        self.floorG = floorTexture()
        self.tab3.layout.addWidget(self.floorG)

        # add all layouts to tab3
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

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
        self.gameG.setStyleSheet('background-color: rgb(240,255,255);')

        # click buttons
        self.Spell1.clicked.connect(lambda: self.rBtn_clk(self.Spell1))
        self.Spell2.clicked.connect(lambda: self.rBtn_clk(self.Spell2))
        self.Spell3.clicked.connect(lambda: self.rBtn_clk(self.Spell3))
        self.Spell4.clicked.connect(lambda: self.rBtn_clk(self.Spell4))
        self.Spell5.clicked.connect(lambda: self.rBtn_clk(self.Spell5))
        self.Spell6.clicked.connect(lambda: self.rBtn_clk(self.Spell6))
        self.Spell7.clicked.connect(lambda: self.rBtn_clk(self.Spell7))
        self.Spell8.clicked.connect(lambda: self.rBtn_clk(self.Spell8))


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


    def rBtn_clk(self, button):
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

        self.currentRBtn = self.BulTrue

        # set texture choice
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
        self.bulG.setStyleSheet('background-color: rgb(240,255,255);')


        # click buttons
        self.BulTrue.clicked.connect(lambda: self.rBtn_clk(self.BulTrue))
        self.BulFalse.clicked.connect(lambda: self.rBtn_clk(self.BulFalse))


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


    def rBtn_clk(self, button):
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




class wallTexture(QWidget):
    def __init__(self):
        super().__init__()

        # set wall texture layout
        self.wallG = QGroupBox(self)

        # set button layout
        self.button_layout1 = QVBoxLayout()

        # create buttons
        self.texture1 = QRadioButton("Metall wall")
        self.texture2 = QRadioButton("Red wall")
        self.texture3 = QRadioButton("Mosaik wall")
        self.btn = QPushButton("Select")

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

        self.wallG.setTitle("Texture Wall")

        # adjust icons on buttons
        self.texture1.setIcon(QIcon(Server.wallTextures["Metall wall"]))
        self.texture2.setIcon(QIcon(Server.wallTextures["Red wall"]))
        self.texture3.setIcon(QIcon(Server.wallTextures["Mosaik wall"]))

        self.button_layout1.addWidget(self.texture1)
        self.button_layout1.addWidget(self.texture2)
        self.button_layout1.addWidget(self.texture3)
        self.button_layout1.addWidget(self.btn)
        self.button_layout1.addWidget(self.label)

        # add button layout in wall layout
        self.wallG.setLayout(self.button_layout1)
        self.wallG.setStyleSheet('background-color: rgb(240,255,255);')

        # click buttons
        self.texture1.clicked.connect(lambda: self.rBtn_clk(self.texture1))
        self.texture2.clicked.connect(lambda: self.rBtn_clk(self.texture2))
        self.texture3.clicked.connect(lambda: self.rBtn_clk(self.texture3))


        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))


    # show new setting, after returing to options
    def chk_RBtn(self):
        global CurWall

        self.texture2.setChecked(False)
        self.texture3.setChecked(False)
        self.texture3.setChecked(False)

        if CurWall == "Metall wall":
            self.texture1.setChecked(True)


        elif CurWall == "Red wall":
            self.texture2.setChecked(True)

        elif CurWall == "Mosaik wall":
            self.texture3.setChecked(True)

        else:
            self.texture1.setChecked(True)

        self.label.setText('currently used\n' + CurWall)
        self.label.update()


    def rBtn_clk(self, button):
        self.currentRBtn = button


    def btn_clk(self, button):
        global CurWall
        print(button.text() + ' clicked')

        if button == self.texture1:
            Server.wtexture = "Metall wall"
            CurWall = "Metall wall"

        elif button == self.texture2:
            Server.wtexture = "Red wall"
            CurWall = "Red wall"

        elif button == self.texture3:
            Server.wtexture = "Mosaik wall"
            CurWall = "Mosaik wall"
        else:
            pass

        self.label.setText("You selected: \n" + button.text())
        QtGui.QGuiApplication.processEvents()


class floorTexture(QWidget):

    def __init__(self):
        super().__init__()

        # set floor texture layout
        self.floorG = QGroupBox(self)

        # set button layout
        self.button_layout2 = QVBoxLayout()

        # create floor texture buttons
        self.texture1 = QRadioButton("Brown floor")
        self.texture2 = QRadioButton("Wood floor")
        self.texture3 = QRadioButton("Grass floor")
        self.texture4 = QRadioButton("Pink floor")
        self.texture5 = QRadioButton("Whitestone floor")
        self.texture6 = QRadioButton("Brownstone floor")
        # create selector
        self.btn = QPushButton("Select")

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

        # add button icons
        self.texture1.setIcon(QIcon(Server.floorTextures["Brown floor"]))
        self.texture2.setIcon(QIcon(Server.floorTextures["Wood floor"]))
        self.texture3.setIcon(QIcon(Server.floorTextures["Grass floor"]))
        self.texture4.setIcon(QIcon(Server.floorTextures["Pink floor"]))
        self.texture5.setIcon(QIcon(Server.floorTextures["Whitestone floor"]))
        self.texture6.setIcon(QIcon(Server.floorTextures["Brownstone floor"]))

        self.texture1.clicked.connect(lambda: self.rBtn_clk(self.texture1))


        # clicked buttons
        self.texture1.clicked.connect(lambda: self.rBtn_clk(self.texture1))
        self.texture2.clicked.connect(lambda: self.rBtn_clk(self.texture2))
        self.texture3.clicked.connect(lambda: self.rBtn_clk(self.texture3))
        self.texture4.clicked.connect(lambda: self.rBtn_clk(self.texture4))
        self.texture5.clicked.connect(lambda: self.rBtn_clk(self.texture5))
        self.texture6.clicked.connect(lambda: self.rBtn_clk(self.texture6))


        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))


        # add buttons to layout
        self.button_layout2.addWidget(self.texture1)
        self.button_layout2.addWidget(self.texture2)
        self.button_layout2.addWidget(self.texture3)
        self.button_layout2.addWidget(self.texture4)
        self.button_layout2.addWidget(self.texture5)
        self.button_layout2.addWidget(self.texture6)

        self.button_layout2.addWidget(self.btn)
        self.button_layout2.addWidget(self.label)

        # add button layout in floor layout
        self.floorG.setLayout(self.button_layout2)
        self.floorG.setStyleSheet('background-color: rgb(240,255,255);')


    # show new setting, after returing to options
    def chk_RBtn(self):
        global CurFloor

        self.texture1.setChecked(False)
        self.texture2.setChecked(False)
        self.texture3.setChecked(False)
        self.texture4.setChecked(False)
        self.texture5.setChecked(False)
        self.texture6.setChecked(False)


        if CurFloor == "Wood floor":
            self.texture2.setChecked(True)

        elif CurFloor == "Brown floor":
            self.texture1.setChecked(True)

        elif CurFloor == "Grass floor":
            self.texture3.setChecked(True)

        elif CurFloor == "Pink floor":
            self.texture4.setChecked(True)

        elif CurFloor == "Whitestone floor":
            self.texture5.setChecked(True)

        elif CurFloor == "Brownstone floor":
            self.texture6.setChecked(True)

        else:
            self.texture1.setChecked(True)

        self.label.setText('currently used\n' + CurFloor)


    def rBtn_clk(self, button):
        self.currentRBtn = button


    def btn_clk(self, button):
        global CurFloor

        if button == self.texture1:
            Server.ftexture = "Brown floor"
            CurFloor = "Brown floor"

        elif button == self.texture2:
            Server.ftexture = "Wood floor"
            CurFloor = "Wood floor"

        elif button == self.texture3:
            Server.ftexture = "Grass floor"
            CurFloor = "Grass floor"

        elif button == self.texture4:
            Server.ftexture = "Pink floor"
            CurFloor = "Pink floor"

        elif button == self.texture5:
            Server.ftexture = "Whitestone floor"
            CurFloor = "Whitestone floor"

        elif button == self.texture6:
            Server.ftexture = "Brownstone floor"
            CurFloor = "Brownstone floor"

        else:
            pass

        self.label.setText("You selected: \n" + button.text())



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

        pygame.mixer.music.load(playlist["Track 3"])
        pygame.mixer.music.play(-1, 0.0)

        self.show()

    def Back2Menu(self):
            start_Menu.Back2Menu(self)



class How2PlayText(QWidget):

    def __init__(self):
        super(How2PlayText, self).__init__()

        self.layout = QVBoxLayout()
        self.label = QLabel("")
        self.label.setText("INSTRUCTIONS \n \n blabla "
                           "\n \n \n \n ")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.setWindowTitle('How to Play')
        Server.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200,400)

        self.show()

    def Back2Menu(self):
            start_Menu.Back2Menu(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
