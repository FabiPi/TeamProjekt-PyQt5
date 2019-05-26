"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QBasicTimer
import math
import sys
import time
import threading

class SpielFeld(QWidget):


    PlayFieldAR = [[0 for x in range(100)] for y in range(100)]

    Speed = 200

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('PlayField')
        self.center()
        self.timer = QBasicTimer()
        self.timer.start(SpielFeld.Speed, self)
        self.show()

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


    def timerEvent(self, event):
        screen = QDesktopWidget().screenGeometry()

        if (BaseRobot.xPosition == (screen.width() - (BaseRobot.radius +10))) or (BaseRobot.yPosition == (screen.height() - (BaseRobot.radius + 10))):
            self.timer.stop()
        else:
            if BaseRobot.alpha == 90:
                self.moveUp()
            
            elif BaseRobot.alpha == 45:
                self.moveUp()
                self.moveRight()
              
            elif BaseRobot.alpha == 0:
                self.moveRight()
     
            elif BaseRobot.alpha == 315:
                self.moveDown()
                self.moveRight()

            elif BaseRobot.alpha == 270:
                self.moveDown()
                
            elif BaseRobot.alpha == 225:
                self.moveDown()
                self.moveLeft()
                
            elif BaseRobot.alpha == 180:
                self.moveLeft()
                
            elif BaseRobot.alpha == 135:
                self.moveUp()
                self.moveLeft()

        
        """
        XPos = BaseRobot.xPosition
        YPos = BaseRobot.yPosition
        block = 10
        # stops if its near the fieldborders, if not moves to the right
        if (XPos < block) or (XPos > (1000 - block) ) or (YPos < block) or (YPos > (1000- block)):
            self.timer.stop()
        else:
            BaseRobot.xPosition += 10
        """

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


    def paintEvent(self, qp ):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        self.drawFirstRobo(qp)
        qp.end()
        

    def drawField(self, qp):

        #Array construction

        #set Walls, set array value to 1 to place Wall

        #set Wall around the edges
        for x in range(0,100,1):
            SpielFeld.PlayFieldAR[x][0]= 1
            SpielFeld.PlayFieldAR[x][99]= 1
        for y in range(1,99,1):
            SpielFeld.PlayFieldAR[0][y]= 1
            SpielFeld.PlayFieldAR[99][y]= 1

        #set some Obstacle
        for i in range(0, 25, 1):
            SpielFeld.PlayFieldAR[70][i+45] = 1

        for i in range(0, 40, 1):
            SpielFeld.PlayFieldAR[i+10][40] = 1
        for i in range(0, 50, 1):
            SpielFeld.PlayFieldAR[i+30][70] = 1

        for i in range(0, 30, 1):
            SpielFeld.PlayFieldAR[i+25][20] = 1

        for i in range(0, 10, 1):
            SpielFeld.PlayFieldAR[10][i+50] = 1

        #Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if SpielFeld.PlayFieldAR[i][j]==1:
                        qp.setBrush(QColor(0, 0, 0))
                        qp.drawRect(i*10, j*10, 10, 10)
                    else:
                        qp.setBrush(QColor(150, 150, 150))
                        qp.drawRect(i*10, j*10, 10, 10)


#Robots
    # RED
    def drawFirstRobo(self, br):

        br.setBrush(QColor(255, 0, 0))
        br.setPen(QColor(0,0,0))
        br.drawEllipse(BaseRobot.xPosition, BaseRobot.yPosition , 2* BaseRobot.radius, 2*BaseRobot.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(BaseRobot.alpha)) * BaseRobot.radius
        yPos = math.sin(math.radians(BaseRobot.alpha)) * BaseRobot.radius

        br.drawLine(BaseRobot.xPosition + BaseRobot.radius, BaseRobot.yPosition + BaseRobot.radius, (BaseRobot.xPosition + BaseRobot.radius) + xPos, (BaseRobot.yPosition + BaseRobot.radius) - yPos)

        self.update()


    # GREEN
    def drawSecondRobo(self, br):

        br.setBrush(QColor(0, 255, 0))
        br.setPen(QColor(0,0,0))
        br.drawEllipse(BaseRobot.xPosition, BaseRobot.yPosition , 2* BaseRobot.radius, 2*BaseRobot.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(BaseRobot.alpha)) * BaseRobot.radius
        yPos = math.sin(math.radians(BaseRobot.alpha)) * BaseRobot.radius

        br.drawLine(BaseRobot.xPosition + BaseRobot.radius, BaseRobot.yPosition + BaseRobot.radius, (BaseRobot.xPosition + BaseRobot.radius) + xPos, (BaseRobot.yPosition + BaseRobot.radius) - yPos)

        self.update()

    # BLUE
    def drawThirdRobo(self, br):

        br.setBrush(QColor(0, 255, 0))
        br.setPen(QColor(0,0,0))
        br.drawEllipse(BaseRobot.xPosition, BaseRobot.yPosition , 2* BaseRobot.radius, 2*BaseRobot.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(BaseRobot.alpha)) * BaseRobot.radius
        yPos = math.sin(math.radians(BaseRobot.alpha)) * BaseRobot.radius

        br.drawLine(BaseRobot.xPosition + BaseRobot.radius, BaseRobot.yPosition + BaseRobot.radius, (BaseRobot.xPosition + BaseRobot.radius) + xPos, (BaseRobot.yPosition + BaseRobot.radius) - yPos)

        self.update()

    # YELLOW
    def drawFourthRobo(self, br):

        br.setBrush(QColor(255, 255, 0))
        br.setPen(QColor(0,0,0))
        br.drawEllipse(BaseRobot.xPosition, BaseRobot.yPosition , 2* BaseRobot.radius, 2*BaseRobot.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(BaseRobot.alpha)) * BaseRobot.radius
        yPos = math.sin(math.radians(BaseRobot.alpha)) * BaseRobot.radius

        br.drawLine(BaseRobot.xPosition + BaseRobot.radius, BaseRobot.yPosition + BaseRobot.radius, (BaseRobot.xPosition + BaseRobot.radius) + xPos, (BaseRobot.yPosition + BaseRobot.radius) - yPos)

        self.update()




        
    def keyPressEvent(self, event):
        '''process key press'''
        key = event.key()

        if key == Qt.Key_A:
            BaseRobot.alpha = int(round((BaseRobot.alpha - 45) % 360))
            return

        elif key == Qt.Key_D:
            BaseRobot.alpha = int(round((BaseRobot.alpha + 45) %360))
            return

    def moveUp(self):
        RobotX = int(round(BaseRobot.xPosition/10))
        RobotY = int(round(BaseRobot.yPosition/10))
        if SpielFeld.PlayFieldAR[RobotX][RobotY-1] == SpielFeld.PlayFieldAR[RobotX+1][RobotY-1] == SpielFeld.PlayFieldAR[RobotX+2][RobotY-1] == 0:
            BaseRobot.yPosition -= 10

    def moveDown(self):
        RobotX = int(round(BaseRobot.xPosition/10))
        RobotY = int(round(BaseRobot.yPosition/10))
        if SpielFeld.PlayFieldAR[RobotX][RobotY+3] == SpielFeld.PlayFieldAR[RobotX+1][RobotY+3] == SpielFeld.PlayFieldAR[RobotX+2][RobotY+3] == 0:
            BaseRobot.yPosition += 10

    def moveLeft(self):
        RobotX = int(round(BaseRobot.xPosition/10))
        RobotY = int(round(BaseRobot.yPosition/10))
        if SpielFeld.PlayFieldAR[RobotX-1][RobotY] == SpielFeld.PlayFieldAR[RobotX-1][RobotY+1] == SpielFeld.PlayFieldAR[RobotX-1][RobotY+2] == 0:
            BaseRobot.xPosition -= 10

    def moveRight(self):
        RobotX = int(round(BaseRobot.xPosition/10))
        RobotY = int(round(BaseRobot.yPosition/10))
        if SpielFeld.PlayFieldAR[RobotX+3][RobotY] == SpielFeld.PlayFieldAR[RobotX+3][RobotY+1] == SpielFeld.PlayFieldAR[RobotX+3][RobotY+2] == 0:
            BaseRobot.xPosition += 10        
    """
    def keyPressEvent(self, event):
        '''process key press'''
        RobotX = int(round(BaseRobot.xPosition/10))
        RobotY = int(round(BaseRobot.yPosition/10))
        key = event.key()
        if key == Qt.Key_W:
            if SpielFeld.PlayFieldAR[RobotX][RobotY-1] == SpielFeld.PlayFieldAR[RobotX+1][RobotY-1] == SpielFeld.PlayFieldAR[RobotX+2][RobotY-1] == 0:
                BaseRobot.yPosition -= 10
            return
        elif key == Qt.Key_S:
            if SpielFeld.PlayFieldAR[RobotX][RobotY+3] == SpielFeld.PlayFieldAR[RobotX+1][RobotY+3] == SpielFeld.PlayFieldAR[RobotX+2][RobotY+3] == 0:
                BaseRobot.yPosition += 10
            return
        elif key == Qt.Key_A:
            if SpielFeld.PlayFieldAR[RobotX-1][RobotY] == SpielFeld.PlayFieldAR[RobotX-1][RobotY+1] == SpielFeld.PlayFieldAR[RobotX-1][RobotY+2] == 0:
                BaseRobot.xPosition -= 10
            return
        elif key == Qt.Key_D:
            if SpielFeld.PlayFieldAR[RobotX+3][RobotY] == SpielFeld.PlayFieldAR[RobotX+3][RobotY+1] == SpielFeld.PlayFieldAR[RobotX+3][RobotY+2] == 0:
                BaseRobot.xPosition += 10
            return
    """

class BaseRobot (QWidget):
    xPosition = 20
    yPosition = 30
    radius = 15
    alpha = 45

    a = 1
    a_alpha = 1

    a_max = 3
    a_alpha_max = 3

    #v
    #v_alpha


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = SpielFeld()
    sys.exit(app.exec_())
