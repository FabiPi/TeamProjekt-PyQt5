## Index

## Chess.py
**Full Code:**
```python
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
Durch Veränderung der Step-Konstante lassen sich verschiedene Verteilungen des Schachbretts auf die feste 1000x1000 Fläche zeichnen.

Mit der Methode setBrush() definieren wir einen pen und eine QColor. Die QColor für unser Schachbrett ist einmal white (255, 255, 255) und black (0, 0, 0). Die Methode drawRect(x, y, width, height) zeichnet uns dann einen Rechteck, in der Farbe von unserer setBrush() Methode.

In Zeile 17 wird der erste weiße Block links oben konstruiert. In Zeile 20 der erste schwarze Block rechts oben. In Zeile 22 erfolgt dann der nächste schwarze Block links unten und daneben in Zeile 26 der nächste weiße Block rechts unten. Es wird somit ein 2x2 Block konstruiert. 

Mit step = 125 wird dann das klassische 8x8 Schachbrett gezeichnet.
