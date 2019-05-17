"""
Roboter Feld
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys

class SpielFeld(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('PlayField')
        self.show()

    def paintEvent(self, qp):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        self.drawRobo(qp)
        qp.end()

    def drawField(self, qp):

        #Array construction
        width = 100
        height = 100
        PlayFieldAR = [[0 for x in range(width)] for y in range(height)]

        #set Walls, set array value to 1 to place Wall

        #set Wall around the edges
        for x in range(0,100,1):
            PlayFieldAR[x][0]= 1
            PlayFieldAR[x][99]= 1
        for y in range(1,99,1):
            PlayFieldAR[0][y]= 1
            PlayFieldAR[99][y]= 1

        #set some Obstacle
        for i in range(0, 25, 1):
            PlayFieldAR[70][i+45] = 1

        for i in range(0, 40, 1):
            PlayFieldAR[i+10][40] = 1
        for i in range(0, 50, 1):
            PlayFieldAR[i+30][70] = 1

        for i in range(0, 30, 1):
            PlayFieldAR[i+25][20] = 1

        for i in range(0, 10, 1):
            PlayFieldAR[10][i+50] = 1

        """
        Randomisierte Verteilung von field oder wall
        for i in range (0,100,1):
            for j in range(0,100,1):
                if (PlayFieldAR[i-1][i-1] != 1):
                    PlayFieldAR[i][j] = random.randint(0,1)
                else:
                    PlayFieldAR[i][j] = 0
        """

        #Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if PlayFieldAR[i][j]==1:
                        qp.setBrush(QColor(0, 0, 0))
                        qp.drawRect(i*10, j*10, 10, 10)
                    else:
                        qp.setBrush(QColor(150, 150, 150))
                        qp.drawRect(i*10, j*10, 10, 10)
                    
    def drawRobo(self, br):
        br.setBrush(QColor(255, 0, 0))
        br.drawEllipse(50, 50, 50 ,50)
        
                    

class BaseRobot (QWidget):
    Position = [0][0]
    r = 5
    alpha = 45
    
"""

    def paintEvent(self, e):

        br = QPainter()
        br.begin(self)
        self.drawField(e)
        br.end()

    def drawField(self, br):
        br.setBrush(QColor(255, 0, 0))
        br.drawEllipse(50, 50, 50 ,50)
"""


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = SpielFeld()
sys.exit(app.exec_())
