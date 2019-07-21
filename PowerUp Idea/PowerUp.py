"""
PowerUp Groups
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QBasicTimer, QThread
import keyboard
import sys
import math
import threading
import time
import Server
import random
import Robots

STAR_RESPAWN_TIME = 1000


class Star(object):

    
    def __init__(self, position):       
        self.texture = QPixmap('textures/star.png')
        self.position = position
        self.respawntimer = 0

    def starShape(self):
        shape = QPainterPath()
        shape.AddEllipse(self.position.x(), self.position.y(), 32, 32)
        return shape

  #  def starIntersect(self, robo):
       # if self.starShape().intersects(robo.roboShape()):
           # return True
       # else: pass

    

    
        


