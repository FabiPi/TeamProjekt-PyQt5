"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtGui import QVector2D
from PyQt5.QtCore import QThread
import threading
import keyboard



class RobotControl(QThread):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        threading.Thread.__init__(self)


# Roboter Steuerung

class RunAwayKeyBoard(RobotControl):
    def run(self):
        while True:
            self.msleep(100)

            if keyboard.is_pressed('w'):
                # print('W-Key')
                self.robot.a = 0.1

            if keyboard.is_pressed('s'):
                # print('S-Key')
                self.robot.a = -0.1

            if keyboard.is_pressed('a'):
                # print('A-Key')
                self.robot.a_alpha = 0.5

            if keyboard.is_pressed('d'):
                # print('D-Key')
                self.robot.a_alpha = -0.5

            if keyboard.is_pressed('j'):
                # print('J-Key')
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
                target = QVector2D(950, 950)
            elif targetnum == 1:
                target = QVector2D(950, 50)
            elif targetnum == 2:
                target = QVector2D(50, 50)
            elif targetnum == 3:
                target = QVector2D(50, 950)

            if self.robot.inVicinity(target):
                targetnum = (targetnum + 1) % 4
            self.robot.aimTarget(target)
            self.msleep(100)
            self.robot.shoot()


class CircleMap2(RobotControl):
    def run(self):
        self.robot.a = 1
        targetnum = 3
        while True:
            if targetnum == 0:
                target = QVector2D(900, 900)
            elif targetnum == 1:
                target = QVector2D(900, 100)
            elif targetnum == 2:
                target = QVector2D(100, 100)
            elif targetnum == 3:
                target = QVector2D(100, 900)

            if self.robot.inVicinity(target):
                targetnum = (targetnum + 1) % 4
            self.robot.aimTarget(target)
            self.msleep(100)
            self.robot.shoot()


class CircleMap3(RobotControl):
    def run(self):
        self.robot.a = 1
        targetnum = 2
        while True:
            if targetnum == 0:
                target = QVector2D(900, 900)
            elif targetnum == 1:
                target = QVector2D(900, 100)
            elif targetnum == 2:
                target = QVector2D(100, 100)
            elif targetnum == 3:
                target = QVector2D(100, 900)

            if self.robot.inVicinity(target):
                targetnum = (targetnum + 1) % 4
            self.robot.aimTarget(target)
            self.msleep(100)
            self.robot.shoot()


class TargetChase(RobotControl):

    def run(self):
        self.robot.a = 1
        target = QVector2D(900, 900)
        while True:
            if self.robot.inVicinity(QVector2D(900, 900)):
                target = QVector2D(100, 100)
            if self.robot.inVicinity(QVector2D(100, 100)):
                target = QVector2D(900, 900)
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
