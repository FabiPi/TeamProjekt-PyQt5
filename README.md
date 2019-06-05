## Roboter - Geschwindigkeitsvektor Update
**Overlapping**
```python
def is_overlapping (self, x1, y1, r1,x2, y2, r2):
    return self.distanceTwoPoints(x1, y1, x2, y2) <= (r1+r2)
```
Prüfen, ob die zwei Roboter überlappen. Dazu wird mit distanceTwoPoints der Abstand zwischen den Beiden gemessen.
**Distanz zw. Robos**
```python
def distanceTwoPoints(self, x1, y1, x2, y2):
    return math.sqrt((x2-x1) * (x2-x1) + (y2-y1)*(y2-y1))
```
**Collision Funktion**
```python
# with elastic collision
# problem: only one velocity
newVelX1 = (robo.v * (robo.mass - robot.mass) + (2 * robot.mass * robot.v)) /(robo.mass + robot.mass)
newVelY1 = (robo.v * (robo.mass - robot.mass) + (2 * robot.mass * robot.v)) / (robo.mass + robot.mass)

newVelX2 = (robot.v * (robot.mass - robo.mass) + (2 * robo.mass * robo.v)) / (robo.mass + robot.mass)
newVelY2 = (robot.v * (robot.mass - robo.mass) + (2 * robo.mass * robo.v)) / (robo.mass + robot.mass)

robo.xPosition += newVelX1
robo.yPosition += newVelY1
robot.xPosition += newVelX2
robot.yPosition += newVelY2
```
Es werden die neuen Geschwindigkeiten ausgerechnet, um die neue Position der Roboter zu berechnen. Wenn z.B. beide in entegengesetze Richtungen sich bewegen und kollidieren, würden sich dessen Geschwindigkeiten in dem Moment aufheben (wenn beide Massen auch gleich sind).

Unsere Problematik liegt daran, da wir (um den Geschw.-vektor zu bilden) die Geschwindigkeit auf die X und Y Achse gespalten haben, funktioniert diese Kollisionsfunktion nicht mehr, wenn wir auf diese die GesX und GesY Werte anwenden. Deswegen blieben wir ausnahmsweise bei robot.v in collison(self,robo).

**Collision** </br>
Um die Collision abzufragen wird wie bereits in einer vorherigen Version die umliegenden Felder des Roboters geprüft.</br>
Dazu wird eine Schleife anhand des Radius durchlaufen und prüft je nach Bewegungsrichtung die notwendigen Felder.

```python
def barrierCollision(self, robo):
        PosX = int(round(robo.xPosition/ 10))
        PosY = int(round(robo.yPosition/ 10))
        Rad = int(round((robo.radius *2)/10))
        for i in range(0, Rad, 1):
            #print('rob ',rob)
            #print('Rad ',Rad)
            #oben
            if (SpielFeld.PlayFieldAR[PosX + i][PosY-1] == 1) & (robo.v_Y<0):
                robo.v = 0
                #print('up')
            #unten
            if (SpielFeld.PlayFieldAR[PosX + i][PosY + Rad] == 1) & (robo.v_Y>0):
                robo.v = 0
                #print('down')
            #links
            if (SpielFeld.PlayFieldAR[PosX - 1][PosY + i] == 1) & (robo.v_X<0):
                robo.v = 0
                #print('left')
            #rechts
            if (SpielFeld.PlayFieldAR[PosX + Rad][PosY + i] == 1) & (robo.v_X>0):
                robo.v = 0
                #print('right')

```

**Roboterkoordinaten senden** </br>
Der Timer zählt jeden Tick
```python
def timerEvent(self, Event):
        self.tickCount += 1
```
Um jeden 10ten Tick die Koordinaten zu senden teilen wir den TickCount einfach durch modulo 10 </br>
```python
        if self.tickCount % 10 == 0:
            print('send Robot Pos')
```

## Roboter und Threads 
**Modifizierung der Roboterbasisklasse**
Für die spätere Ausführung der Threads in den jeweiligen Robotern, wurde die Roboterbasisklasse in eine Subklasse von der threading.Threads Klasse umgewandelt. 

```python
class BaseRobot(threading.Thread):

```
In der Spielfeld Klasse wurden die 4 Roboterinstanzen dann initialisiert.
```python
    # Roboterinstanzen
        #                     x    y    r  alph a a+  a_al al+ v v_al col
        self.Robo1 = RoboType1(400, 10, 15, 0, 0, 2, 0, 3, 0, 0, QColor(255, 0, 250))
        self.Robo2 = RoboType2(10, 900, 20, 0, 0, 2, 0, 3, 0, 0, QColor(0, 0, 250))
        self.Robo3 = RoboType3(800, 100, 25, 270, 0, 2, 0, 3, 2, 0, QColor(0, 145, 250))
        self.Robo4 = RoboType4(500, 500, 30, 225, 0, 2, 0, 4, 0, 0, QColor(245, 120, 0))

        self.Robo1.start()
        self.Robo2.start()
        self.Robo3.start()
        self.Robo4.start()

```
Zudem wurden 4 neue Klassen erstellt, die die 4 Roboter mit ihren jeweiligen Aktionen repräsentieren sollen. Die 4 Klassen sind Subklassen der Roboterbasisklasse. Jeder dieser Klassen soll eine run-Funktion enthalten, mit der die Beschleunigung der Roboter geändert wird. Um zu testen wird deren aktuelle Geschwindigkeit, wie Beschleunigung ausgegeben.
Die einzelnen RoboterTypen erben dabei von der BaseRobot class.

```python
class RoboType1(BaseRobot):
    def run(self):
        while True:
            print('Ges. ', self.v , '\n' , 'a ', self.a)
            #ToDo
```

**Erweiterung der Roboterbasisklasse**
Für die Erweiterung der Roboterbasisklasse haben wir unsere alte Version mit den neuen Attributen umgeschrieben:
```python
class BaseRobot(threading.Thread):
    
    def __init__(self, xPosition, yPosition, radius, alpha, a, a_max, a_alpha, a_alpha_max, v, v_alpha, color):
        threading.Thread.__init__(self)
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.radius = radius
        self.alpha = alpha
        self.a = a
        self.a_max = a_max
        self.a_alpha = a_alpha
        self.a_alpha_max = a_alpha_max
        self.v = v
        self.v_alpha = v_alpha
        self.color = color
```

**Roboterbewegung**
Zuerst werden mit der accelerate Methode die neuen Beschleunigungen der Roboter berechnet:<br/>
Dazu gibt es jeweils 3 Fälle zu prüfen:<br/>
1)Beschleunigung unterschreiten den Minimalwert         -> Beschleunigung wird auf das Minimum gesetzt<br/>
2)Beschleunigung befindet sich im gültigen Intervall    -> Beschleunigung wird auf den gegebenen Wert gesetzt<br/>
3)Beschleunigung überschreitet den Maximalwert          -> Beschleunigung wird auf das Maximum gesetzt<br/>
```python
    def accelerate(self, Robo, add_a, add_alpha):
        #neue Beschleunigung
        if Robo.a + add_a <= -Robo.a_max:
            Robo.a = -Robo.a_max
        elif Robo.a + add_a < Robo.a_max:
            Robo.a = add_a
        elif Robo.a + add_a >= Robo.a_max:
            Robo.a = Robo.a_max


        #neue Drehbeschleunigung
        if Robo.a_alpha + add_alpha <= -Robo.a_alpha_max:
            Robo.a_alpha = -Robo.a_alpha_max
        elif Robo.a_alpha + add_alpha < Robo.a_alpha_max:
            Robo.a_alpha = add_alpha
        elif Robo.a_alpha + add_alpha >= Robo.a_alpha_max:
            Robo.a_alpha = Robo.a_alpha_max
```

Die Roboter werden mit der moveRobo Methode bewegt.
Hierzu werden die neue Richtung aus der Drehgeschwindigkeit + Blickrichtung berechnet.
Für die neue Position des Roboters wird die Geschwindigkeit in eine x- und y-Richtung zerlegt, und aus diesen wird
dann jeweils die neue x- bzw. y-Position berechnet. <br/>
Wände und andere Roboter werden noch nicht als Hindernisse erkann, Roboter fahren also weiter auch wenn sie auf eine Wand treffen.

```python
def moveRobo(self, Robo):

        #berechne neue Lenkgeschwindigkeit
        if (Robo.v_alpha + Robo.a_alpha) < -v_alpha_Max:
            Robo.v_alpha = -v_alpha_Max
        elif (Robo.v_alpha + Robo.a_alpha) <= v_alpha_Max:
            Robo.v_alpha = (Robo.v_alpha + Robo.a_alpha)
        elif (Robo.v_alpha + Robo.a_alpha) >= v_alpha_Max:
            Robo.v_alpha = v_alpha_Max

        #Neue Richtung   
        Robo.alpha = (Robo.alpha + Robo.v_alpha) % 360

        #berechne neue Geschwindigkeit
        if (Robo.v + Robo.a) <= -vMax:
            Robo.v = -vMax
        elif (Robo.v + Robo.a) < vMax:
            Robo.v += Robo.a
        elif (Robo.v + Robo.a) >= vMax:
            Robo.v = vMax


        #X-Y Geschwindigkeit
        GesX = math.cos(math.radians(Robo.alpha)) * Robo.v
        GesY = -math.sin(math.radians(Robo.alpha)) * Robo.v

        #Neue Positiion
        Robo.xPosition += GesX 
        Robo.yPosition += GesY
```

Anschließend wir das Spielfeld mit den Robotern an ihren neuen Positionen neu gezeichnet

```python
    def drawRobo(self, Robo, br):

        br.setBrush(Robo.color)
        br.setPen(QColor(0,0,0))
        br.drawEllipse(Robo.xPosition, Robo.yPosition , 2* Robo.radius, 2*Robo.radius)

        # Berechnung der neuen xPos und yPos für die Blickausrichtung
        xPos = math.cos(math.radians(Robo.alpha)) * Robo.radius
        yPos = math.sin(math.radians(Robo.alpha)) * Robo.radius

        br.drawLine(Robo.xPosition + Robo.radius, Robo.yPosition + Robo.radius,
                    (Robo.xPosition + Robo.radius) + xPos, (Robo.yPosition + Robo.radius) - yPos)
```

Die Move bzw. Draw Methoden werden über einen Timer in regelmäßigen Abständen aufgerufen.

**Roboteraktionen**
Roboter 1:<br/>
Der Roboter fährt vor und zurück, ohne sich zu drehen
```python
class RoboType1(BaseRobot):
    def run(self):
        while True:
            #als hilfe um a und v zu sehen
            #print('Ges. ', self.v , '\n' , 'a ', self.a)
            #fährt vor und zurück(ohne drehen)
            if self.xPosition <= 400:
                SpielFeld.accelerate(self, self, 0.5, 0)
            else:
                SpielFeld.accelerate(self, self, -0.5, 0)
            time.sleep(0.2)
```

Roboter 2:<br/>
Der Roboter beschleunigt, bremst und fährt anschließend im Kreis
```python
class RoboType2(BaseRobot):
    def run(self):
            time.sleep(4*GameStep)
            SpielFeld.accelerate(self, self, -0.5, 0)
            time.sleep(1*GameStep)
            SpielFeld.accelerate(self, self, 1, 0)
            time.sleep(2*GameStep)
            SpielFeld.accelerate(self, self, 0, 1)
```

Roboter 3:<br/>
Der Roboter fährt im Kreis, abwechselnd links und rechts
```python
class RoboType3(BaseRobot):
    def run(self):
        while True:
            #lenkt nach links und rechts
            for i in range(0, 10, 1):
                SpielFeld.accelerate(self, self, 0, -1)
                time.sleep(GameStep*0.5)
            for i in range(0, 10, 1):
                SpielFeld.accelerate(self, self, 0, 2)
                time.sleep(GameStep*0.5)
```

Roboter 4:<br/>
Der Roboter fährt mit langsamen Kreisbewegungen über das Spielfeld.
```python

class RoboType4(BaseRobot):
    def run(self):
        while True:
            #Drehung + Pause
            SpielFeld.accelerate(self, self, 0, 1)
            time.sleep(GameStep*2)
            SpielFeld.accelerate(self, self, 0, -0.5)
            time.sleep(GameStep*3)
```


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
![Grid](/BlogIMG/02_Spielfeld_mit_outer_Ring.png)

Im nächsten Schritt haben wir begonnen erste Hindernisse zu platzieren.

```python
    #set Walls, set array value to 1 to place Wall
    PlayFieldAR[0][0]= 1
    PlayFieldAR[10][0]= 1
    PlayFieldAR[0][10]= 1
    PlayFieldAR[25][20]= 1
    PlayFieldAR[10][50]= 1
```

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
![Grid2](/BlogIMG/03_Final_Spielfeld.png)

**Entwurf des Roboters**
Für die Implementierung des Robotors wurde zunächst eine Klasse BaseRobot erstellt. In dieser Klasse befinden sich folgende Attribute des Roboters: die x,y Positionen, der Radius und der Alpha-Wert für die Blickrichtung. Der Roboter startet an der Position (20, 30) im Spielfeld.
```python
class BaseRobot (QWidget):
    xPosition = 20
    yPosition = 30
    radius = 15
    alpha = 45
```
Um den Robotor ins Spielfeld zu zeichnen, müssen wurde eine drawRobo Methode in der Klasse Spielfeld angefertigt. Damit die Positionsänderungen des Robotors im Spielfeld erkennbar sind, wurde auf die self.update() Methode zurückgegriffen.
```python
   def drawRobo(self, br):

        br.setBrush(QColor(255, 0, 0))
        br.drawEllipse(BaseRobot.xPosition, BaseRobot.yPosition, 2* BaseRobot.radius, 2*BaseRobot.radius)

        self.update()
```
Für die selbständige Bewegung des Roboters im Feld haben wir dazu einen timer genutzt. In timer Event soll sich der Robotor je nach Blickrichtung bzw. Alpha-Wert der Robotor in verschiedenen Richtungen fortbewegen. Bewegt er sich jedoch auserhalb des Spielfeldes soll der timer stoppen.

```python
    def timerEvent(self, event):
        screen = QDesktopWidget().screenGeometry()

        if (BaseRobot.xPosition == (screen.width() - (BaseRobot.radius +10))) or (BaseRobot.yPosition == (screen.height() -         (BaseRobot.radius + 10))):
            self.timer.stop()
        else:
            if BaseRobot.alpha == 0:
                self.moveUp()

            elif BaseRobot.alpha == 45:
                self.moveUp()
                self.moveRight()

            elif BaseRobot.alpha == 90:
                self.moveRight()

            elif BaseRobot.alpha == 135:
                self.moveDown()
                self.moveRight()

            elif BaseRobot.alpha == 180:
                self.moveDown()

            elif BaseRobot.alpha == 225:
                self.moveDown()
                self.moveLeft()

            elif BaseRobot.alpha == 270:
                self.moveLeft()

            elif BaseRobot.alpha == 315:
                self.moveUp()
                self.moveLeft()
```
Hier erfolgte die Steuerung des Robotors mithilfe der keypressEvent Methode. Die Tasten A und D führen hierbei Rotationsbewegen aus. Indem sie die Alpha-Werte des Roboters verändern und diese in den folgenden Methoden moveUp(), moveDown(), moveLeft() und moveRight() nutzen, bewegen sie den Robotor abhängig von dem veränderten Alpha-Wert in eine bestimmte Richtung. Dadurch sind dann auch 360° Bewegungen möglich.
```python
   def keyPressEvent(self, event):
        '''process key press'''
        key = event.key()

        if key == Qt.Key_A:
            BaseRobot.alpha = int(round((BaseRobot.alpha - 45) % 360))
            return

        elif key == Qt.Key_D:
            BaseRobot.alpha = int(round((BaseRobot.alpha + 45) %360))
            return
 ```           
 ```python           
            
    def moveUp(self):
        if SpielFeld.PlayFieldAR[int(round(BaseRobot.xPosition /10))][(int(round(BaseRobot.yPosition / 10)))-1] == 0:
            BaseRobot.yPosition -= 10

```
```python
    def moveDown(self):
        if SpielFeld.PlayFieldAR[int(round(BaseRobot.xPosition /10))][int(round((BaseRobot.yPosition / 10)))+1] == 0:
            BaseRobot.yPosition += 10
```
```python
    def moveLeft(self):
        if SpielFeld.PlayFieldAR[(int(round(BaseRobot.xPosition /10)))-1][int(round(BaseRobot.yPosition / 10))] == 0:
            BaseRobot.xPosition -= 10
```
```python
    def moveRight(self):
        if SpielFeld.PlayFieldAR[(int(round(BaseRobot.xPosition /10)))+1][int(round(BaseRobot.yPosition / 10))] == 0:
            BaseRobot.xPosition += 10
```

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

![RoboGrid](/BlogIMG/Roboter_mit_Grid.png)


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
