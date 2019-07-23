"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QBasicTimer, QThread
from playsound import playsound
import keyboard
import sys
import math
import threading
import time
import random
import Server
import Bullet
import Control
import pygame

pygame.mixer.init()

#Constants
alpha_eps = 0.5 #velocity-stop breakpoint
vMax = 5 #max velocity
v_alpha_Max = 10 #max alpha velocity
RELOAD_TIME = 50


class Robot(object):
    def __init__(self, robotid, position, alpha, a_max, a_alpha_max, radius, FOV, texture):

        self.robotid = robotid
        self.position = position
        self.alpha = alpha % 360
        self.radius = radius
        self.texture = texture
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
        self.coolDown = 0
        self.deathTime = 0
        self.immuneTime = 0
        
        self.a = 0
        self.a_max = a_max
        self.a_alpha= 0
        self.a_alpha_max = a_alpha_max

        self.v_vector = QVector2D(0,0)
        self.v_alpha = 0
        self.v = 0

        self.SoundSpecial1 = pygame.mixer.Sound('sounds/special1.wav')
        self.SoundSpecial2 = pygame.mixer.Sound('sounds/special2.wav')
        self.SoundSpecial3 = pygame.mixer.Sound('sounds/special3.wav')
        self.SoundSpecial4 = pygame.mixer.Sound('sounds/special4.wav')
        self.SoundSpecial5 = pygame.mixer.Sound('sounds/special5.wav')                    
        self.SoundSpecial6 = pygame.mixer.Sound('sounds/special6.wav')
        self.SoundSpecial7 = pygame.mixer.Sound('sounds/special7.wav')

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
        #Values
        LifeTime = 100
        
        if self.reload == 0 and self.deathTime == 0:
            Bullet1 = self.createBullet(0,LifeTime, 0, self.alpha, self.v,0,0)

            self.BulList.append(Bullet1)
            self.reload = RELOAD_TIME

    def spellcard1(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            Repetitions = 10
            LifeTime = 90
            alpha1 = self.alpha
            alphaStep = 45
                  
            #Create Bullets
            for delay in range(0, Repetitions, 1):
                for n in range(0, 8, 1):
                    self.BulList.append(self.createBullet(1,LifeTime, delay*4, (alpha1 + n*alphaStep),0,6,0))
                    self.BulList.append(self.createBullet(4,LifeTime, delay*4, (alpha1 + n*alphaStep),0,6,0))

            
            pygame.mixer.Sound.play(self.SoundSpecial1)

            self.coolDown = 150

    def spellcard2(self):
        if self.coolDown == 0 and self.deathTime == 0:  
            #Values
            Repetitions = 10
            LifeTime = 450
            alpha1 = self.alpha
            alphaStep = 45

            #Create Bullets
            for delay in range(0, Repetitions, 1):
                for i in range(0, 8, 1):
                    self.BulList.append(self.createBullet(6,LifeTime, delay*4,(alpha1 + i*alphaStep) % 360,0,6,0))
            
            pygame.mixer.Sound.play(self.SoundSpecial2)
           

            self.coolDown = 550


    def spellcard3(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            BulletAmmount = 30
            Repetitions = int(round(BulletAmmount/2))
            LifeTime = 400 + 4*Repetitions
            
            #Calculate Angles
            alpha1 = self.alpha
            alphaStep = 360 / BulletAmmount
            
            #Calculate Target
            DistTo2 = QVector2D(self.position.x() - self.RobotList[2].x(), self.position.y() - self.RobotList[2].y())
            DistTo3 = QVector2D(self.position.x() - self.RobotList[3].x(), self.position.y() - self.RobotList[3].y())
            DistTo4 = QVector2D(self.position.x() - self.RobotList[4].x(), self.position.y() - self.RobotList[4].y())
            Distance2 = DistTo2.x()*DistTo2.x() + DistTo2.y() * DistTo2.y()
            Distance3 = DistTo3.x()*DistTo3.x() + DistTo3.y() * DistTo3.y()
            Distance4 = DistTo4.x()*DistTo4.x() + DistTo4.y() * DistTo4.y()
            
            closest = min(Distance2, Distance3, Distance4)

            if closest == Distance2:
                #print("darkBlue")
                target = 2
            elif closest == Distance3:
                #print("lightBlue")
                target = 3
            elif closest == Distance4:
                #print("orange")
                target = 4
                
            #Create Bullets
            for i in range(0,Repetitions,1):
                self.BulList.append(self.createBullet(14,LifeTime - 4*i, 4*i, (alpha1 + i*alphaStep) % 360 ,0 ,50,self.RobotList[target]))
                self.BulList.append(self.createBullet(14,LifeTime - 4*i, 4*i, (alpha1 + 180 + i*alphaStep) % 360 ,0 ,50,self.RobotList[target]))

            pygame.mixer.Sound.play(self.SoundSpecial3)
            
            self.coolDown = 250

    def spellcard4(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            BulletAmmount = 5
            Repetitions = 15

            #Calculate Angles
            alpha1 = self.alpha
            alphaStep = 360 / BulletAmmount

            for i in range(0,Repetitions,1):
                LifeTime = random.randint(250,350)
                for step in range(0,BulletAmmount,1):
                    self.BulList.append(self.createBullet(15,LifeTime, 0,(alpha1 + step*alphaStep) % 360,0,6,0))
            

            pygame.mixer.Sound.play(self.SoundSpecial4)
            
            self.coolDown = 400


    def spellcard5(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            BulletAmmount = 5
            Repetitions = 20
            LifeTime = 350

            #Calculate Angles
            alpha1 = self.alpha
            alphaStep = 360 / BulletAmmount

            #Create Bullets
            for delay in range(0, Repetitions, 1):
                for i in range(0, BulletAmmount, 1):
                    self.BulList.append(self.createBullet(17,LifeTime, delay*4,(alpha1 + i*alphaStep) % 360,0,6,0))

            pygame.mixer.Sound.play(self.SoundSpecial5)

            self.coolDown = 450

    def spellcard6(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            BulletAmmount = 4
            Repetitions = 25
            LifeTime = 600

            #Calculate Angles
            alpha1 = self.alpha
            alphaStep = 360 / BulletAmmount
            alphaWindow = ((360 / BulletAmmount)/ 5) * 1.5
            

            #Create Bullets
            for delay in range(0, Repetitions, 1):
                for i in range(0, BulletAmmount, 1):
                    self.BulList.append(self.createBullet(22,LifeTime, delay*4,((alpha1 + i*alphaStep) + alphaWindow * delay) % 360,0,6,0))

            pygame.mixer.Sound.play(self.SoundSpecial6)
            
            self.coolDown = 900

    def spellcard7(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            BulletAmmount = 5
            Repetitions = 20
            LifeTime = 350

            #Calculate Angles
            alpha1 = self.alpha
            alphaStep = 360 / BulletAmmount

            #Create Bullets
            for delay in range(0, Repetitions, 1):
                for i in range(0, BulletAmmount, 1):
                    self.BulList.append(self.createBullet(27,LifeTime-delay*4, delay*4,(alpha1 + i*alphaStep) % 360,0,6,0))

            pygame.mixer.Sound.play(self.SoundSpecial7)
            
            self.coolDown = 700
        

    def createBullet(self, bulletType, life, delayT, alpha, addSpeed, offset, target):
        
        #Position
        bulletpos = QVector2D(self.position.x(),self.position.y())
        #velocity
        speed = Bullet.Bullet_Speed + addSpeed
        #velocity based on angle
        GesX = math.cos(math.radians(alpha)) * speed
        GesY = - math.sin(math.radians(alpha)) * speed
        #set Bullet to middle of Robot
        OffsetVector = QVector2D((self.radius-2)/2,(self.radius-2)/2)
        bulletpos.__iadd__(OffsetVector)
        #set bullet to edge in firing direction
        OffsetX = math.cos(math.radians(alpha)) * (self.radius + offset)
        OffsetY = - math.sin(math.radians(alpha)) * (self.radius + offset)
        OffsetVector = QVector2D(OffsetX,OffsetY)
        bulletpos.__iadd__(OffsetVector)

        if target != 0:
            #Calculate Target Alpha
            target_x = target.x()
            target_y = target.y()

            pos_x = bulletpos.x()
            pos_y = bulletpos.y()


            #Berechnung Blickrichtung
            delta_x = target_x - pos_x
            delta_y = target_y - pos_y
            target_alpha = -math.degrees(math.atan2(delta_y, delta_x)) % 360

        else:
            target_alpha = alpha

        #create Bullet
        Bullet1 = Bullet.Bullet(bulletpos, speed, target_alpha, life, delayT, bulletType, self.robotid)
        return Bullet1

class RobotControl(QThread):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        threading.Thread.__init__(self)


#Roboter Steuerung
# Is in another file
class RunAwayKeyBoard(RobotControl):
    def run(self):
        while True:
            self.msleep(100)
            
            if keyboard.is_pressed('w'):
                self.robot.a = 0.1

            if keyboard.is_pressed('s'):
                self.robot.a = -0.1

            if keyboard.is_pressed('a'):
                self.robot.a_alpha = 0.5

            if keyboard.is_pressed('d'):
                self.robot.a_alpha = -0.5
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack1
            if keyboard.is_pressed('1'):
                self.robot.spellcard1()

            #Special Attack2
            if keyboard.is_pressed('2'):
                self.robot.spellcard2()

            #Special Attack3
            if keyboard.is_pressed('3'):
                self.robot.spellcard3()

            #Special Attack4
            if keyboard.is_pressed('4'):
                self.robot.spellcard4()

            #Special Attack5
            if keyboard.is_pressed('5'):
                self.robot.spellcard5()

            #Special Attack6
            if keyboard.is_pressed('6'):
                self.robot.spellcard6()

            #Special Attack6
            if keyboard.is_pressed('7'):
                print('hi')
                self.robot.spellcard7()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0

