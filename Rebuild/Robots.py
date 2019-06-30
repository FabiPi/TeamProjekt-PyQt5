"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

"""
TODO-LIST
Move-Methode in RoboterClass legen
Timer-Steuerung verstehen/anpassen
collision und FOV einfügen
RobotLists und stuff
"""


from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QBasicTimer, QThread
import sys
import math
import threading
import time
import Server


#Constants
alpha_eps = 0.5 #velocity-stop breakpoint
vMax = 5 #max velocity
v_alpha_Max = 10 #max alpha velocity

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
        
                # for FOV
                            # Position, Distanz zueinander, Blickwinkel, seen
        self.ViewList = {1 : [ QVector2D(0,0), 0, 0, False],
                         2 : [ QVector2D(0,0), 0, 0, False],
                         3 : [ QVector2D(0,0), 0, 0, False],
                         4 : [ QVector2D(0,0), 0, 0, False]}
        self.FOV = FOV

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

    #Getter Methods
    #nicht sicher ob die gebraucht werden, evtl entfernen
    def get_Id(self):
        return self.robotid

    def get_position(self):
        return self.position

    def get_xPos(self):
        return self.position.x()
    
    def get_yPos(self):
        return self.position.y()
    
    def get_alpha(self):
        return self.alpha
    
    def get_List(self):
        return self.RobotList
    
    def get_v_Vector(self):
        return self.v_vector

    def get_v_Total(self):
        return self.v

    def get_v_alpha(self):
        return self.v_alpha

    def get_a_max(self):
        return self.a_max

    def get_a_alpha_max(self):
        return self.a_alpha_max

        # for the FOV
    def roboShape(self):
        shape = QPainterPath()
        shape.addEllipse(int(round(self.position.x())), int(round(self.position.y())), self.radius, self.radius)

        return shape
    
    def moveChase(self, tarAlpha):
        target_alpha = tarAlpha

        if 0 + self.alpha < target_alpha <= 180 + self.alpha:
            # turn left
            self.a_alpha = 0.5
        elif self.alpha == target_alpha:
            # keep straight
            self.a_alpha = 0
            self.v_alpha = 0
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

        # no, wait around
        else:
            self.v = 0
            self.a_alpha = 2   
      

class RobotControl(QThread):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        threading.Thread.__init__(self)
    

#Roboter Steuerung
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
            target = 1
            chaserFriend = 2
            self.robot.aimTargetIntelligent(target, chaserFriend)
            self.msleep(100)
    
