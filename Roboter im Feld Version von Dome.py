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
vMax = 8
v_alpha_Max = 5

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
            print('Ges. ', self.v , '\n' , 'a ', self.a)
            if self.xPosition <= 400:
                SpielFeld.accelerate(self, self, 0.5, 0)
            else:
                SpielFeld.accelerate(self, self, -0.5, 0)
            time.sleep(0.2)
        

class RoboType2(BaseRobot):
    def run(self):
        while True:
            #print('hello this is Robo2 \n')
            
            time.sleep(1)

class RoboType3(BaseRobot):
    def run(self):
        while True:
            #print('hello this is Robo3 \n')
            
            time.sleep(1)

class RoboType4(BaseRobot):
    def run(self):
        while True:
            #print('hello this is Robo4 \n')
            
            time.sleep(1)
        

class SpielFeld(QWidget):
    
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
        # Roboterinstanzen
        #                     x    y    r  alph a a+  a_al al+ v v_al col
        self.Robo1 = RoboType1(400, 10, 15, 0, 0, 2, 0, 3, 0, 0, QColor(255, 0, 250))
        self.Robo2 = RoboType2(10, 900, 20, 0, 0, 2, 0, 3, 0, 0, QColor(0, 0, 250))
        self.Robo3 = RoboType3(900, 10, 25, 90, 0, 2, 0, 3, 0, 0, QColor(0, 145, 250))
        self.Robo4 = RoboType4(900, 900, 30, 225, 0, 2, 0, 4, 0, 0, QColor(245, 120, 0))

        self.Robo1.start()
        self.Robo2.start()
        self.Robo3.start()
        self.Robo4.start()
        
        self.show()

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def timerEvent(self, Event):
        self.moveRobo(self.Robo1)
        self.moveRobo(self.Robo2)
        self.moveRobo(self.Robo3)
        self.moveRobo(self.Robo4)
        
    def paintEvent(self, qp):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        self.drawRobo(self.Robo1, qp)
        self.drawRobo(self.Robo2, qp)
        self.drawRobo(self.Robo3, qp)
        self.drawRobo(self.Robo4, qp)
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

    def accelerate(self, Robo, add_a, add_alpha):
        #neue Beschleunigung
        if Robo.a + add_a <= -Robo.a_max:
            Robo.a = -Robo.a_max
        elif Robo.a + add_a < Robo.a_max:
            Robo.a += add_a
        elif Robo.a + add_a >= Robo.a_max:
            Robo.a = Robo.a_max


        #neue Drehbeschleunigung
        if Robo.a_alpha + add_alpha <= -Robo.a_alpha_max:
            Robo.a_alpha = -Robo.a_alpha_max
        elif Robo.a_alpha + add_alpha < Robo.a_alpha_max:
            Robo.a_alpha += add_alpha
        elif Robo.a_alpha + add_alpha >= Robo.a_alpha_max:
            Robo.a_alpha = Robo.a_alpha_max


    def moveRobo(self, Robo):

        #berechne neue Lenkrichtung
        if (Robo.v_alpha + Robo.a_alpha) < v_alpha_Max:
            Robo.v_alpha = (Robo.v_alpha + Robo.a_alpha)

        #Neue Richtung   
        Robo.alpha = (Robo.alpha + Robo.v_alpha) % 360

        #berechne neue Geschwindigkeit
        if (Robo.v + Robo.a) <= -vMax:
            Robo.v = -vMax
        elif (Robo.v + Robo.a) < vMax:
            Robo.v += Robo.a
        elif (Robo.v + Robo.a) >= vMax:
            Robo.v = vMax


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
