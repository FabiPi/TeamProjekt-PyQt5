"""
Chess - Schachbrett
von B-Dome, JangJang3, FabiPi
"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys

class Chess(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Chess')
        self.show()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawBlocks(qp)
        qp.end()

    def drawBlocks(self, qp):

        step = 125
        colWhite = QColor(255, 255, 255)
        colBlack = QColor(0, 0, 0)

        #each step draws a 2x2 block consisting of 4 "step"-sized blocks
        for X in range(0, 1000, 2*step):
            for Y in range(0, 1000, 2*step):
                #White top left
                qp.setBrush(colWhite)
                qp.drawRect(X , Y, step, step)
                #Black top right
                qp.setBrush(colBlack)
                qp.drawRect(X+step, Y, step, step)
                #Black bottom left
                qp.setBrush(colBlack)
                qp.drawRect(X , Y+step, step, step)
                #White bottom right
                qp.setBrush(colWhite)
                qp.drawRect(X+step, Y+step, step, step)      
        
"""
Working Loop (All Colums / No Variation inbetween)
        for Vertical in range(0, 1000, 250):
            for Horizontal in range(0, 1000, 125):
                qp.setBrush(QColor(255, 255, 255))
                qp.drawRect(Horizontal, Vertical, 125, 125)
                qp.setBrush(QColor(0, 0, 0))
                qp.drawRect(Horizontal, Vertical+125, 125, 125)
                
                
with some variations 
          
        for Vertical in range(0, 1000, 125):
            for Horizontal in range(0, 1000, 125):
                if ((Vertical + Horizontal) % 2 != 0):
                    qp.setBrush(QColor(255, 255, 255))
                    qp.drawRect(Horizontal, Vertical, 125, 125)
                else:
                    qp.setBrush(QColor(0, 0, 0))
                    qp.drawRect(Horizontal, Vertical, 125, 125)





"""

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Chess()
    sys.exit(app.exec_())
