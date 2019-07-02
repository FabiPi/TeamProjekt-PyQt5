"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QBasicTimer, QPoint
import sys
import math
import threading
import time
import Robots
import Bullet

SCREENWIDTH = 1000
SCREENHEIGHT = 1000
FPS = 100/ 30
GameStep = (1/ FPS)
alpha_eps = 0.5
vMax = 3
v_alpha_Max = 3
count = 0

# color library
colors = {
    "pink":     QColor(255, 0, 250),
    "darkblue": QColor(0, 0, 250),
    "lightblue": QColor(0, 145, 250),
    "orange": QColor(245, 120, 0),
    "black": QColor(0,0,0),
    "yellow": QColor(255,255,0)
}



VISUALS =  True

class SpielFeld(QWidget):

    #Array construction
    PlayFieldAR = [[0 for x in range(100)] for y in range(100)]
    BarrierList = []


    def __init__(self):
        super().__init__()

        self.wallTexture = QPixmap('textures/wall.png')
        self.floorTexture = QPixmap('textures/floor.png')
        self.createBoard()

        #init Robots
        Robot1 = Robots.Robot(1, QVector2D(50,110), 0, 2, 2, 15, 90, colors["pink"])
        Robot2 = Robots.Robot(2, QVector2D(500,500), 20, 2, 2, 15, 90, colors["darkblue"])
        Robot3 = Robots.Robot(3, QVector2D(400,460), 240, 2, 2, 15, 90, colors["lightblue"])
        Robot4 = Robots.Robot(4, QVector2D(360,260), 30, 2, 2, 15, 90, colors["orange"])
        #test
        Bullet1 = Bullet.Bullet(QVector2D(50,50), QVector2D(1,1))


        Robot1.setProgram(Robots.TargetChase(Robot1))
        Robot2.setProgram(Robots.TargetChase2(Robot2))
        Robot3.setProgram(Robots.TargetChase3(Robot3))
        Robot4.setProgram(Robots.TargetChase4(Robot4))

        self.robots = [Robot1, Robot2, Robot3, Robot4]
        self.bullets = []
        self.bullets.append(Bullet1)

        Robot1.executeProgram()
        Robot2.executeProgram()
        Robot3.executeProgram()
        Robot4.executeProgram()

        self.timer = QBasicTimer()
        self.timer.start(FPS, self)
        self.tickCount = 0

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, SCREENWIDTH, SCREENHEIGHT)
        self.setWindowTitle('Game.exe')
        self.center()



        self.show()



    def createBoard(self):

        #set Walls, set array value to 1 to place Wall
        #set Wall around the edges

        #SpielFeld.PlayFieldAR[90][90] = 1
        #SpielFeld.PlayFieldAR[10][10] = 1

        for x in range(0,100,1):
            SpielFeld.PlayFieldAR[x][0]= 1
            SpielFeld.PlayFieldAR[x][99]= 1
        for y in range(1,99,1):
            SpielFeld.PlayFieldAR[0][y]= 1
            SpielFeld.PlayFieldAR[99][y]= 1

        #set some Obstacle
        for i in range(0, 25, 1):
            SpielFeld.PlayFieldAR[70][i+45] = 1
            SpielFeld.PlayFieldAR[71][i+45] = 1

        for i in range(0, 40, 1):
            SpielFeld.PlayFieldAR[i+10][40] = 1
            SpielFeld.PlayFieldAR[i+10][41] = 1
        for i in range(0, 50, 1):
            SpielFeld.PlayFieldAR[i+30][70] = 1
            SpielFeld.PlayFieldAR[i+30][71] = 1

        for i in range(0, 30, 1):
            SpielFeld.PlayFieldAR[i+25][20] = 1
            SpielFeld.PlayFieldAR[i+25][21] = 1

        for i in range(0, 10, 1):
            SpielFeld.PlayFieldAR[10][i+50] = 1
            SpielFeld.PlayFieldAR[11][i+50] = 1


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
        if self.tickCount % 5 == 0:
            for y in self.robots:
                for x in self.robots:
                    y.RobotList[x.robotid] = x.position

        # move robots on the game field
        for robot in self.robots:
            self.moveRobot(robot)
            #self.barrierCollision(robot)
            self.roboCollision(robot, self.robots[0])
            self.SightingData(robot)
        for bul in self.bullets:
            bul.moveBullet()

        self.update()

    def paintEvent(self, qp):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        # draw Robots on the game field
        for robot in self.robots:
            self.drawRobo(robot,qp)
            #qp.drawPath(self.FOV(robot))
        for bul in self.bullets:
            bul.drawBullet(qp)



    def drawRobo(self, Robo, br):
        br.setBrush(Robo.color)
        br.setPen(colors["black"])
        br.drawEllipse(int(round(Robo.position.x())), int(round(Robo.position.y())) , 2* Robo.radius, 2*Robo.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(Robo.alpha)) * Robo.radius
        yPos = math.sin(math.radians(Robo.alpha)) * Robo.radius

        br.drawLine(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius,
                    (int(round(Robo.position.x())) + Robo.radius) + xPos, (int(round(Robo.position.y())) + Robo.radius) - yPos)


    def FOV(self, Robo):
        view = QPainterPath()

        xPos = math.cos(math.radians(Robo.alpha + (Robo.FOV / 2))) * Robo.radius
        yPos = math.sin(math.radians(Robo.alpha + (Robo.FOV / 2))) * Robo.radius

        xPos2 = math.cos(math.radians(Robo.alpha - (Robo.FOV / 2))) * Robo.radius
        yPos2 = math.sin(math.radians(Robo.alpha - (Robo.FOV / 2))) * Robo.radius

        x1 = QPoint(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius)
        x2 = x1 + QPoint((int(round(Robo.position.x())) + Robo.radius) + 1000 * xPos, (int(round(Robo.position.y())) + Robo.radius) - 1000 * yPos)
        x3 = x1 + QPoint((int(round(Robo.position.x())) + Robo.radius) + 1000 * xPos2, (int(round(Robo.position.y())) + Robo.radius) - 1000 * yPos2)

        view.addPolygon(QPolygonF([x1, x2, x3]))
        view.closeSubpath()

        return view

    def SightingData(self, robo):

        viewPanel = self.FOV(robo)

        ids = []

        # seeing other robots in FOV
        for x in self.robots:
            if robo != x:
                if viewPanel.intersects(x.roboShape()):
                    ids.append(x.robotid)
                    #print(robo.robotid, ids)
                else:
                    robo.ViewList[x.robotid][3] = False

        # update ViewList
        for id in ids:
            for robot in self.robots:

                if robot.robotid == id and (robo.position - robot.position).length() < 400:
                    viewedRobo = robot.robotid
                    distance = (robo.position - robot.position).length()
                    viewedDirection = robot.alpha
                    seen = True

                    toUpDate = {viewedRobo: [robot.position, distance, viewedDirection, seen]}

                    robo.ViewList.update(toUpDate)
                    #print(robo.robotid, robo.ViewList)


    def drawField(self, qp):
        qp.setPen(Qt.NoPen)
        #Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if SpielFeld.PlayFieldAR[i][j]==1:
                        texture = self.wallTexture
                        self.BarrierList.append(texture)
                    else:
                        texture = self.floorTexture
                    qp.drawPixmap(i*10, j*10, texture)


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
        if (Robo.v + Robo.a) <= -vMax:
            Robo.v = -vMax
        elif (Robo.v + Robo.a) < vMax:
            Robo.v += Robo.a
        elif (Robo.v + Robo.a) >= vMax:
            Robo.v = vMax

        #X-Y Geschwindigkeit
        GesX = math.cos(math.radians(Robo.alpha)) * Robo.v
        GesY = - math.sin(math.radians(Robo.alpha)) * Robo.v

        #setze neue Geschwindigkeit
        Robo.v_vector = QVector2D(GesX,GesY)

        #berechne neue Position
        Robo.position.__iadd__(Robo.v_vector)


    def distanceTwoPoints(self, x1, y1, x2, y2):
        return math.sqrt((x2-x1) * (x2-x1) + (y2-y1)*(y2-y1))


    def distance(self, robo1, robo2):
        return self.distanceTwoPoints(int(round(robo1.position.x())) + robo1.radius,
                                                  int(round(robo1.position.y()))+ robo1.radius,
                                                  int(round(robo2.position.x())) + robo2.radius,
                                                  int(round(robo2.position.y())) + robo2.radius)


    def roboCollision(self, robo, target):
        for robot in self.robots:
            if robot != robo and robot != target and robo != target :
                distance = self.distance(robot, robo)

                if distance <= robot.radius + robo.radius :

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

        MID = 500

        if robot != target:
            distance = self.distance(robot, target)

            if distance <= target.radius + robot.radius:

                if  int(round(target.position.x())) > MID and  int(round(target.position.y())) < MID:

                    robot.position = QVector2D(100,850)

                elif int(round(target.position.x())) > MID and int(round(target.position.y())) > MID:
                    robot.position = QVector2D(100,100)

                elif int(round(target.position.x())) < MID and int(round(target.position.y())) < MID:
                    robot.position = QVector2D(850,850)


                elif int(round(target.position.x())) < MID and int(round(target.position.y())) > MID:
                    robot.position = QVector2D(850,100)


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
                    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SpielFeld()
    sys.exit(app.exec_())
