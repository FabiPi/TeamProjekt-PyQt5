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

"""


from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
import math
import Server
import Robots

#####  BULLET   ######

Bullet_Size = 10
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
        self.BulletTextures = {0:QPixmap('textures/bullet.png'), #Standart
                               1:QPixmap('textures/bullet01.png'), #Green 1
                               2:QPixmap('textures/bullet02.png'), #Blue 1
                               3:QPixmap('textures/bullet03.png'), #Red
                               4:QPixmap('textures/bullet01.png'), #Green 2
                               5:QPixmap('textures/bullet02.png')} #Blue 2


    def drawBullet(self, br):
        br.setBrush(QColor(255, 255, 250))
        texture = self.BulletTextures[self.bulType]
        br.drawPixmap(self.position.x() - (0.5 * Bullet_Size),self.position.y() - (0.5 * Bullet_Size), texture)

    def moveBullet(self):
        if self.bulType == 1:
            if self.time == 60:
                self.alpha =  (self.alpha - 90) % 360
                self.bulType = 2            
            GesX = math.cos(math.radians(self.alpha)) * self.speed
            GesY = - math.sin(math.radians(self.alpha)) * self.speed
            
        if self.bulType == 2:
            if self.time == 30:
                self.alpha =  (self.alpha + 90) % 360
                self.bulType = 3
            
            GesX = math.cos(math.radians(self.alpha)) * self.speed
            GesY = - math.sin(math.radians(self.alpha)) * self.speed


        if self.bulType == 4:
            if self.time == 60:
                self.alpha =  (self.alpha + 90) % 360
                self.bulType = 5            
            GesX = math.cos(math.radians(self.alpha)) * self.speed
            GesY = - math.sin(math.radians(self.alpha)) * self.speed
            
        if self.bulType == 5:
            if self.time == 30:
                self.alpha =  (self.alpha - 90) % 360
                self.bulType = 3
            
            GesX = math.cos(math.radians(self.alpha)) * self.speed
            GesY = - math.sin(math.radians(self.alpha)) * self.speed

        else:   #equals normal shot
            GesX = math.cos(math.radians(self.alpha)) * self.speed
            GesY = - math.sin(math.radians(self.alpha)) * self.speed
            
        SpeedVector = QVector2D(GesX,GesY)
        self.position.__iadd__(SpeedVector)


    def bulletShape(self):
        shape = QPainterPath()
        shape.addEllipse(self.position.x() - (0.5 * Bullet_Size) , self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)
        return shape

    def one_hit(self, robo):
        if self.bulletShape().intersects(robo.roboShape()):
            return True
        else: pass
        
        
        

        
 
