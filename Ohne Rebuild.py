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
import random

VISUALS =  True #False

SCREENWIDTH = 1000
SCREENHEIGHT = 1000

FPS = 100/ 30
GameStep = (1/ FPS)
alpha_eps = 0.5
vMax = 5
v_alpha_Max = 10
count = 0
PINK =  QColor(255, 0, 250)
DARKBLUE = QColor(0, 0, 250)
LIGHTBLUE = QColor(0, 145, 250)
ORANGE = QColor(245, 120, 0)


class BaseRobot(threading.Thread):
    #mit Id, Position, Richtung, max Beschleunigung, max Dreh.Beschl., Radius, Color
    def __init__(self, robotid, position, alpha, a_max, a_alpha_max, radius,FOV , color):
        threading.Thread.__init__(self)
        self.robotid = robotid
        self.position = position
        self.alpha = alpha
        self.a_max = a_max
        self.a_alpha_max = a_alpha_max
        self.radius = radius
        self.FOV = FOV
        self.color = color
        self.mass = radius*3

        #Values set to "0" so Robot stands still at the start
        self.v_vector = QVector2D(0,0)
        self.v_alpha = 0
        self.a = 0
        self.a_alpha= 0
        self.RobotList = {1 : QVector2D(0,0),
                          2 : QVector2D(0,0),
                          3 : QVector2D(0,0),
                          4 : QVector2D(0,0)}

    #brings Rotation to a halt
    def Stabilize(self):
        while self.v_alpha != 0:
            if self.v_alpha > 0:
                self.a_alpha = -0.5
            elif self.v_alpha < 0:
                self.a_alpha = 0.5
        self.a_alpha=0

    def ReStart(self):
            if self.v_vector.x() == self.v_vector.y() == 0:
                self.a_alpha= 0.7
                time.sleep(GameStep)
                self.a=1
                self.Stabilize()

    def velocity(self):
        return math.sqrt(math.pow(self.v_vector.x(),2) + math.pow(self.v_vector.y(),2))

    def checkChase(self, ID):
        xEnemy = self.RobotList[ID].x()
        yEnemy = self.RobotList[ID].y()

        xSelf = self.position.x()
        ySelf = self.position.y()

        spot = ''
        action =''

        #search position of enemy
        if xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'TopLeft'
        elif xEnemy >= xSelf and yEnemy <= ySelf:
            spot = 'TopRight'
        elif xEnemy <= xSelf and yEnemy >= ySelf:
            spot = 'BotLeft'
        elif xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'BotRight'

        #check direktion (rough)
        #right -> 0° up -> 90° left -> 180° down -> 270°
        view = ''

        if  0 <= self.alpha <= 90:
            view = 'TopRight'
        elif 90 <= self.alpha <= 180:
            view = 'TopLeft'
        elif 180 <= self.alpha <= 270:
            view = 'BotLeft'
        elif 270 <= self.alpha <= 360:
            view = 'BotRight'

        #determin turn-type
        if view == spot:
            #hard Turn
            action = 'hard Turn'
        elif (view == 'TopRight' and spot == 'BotLeft') or (view == 'TopLeft' and spot == 'TopRight') or (view == 'BotRight' and spot == 'TopLeft') or (view == 'BotLeft' and spot == 'TopRight'):
            #no turn
            action = 'no Turn'
        elif (view == 'TopRight' and spot == 'TopLeft') or (view == 'BotRight' and spot == 'TopRight') or (view == 'BotLeft' and spot == 'BotRight') or (view == 'TopLeft' and spot == 'BotLeft'):
            #left turn
            action = 'right Turn'
        else:
            #right turn
            action = 'left Turn'

        print(action)
        
        if action == 'hard Turn':
            self.a_alpha = 2
        elif action == 'no Turn':
            self.a_alpha = 0
        elif action == 'left Turn':
            self.a_alpha = 0.7
        elif action == 'right Turn':
            self.a_alpha = -0.7

    def lookTarget(self, ID):
        #Based on check Chase Method

        xEnemy = self.RobotList[ID].x()
        yEnemy = self.RobotList[ID].y()

        xSelf = self.position.x()
        ySelf = self.position.y()

        spot = ''
        action =''
        #search position of target
        if xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'TopLeft'
        elif xEnemy >= xSelf and yEnemy <= ySelf:
            spot = 'TopRight'
        elif xEnemy <= xSelf and yEnemy >= ySelf:
            spot = 'BotLeft'
        elif xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'BotRight'

        #check direktion (rough)
        #right -> 0° up -> 90° left -> 180° down -> 270°
        view = ''

        if  0 <= self.alpha <= 90:
            view = 'TopRight'
        elif 90 <= self.alpha <= 180:
            view = 'TopLeft'
        elif 180 <= self.alpha <= 270:
            view = 'BotLeft'
        elif 270 <= self.alpha <= 360:
            view = 'BotRight'

        #determin turn-type
        if view == spot:
            #hard Turn
            action = 'no Turn'
        elif (view == 'TopRight' and spot == 'BotLeft') or (view == 'TopLeft' and spot == 'TopRight') or (view == 'BotRight' and spot == 'TopLeft') or (view == 'BotLeft' and spot == 'TopRight'):
            #no turn
            action = 'hard Turn'
        elif (view == 'TopRight' and spot == 'TopLeft') or (view == 'BotRight' and spot == 'TopRight') or (view == 'BotLeft' and spot == 'BotRight') or (view == 'TopLeft' and spot == 'BotLeft'):
            #left turn
            action = 'left Turn'
        else:
            #right turn
            action = 'right Turn'

        print(action)
        
        if action == 'hard Turn':
            self.a_alpha = 2
        elif action == 'no Turn':
            self.a_alpha = 0
        elif action == 'left Turn':
            self.a_alpha = 0.7
        elif action == 'right Turn':
            self.a_alpha = -0.7


class RoboTypeRun(BaseRobot):  
    def run(self):
        while True:
            self.a = 1
            time.sleep(GameStep)
            for ID in range(2, 5,1):
                if self.position.distanceToPoint(self.RobotList[ID]) < 150:
                    #check where Chaser is
                    self.checkChase(ID)
                    time.sleep(0.5)
                    self.Stabilize()
            self.ReStart()


                

class RoboTypeChase1(BaseRobot):
    def run(self):
        self.a=1
        time.sleep(10* GameStep)
        self.a=-1
        time.sleep(2)
        self.position = QVector2D(800,800)
        while True:
                self.ReStart()


class RoboTypeChase2(BaseRobot):
    def run(self):
        while True:
            self.a = 1
            time.sleep(GameStep)
            if self.position.distanceToPoint(self.RobotList[1]) < 250:
                #check where Chaser is
                self.lookTarget(1)
                time.sleep(0.5)
                self.Stabilize()
            self.ReStart()

class RoboTypeChase3(BaseRobot):
    def run(self):
        while True:
            self.a = 1
            self.ReStart()


class SpielFeld(QWidget):

    #Array construction
    PlayFieldAR = [[0 for x in range(100)] for y in range(100)]
    BarrierList = []

    # Teleport Positions
    TP_TopL = QVector2D(100, 100)
    TP_TopR = QVector2D(850, 100)
    TP_BotL = QVector2D(100, 850)
    TP_BotR = QVector2D(850, 850)


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
            
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                if SpielFeld.PlayFieldAR[i][j]==1:
                    SpielFeld.BarrierList.append(QVector2D(i,j))
        
        #init Robots
        Robot1 = RoboTypeRun(1, QVector2D(500,500), 0, 2, 2, 20, 40 ,PINK)
        Robot2 = RoboTypeChase1(2, QVector2D(200,200), 90, 2, 2, 20, 50,DARKBLUE)
        Robot3 = RoboTypeChase2(3, QVector2D(550,550), 180, 2, 2, 30, 60,LIGHTBLUE)
        Robot4 = RoboTypeChase3(4, QVector2D(600,150), 270, 2, 2, 25, 85,ORANGE)

        self.robots = [Robot1, Robot2, Robot3, Robot4]

        for robot in self.robots:
            robot.start()

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
        
        #update RobotLists of each Robot
        if self.tickCount % 10 == 0:
            for y in self.robots:
                for x in self.robots:
                    y.RobotList[x.robotid] = x.position

        # move robots on the game field
        for robot in self.robots:
            self.moveRobot(robot)
            self.barrierCollision(robot)
            self.collision(robot, self.robots[0])

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

        #draw FOV
        if VISUALS:
            br.setPen(QColor(255,255,255))
            xPos = math.cos(math.radians(Robo.alpha + (Robo.FOV/2))) * Robo.radius
            yPos = math.sin(math.radians(Robo.alpha + (Robo.FOV/2))) * Robo.radius
            br.drawLine(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius,
                        (int(round(Robo.position.x())) + Robo.radius) + 10*xPos, (int(round(Robo.position.y())) + Robo.radius) - 10*yPos)
            xPos = math.cos(math.radians(Robo.alpha - (Robo.FOV/2))) * Robo.radius
            yPos = math.sin(math.radians(Robo.alpha - (Robo.FOV/2))) * Robo.radius
            br.drawLine(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius,
                        (int(round(Robo.position.x())) + Robo.radius) + 10*xPos, (int(round(Robo.position.y())) + Robo.radius) - 10*yPos)
 

    def drawField(self, qp):
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
        if (abs(Robo.v_alpha) <= alpha_eps) and (abs(Robo.a_alpha) <= alpha_eps):
            Robo.v_alpha = 0
        elif (Robo.v_alpha + Robo.a_alpha) < -v_alpha_Max:
            Robo.v_alpha = -v_alpha_Max
        elif (Robo.v_alpha + Robo.a_alpha) <= v_alpha_Max:
            Robo.v_alpha = (Robo.v_alpha + Robo.a_alpha)
        elif (Robo.v_alpha + Robo.a_alpha) >= v_alpha_Max:
            Robo.v_alpha = v_alpha_Max

        #Neue Richtung
        Robo.alpha = (Robo.alpha + Robo.v_alpha) % 360
        
        #berechne geschwindigkeit
        v= math.sqrt(math.pow(Robo.v_vector.x(),2) + math.pow(Robo.v_vector.y(),2))
        
        if (v + Robo.a) <= 0:
            v = 0
            Robo.a = 0
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

    def distanceTwoPoints(self, x1, y1, x2, y2):
        return math.sqrt((x2-x1) * (x2-x1) + (y2-y1)*(y2-y1))

    def is_overlapping (self, x1, y1, r1,x2, y2, r2):
        return self.distanceTwoPoints(x1, y1, x2, y2) < (r1+r2)


    def barrierCollision(self, robo):
        #Collision with Obstacles
        PosX = int(round(robo.position.x()/ 10))
        PosY = int(round(robo.position.y()/ 10))
        Rad = int(round((robo.radius *2)/10))
        for i in range(0, Rad, 1):
            #oben
            if (SpielFeld.PlayFieldAR[PosX + i][PosY-1] == 1) & (robo.v_vector.y()<0):
                robo.position.__isub__(robo.v_vector)
                robo.v_vector = QVector2D(0,0)
                robo.a = 0
            #unten
            if (SpielFeld.PlayFieldAR[PosX + i][PosY + Rad] == 1) & (robo.v_vector.y()>0):
                robo.position.__isub__(robo.v_vector)
                robo.v_vector = QVector2D(0,0)
                robo.a = 0
            #links
            if (SpielFeld.PlayFieldAR[PosX - 1][PosY + i] == 1) & (robo.v_vector.x()<0):
                robo.position.__isub__(robo.v_vector)
                robo.v_vector = QVector2D(0,0)
                robo.a = 0
            #rechts
            if (SpielFeld.PlayFieldAR[PosX + Rad][PosY + i] == 1) & (robo.v_vector.x()>0):
                robo.position.__isub__(robo.v_vector)
                robo.v_vector = QVector2D(0,0)
                robo.a = 0


    def collision(self, robo, target):
        for robot in self.robots:
            if robot != robo and robot != target and robo != target :
                distance = self.distanceTwoPoints(int(round(robot.position.x())) + robot.radius,
                                                  int(round(robot.position.y()))+ robot.radius,
                                                  int(round(robo.position.x())) + robo.radius,
                                                  int(round(robo.position.y())) + robo.radius)


                if self.is_overlapping(int(round(robot.position.x())) + robot.radius, int(round(robot.position.y())) + robot.radius, robot.radius,
                                       int(round(robo.position.x())) + robo.radius, int(round(robo.position.y()))+ robo.radius,
                                       robo.radius) and distance < robot.radius + robo.radius :

                    # with elastic collision, does not apply to the reality because of spin, friction etc.
                    # our only concern is the mass of the robots
                    # new velocity of robo1
                    newVelX1 = (int(round(robo.v_vector.x())) * (robo.mass - robot.mass) + (2 * robot.mass * int(round(robot.v_vector.x())))) / (
                            robo.mass + robot.mass)
                    newVelY1 = (int(round(robo.v_vector.y()))* (robo.mass - robot.mass) + (2 * robot.mass * int(round(robot.v_vector.y())))) / (
                            robo.mass + robot.mass)

                    # new velocity of robo2
                    newVelX2 = (int(round(robot.v_vector.x())) * (robot.mass - robo.mass) + (2 * robo.mass * int(round(robo.v_vector.x())))) / (
                            robo.mass + robot.mass)
                    newVelY2 = (int(round(robot.v_vector.y())) * (robot.mass - robo.mass) + (2 * robo.mass * int(round(robo.v_vector.y())))) / (
                            robo.mass + robot.mass)

                    newV_1 = QVector2D(newVelX1, newVelY1)
                    newV_2 = QVector2D(newVelX2, newVelY2)

                    robo.position.__iadd__(newV_1)

                    robot.position.__iadd__(newV_2)

            else: self.teleport(target, robo)



    def teleport(self, target, robot):

        if robot != target:
            distance = self.distanceTwoPoints(int(round(robot.position.x())) + robot.radius,
                                              int(round(robot.position.y())) + robot.radius,
                                              int(round(target.position.x())) + target.radius,
                                              int(round(target.position.y())) + target.radius)

            if distance <= target.radius + robot.radius:

                if  int(round(target.position.x())) > 500 and  int(round(target.position.y())) < 500:

                    robot.position = QVector2D(100,850)

                elif int(round(target.position.x())) > 500 and int(round(target.position.y())) > 500:
                    robot.position = QVector2D(100,100)

                elif int(round(target.position.x())) < 500 and int(round(target.position.y())) < 500:
                    robot.position = QVector2D(850,850)


                elif int(round(target.position.x())) < 500 and int(round(target.position.y())) > 500:
                    robot.position = QVector2D(850,100)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SpielFeld()
    sys.exit(app.exec_())
