"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel, \
    QVBoxLayout, QTabWidget, QRadioButton, QHBoxLayout, QGridLayout, QGroupBox

import sys

import Server

WIDTH = 500
HEIGHT = 500

XPosStart = 25
YPosStart = 75

PAUSE_STATE = False
START_STATE = False


class Game (QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.resize(WIDTH, HEIGHT)
        Server.center(self)
        self.setWindowTitle('Intro')
        
        # create start button
        self.enter = QPushButton('enter', self)
        self.enter.move(50,400)
        self.enter.resize(400, 50)
        self.enter.clicked.connect(self.GAME_Menu)

        self.show()


    def GAME_Menu(self):
        self.startM = start_Menu()
        self.close()


class start_Menu(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('Start Menu')
        Server.center(self)

        # switch to gameboard
        self.button1 = QPushButton('Start Game', self)
        self.button1.move(XPosStart, YPosStart)
        self.button1.clicked.connect(self.startGame)

        # switch to options
        self.button2 = QPushButton('Options', self)
        self.button2.clicked.connect(self.Options)
        self.button2.move(XPosStart, 2 * YPosStart)

        # switch to manuel
        self.button3 = QPushButton('How to Play', self)
        self.button3.clicked.connect(self.How2Play)
        self.button3.move(XPosStart, 3 * YPosStart)

        # switch to credits
        self.button4 = QPushButton('Credits', self)
        self.button4.clicked.connect(self.Credits)
        self.button4.move(XPosStart, 4 * YPosStart)

        # quite game
        self.button5 = QPushButton('Quit', self)
        self.button5.clicked.connect(self.closeEvent)
        self.button5.move(XPosStart, 5 * YPosStart)

        # State: Start
        global START_STATE
        START_STATE = True

        self.show()


    def Instance(self):
        self.gBoard = Server.SpielFeld()
        return self.gBoard

    def startGame(self):
        self.Instance().start()
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
        if not START_STATE:
            app = QtGui.QGuiApplication.instance()
            app.closeAllWindows()

        self.close()

    def Back2Menu(self):
        Game.GAME_Menu(self)


class pause_Menu(start_Menu):

    def __init__(self):
        super().__init__()

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle('Pause Menu')

        self.button6 = QPushButton('Continue', self)
        self.button6.clicked.connect(self.back2Game)
        self.button6.move(XPosStart, YPosStart)

        # overwrite button1
        self.button1.hide()
        self.button6.show()

        # State: Pause
        global START_STATE
        START_STATE = False



    def back2Game(self):
        Server.SpielFeld.PAUSE = False
        self.close()

    def Back2Menu(self):
        self.pMenu = pause_Menu()
        self.close()



class OptionField(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUI()

    def InitUI(self):
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('Options')
        Server.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200, 400)

        self.table_widget = TableWidget(self)
        self.table_widget.resize(500,400)

        self.show()

    def Back2Menu(self):
        if START_STATE:
            start_Menu.Back2Menu(self)
        else:
            pause_Menu.Back2Menu(self)




class TableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QGridLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Keyboard")
        self.tabs.addTab(self.tab2, "Audio")
        self.tabs.addTab(self.tab3, "Grafik")

        # Create first tab
        self.tab1.layout = QGridLayout(self)
        #self.pushButton1 = QPushButton("PyQt5 button")

        #self.tab1.layout.addWidget(self.pushButton1, 0, 1, 1, 2)
        self.tab1.setLayout(self.tab1.layout)

        # create second tab
        self.tab2.layout = QGridLayout(self)

        #self.pushButton2 = QPushButton("Test")

        #self.tab2.layout.addWidget(self.pushButton2)
        self.tab2.setLayout(self.tab2.layout)


        # create content grafic tab
        self.tab3.layout = QHBoxLayout()

        # add wallG to tab3
        self.wallG = wallTexture()
        self.tab3.layout.addWidget(self.wallG)


        # add floorG to tab3
        self.floorG = floorTexture()
        self.tab3.layout.addWidget(self.floorG)


        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class wallTexture(QWidget):
    def __init__(self):
        super().__init__()

        self.iniUt()

    def iniUt(self):

        # set wall texture layout
        self.wallG = QGroupBox(self)
        self.wallG.setTitle("Texture Wall")

        self.button_layout1 = QVBoxLayout()
        self.texture1 = QRadioButton("Texture 1")

        self.texture2 = QRadioButton("Texture 2")

        self.button_layout1.addWidget(self.texture1)
        self.button_layout1.addWidget(self.texture2)

        # add button layout in wall layout
        self.wallG.setLayout(self.button_layout1)


class floorTexture(QWidget):
    def __init__(self):
        super().__init__()

        self.iniUt()

    def iniUt(self):

        # set floor texture layout
        self.floorG = QGroupBox(self)
        self.floorG.setTitle("Texture Floor")

        self.button_layout2 = QVBoxLayout()

        # creat button brown floor
        self.texture3 = QRadioButton("Brown Floor")
        self.texture3.setIcon(QIcon(Server.floorTextures["floor"]))
        self.texture3.setChecked(True)

        self.texture3.toggled.connect(self.onClicked)
        self.texture4 = QRadioButton("Texture 4")

        self.button_layout2.addWidget(self.texture3)
        self.button_layout2.addWidget(self.texture4)

        # add button layout in floor layout
        self.floorG.setLayout(self.button_layout2)

    def onClicked(self):
        Server.SpielFeld.floorTexture = Server.floorTextures["floor"]


class CreditText(QWidget):

    def __init__(self):
        super(CreditText, self).__init__()

        self.layout = QVBoxLayout()
        self.label = QLabel("")
        self.label.setText("CREATED BY \n \n Dominik \t aka B-Dome \n \n Jang Jang \t aka JangJang3 \n \n Fabian \t aka FabiPi"
                           "\n \n \n \n ")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.initUI()

    def initUI(self):
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('Credits')
        Server.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200,400)

        self.show()

    def Back2Menu(self):
        if START_STATE:
            start_Menu.Back2Menu(self)
        else:
            pause_Menu.Back2Menu(self)


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
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('How to Play')
        Server.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200,400)

        self.show()
        
    def Back2Menu(self):
        if START_STATE:
            start_Menu.Back2Menu(self)
        else:
            pause_Menu.Back2Menu(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())





