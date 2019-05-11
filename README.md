title: JDF - PyQt5 TeamProjekt
description: von JangJang3, B-Dome, FabiPi
## Index

## Chess.py
**Full Code:**
```
def drawBlocks(self, qp):

    step = 125

    #each step draws a 2x2 block consisting of 4 "step"-sized blocks
    for X in range(0, 1000, 2*step):
        for Y in range(0, 1000, 2*step):
            #White top left
            qp.setBrush(QColor(255, 255, 255))
            qp.drawRect(X , Y, step, step)
            #Black top right
            qp.setBrush(QColor(0, 0, 0))
            qp.drawRect(X+step, Y, step, step)
            #Black bottom left
            qp.setBrush(QColor(0, 0, 0))
            qp.drawRect(X , Y+step, step, step)
            #White bottom right
            qp.setBrush(QColor(255, 255, 255))
            qp.drawRect(X+step, Y+step, step, step) 
```
Zwei for-Schleifen erzeugen das ganze Schachbrett.
*For-X* übernimmt die Horizontalen Steps, *For-Y* die Vertikalen.
Durch Veränderung der Step-Konstane lassen sich verschieden Verteilungen des Schachbretts auf die feste 1000x1000 Fläche zeichnen.
(Mit step = 125 für das klassische 8x8 Brett)
