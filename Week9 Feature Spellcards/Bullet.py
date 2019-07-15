"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

"""
Change-List
    add Attributes
    -Direction
    -Velocity (non vector)
    -type
    -textures
    -delay

    add CD to Robot class

    update shoot() method
    create special() method
    update moveBullet() method

    update tick-event for bullet
    add Cooldown to reduceDelay

    *** first upload***

    adjusted speed in spellcards / shoot

    change moveBullet
    add spellcard2
    import random

    add Spellcard3
    refactor other Spellcards, shoot, create Bullet

    *** second Upload***

    update Draw Method to include Rotation
    update Robot Visual

    *** third Upload ***

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
    #add Attributes
    #-Direction
    #-Velocity (non vector)
    #-type
    #-time
    def __init__(self, position, velocity, speed, alpha, time, delay, bulType):
        self.position = position
        self.velocity = velocity
        self.speed = speed
        self.alpha = alpha
        self.bulType = bulType
        self.time = time
        self.delay = delay
        self.BulletTextures = {0:QPixmap('textures/bullet00.png'), #Standart
                               1:QPixmap('textures/bullet01.png'), #Green 1
                               2:QPixmap('textures/bullet02.png'), #Blue 1
                               3:QPixmap('textures/bullet03.png'), #Red
                               4:QPixmap('textures/bullet01.png'), #Green 2
                               5:QPixmap('textures/bullet02.png'), #Blue 2

                               6:QPixmap('textures/bullet01.png'), #Green
                               7:QPixmap('textures/bullet02.png'), #Blue
                               8:QPixmap('textures/bullet04.png'), #Kunai
                               
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

    def moveBullet(self): #export Spellcards later in extra Method
        #Spellcard 1                     
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

            
        #Spellcard 2
        elif self.bulType == 6:
            if self.speed > 0:
                self.speed -= 0.08
        
            else:
                self.speed = 3
                self.bulType = 7

        elif self.bulType == 7:
            self.alpha = (self.alpha + 2.5) % 360
            if self.time == 100:
                self.bulType = 0
                self.alpha = random.randint(0,360)
                

        #Spellcard 3
        elif self.bulType == 8:
            if self.time > 400:
                self.speed = 0
            elif self.time == 400:
                self.speed = 5


        #if standart shot, dont change anything
        GesX = math.cos(math.radians(self.alpha)) * self.speed
        GesY = - math.sin(math.radians(self.alpha)) * self.speed  
        SpeedVector = QVector2D(GesX,GesY)
        self.position.__iadd__(SpeedVector)
        #print(self.speed)


    def bulletShape(self):
        shape = QPainterPath()
        shape.addEllipse(self.position.x() - (0.5 * Bullet_Size) , self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)
        return shape

    def one_hit(self, robo):
        if self.bulletShape().intersects(robo.roboShape()):
            return True
        else: pass
        
        
        

        
 
