"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""


from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
import math
import Server
import Robots

#####  BULLET   ######

Bullet_Size = 10
Bullet_Speed =5

class Bullet(object):
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


    def drawBullet(self, br):
        br.setBrush(QColor(255, 255, 250))
        br.drawEllipse(self.position.x() - (0.5 * Bullet_Size),self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)

    def moveBullet(self):
        self.position.__iadd__(self.velocity)


    def bulletShape(self):
        shape = QPainterPath()
        shape.addEllipse(self.position.x() - (0.5 * Bullet_Size) , self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)
        return shape

    def one_hit(self, robo):
        return self.bulletShape().intersects(robo.roboShape())

        
        

        
 
