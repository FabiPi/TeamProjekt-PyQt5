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
      
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

#First Column
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 0, step, step)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, step, step, step)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 2*step, step, step)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 3*step, step, step)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 4*step, step, step)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 5*step, step, step)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 6*step, step, step)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 7*step, step, step)
        
"""
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 8*step, step, step)
"""       
        
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
