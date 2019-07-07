"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D
from PyQt5.QtCore import Qt, QBasicTimer
import sys
import math
import threading
import time

SCREENWIDTH = 1000
SCREENHEIGHT = 1000

FPS = 100/ 30
GameStep = 1/ FPS
vMax = 8
v_alpha_Max = 10
count = 0
PINK =  QColor(255, 0, 250)
DARKBLUE = QColor(0, 0, 250)
LIGHTBLUE = QColor(0, 145, 250)
ORANGE = QColor(245, 120, 0)

class RobotData(object):
    #mit Id, Position, Richtung, max Beschleunigung, max Dreh.Beschl., Radius, Color
    def __init__(self, robotid, position, alpha, a_max, a_alpha_max, radius, color):
        self.robotid = robotid
        self.position = position
        self.alpha = alpha
        self.a_max = a_max
        self.a_alpha_max = a_alpha_max
        self.radius = radius
        self.color = color

        #Values set to "0" so Robot stands still at the start
        self.v_vector = QVector2D(0,0)
        self.v_alpha = 0
        self.a = 0
        self.a_alpha= 0
        self.RobotList = {}

#class RobotControl
        #TODO ROBOT-CONTROL

class SpielFeld(QWidget):

    #Array construction
    PlayFieldAR = [[0 for x in range(100)] for y in range(100)]
    #Dictionary for RobotPositions
    RobotList={1 : "temp",
               2 : "temp",
               3 : "temp",
               4 : "temp"}


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(0, 0, SCREENWIDTH, SCREENHEIGHT)
        self.setWindowTitle('Game.exe')
        self.center()
        self.timer = QBasicTimer()
        self.timer.start(FPS, self)
        self.tickCount = 0

        #init Robots
        self.Robot1 = RobotData(1, QVector2D(50,110), 300, 2, 2, 15, PINK)
        self.Robot2 = RobotData(2, QVector2D(500,500), 150, 2, 2, 15, DARKBLUE)
        self.Robot3 = RobotData(3, QVector2D(400,460), 240, 2, 2, 15, LIGHTBLUE)
        self.Robot4 = RobotData(4, QVector2D(360,260), 30, 2, 2, 15, ORANGE)

        #temporary Robot Actions
        self.Robot1.v_vector = QVector2D(2,2)
        self.Robot1.v_alpha = 3
        self.Robot2.v_vector = QVector2D(2,2)
        self.Robot3.v_vector = QVector2D(2,2)
        self.Robot4.v_vector = QVector2D(2,2)

        self.robots = [self.Robot1, self.Robot2, self.Robot3, self.Robot4]

        #Start RobotThreads
        #for robot in self.robots:
        #    robot.start()
        
        self.show()

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def timerEvent(self, Event):
        #Count
        self.tickCount += 1

        #update RobotPositions each step
        for robot in self.robots:
            self.RobotList[robot.robotid] = robot.position

        #update RobotLists of each Robot
        if self.tickCount % 10 == 0:
            for robot in self.robots:
                #print(self.RobotList[robot.robotid].x(), '---', self.RobotList[robot.robotid].y())
                robot.RoboList = self.RobotList

        # move robots on the game field
        for robot in self.robots:
            self.moveRobot(robot)
            self.barrierCollision(robot)
            #TODO COLLISION
                   
        self.update()

    def paintEvent(self, qp):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        # draw Robots on the game field
        for robot in self.robots:
            self.drawRobo(robot,qp)
        

    def drawRobo(self, Robo, br):
        br.setBrush(Robo.color)
        br.setPen(QColor(0,0,0))
        br.drawEllipse(int(round(Robo.position.x())), int(round(Robo.position.y())) , 2* Robo.radius, 2*Robo.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(Robo.alpha)) * Robo.radius
        yPos = math.sin(math.radians(Robo.alpha)) * Robo.radius

        br.drawLine(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius,
                    (int(round(Robo.position.x())) + Robo.radius) + xPos, (int(round(Robo.position.y())) + Robo.radius) - yPos)
        
            
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

    def moveRobot(self, Robo):
        #berechne neue Lenkrichtung
        if (Robo.v_alpha + Robo.a_alpha) < -v_alpha_Max:
            Robo.v_alpha = -v_alpha_Max
        elif (Robo.v_alpha + Robo.a_alpha) <= v_alpha_Max:
            Robo.v_alpha = (Robo.v_alpha + Robo.a_alpha)
        elif (Robo.v_alpha + Robo.a_alpha) >= v_alpha_Max:
            Robo.v_alpha = v_alpha_Max

        #Neue Richtung
        Robo.alpha = (Robo.alpha + Robo.v_alpha) % 360
        
        #berechne geschwindigkeit
        v= math.sqrt(math.pow(Robo.v_vector.x(),2) + math.pow(Robo.v_vector.y(),2))
        if (v + Robo.a) <= -vMax:
            v = -vMax
        elif (v + Robo.a) < vMax:
            v += Robo.a
        elif (v + Robo.a) >= vMax:
            v = vMax

        #X-Y Geschwindigkeit
        GesX = math.cos(math.radians(Robo.alpha)) * v
        GesY = - math.sin(math.radians(Robo.alpha)) * v

        #setze neue Geschwindigkeit
        Robo.v_vector = QVector2D(GesX,GesY)

        #berechne neue Position
        Robo.position.__iadd__(Robo.v_vector)

    def barrierCollision(self, robo):
        #Collision with Obstacles
        PosX = int(round(robo.position.x()/ 10))
        PosY = int(round(robo.position.y()/ 10))
        Rad = int(round((robo.radius *2)/10))
        for i in range(0, Rad, 1):
            #oben
            if (SpielFeld.PlayFieldAR[PosX + i][PosY-1] == 1) & (robo.v_vector.y()<0):
                robo.v_vector = QVector2D(0,0)     
            #unten
            if (SpielFeld.PlayFieldAR[PosX + i][PosY + Rad] == 1) & (robo.v_vector.y()>0):
                robo.v_vector = QVector2D(0,0) 
            #links
            if (SpielFeld.PlayFieldAR[PosX - 1][PosY + i] == 1) & (robo.v_vector.y()<0):
                robo.v_vector = QVector2D(0,0) 
            #rechts
            if (SpielFeld.PlayFieldAR[PosX + Rad][PosY + i] == 1) & (robo.v_vector.y()>0):
                robo.v_vector = QVector2D(0,0)

    def distanceTwoPoints(self, x1, y1, x2, y2):
        return math.sqrt((x2-x1) * (x2-x1) + (y2-y1)*(y2-y1))

    def is_overlapping (self, x1, y1, r1,x2, y2, r2):
        return self.distanceTwoPoints(x1, y1, x2, y2) < (r1+r2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SpielFeld()
    sys.exit(app.exec_())
