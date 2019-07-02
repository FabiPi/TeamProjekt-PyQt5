"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""


from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
import math
import Server
import Robots

#####  BULLET   ######

BULLET_SIZE = 10


class Bullet(object):
    def __init__(self, position, alpha, bulletspeed):
        self.position = position
        self.alpha = alpha
        self.bulletspeed = bulletspeed

        # bulletstate:
        # ready - is ready to fire
        # fire - bullet is firing
        # loading - bullet is not ready
        self.bulletstate = "ready"

    # Funktion | Zeichnen von Bullet #
    def drawBullet(self, Bullet, br):
        br.setBrush(Server.colors["yellow"])
        br.setPen(Server.colors["black"])
        br.drawEllipse(int(round(Bullet.position.x())), int(round(Bullet.position.y())), BULLET_SIZE, BULLET_SIZE)

        # Flugrichtung bzw. Richtungsvektor
        xPos = math.cos(math.radians(Robots.alpha))
        yPos = - math.sin(math.radians(Robots.alpha))


    def fire_Bullet(self):
        # fire bullet if other robot is in view

        # set bullet position so it is where the other robo is

        # add bullet to list for later remove

        pass



# TODO: If Robo1-Blickwinkel intersects Robo2-Position ==> drawBullet
# and move it with constant Robo.alpha and Robo.speed [While (CheckIfBulletOutOfSpielFeld = FALSE) do moveBullet)

######################
