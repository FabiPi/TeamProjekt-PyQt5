"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QBasicTimer, QThread
import sys
import math
import threading
import time
import Server
import random
import Bullet
import keyboard

#Constants
alpha_eps = 0.5 #velocity-stop breakpoint
vMax = 5 #max velocity
v_alpha_Max = 10 #max alpha velocity
RELOAD_TIME = 100

class Robot(object):
    def __init__(self, robotid, position, alpha, a_max, a_alpha_max, radius, FOV, color):

        self.robotid = robotid
        self.position = position
        self.alpha = alpha % 360
        self.radius = radius
        
        self.color = color
        self.RobotList = {1 : QVector2D(0,0),
                          2 : QVector2D(0,0),
                          3 : QVector2D(0,0),
                          4 : QVector2D(0,0)}
        self.BulList= []

        # for FOV
                            # Position, Distanz zueinander, Blickwinkel, seen
        self.ViewList = {1 : [ QVector2D(0,0), 0, 0, False],
                         2 : [ QVector2D(0,0), 0, 0, False],
                         3 : [ QVector2D(0,0), 0, 0, False],
                         4 : [ QVector2D(0,0), 0, 0, False]}
        self.FOV = FOV

        self.reload = 0
        self.deathTime = 0
        self.immuneTime = 0
        
        self.a = 0
        self.a_max = a_max
        self.a_alpha= 0
        self.a_alpha_max = a_alpha_max

        self.v_vector = QVector2D(0,0)
        self.v_alpha = 0
        self.v = 0

    #Methods for Robot Controll
    def setProgram(self, program):
        self.program = program

    def executeProgram(self):
        self.program.start()
        return self.a_alpha_max

    # for the FOV
    def roundshape(self, position, r ):
        shape = QPainterPath()
        shape.addEllipse(int(round(position.x())), int(round(position.y())), r, r)
        return shape

    def roboShape(self):
        return self.roundshape(self.position, self.radius)


    def moveChase(self, tarAlpha):
        target_alpha = tarAlpha

        if target_alpha < 180:
            if  target_alpha+180 < self.alpha or target_alpha > self.alpha:
                # turn left
                self.a_alpha = 0.5

            else:
                # turn right
                self.a_alpha = -0.5
        else:
            if  target_alpha > self.alpha >= ((target_alpha+180)% 360):
                # turn left
                self.a_alpha = 0.5

            else:
                # turn right
                self.a_alpha = -0.5
        

    def aimTarget(self, target):
        target_x = target.x()
        target_y = target.y()

        pos_x = self.position.x()
        pos_y = self.position.y()


        #Berechnung Blickrichtung
        delta_x = target_x - pos_x
        delta_y = target_y - pos_y
        target_alpha = -math.degrees(math.atan2(delta_y, delta_x)) % 360

        self.moveChase(target_alpha)

        #self.alpha = target_alpha

        #print(target_alpha)

    def inVicinity(self, target):
        eps = 20
        #print(self.position)
        if (self.position.x()- eps <= target.x() <= self.position.x()+ eps) and(self.position.y()- eps <= target.y() <= self.position.y()+ eps):
            return True
        else:
            return False


    def aimTargetView(self, target):
        # who is my target
        target_id = target

        # is my target in my FOV?
        if self.ViewList[target_id][3]:

            # Yes, chase him
            target_alpha = self.ViewList[target_id][2]

            self.moveChase(target_alpha)

        # no, turn around and wait
        else:
            self.v = 0
            self.a_alpha = 2

    def aimTargetIntelligent(self, target, chaserFriend):

        # who is my target
        target_id = target
        chaser_id = chaserFriend

        # is my target in my FOV?
        if self.ViewList[target_id][3]:
            # yes, chase him
            target_alpha = self.ViewList[target_id][2]
            self.moveChase(target_alpha)

        # no, follow different chaser, maybe they saw him
        elif self.ViewList[chaser_id][3]:
            chaser_alpha = self.ViewList[chaser_id][2]
            self.moveChase(chaser_alpha)

        # no, look around
        else:
            self.v = 0
            self.a_alpha = 2

            # or walk around
            # self.aimTarget(self.findTarget_pos())
       
    def shoot(self):
        if self.reload == 0 and self.deathTime == 0:
            #StartPosition sollte um ein Offset in Blickrichtung verschoben werden
            bulletpos = QVector2D(self.position.x(),self.position.y())
            #velocity based on angle
            GesX = math.cos(math.radians(self.alpha)) * Bullet.Bullet_Speed
            GesY = - math.sin(math.radians(self.alpha)) * Bullet.Bullet_Speed
            #set Bullet to middle of Robot
            OffsetVector = QVector2D((self.radius + Bullet.Bullet_Size)/2,(self.radius + Bullet.Bullet_Size)/2)
            bulletpos.__iadd__(OffsetVector)
            #set bullet to edge in firing direction
            OffsetX = math.cos(math.radians(self.alpha)) * (self.radius + 6)
            OffsetY = - math.sin(math.radians(self.alpha)) * (self.radius + 6)
            OffsetVector = QVector2D(OffsetX,OffsetY)
            bulletpos.__iadd__(OffsetVector)
            Vel = QVector2D(GesX,GesY)
            Vel.__iadd__(self.v_vector)
            Bullet1 = Bullet.Bullet(bulletpos, Vel)
            self.BulList.append(Bullet1)
            self.reload = RELOAD_TIME
            #print(self.BulList)

        


class RobotControl(QThread):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        threading.Thread.__init__(self)


#Roboter Steuerung

class RunAwayKeyBoard(RobotControl):
    def run(self):
        while True:
            self.msleep(100)
            
            if keyboard.is_pressed('w'):
                #print('W-Key')
                self.robot.a = 0.1

            if keyboard.is_pressed('s'):
                #print('S-Key')
                self.robot.a = -0.1

            if keyboard.is_pressed('a'):
                #print('A-Key')
                self.robot.a_alpha = 0.5

            if keyboard.is_pressed('d'):
                #print('D-Key')
                self.robot.a_alpha = -0.5
                
            if keyboard.is_pressed('j'):
                #print('J-Key')
                self.robot.shoot()

class TargetHunt(RobotControl):
    def run(self):
        while True:
            self.robot.a = 1
            target = 1
            self.robot.aimTargetView(target)
            self.msleep(100)
            if self.robot.ViewList[target][3]:
                self.robot.shoot()

class CircleMap1(RobotControl):
    def run(self):
        self.robot.a = 1
        targetnum = 0
        while True:
            if targetnum == 0:
                target= QVector2D(950,950)
            elif targetnum == 1:
                target= QVector2D(950,50)
            elif targetnum == 2:
                target= QVector2D(50,50)
            elif targetnum == 3:
                target= QVector2D(50,950)
                
            if self.robot.inVicinity(target):
                targetnum = (targetnum +1) % 4
            self.robot.aimTarget(target)
            self.msleep(100)
            self.robot.shoot()

class CircleMap2(RobotControl):
    def run(self):
        self.robot.a = 1
        targetnum = 3
        while True:
            if targetnum == 0:
                target= QVector2D(900,900)
            elif targetnum == 1:
                target= QVector2D(900,100)
            elif targetnum == 2:
                target= QVector2D(100,100)
            elif targetnum == 3:
                target= QVector2D(100,900)
                
            if self.robot.inVicinity(target):
                targetnum = (targetnum +1) % 4
            self.robot.aimTarget(target)
            self.msleep(100)
            self.robot.shoot()

class CircleMap3(RobotControl):
    def run(self):
        self.robot.a = 1
        targetnum = 2
        while True:
            if targetnum == 0:
                target= QVector2D(900,900)
            elif targetnum == 1:
                target= QVector2D(900,100)
            elif targetnum == 2:
                target= QVector2D(100,100)
            elif targetnum == 3:
                target= QVector2D(100,900)
                
            if self.robot.inVicinity(target):
                targetnum = (targetnum +1) % 4
            self.robot.aimTarget(target)
            self.msleep(100)
            self.robot.shoot()

class TargetChase(RobotControl):

    def run(self):
        self.robot.a = 1
        target = QVector2D(900,900)
        while True:
            if self.robot.inVicinity(QVector2D(900,900)):
                target = QVector2D(100,100)
            if self.robot.inVicinity(QVector2D(100,100)):
                target = QVector2D(900,900)
            self.robot.inVicinity(target)
            self.robot.aimTarget(target)
            self.robot.aimTarget(target)
            self.msleep(100)


class Stationary(RobotControl):
    def run(self):
        while True:
            self.robot.shoot()
            self.msleep(100)

            
class TargetChase2(RobotControl):

    def run(self):
        self.robot.a = 1
        while True:
            target = self.robot.RobotList[1]
            self.robot.inVicinity(target)
            self.robot.aimTarget(target)
            self.msleep(100)


class TargetChase3(RobotControl):

    def run(self):
        self.robot.a = 1

        while True:
            target = 1
            self.robot.aimTargetView(target)
            self.msleep(100)



class TargetChase4(RobotControl):
    def run(self):
        self.robot.a = 1

        while True:
            target = 3
            chaserFriend = 2
            self.robot.aimTargetIntelligent(target, chaserFriend)
            self.msleep(100)
