"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath, QPolygonF, QMovie
from PyQt5.QtCore import Qt, QBasicTimer, QPoint, QEvent, QRectF


import sys
import math
import random
import threading
import time
import Robots
import Bullet
import Control
import Menu
# needs to be installed (https://www.pygame.org/docs/ref/mixer.html)
import pygame

pygame.mixer.init()

SCREENWIDTH = 1000
SCREENHEIGHT = 1000

FPS = 10
GameStep = (1/ FPS)
alpha_eps = 0.5
vMax = 3
v_alpha_Max = 2
count = 0
DEATH_TIME = 100
IMMUNE_TIME = 150
BOMB_SIZE = 32
BOMB_TIMER = 5000

# selected floor texture
ftexture = "White Stone"

# selected wall texture
wtexture = "Metall wall"

# selected Spellcard
spellcard = "Spellcard1"

# selected Collision
BulCollision = True

# wall libraries
floorTextures = {
    "Background Dirt": 'textures/Board/Background Dirt.png',
    "Background Pattern": 'textures/Board/Background Pattern.png',
    "Background Sakura": 'textures/Board/Background Sakura.png',
    "Background Water": 'textures/Board/Background Water.png',
    "Dirt": 'textures/Board/Dirt.png',
    "Brown Stone": 'textures/Board/Brown Stone.png',
    "White Stone": 'textures/Board/White Stone.png'
}
# wall libraries
wallTextures = {
    "Metall wall": 'textures/Board/wall00.png',
    "Metall Bar": 'textures/Board/wall01.png',
    "Mosaik wall": 'textures/Board/wall02.png',
    "Metall Fence": 'textures/Board/wall03.png',
    "Rusty Bar": 'textures/Board/wall04.png'

}

# color libraries
colors = {
    "pink":     QColor(255, 0, 250),
    "darkblue": QColor(0, 0, 250),
    "lightblue": QColor(0, 145, 250),
    "orange": QColor(245, 120, 0),
    "black": QColor(0,0,0),
    "yellow": QColor(255,255,0),
    "light cyan":  	QColor(224,255,255),
    "white smoke":  QColor(245,245,245)
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

       # change texture preferences
        self.wallTexture = self.changeWall(wtexture)
        #print(wtexture)
        self.floorTexture = self.changeFloor(ftexture)

        self.spellcard = self.changeSpellcard(spellcard)

        #print(ftexture)

        self.SoundBomb = pygame.mixer.Sound('sounds/getbomb.wav')
        self.SoundRedBomb = pygame.mixer.Sound('sounds/getredbomb.wav')
        self.DeathSound = pygame.mixer.Sound('sounds/death.wav')

        self.RoboTextures = {0: QPixmap('textures/Robots/Robot01.png'),  # MainRobot
                             1: QPixmap('textures/Robots/Robot_Dead.png'),  # Dead
                             2: QPixmap('textures/Robots/Robot_In.png'),  # Ivincible
                             3: QPixmap('textures/Robots/Robot02.png')  # EnemyRobot
                             }

        self.bombPosition = {0: [50,50],
                             1: [900,50],                            
                             2: [900,900],
                             3: [50,900],
                             }

        #randomize inital bomb-status  (50/50 Chance)
        number = random.randint(1, 2)
        if number == 1:
            self.bombStatus = 'green'
        elif number == 2:
            self.bombStatus = 'red' 

        self.bombTime = BOMB_TIMER
        self.currentBombPos = 0

        self.createBoard()

        self.RobotType = self

        # init Robots
        Robot1 = Robots.Robot(1, QVector2D(500, 500), 290, 2, 2, 15, 90, 0)
        Robot2 = Robots.Robot(2, QVector2D(100, 900), 90, 2, 2, 15, 90, 3)
        Robot3 = Robots.Robot(3, QVector2D(250, 650), 270, 2, 2, 15, 90, 3)
        Robot4 = Robots.Robot(4, QVector2D(950, 100), 180, 2, 2, 15, 90, 3)

        if self.spellcard == "Spellcard1":
            Robot1.setProgram(Control.PlayerRobot_Ability01(Robot1))
        elif self.spellcard == "Spellcard2":
            Robot1.setProgram(Control.PlayerRobot_Ability02(Robot1))
        elif self.spellcard == "Spellcard3":
            Robot1.setProgram(Control.PlayerRobot_Ability03(Robot1))
        elif self.spellcard == "Spellcard4":
            Robot1.setProgram(Control.PlayerRobot_Ability04(Robot1))
        elif self.spellcard == "Spellcard5":
            Robot1.setProgram(Control.PlayerRobot_Ability05(Robot1))
        elif self.spellcard == "Spellcard6":
            Robot1.setProgram(Control.PlayerRobot_Ability06(Robot1))
        elif self.spellcard == "Spellcard7":
            Robot1.setProgram(Control.PlayerRobot_Ability07(Robot1))
        elif self.spellcard == "AllSpellcards":
            Robot1.setProgram(Control.PlayerRobot_All_Abilities(Robot1))

        Robot2.setProgram(Control.TargetHunt(Robot2))
        Robot3.setProgram(Control.TargetHunt(Robot3))
        Robot4.setProgram(Control.TargetHunt(Robot4))

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

    def changeSpellcard(self, name):

        if name == "Spellcard1":
            Menu.CurSpell = "Spellcard1"
            return "Spellcard1"

        elif name == "Spellcard2":
            Menu.CurSpell = "Spellcard2"
            return "Spellcard2"

        elif name == "Spellcard3":
            Menu.CurSpell = "Spellcard3"
            return "Spellcard3"

        elif name == "Spellcard4":
            Menu.CurSpell = "Spellcard4"
            return "Spellcard4"

        elif name == "Spellcard5":
            Menu.CurSpell = "Spellcard5"
            return "Spellcard5"

        elif name == "Spellcard6":
            Menu.CurSpell = "Spellcard6"
            return "Spellcard6"

        elif name == "Spellcard7":
            Menu.CurSpell = "Spellcard7"
            return "Spellcard7"

        elif name == "AllSpellcards":
            Menu.CurSpell = "AllSpellcards"
            return "AllSpellcards"

        else:
            pass

    def changeWall(self, name):

        if name == "Metall wall":
            Menu.CurWall = "Metall wall"
            return QPixmap(wallTextures["Metall wall"])

        elif name == "Metall Bar":
            Menu.CurWall = "Metall Bar"
            return QPixmap(wallTextures["Metall Bar"])

        elif name == "Mosaik wall":
            Menu.CurWall = "Mosaik wall"
            return QPixmap(wallTextures["Mosaik wall"])
        
        elif name == "Metall Fence":
            Menu.CurWall = "Metall Fence"
            return QPixmap(wallTextures["Metall Fence"])
        
        elif name == "Rusty Bar":
            Menu.CurWall = "Rusty Bar"
            return QPixmap(wallTextures["Rusty Bar"])
        else:
            pass

    def changeFloor(self, name):

        if name == "Background Dirt":
            Menu.CurFloor = "Background Dirt"
            return QPixmap(floorTextures["Background Dirt"])

        elif name == "Background Pattern":
            Menu.CurFloor = "Background Pattern"
            return QPixmap(floorTextures["Background Pattern"])

        elif name == "Background Sakura":
            Menu.CurFloor = "Background Sakura"
            return QPixmap(floorTextures["Background Sakura"])

        elif name == "Background Water":
            Menu.CurFloor = "Background Water"
            return QPixmap(floorTextures["Background Water"])

        elif name == "Dirt":
            Menu.CurFloor = "Dirt"
            return QPixmap(floorTextures["Dirt"])

        elif name == "Brown Stone":
            Menu.CurFloor = "Brown Stone"
            return QPixmap(floorTextures["Brown Stone"])

        elif name == "White Stone":
            Menu.CurFloor = "White Stone"
            return QPixmap(floorTextures["White Stone"])

        else:
            pass

    def start(self):

        if self.isPaused:
            return

        self.isStarted = True

        self.timer.start(FPS, self)

    def createBoard(self):

        # set Walls, set array value to 1 to place Wall
        # set Wall around the edges

        # SpielFeld.PlayFieldAR[90][90] = 1
        # SpielFeld.PlayFieldAR[10][10] = 1

        for x in range(0, 100, 1):
            SpielFeld.PlayFieldAR[x][0] = 1
            SpielFeld.PlayFieldAR[x][99] = 1
        for y in range(1, 99, 1):
            SpielFeld.PlayFieldAR[0][y] = 1
            SpielFeld.PlayFieldAR[99][y] = 1

        # set some Obstacle
        for i in range(0, 25, 1):
            SpielFeld.PlayFieldAR[70][i + 45] = 1
            SpielFeld.PlayFieldAR[71][i + 45] = 1

        for i in range(0, 40, 1):
            SpielFeld.PlayFieldAR[i + 10][40] = 1
            SpielFeld.PlayFieldAR[i + 10][41] = 1
        for i in range(0, 50, 1):
            SpielFeld.PlayFieldAR[i + 30][70] = 1
            SpielFeld.PlayFieldAR[i + 30][71] = 1

        for i in range(0, 30, 1):
            SpielFeld.PlayFieldAR[i + 25][20] = 1
            SpielFeld.PlayFieldAR[i + 25][21] = 1

        for i in range(0, 10, 1):
            SpielFeld.PlayFieldAR[10][i + 50] = 1
            SpielFeld.PlayFieldAR[11][i + 50] = 1

    def randomizeBombStatus(self):
        number = random.randint(1, 2)
        if number == 1:
            self.bombStatus = 'green'
        elif number == 2:
            self.bombStatus = 'red' 

    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():

            # Count
            self.tickCount += 1

            # update RobotLists of each Robot
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
                self.roboCollision(robot, self.robots[0])
                self.SightingData(robot)
                self.reduceDelay(robot)
                self.reduceDeathTime(robot)
                self.reduceImmuneTime(robot)
                self.reduceBombTime()
                #print(self.currentBombPos)


            # Green-Bomb : Grants immunity to the robot
                if self.bomb_hit(robot) and self.bombStatus == 'green':
                        self.randomizeBombStatus()
                        
                        #Hier: Hit-Effekte
                        self.setNextBombPos()
                        
                        # Immunity
                        robot.immuneTime = 500
                        robot.texture = 2
                                                        
                                
                        pygame.mixer.Sound.play(self.SoundBomb)
            # Red-Bomb : Eliminates all other robots
                if self.bomb_hit(robot) and self.bombStatus == 'red' and robot.robotid == 1:
                    self.setNextBombPos()

                    self.randomizeBombStatus()                                      

                    for robot in self.robots:
                        if robot.robotid != 1:
                            robot.deathTime = 150
                            robot.texture = 1
                    

                    pygame.mixer.Sound.play(self.SoundRedBomb)
                        
            for bul in SpielFeld.Bullets:
                if bul.delay == 0:
                    bul.moveBullet()
                    bul.time -= 1
                    if bul.time == 0:
                        SpielFeld.Bullets.remove(bul)
                    if BulCollision:
                        if self.BulletBarrierCollision(bul) and bul in SpielFeld.Bullets:
                            SpielFeld.Bullets.remove(bul)
                            Menu.CurCol = "Wall Collision   On"
                    else:
                        Menu.CurCol = "Wall Collision   Off"
                    for robot in self.robots:
                        if bul.one_hit(robot):
                            if robot.robotid == 1 and robot.immuneTime == 0 and robot.deathTime == 0:
                                robot.deathTime = DEATH_TIME
                                robot.texture = 1
                                pygame.mixer.Sound.play(self.DeathSound)
                            elif robot.robotid != 1 and robot.immuneTime == 0:
                                self.teleport_bullet(robot)
                                robot.immuneTime = IMMUNE_TIME
                                robot.texture = 2
                            if bul in SpielFeld.Bullets:
                                SpielFeld.Bullets.remove(bul)

                            
                    
                            

                            
                            ###
                else:
                    bul.delay -= 1

            self.update()

        else:
            super(SpielFeld, self).timerEvent(event)

    def fetchBullets(self, Robot):
        SpielFeld.Bullets.extend(Robot.BulList)
        # print(SpielFeld.Bullets)
        Robot.BulList.clear()

    def reduceDelay(self, Robot):
        if Robot.reload != 0:
            Robot.reload -= 1
        if Robot.coolDown != 0:
            Robot.coolDown -= 1

        # Death Counter (Down) {see Constants}

    def reduceDeathTime(self, Robot):
        if Robot.deathTime != 0:
            Robot.deathTime -= 1
            if Robot.deathTime == 0:
                Robot.immuneTime = IMMUNE_TIME
                Robot.texture = 2

    def teleport_bullet(self, robo):
        spot = random.randint(1, 5)
        if spot == 1:
            robo.position = QVector2D(100, 100)
        elif spot == 2:
            robo.position = QVector2D(100, 850)
        elif spot == 3:
            robo.position = QVector2D(850, 100)
        elif spot == 4:
            robo.position = QVector2D(850, 850)
        elif spot == 5:
            robo.position = QVector2D(500, 500)

    def reduceImmuneTime(self, Robot):
        if Robot.immuneTime != 0:
            Robot.immuneTime -= 1
            if Robot.immuneTime == 0:
                if Robot.robotid == 1:
                    Robot.texture = 0
                else:
                    Robot.texture = 3

    def paintEvent(self, qp):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        # draw Robots on the game field
        for robot in self.robots:
            self.drawRobo(robot, qp)
            # qp.drawPath(self.FOV(robot))
        for bul in SpielFeld.Bullets:
            if bul.delay == 0:
                bul.drawBullet(qp)

        if self.bombStatus == 'green':
            self.drawBomb(qp)
        if self.bombStatus == 'red':
            self.drawRedBomb(qp)

    def drawRobo(self, Robo, br):

        # Set Rotation, place etc
        texture = self.RoboTextures[Robo.texture]
        br.save()
        br.translate(Robo.position.x() + Robo.radius, Robo.position.y() + Robo.radius)
        br.rotate(-Robo.alpha)
        source = QRectF(0, 0, 2 * Robo.radius, 2 * Robo.radius)
        target = QRectF(-Robo.radius, -Robo.radius,
                        2 * Robo.radius, 2 * Robo.radius)
        # Draw
        br.drawPixmap(target, texture, source)
        br.restore()

    def FOV(self, Robo):
        view = QPainterPath()

        xPos = math.cos(math.radians(Robo.alpha + (Robo.FOV / 2))) * Robo.radius
        yPos = math.sin(math.radians(Robo.alpha + (Robo.FOV / 2))) * Robo.radius

        xPos2 = math.cos(math.radians(Robo.alpha - (Robo.FOV / 2))) * Robo.radius
        yPos2 = math.sin(math.radians(Robo.alpha - (Robo.FOV / 2))) * Robo.radius

        x1 = QPoint(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius)
        x2 = x1 + QPoint((int(round(Robo.position.x())) + Robo.radius) + 1000 * xPos,
                         (int(round(Robo.position.y())) + Robo.radius) - 1000 * yPos)
        x3 = x1 + QPoint((int(round(Robo.position.x())) + Robo.radius) + 1000 * xPos2,
                         (int(round(Robo.position.y())) + Robo.radius) - 1000 * yPos2)

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
                    # print(robo.robotid, ids)
                else:
                    robo.ViewList[x.robotid][3] = False

        # update ViewList
        for id in ids:
            for robot in self.robots:

                if robot.robotid == id and (robo.position - robot.position).length() < 300:
                    viewedRobo = robot.robotid
                    distance = (robo.position - robot.position).length()
                    viewedDirection = robot.alpha
                    seen = True

                    toUpDate = {viewedRobo: [robot.position, distance, viewedDirection, seen]}

                    robo.ViewList.update(toUpDate)
                    # print(robo.robotid, robo.ViewList)

    def drawField(self, qp):
        qp.setPen(Qt.NoPen)
        texture = self.floorTexture
        if ftexture == "Background Dirt" or  ftexture == "Background Pattern" or ftexture == "Background Sakura" or  ftexture == "Background Water":
            qp.drawPixmap(- ((self.tickCount/2) % 1000), - ((self.tickCount/2) % 1000), texture)
        else:
            qp.drawPixmap(0,0, texture)
        #Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if SpielFeld.PlayFieldAR[i][j]==1:
                        texture = self.wallTexture
                        self.BarrierList.append(texture)
                        qp.drawPixmap(i*10, j*10, texture)
## BOMB ##           

    def bombShape(self, bombPos):
        shape = QPainterPath()
        shape.addRect(bombPos[0], bombPos[1], BOMB_SIZE, BOMB_SIZE)
        return shape

    def bomb_hit(self, robo):
        if self.bombShape(self.bombPosition[self.currentBombPos]).intersects(robo.roboShape()):
            return True
        else: pass

    def randomizeBombIcon(self):
        number = random.randint(1, 2)

        if number == 1:
            self.bombStatus = 'green' 
        elif number == 2:
            self.bombStatus = 'red'

    def drawBomb(self, qp):        
        texture = QPixmap('textures/bomb.jpg')

        qp.drawPixmap(self.bombPosition[self.currentBombPos][0], self.bombPosition[self.currentBombPos][1], texture)

    def drawRedBomb(self,qp):
        texture = QPixmap('textures/redbomb.jpg')

        qp.drawPixmap(self.bombPosition[self.currentBombPos][0], self.bombPosition[self.currentBombPos][1], texture)
  

    def reduceBombTime(self):
        if self.bombTime != 0:
            self.bombTime -= 1
            if self.bombTime == 0:
                self.bombTime = BOMB_TIMER
                self.randomizeBombIcon()
                self.setNextBombPos()
                #self.setCurrBombPos()

    def setCurrBombPos(self, bombPos ):
        if bombPos >= 0 and bombPos < 3:
            bombPos += 1
        else:
            bombPos = 0

        return bombPos

    def setNextBombPos(self):
        self.currentBombPos = self.setCurrBombPos(self.currentBombPos)
        
        

##

    def keyPressEvent(self, event):
        if not self.isStarted:
            super(SpielFeld, self).keyPressEvent(event)
            return

        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_P:
                self.pause()
                return

        else:
            super(SpielFeld, self).keyPressEvent(event)

    def Message(self):
        msgBox = QMessageBox()

        msgBox.setWindowTitle("Pause Screen")
        msgBox.setIconPixmap(QPixmap('textures/Board/pauseEmoji.png'))
        msgBox.setText("Your in the pause screen. \n Do you want to continue? \n")

        # set Buttons
        msgBox.addButton(QMessageBox.Yes)
        msgBox.addButton(QMessageBox.No)

        # change backgroundstyle
        p = self.palette()
        p.setColor(self.backgroundRole(), colors["white smoke"])
        msgBox.setPalette(p)
        msgBox.exec_()

        return msgBox

    def pause(self):

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        print(self.isPaused)

        if self.isPaused:
            self.timer.stop()

            # switch to pause screen
            self.msgBox = self.Message().result()
            if self.msgBox == QMessageBox.No:
                self.startMenu = Menu.start_Menu()
                self.close()
            else:
                self.isPaused = False
                self.timer.start(FPS, self)
        else:
            self.timer.start(FPS, self)

        self.update()

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

    def roboCollision(self, robo, target):
        for robot in self.robots:
            if robot != robo:
                distance = self.distance(robot, robo)

                if distance <= robot.radius + robo.radius:
                    dx = (robot.position - robo.position).x()
                    dy = (robot.position - robo.position).y()

                    tangent = math.atan2(dy, dx)

                    robo.alpha = 2 * tangent - robo.alpha

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
