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

        self.setGeometry(300, 300, 1000, 1000)
        self.setWindowTitle('Chess')
        self.show()

    def PaintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawBlocks(qp)
        qp.end()

    def drawBlocks(self, qp):

        colBlack = QColor(0, 0, 0)
        colBlack.setNamedColor('black')

        colWhite = QColor(0, 0, 0)
        colWhite.setNamedColor('white')
        
        qp.setPen(colBlack)
        qp.setBrush(QColor(100, 0, 0))
        qp.drawRect(100, 100, 100, 100)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chess()
    sys.exit(app.exec_())
