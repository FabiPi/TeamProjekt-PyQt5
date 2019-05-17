

## Roboter im Spielfeld
**Erste Entwürfe des Spielfelds**

Wir haben uns zuerst einmal damit beschäftigt das 1000x1000 Pixel große Spielfeld zu entwerfen.

```python
    def drawField(self, qp):
        
        #Array construction
        width = 100
        height = 100
        PlayFieldAR = [[0 for x in range(width)] for y in range(height)]
```

Dafür haben wie einen 2D-Array der Größe 100x100 entworfen, dessen Werte später auf 0 für Ground und 1 für Wall gesetzt werden.

Das Spielfeld wird über eine Schleife gezeichnet, welche erst in y und anschließend in x Richtung alle einzelnen 10x10 große Felder zeichnet.
```python
#Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if PlayFieldAR[i][j]==1:
                        qp.setBrush(QColor(0, 0, 0))
                        qp.drawRect(i*10, j*10, 10, 10)
                    else:
                        qp.setBrush(QColor(150, 150, 150))
                        qp.drawRect(i*10, j*10, 10, 10)
```
Placeholder Bild 00

Im nächsten Schritt haben wir begonnen erste Hindernisse zu platzieren.

```python
    #set Walls, set array value to 1 to place Wall
    PlayFieldAR[0][0]= 1
    PlayFieldAR[10][0]= 1
    PlayFieldAR[0][10]= 1
    PlayFieldAR[25][20]= 1
    PlayFieldAR[10][50]= 1
```
Placeholder Bild 01

Das Spielfeld mit einer Wand zu umranden,

```python
        #set Wall around the edges
        for x in range(0,100,1):
            PlayFieldAR[x][0]= 1
            PlayFieldAR[x][99]= 1
        for y in range(1,99,1):
            PlayFieldAR[0][y]= 1
            PlayFieldAR[99][y]= 1
```
Placeholder Bild 02

und noch einige Hindernisse in der Mitte des Spielfelds zu platzieren.

```python
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
```
Placeholder Bild 03

**Entwurf des Roboters**
Für die Implementierung des Robotors wurde zunächst eine Klasse BaseRobot erstellt. In dieser mit den x,y Positionen, dem Radius und der Wert Alpha für die Blickrichtung.
```python
class BaseRobot (QWidget):
    xPosition = 20
    yPosition = 30
    radius = 5
    alpha = 45
```

Place for Timer implement.

**Steuerung des Roboters mit WASD**
Um den Roboter mit der Tastatur zu steuern haben wir das keyPressEvent verwendet.
Wir wollen mit W nach oben fahren, mit S nach unten, A nach links und mit D nach rechts, d.h wir müssen jeweils die x bzw. y Koordinaten des Roboters anpassen.

```python
def keyPressEvent(self, event):
        
        key = event.key()

        if key == Qt.Key_W:
            BaseRobot.yPosition -= 10
            return
        
        elif key == Qt.Key_S:
            BaseRobot.yPosition += 10
            return

        elif key == Qt.Key_A:
            BaseRobot.xPosition -= 10
            return

        elif key == Qt.Key_D:
            iBaseRobot.xPosition += 10
            return     
```
Um Kollision mit den Wänden einzufügen müssen wir jeweils prüfen ob einer der Blöcke in Fahrtrichtung eine Wand ist.
Da unser Roboter aus 3x3 Feldern besteht muss man jeweils 3 Blöcke prüfen.

Bild mit Roboter und Grid


```python
def keyPressEvent(self, event):
        '''process key press'''
        RobotX = int(round(BaseRobot.xPosition/10))
        RobotY = int(round(BaseRobot.yPosition/10))

        print(RobotX)
        
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
```


## Chess.py
**Full Code:**
```python
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
            qp.setBrush(colWhite))
            qp.drawRect(X+step, Y+step, step, step) 
```
Zwei for-Schleifen erzeugen das ganze Schachbrett.
*For-X* übernimmt die Horizontalen Steps, *For-Y* die Vertikalen.
Durch Veränderung der Step-Konstante lassen sich verschiedene Verteilungen des Schachbretts auf die feste 1000x1000 Fläche zeichnen.

Die Methode setBrush() zeichnet mithilfe von QColor den Hintergrund einer grafischen Form. Die QColor für unser Schachbrett ist einmal colWhite (255, 255, 255) und colBlack (0, 0, 0). Die Methode drawRect(x, y, width, height) zeichnet uns dann einen Rechteck, in der Farbe von unserer setBrush() Methode.

In Zeile 17 wird der erste weiße Block links oben konstruiert. In Zeile 20 der erste schwarze Block rechts oben. In Zeile 22 erfolgt dann der nächste schwarze Block links unten und daneben in Zeile 26 der nächste weiße Block rechts unten. Es wird somit immer ein 2x2 Block konstruiert. Dabei wird das Schachbrett abwechselnd immer zuerst vertikal nach unten mit den 2x2 Blöcken gefüllt, dann mit 2x2 Blöcken einmal horizontal, wieder vertikal nach unten und so weiter. 


Mit step = 125 wird dann das klassische 8x8 Schachbrett gezeichnet.
