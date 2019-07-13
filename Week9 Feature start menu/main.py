"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMainWindow, QPushButton, QMessageBox, QLabel, \
    QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QVector2D, QPixmap, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QBasicTimer, QPoint
import sys
import math

import Server


WIDTH = 500
HEIGHT = 500

XPosStart = 25
YPosStart = 75

class Game (QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.resize(WIDTH, HEIGHT)
        Server.SpielFeld.center(self)
        self.setWindowTitle('Intro')
        #
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
        Server.SpielFeld.center(self)

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


        self.button5 = QPushButton('Quit', self)
        self.button5.clicked.connect(self.closeGame)
        self.button5.move(XPosStart, 5 * YPosStart)

        self.show()


    def startGame(self):
        self.gBoard = Server.SpielFeld()
        self.gBoard.start()
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

    def closeGame(self):
        self.close()

    def Back2Menu(self):
        Game.GAME_Menu(self)


class pause_Menu(start_Menu):

    def __init__(self):
        start_Menu.__init__(self)

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle('Break Menu')

        self.button1.setText('Continue')
        self.button1.clicked.connect(self.back2Game)

        self.show()


    def back2Game(self):
        self.close()





class OptionField(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUI()

    def InitUI(self):
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('Keyboard')
        Server.SpielFeld.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200, 400)

        self.show()


    def Back2Menu(self):
        start_Menu.Back2Menu(self)


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
        Server.SpielFeld.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200,400)

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
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('How to Play')
        Server.SpielFeld.center(self)

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





