"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
from PyQt5.QtCore import QRectF
import random
import math
import Server
import Robots

#####  BULLET   ######

Bullet_Size = 18
Bullet_Speed =5

                  
class Bullet(object):
    def __init__(self, position, speed, alpha, time, delay, bulType, owner):
        self.position = position
        self.speed = speed
        self.alpha = alpha
        self.bulType = bulType
        self.time = time
        self.delay = delay
        self.owner = owner
        self.BulletTextures = {0:QPixmap('textures/Bullets/Standart.png'), #Standart
                               #Spellcard1
                               1:QPixmap('textures/Bullets/GreenOrb.png'), #Green 1
                               2:QPixmap('textures/Bullets/BlueOrb.png'), #Blue 1
                               3:QPixmap('textures/Bullets/RedOrb.png'), #Red
                               4:QPixmap('textures/Bullets/GreenOrb.png'), #Green 2
                               5:QPixmap('textures/Bullets/BlueOrb.png'), #Blue 2
                               #Spellcard2
                               6:QPixmap('textures/Bullets/GreenOrb.png'), #GreenOrb
                               7:QPixmap('textures/Bullets/BlueOrb.png'), #BlueOrb
                               8:QPixmap('textures/Bullets/Star01.png'), #Star1
                               9:QPixmap('textures/Bullets/Star02.png'), #Star2
                               10:QPixmap('textures/Bullets/Star03.png'), #Star3
                               11:QPixmap('textures/Bullets/Star04.png'), #Star4
                               12:QPixmap('textures/Bullets/Star05.png'), #Star5
                               13:QPixmap('textures/Bullets/Star06.png'), #Star6                               
                               #Spellcard3
                               14:QPixmap('textures/Bullets/Kunai.png'), #Kunai
                               #Spellcard4
                               15:QPixmap('textures/Bullets/BlackCircle.png'), #BlackMain
                               16:QPixmap('textures/Bullets/PurpleBullet.png'), #Purple Splits
                               #Spellcard5
                               17:QPixmap('textures/Bullets/RedSeal.png'), #RedSeal
                               18:QPixmap('textures/Bullets/RedSeal.png'), #RedSeal
                               19:QPixmap('textures/Bullets/RedSeal.png'), #RedSeal
                               20:QPixmap('textures/Bullets/BlueSeal.png'), #BlueSeal
                               21:QPixmap('textures/Bullets/GreenSeal.png'), #GreenSeal
                               #Spellcard6
                               22:QPixmap('textures/Bullets/Butterfly.png'), #Butterfly
                               23:QPixmap('textures/Bullets/Butterfly.png'), #Butterfly
                               24:QPixmap('textures/Bullets/Butterfly.png'), #Butterfly
                               25:QPixmap('textures/Bullets/BlueOrb.png'), #BlueOrb
                               26:QPixmap('textures/Bullets/RedOrb.png'), #RedOrb
                               #Spellcard7
                               27:QPixmap('textures/Bullets/Kunai.png'), #Kunai
                               28:QPixmap('textures/Bullets/Kunai.png'), #Kunai
                               29:QPixmap('textures/Bullets/Star05.png'), #purpleStar
                               }


    def drawBullet(self, br):

        #Set Rotation, place etc
        texture = self.BulletTextures[self.bulType]
        br.save()
        br.translate(self.position.x() + 0.5 * Bullet_Size, self.position.y() + 0.5 * Bullet_Size)
        br.rotate(-self.alpha)
        source = QRectF(0, 0, Bullet_Size, Bullet_Size)
        target = QRectF(-Bullet_Size/2, -Bullet_Size/2,
                Bullet_Size, Bullet_Size)
        #Draw
        br.drawPixmap(target, texture, source)
        br.restore()

    def moveBullet(self):
        
        #Spellcard 1    (Star Pattern)
        if  1<= self.bulType <= 5:
            self.Spellcard01()

            
        #Spellcard 2    (Circles into Random stars)
        elif  6<= self.bulType <= 7: #8 to 13 have standart movement
            self.Spellcard02()

        #Spellcard 3    (Circle into Target Aim)
        elif self.bulType == 14:
            self.Spellcard03()


        #Spellcard 4    (Random Delay Split)
        elif 15 <= self.bulType <= 16:
            self.Spellcard04()

        #Spellcard 5    (Circle Star)
        elif 17 <= self.bulType <= 19: # 20,21 have standart movement
            self.Spellcard05()

        #Spellcard 6    (Spiral)
        elif 22 <= self.bulType <= 26:
            self.Spellcard06()

        #Spellcard 7    (Star - sweep - Star)
        elif 27 <= self.bulType <= 29:
            self.Spellcard07()

        #Standart Behavior does not change speed/angle
        #=> if shot not defined, or Standart dont change anything
        GesX = math.cos(math.radians(self.alpha)) * self.speed
        GesY = - math.sin(math.radians(self.alpha)) * self.speed  
        SpeedVector = QVector2D(GesX,GesY)
        self.position.__iadd__(SpeedVector)


    def bulletShape(self):
        shape = QPainterPath()
        shape.addEllipse(self.position.x() - (0.5 * Bullet_Size) , self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)
        return shape

    def one_hit(self, robo):
        if self.bulletShape().intersects(robo.roboShape()) and self.owner != robo.robotid:
            return True
        else: pass

#Movement-patterns for Bullets in given Spellcard

    def Spellcard01(self):
        if self.bulType == 1:
            if self.time == 60:
                self.alpha =  (self.alpha - 90) % 360
                self.bulType = 2            
            
        elif self.bulType == 2:
            if self.time == 30:
                self.alpha =  (self.alpha + 90) % 360
                self.bulType = 3

        elif self.bulType == 4:
            if self.time == 60:
                self.alpha =  (self.alpha + 90) % 360
                self.bulType = 5            
            
        elif self.bulType == 5:
            if self.time == 30:
                self.alpha =  (self.alpha - 90) % 360
                self.bulType = 3
        

    def Spellcard02(self):
        if self.bulType == 6:
            if self.speed > 0:
                self.speed -= 0.08
        
            else:
                self.speed = 3
                self.bulType = 7

        elif self.bulType == 7:
            self.alpha = (self.alpha + 2.5) % 360
            if self.time == 100:
                self.bulType = random.randint(8,13)
                self.alpha = random.randint(0,360)
                #BulletType 8 to 13 are not defined in move -> use standart Behavior

    def Spellcard03(self):
        if self.bulType == 14:
            if self.time > 400:
                self.speed = 0
            elif self.time == 400:
                self.speed = 5
        

    def Spellcard04(self):
        if self.bulType == 15:
            if self.time == 100:
                self.speed = 4
                self.alpha = random.randint(0,360)
                self.bulType = 16
            elif self.time > 100:
                if self.speed >0:
                    self.speed -= 0.05
                    
        
    def Spellcard05(self):
        if self.bulType == 17:
            if self.time == 335:
                self.bulType = 18
                self.alpha = (self.alpha + 90) % 360                               
        elif self.bulType == 18:
            self.alpha = (self.alpha + 3) % 360
            if self.time == 230:
                self.alpha = (self.alpha + 72) % 360
                self.bulType = 19
                
        elif self.bulType == 19:
            if self.time == 193:
                self.alpha += random.randint(-36,18)
                self.speed = 1
                self.bulType = random.randint(20,21)
            
            
    def Spellcard06(self):
        if self.bulType == 22:
            self.speed = 1
            if self.time == 450:
                self.bulType = 23
        elif self.bulType == 23:
                self.alpha += 2
                if self.time == 350:
                    self.bulType = 24
        elif self.bulType == 24:
            if self.time == 160:
                self.speed = 3
                self.bulType = 25
        elif self.bulType == 25:
            if self.time == 50:
                self.bulType = 26
                self.speed = 0
                self.time = 150                
        elif self.bulType == 26:
            if self.time == 100:
                self.bulType = random.randint(8,13)
                self.alpha += 180
                self.speed = 3

    def Spellcard07(self):
        if self.bulType == 27:
            if self.time == 300:
                self.alpha += 162
                self.speed = 3
            if self.time == 200:
                self.bulType = 28
                self.time = 370
        elif self.bulType == 28:
            self.alpha += 1
            if self.time == 77:
                self.time = 200
                self.speed = 0
                self.alpha -= 162
                self.bulType = 29
        elif self.bulType == 29:
            if self.time == 150:
                self.alpha += random.randint(0,360)
                self.bulType = random.randint(8,13)
                self.speed = 4

