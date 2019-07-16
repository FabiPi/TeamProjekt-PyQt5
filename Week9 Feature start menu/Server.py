"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QVector2D, QPixmap, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QBasicTimer, QPoint, pyqtSignal
import math

import Robots
import Controller
import main

SCREENWIDTH = 1000
SCREENHEIGHT = 1000

FPS = 100/ 30
GameStep = (1/ FPS)
alpha_eps = 0.5
vMax = 3
v_alpha_Max = 2
count = 0
DEATH_TIME = 100
IMMUNE_TIME = 150


# color libraries
colors = {
    "pink":     QColor(255, 0, 250),
    "darkblue": QColor(0, 0, 250),
    "lightblue": QColor(0, 145, 250),
    "orange": QColor(245, 120, 0),
    "black": QColor(0,0,0),
    "yellow": QColor(255,255,0)
}

def center(self):
    '''centers the window on the screen'''

    screen = QDesktopWidget().screenGeometry()
    size = self.geometry()
    self.move((screen.width() - size.width()) / 2,
              (screen.height() - size.height()) / 2)

class SpielFeld(QWidget):

    #Array construction
    PlayFieldAR = [[0 for x in range(100)] for y in range(100)]
    BarrierList = []
    Bullets = []

    def __init__(self):
        super().__init__()

        self.wallTexture = QPixmap('textures/wall.png')
        self.floorTexture = QPixmap('textures/floor.png')
        self.createBoard()

        #init Robots
        Robot1 = Robots.Robot(1, QVector2D(200,250), 290, 2, 2, 15, 90, colors["pink"])
        Robot2 = Robots.Robot(2, QVector2D(200,600), 10, 2, 2, 15, 90, colors["darkblue"])
        Robot3 = Robots.Robot(3, QVector2D(250,650), 270, 2, 2, 15, 90, colors["lightblue"])
        Robot4 = Robots.Robot(4, QVector2D(950,100), 180, 2, 2, 15, 90, colors["orange"])


        Robot1.setProgram(Controller.RunAwayKeyBoard(Robot1))
        Robot2.setProgram(Controller.TargetHunt(Robot2))
        Robot3.setProgram(Controller.TargetHunt(Robot3))
        Robot4.setProgram(Controller.TargetHunt(Robot4))

        self.robots = [Robot1, Robot2, Robot3, Robot4]
        
        Robot1.executeProgram()
        Robot2.executeProgram()
        Robot3.executeProgram()
        Robot4.executeProgram()

        self.timer = QBasicTimer()
        self.tickCount = 0

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, SCREENWIDTH, SCREENHEIGHT)
        self.setWindowTitle('Game.exe')
        center(self)

        self.isStarted = False
        self.isPaused = False

        self.show()

    
    def start(self):
        if self.isPaused:
            return
        
        # start GameBoard
        self.isStarted = True
        self.timer.start(FPS, self)

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
            if robot.deathTime == 0:
                self.fetchBullets(robot)
                self.moveRobot(robot)
            self.barrierCollision(robot)
            self.roboCollision(robot)
            self.SightingData(robot)
            self.reduceDelay(robot)
            self.reduceDeathTime(robot)
            self.reduceImmuneTime(robot)

            

        for bul in SpielFeld.Bullets:
            bul.moveBullet()
            if self.BulletBarrierCollision(bul):
               SpielFeld.Bullets.remove(bul)
            for robot in self.robots:
                if bul.one_hit(robot):
                    if robot.robotid == 1 and robot.immuneTime == 0 and robot.deathTime == 0:
                        #print('oof')
                        robot.deathTime = DEATH_TIME
                        robot.color = QColor(255, 0, 250, 50)
                    elif robot.robotid != 1:
                        self.teleport_bullet(robot)
                    if bul in SpielFeld.Bullets:
                        SpielFeld.Bullets.remove(bul)

            
        self.update()

    def fetchBullets(self,Robot):
        SpielFeld.Bullets.extend(Robot.BulList)
        #print(SpielFeld.Bullets)
        Robot.BulList.clear()

    def reduceDelay(self,Robot):
        if Robot.reload != 0:
            Robot.reload -= 1
            
    # Death Counter (Down) {see Constants}
    def reduceDeathTime(self,Robot):
        if Robot.deathTime != 0:
            Robot.deathTime -= 1
            if Robot.deathTime == 0:
                Robot.immuneTime = IMMUNE_TIME
                Robot.color = colors["yellow"]
            
    def reduceImmuneTime(self,Robot):
        if Robot.immuneTime != 0:
            Robot.immuneTime -= 1
            if Robot.immuneTime == 0:
                Robot.color = colors["pink"]

    def teleport_bullet(self, robo):
        robo.position = QVector2D(100,850) 
        

    def paintEvent(self, qp):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        # draw Robots on the game field
        for robot in self.robots:
            self.drawRobo(robot,qp)
            #qp.drawPath(self.FOV(robot))
        for bul in SpielFeld.Bullets:
            #qp.drawPath(bul.bulletShape())
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

                if robot.robotid == id and (robo.position - robot.position).length() < 200:
                    viewedRobo = robot.robotid
                    distance = (robo.position - robot.position).length()
                    viewedDirection = robot.alpha
                    seen = True

                    toUpDate = {viewedRobo: [robot.position, distance, viewedDirection, seen]}

                    robo.ViewList.update(toUpDate)
                    #print(robo.robotid, robo.ViewList)



    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

    def closeEvent(self, event):
        app = QtGui.QGuiApplication.instance()
        app.closeAllWindows()        


    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        
        if self.isPaused:
            self.timer.stop()
            self.pMenu = main.pause_Menu()
        else:
            self.timer.start(FPS, self)

        self.update()

        
    def drawField(self, qp):
        qp.setPen(Qt.NoPen)
        # Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                if SpielFeld.PlayFieldAR[i][j] == 1:
                    texture = self.wallTexture
                    self.BarrierList.append(texture)
                else:
                    texture = self.floorTexture
                qp.drawPixmap(i * 10, j * 10, texture)

    def moveRobot(self, Robo):
        # berechne neue Lenkrichtung
        if (Robo.v_alpha + Robo.a_alpha) < -v_alpha_Max:
            Robo.v_alpha = -v_alpha_Max
        elif (Robo.v_alpha + Robo.a_alpha) <= v_alpha_Max:
            Robo.v_alpha = (Robo.v_alpha + Robo.a_alpha)
        elif (Robo.v_alpha + Robo.a_alpha) >= v_alpha_Max:
            Robo.v_alpha = v_alpha_Max

        # Neue Richtung
        Robo.alpha = (Robo.alpha + Robo.v_alpha) % 360

        # berechne geschwindigkeit
        if (Robo.v + Robo.a) <= -vMax:
            Robo.v = -vMax
        elif (Robo.v + Robo.a) < vMax:
            Robo.v += Robo.a
        elif (Robo.v + Robo.a) >= vMax:
            Robo.v = vMax

        # X-Y Geschwindigkeit
        GesX = math.cos(math.radians(Robo.alpha)) * Robo.v
        GesY = - math.sin(math.radians(Robo.alpha)) * Robo.v

        # setze neue Geschwindigkeit
        Robo.v_vector = QVector2D(GesX, GesY)

        # berechne neue Position
        Robo.position.__iadd__(Robo.v_vector)

    def distanceTwoPoints(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    def distance(self, robo1, robo2):
        return self.distanceTwoPoints(int(round(robo1.position.x())) + robo1.radius,
                                      int(round(robo1.position.y())) + robo1.radius,
                                      int(round(robo2.position.x())) + robo2.radius,
                                      int(round(robo2.position.y())) + robo2.radius)

    def roboCollision(self, robo):
        for robot in self.robots:
            if robot != robo:
                distance = self.distance(robot, robo)

                if distance <= robot.radius + robo.radius:
                    dx = (robot.position - robo.position).x()
                    dy = (robot.position - robo.position).y()

                    tangent = math.atan2(dy, dx)

                    angle = 0.5 * math.pi + tangent

                    overlap = distance - (robot.radius - robo.radius)

                    roboX = math.sin(angle) * overlap
                    roboY = math.cos(angle) * overlap

                    newVel = QVector2D(roboX, roboY).normalized()

                    robo.position.__iadd__(newVel)

                    robot.position.__iadd__(newVel * (-1))

    def teleport(self, target, robot):

        MID = 500

        if robot != target:
            distance = self.distance(robot, target)

            if distance <= target.radius + robot.radius:

                if int(round(target.position.x())) > MID and int(round(target.position.y())) < MID:

                    robot.position = QVector2D(100, 850)

                elif int(round(target.position.x())) > MID and int(round(target.position.y())) > MID:
                    robot.position = QVector2D(100, 100)

                elif int(round(target.position.x())) < MID and int(round(target.position.y())) < MID:
                    robot.position = QVector2D(850, 850)


                elif int(round(target.position.x())) < MID and int(round(target.position.y())) > MID:
                    robot.position = QVector2D(850, 100)

    def barrierCollision(self, robo):
        # Collision with Obstacles
        PosX = int(round(robo.position.x() / 10))
        PosY = int(round(robo.position.y() / 10))
        Rad = int(round((robo.radius * 2) / 10))
        for i in range(0, Rad, 1):
            if 0 <= PosX + i < 100 and 0 <= PosX - i < 100 and 0 <= PosY + i < 100 and 0 <= PosY - i < 100:
                # oben
                if (SpielFeld.PlayFieldAR[PosX + i][PosY - 1] == 1) & (robo.v_vector.y() < 0):
                    robo.position.__isub__(robo.v_vector)
                    robo.v_vector = QVector2D(0, 0)
                    robo.a = 0
                # unten
                if (SpielFeld.PlayFieldAR[PosX + i][PosY + Rad] == 1) & (robo.v_vector.y() > 0):
                    robo.position.__isub__(robo.v_vector)
                    robo.v_vector = QVector2D(0, 0)
                    robo.a = 0
                # links
                if (SpielFeld.PlayFieldAR[PosX - 1][PosY + i] == 1) & (robo.v_vector.x() < 0):
                    robo.position.__isub__(robo.v_vector)
                    robo.v_vector = QVector2D(0, 0)
                    robo.a = 0
                # rechts
                if (SpielFeld.PlayFieldAR[PosX + Rad][PosY + i] == 1) & (robo.v_vector.x() > 0):
                    robo.position.__isub__(robo.v_vector)
                    robo.v_vector = QVector2D(0, 0)
                    robo.a = 0

    def BulletBarrierCollision(self, bullet):
        # Collision with Obstacles
        PosX = int(round(bullet.position.x() / 10))
        PosY = int(round(bullet.position.y() / 10))
        # oben
        if 0 <= PosX + 1 < 100 and 0 <= PosX - 1 < 100 and 0 <= PosY + 1 < 100 and 0 <= PosY - 1 < 100:
            if (SpielFeld.PlayFieldAR[PosX][PosY - 1] == 1):
                return True
            # unten
            if (SpielFeld.PlayFieldAR[PosX][PosY + 1] == 1):
                return True
            # links
            if (SpielFeld.PlayFieldAR[PosX - 1][PosY] == 1):
                return True
            # rechts
            if (SpielFeld.PlayFieldAR[PosX + 1][PosY] == 1):
                return True
        else:
            SpielFeld.Bullets.remove(bullet)
        return False


