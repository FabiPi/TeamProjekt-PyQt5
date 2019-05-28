"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QBasicTimer
import sys
import math
import threading
import time

GameSpeed = 50
vMax = 15
v_alpha_Max = 25

class BaseRobot(threading.Thread):
    
    def __init__(self, xPosition, yPosition, radius, alpha, a, a_max, a_alpha, a_alpha_max, v, v_alpha, color):
        threading.Thread.__init__(self)
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.radius = radius
        self.alpha = alpha
        self.a = a
        self.a_max = a_max
        self.a_alpha = a_alpha
        self.a_alpha_max = a_alpha_max
        self.v = v
        self.v_alpha = v_alpha
        self.color = color

class RoboType1(BaseRobot):
    def run(self):
        while True:
            print('hello this is Robo1')
            
            time.sleep(1)
        

class RoboType2(BaseRobot):
    def run(self):
        while True:
            print('hello this is Robo2')
            
            time.sleep(1)

class RoboType3(BaseRobot):
    def run(self):
        while True:
            print('hello this is Robo3')
            
            time.sleep(1)

class RoboType4(BaseRobot):
    def run(self):
        while True:
            print('hello this is Robo4')
            
            time.sleep(1)
        

class SpielFeld(QWidget):
    
    # Roboterinstanzen
    #                 x    y    r  alph a a+  a_al al+ v v_al col
    Robo1 = RoboType1(500, 500, 15, 30, 0, 10, 1, 3, 2, 0, QColor(255, 0, 250))
    Robo2 = RoboType2(500, 500, 20, 0, 0, 10, 0.2, 3, 6, 0, QColor(0, 0, 250))
    Robo3 = RoboType3(500, 500, 25, 90, 0, 10, 0, 3, 15, 3, QColor(0, 145, 250))
    Robo4 = RoboType4(500, 500, 30, 225, 0, 10, 0, 4, 9, 2, QColor(245, 120, 0))

    Robo1.start()
    Robo2.start()
    Robo3.start()
    Robo4.start()
    
    #Array construction
    PlayFieldAR = [[0 for x in range(100)] for y in range(100)]

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Game.exe')
        self.center()
        self.timer = QBasicTimer()
        self.timer.start(GameSpeed, self)
        self.show()

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def paintEvent(self, qp):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        self.drawRobo(SpielFeld.Robo1, qp)
        self.drawRobo(SpielFeld.Robo2, qp)
        self.drawRobo(SpielFeld.Robo3, qp)
        self.drawRobo(SpielFeld.Robo4, qp)
        qp.end()

    def drawField(self, qp):

        #set Walls, set array value to 1 to place Wall

        #set Wall around the edges
        for x in range(0,100,1):
            SpielFeld.PlayFieldAR[x][0]= 1
            SpielFeld.PlayFieldAR[x][99]= 1
        for y in range(1,99,1):
            SpielFeld.PlayFieldAR[0][y]= 1
            SpielFeld.PlayFieldAR[99][y]= 1

        #set some Obstacle
        for i in range(0, 25, 1):
            SpielFeld.PlayFieldAR[70][i+45] = 1

        for i in range(0, 40, 1):
            SpielFeld.PlayFieldAR[i+10][40] = 1
        for i in range(0, 50, 1):
            SpielFeld.PlayFieldAR[i+30][70] = 1

        for i in range(0, 30, 1):
            SpielFeld.PlayFieldAR[i+25][20] = 1

        for i in range(0, 10, 1):
            SpielFeld.PlayFieldAR[10][i+50] = 1

        #Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if SpielFeld.PlayFieldAR[i][j]==1:
                        qp.setBrush(QColor(65, 50, 25))
                        qp.drawRect(i*10, j*10, 10, 10)
                    else:
                        qp.setBrush(QColor(50, 155, 50))
                        qp.drawRect(i*10, j*10, 10, 10)


    def drawRobo(self, Robo, br):

        br.setBrush(Robo.color)
        br.setPen(QColor(0,0,0))
        br.drawEllipse(Robo.xPosition, Robo.yPosition , 2* Robo.radius, 2*Robo.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(Robo.alpha)) * Robo.radius
        yPos = math.sin(math.radians(Robo.alpha)) * Robo.radius

        br.drawLine(Robo.xPosition + Robo.radius, Robo.yPosition + Robo.radius,
                    (Robo.xPosition + Robo.radius) + xPos, (Robo.yPosition + Robo.radius) - yPos)



        self.update()

    def moveRobo(self, Robo):

        #berechne neue Lenkrichtung
        if (Robo.v_alpha + Robo.a_alpha) < v_alpha_Max:
            Robo.v_alpha = (Robo.v_alpha + Robo.a_alpha)

        #Neue Richtung   
        Robo.alpha = (Robo.alpha + Robo.v_alpha) % 360

        #berechne neue Geschwindigkeit
        if (Robo.v + Robo.a) < vMax:
            Robo.v += Robo.a

        #X-Y Geschwindigkeit
        GesX = math.cos(math.radians(Robo.alpha)) * Robo.v
        GesY = -math.sin(math.radians(Robo.alpha)) * Robo.v

        #Neue Positiion
        Robo.xPosition += GesX 
        Robo.yPosition += GesY
        

  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SpielFeld()
    sys.exit(app.exec_())
