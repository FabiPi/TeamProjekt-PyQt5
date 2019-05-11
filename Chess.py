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
      
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

#First Column
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 0, 100, 100)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 100, 100, 100)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 200, 100, 100)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 300, 100, 100)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 400, 100, 100)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 500, 100, 100)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 600, 100, 100)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 700, 100, 100)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 800, 100, 100)

        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 900, 100, 100)
        
"""
For Loop Idea
#First Column
        for X in range(0, 500, 125):
            qp.setBrush(QColor(255, 255, 255))
            qp.drawRect(0, X, 125, 125)
            qp.setBrush(QColor(0, 0, 0))
            qp.drawRect(0, X+125, 125, 125)
"""
        

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Chess()
    sys.exit(app.exec_())
