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

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        qp.end()

    def drawField(self, qp):
        
        #Array construction
        width = 100
        height = 100
        PlayFieldAR = [[0 for x in range(width)] for y in range(height)]

        #set Walls, set array value to 1 to place Wall
        PlayFieldAR[0][0] = 1
        PlayFieldAR[10][0] = 1
        PlayFieldAR[0][10] = 1
        PlayFieldAR[25][20] = 1
        PlayFieldAR[10][50] = 1

        
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if PlayFieldAR[i][j]==1:
                        qp.setBrush(QColor(0, 0, 0))
                        qp.drawRect(i*10, j*10, 10, 10)
                    else:
                        qp.setBrush(QColor(150, 150, 150))
                        qp.drawRect(i*10, j*10, 10, 10)
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = SpielFeld()
    sys.exit(app.exec_())
