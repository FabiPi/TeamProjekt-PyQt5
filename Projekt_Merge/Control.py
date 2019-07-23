from PyQt5.QtGui import QVector2D
from PyQt5.QtCore import Qt, QThread
import keyboard
import threading
import time

class RobotControl(QThread):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        threading.Thread.__init__(self)


#Roboter Steuerung

class PlayerRobot_All_Abilities(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
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

            #Special Attack7
            if keyboard.is_pressed('7'):
                self.robot.spellcard7()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0

class PlayerRobot_Ability01(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack
            if keyboard.is_pressed('l'):
                self.robot.spellcard1()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0
            

class PlayerRobot_Ability02(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack
            if keyboard.is_pressed('l'):
                self.robot.spellcard2()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0

class PlayerRobot_Ability03(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack
            if keyboard.is_pressed('l'):
                self.robot.spellcard3()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0

class PlayerRobot_Ability04(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack
            if keyboard.is_pressed('l'):
                self.robot.spellcard4()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0


class PlayerRobot_Ability05(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack
            if keyboard.is_pressed('l'):
                self.robot.spellcard5()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0

class PlayerRobot_Ability06(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack
            if keyboard.is_pressed('l'):
                self.robot.spellcard6()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0

class PlayerRobot_Ability07(RobotControl):
    def run(self):
        while True:
            self.msleep(10)
            
            if keyboard.is_pressed('w'):
                if self.robot.a + 0.3 <= self.robot.a_max:
                    self.robot.a += 0.3

            elif keyboard.is_pressed('s'):
                if abs(self.robot.a)  + 0.3 <= self.robot.a_max:
                    self.robot.a += -0.3
                    
            #Slowdown if no key is pressed
            else:
                self.robot.v = self.robot.v * 0.5
                self.robot.a = self.robot.a * 0.5

            if keyboard.is_pressed('a'):
                if self.robot.a_alpha +1 <= self.robot.a_alpha_max:
                    self.robot.a_alpha += 1

            elif keyboard.is_pressed('d'):
                if abs(self.robot.a_alpha) + 1 <=  self.robot.a_alpha_max:
                    self.robot.a_alpha += -1

            #Slowdown if no key is pressed
            else:
                self.robot.v_alpha = self.robot.v_alpha  * 0.4
                self.robot.a_alpha  = self.robot.a_alpha  * 0.4
                
            if keyboard.is_pressed('j'):
                self.robot.shoot()

            #Special Attack
            if keyboard.is_pressed('l'):
                self.robot.spellcard7()

            #temporary Stop key    
            if keyboard.is_pressed('q'):
                self.robot.v = 0
                self.robot.a = 0
                self.robot.v_alpha = 0
                self.robot.a_alpha = 0

class TargetHunt(RobotControl):

    def run(self):
        while True:
            self.robot.a = 1
            target = 1
            self.robot.aimTargetView(target)
            self.msleep(10)
            if self.robot.ViewList[target][3]:
                self.robot.shoot()

class CircleMap(RobotControl):
    
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
            self.msleep(10)
            self.robot.shoot()
