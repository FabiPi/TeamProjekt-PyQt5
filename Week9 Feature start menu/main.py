"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, \
    QVBoxLayout, QTabWidget, QRadioButton, QHBoxLayout, QGridLayout, QGroupBox

import sys

import Server


WIDTH = 500
HEIGHT = 500

XPosStart = 25
YPosStart = 75

#default setting
CurRBtn = "Brown floor "

class Game (QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.resize(WIDTH, HEIGHT)
        Server.center(self)
        self.setWindowTitle('Intro')
        self.enter = QPushButton('enter', self)
        self.enter.move(50,400)
        self.enter.resize(400, 50)
        self.enter.clicked.connect(self.gameMenu)

        self.show()

    def gameMenu(self):
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
        self.button5.clicked.connect(self.close)
        self.button5.move(XPosStart, 5 * YPosStart)

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
        self.close()

    def Back2Menu(self):
        Game.gameMenu(self)



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
        #QtGui.QGuiApplication.processEvents()
        self.table_widget.resize(500,400)

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
        #self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Keyboard")
        #self.tabs.addTab(self.tab2, "Audio")
        self.tabs.addTab(self.tab3, "Grafik")

        # Create first tab
        self.tab1.layout = QGridLayout(self)
        #self.pushButton1 = QPushButton("PyQt5 button")

        #self.tab1.layout.addWidget(self.pushButton1, 0, 1, 1, 2)
        self.tab1.setLayout(self.tab1.layout)

        # create second tab
        #self.tab2.layout = QGridLayout(self)

        #self.pushButton2 = QPushButton("Test")

        #self.tab2.layout.addWidget(self.pushButton2)
        #self.tab2.setLayout(self.tab2.layout)


        # create content grafic tab
        self.tab3.layout = QVBoxLayout()

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


class wallTexture(QWidget):
    def __init__(self):
        super().__init__()

        # set wall texture layout
        self.wallG = QGroupBox(self)

        # set button layout
        self.button_layout1 = QVBoxLayout()

        self.texture1 = QRadioButton("Texture 1")
        self.texture2 = QRadioButton("Texture 2")
        self.btn = QPushButton("Select")

        self.iniUt()

    def iniUt(self):

        self.wallG.setTitle("Texture Wall")

        self.btn.clicked.connect(self.onClicked)


        self.button_layout1.addWidget(self.texture1)
        self.button_layout1.addWidget(self.texture2)
        self.button_layout1.addWidget(self.btn)

        # add button layout in wall layout
        self.wallG.setLayout(self.button_layout1)

    def onClicked(self):
        print("why")



class floorTexture(QWidget):

    def __init__(self):
        super().__init__()

        # set floor texture layout
        self.floorG = QGroupBox(self)

        # set button layout
        self.button_layout2 = QVBoxLayout()


        # create floor texture buttons
        self.texture3 = QRadioButton("Brown Floor")
        self.texture4 = QRadioButton("Wood Floor")
        # create selector
        self.btn = QPushButton("Select")

        self.currentRBtn = self.texture3

        # set texture choice
        self.label = QLabel(self)

        # change style of lettering
        self.style = QFont()
        self.style.setBold(True)
        self.label.setFont(self.style)

        self.chk_RBtn()
        print(CurRBtn)

        self.iniUt()

    def iniUt(self):

        self.floorG.setTitle("Texture Floor")


        # creat button brown floor
        self.texture3.setIcon(QIcon(Server.floorTextures["Brown floor"]))
        self.texture3.clicked.connect(lambda: self.rBtn_clk(self.texture3))

        # default texture


        # create button wood floor
        self.texture4.setIcon(QIcon(Server.floorTextures["Wood floor"]))
        self.texture4.clicked.connect(lambda: self.rBtn_clk(self.texture4))

        self.label.setText('currently used\n' + CurRBtn )

        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))

        #self.texture4.setChecked(True)
        self.button_layout2.addWidget(self.texture3)
        self.button_layout2.addWidget(self.texture4)
        self.button_layout2.addWidget(self.btn)
        self.button_layout2.addWidget(self.label)

        # add button layout in floor layout
        self.floorG.setLayout(self.button_layout2)

    # show new setting, after returing to options
    def chk_RBtn(self):
        if CurRBtn == "Wood floor":
            self.texture3.setChecked(False)
            self.texture4.setChecked(True)


        elif CurRBtn == "Brown floor":
            self.texture4.setChecked(False)
            self.texture3.setChecked(True)
            print('testing branch')
        else:
            self.texture3.setChecked(True)


    def rBtn_clk(self, button):
        self.currentRBtn = button
        #print("nach dem Klick", self.currentRBtn.text())

    def btn_clk(self, button):
        global CurRBtn

        if button == self.texture3:
            Server.ftexture = "Brown floor"
            CurRBtn = "Brown floor"

        elif button == self.texture4:
            Server.ftexture = "Wood floor"
            CurRBtn = "Wood floor"
        else:
            pass

        self.label.setText("You selected: \n" + button.text())





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

