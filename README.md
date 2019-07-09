## Week 7 - Steuerung durch Tastatur
**Keyboard**

**Chasing Robots Shoot**

**Death Timer and Immunity**

## Week 7 - Einbauen der Bullet Class

**Code Refactoring**

Da die Menge an Elementen stark angestiegen ist, haben wir uns entschieden die Robos, den Server und dazu auch die Bullet-Klasse in separate .py Files zu packen, um unseren Code besser zu veranschaulichen.

**Bullet**
```python
Bullet_Size = 10
Bullet_Speed =5

class Bullet(object):
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


    def drawBullet(self, br):
        br.setBrush(QColor(255, 255, 250))
        br.drawEllipse(self.position.x() - (0.5 * Bullet_Size),self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)

    def moveBullet(self):
        self.position.__iadd__(self.velocity)
```
In der Bullet-Klasse befinden sich alle wichtigen Methoden, die zum Zeichnen und Bewegen des Bullets nötig sind.  Da die Wirkungsweise fast identisch zu den Robo-Methoden ist, haben wir eine ähnliche Struktur verwendet, die sich nur in Parametern und Vorbedingungen unterscheidet. Die Kugel wird mit der Geschwindigkeit und Winkel des Robos abgeschossen (danach konstant).<br/>

**Shoot methode**
```python
#in Robots
    def shoot(self):
        #StartPosition sollte um ein Offset in Blickrichtung verschoben werden
        bulletpos = QVector2D(self.position.x(),self.position.y())
        #velocity based on angle
        GesX = math.cos(math.radians(self.alpha)) * Bullet.Bullet_Speed
        GesY = - math.sin(math.radians(self.alpha)) * Bullet.Bullet_Speed
        #set Bullet to middle of Robot
        OffsetVector = QVector2D((self.radius + Bullet.Bullet_Size)/2,(self.radius + Bullet.Bullet_Size)/2)
        bulletpos.__iadd__(OffsetVector)
        #set bullet to edge in firing direction
        OffsetX = math.cos(math.radians(self.alpha)) * (self.radius + 6)
        OffsetY = - math.sin(math.radians(self.alpha)) * (self.radius + 6)
        OffsetVector = QVector2D(OffsetX,OffsetY)
        bulletpos.__iadd__(OffsetVector)
        Vel = QVector2D(GesX,GesY)
        Vel.__iadd__(self.v_vector)
        Bullet1 = Bullet.Bullet(bulletpos, Vel)
        self.BulList.append(Bullet1)
        #print(self.BulList)

```
Wenn ein Roboter einen Schuss abfeuert werden aus dessen momentanen Koordinaten, Blickrichtung und Geschwindigkeit der entsprechende Geschwindigkeitsvektor des Projektils und dessen Starposition berechnet. </br>


**Bullet List**
```python
class SpielFeld(QWidget):

    #Array construction
    PlayFieldAR = [[0 for x in range(100)] for y in range(100)]
    BarrierList = []
    Bullets = []
    ...
```

```python
class Robot(object):
    def __init__(self, robotid, position, alpha, a_max, a_alpha_max, radius, FOV, color):
    ...
        self.BulList= []
    ...
```

```python
    #in SpielFeld
    def fetchBullets(self,Robot):
        SpielFeld.Bullets.extend(Robot.BulList)
        #print(SpielFeld.Bullets)
        Robot.BulList.clear()
```
```python
    #in Timer
        # move robots on the game field
        for robot in self.robots:
            self.fetchBullets(robot)
            self.moveRobot(robot)
            self.barrierCollision(robot)
            self.roboCollision(robot, self.robots[0])
            self.SightingData(robot)
            
```
Um zu verfolgen welche Bullets sich gerade auf dem Spielfeld befinden, erstellen wir eine Liste, die alle Bulletinformationen abspeichert. Wenn eine Bullet im Spielfeld abgefeuert wird, wird diese in die Liste appended. Dazu verfügt jeder Roboter über eine eigene BulletList, welche in jedem Takt vom Server gefetched wird. Trifft eine Bullet einen anderen Robo oder eine Wand, so verschwindet die und wird auch aus der Liste gelöscht.<br/>
```python
    #in Timer
            for bul in SpielFeld.Bullets:
                bul.moveBullet()
                if self.BulletBarrierCollision(bul):
                    SpielFeld.Bullets.remove(bul)
                elif bul.one_hit(robot):
                    #robot.color = colors["yellow"]
                    self.teleport_bullet(robot)
                    SpielFeld.Bullets.remove(bul)
```
Wenn ein Bullet auf einen Roboter trifft, wird dieser Roboter auf eine andere Position transportiert und die Kugel von dem Spielfeld gelöscht. Mithilfe der Funktion on_hit() wird eine True oder ein False ausgegeben, dass anzeigt, ob eine Kugel auf dem Roboter trifft.

```python

    def one_hit(self, robo):
        if self.bulletShape().intersects(robo.roboShape()):
            return True
        else: return False
```
Für den Anfang haben wir uns einen Teleportposition selbst ausgesucht, an denen die getroffenen Robotern spawnen.

```python
    def teleport_bullet(self, robo):
        robo.position = QVector2D(100,850)
```

**Bullet Barrier Collision**

```python
    def BulletBarrierCollision(self, bullet):
        #Collision with Obstacles
        PosX = int(round(bullet.position.x()/ 10))
        PosY = int(round(bullet.position.y()/ 10))
        #oben
        if (SpielFeld.PlayFieldAR[PosX][PosY-1] == 1):
            return True
        #unten
        if (SpielFeld.PlayFieldAR[PosX][PosY + 1] == 1):
            return True
        #links
        if (SpielFeld.PlayFieldAR[PosX - 1][PosY] == 1):
            return True
        #rechts
        if (SpielFeld.PlayFieldAR[PosX + 1][PosY] == 1):
            return True
        return False
```

=======
## Week 6 - Field of View der Roboter

Wir haben uns zuerst entschieden unsere Code so zu ändern, so dass der Server den größeren Teil der Roboterbefehle übernimmt (Da vorher alles auf der Spielfeldklasse vorkam). Wir haben auch die X/Y Koordinaten der Roboter in QVector2D-Form gebracht.
```python
#Runner
Robot1 = RoboTypeRun(1, QVector2D(50,110), 300, 2, 2, 15, 40 ,PINK)
#Chasers
Robot2 = RoboTypeChase1(2, QVector2D(70,200), 0, 2, 2, 15, 50,DARKBLUE)
Robot3 = RoboTypeChase2(3, QVector2D(400,460), 240, 2, 2, 15, 60,LIGHTBLUE)
Robot4 = RoboTypeChase3(4, QVector2D(400,430), 30, 2, 2, 15, 85,ORANGE)

self.robots = [Robot1, Robot2, Robot3, Robot4]
```
Im Timer-Event werden die Parameter der Roboter jetzt in 10 Ticks auf diese Weise weitergegeben:
```python
if self.tickCount % 10 == 0:
    for y in self.robots:
        #print position List of Robots
        #print(int(round(self.RobotList[robot.robotid].x())), '---', int(round(self.RobotList[robot.robotid].y())))
        #robot.RoboList = self.RobotList.copy()
        for x in self.robots:
            y.RobotList[x.robotid] = x.position
```
Unsere Roboter werden durch ein Dictionary gekennzeichnet:
```python
self.RobotList = {1 : QVector2D(0,0),
                  2 : QVector2D(0,0),
                  3 : QVector2D(0,0),
                  4 : QVector2D(0,0)}
```
Um das Sichtfeld besser darzustellen, haben wir in drawRobo die dazugehörigen Linien des FOV implementiert:
```python
#draw FOV
        if VISUALS:
            br.setPen(QColor(255,255,255))
            xPos = math.cos(math.radians(Robo.alpha + (Robo.FOV/2))) * Robo.radius
            yPos = math.sin(math.radians(Robo.alpha + (Robo.FOV/2))) * Robo.radius
            br.drawLine(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius,
                       (int(round(Robo.position.x())) + Robo.radius) + 10*xPos, (int(round(Robo.position.y())) + Robo.radius) - 10*yPos)
            xPos = math.cos(math.radians(Robo.alpha - (Robo.FOV/2))) * Robo.radius
            yPos = math.sin(math.radians(Robo.alpha - (Robo.FOV/2))) * Robo.radius
            br.drawLine(int(round(Robo.position.x())) + Robo.radius, int(round(Robo.position.y())) + Robo.radius,
                       (int(round(Robo.position.x())) + Robo.radius) + 10*xPos, (int(round(Robo.position.y())) + Robo.radius) - 10*yPos)
```

Zunächst suchten wir eine Idee, wie wir überhaupt prüfen können, ob sich andere Objekte im Sichtfeld befinden.

## Week 6  - Geschwindigkeitsvektor Update

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
    def collision(self, robo, target):
        for robot in self.robots:
            if robot != robo and robot != target and robo != target :
                distance = self.distanceTwoPoints(int(round(robot.position.x())) + robot.radius,
                                                  int(round(robot.position.y()))+ robot.radius,
                                                  int(round(robo.position.x())) + robo.radius,
                                                  int(round(robo.position.y())) + robo.radius)


                if self.is_overlapping(int(round(robot.position.x())) + robot.radius, int(round(robot.position.y())) + robot.radius, robot.radius,
                                       int(round(robo.position.x())) + robo.radius, int(round(robo.position.y()))+ robo.radius,
                                       robo.radius) and distance < robot.radius + robo.radius :

                    # with elastic collision, does not apply to the reality because of spin, friction etc.
                    # our only concern is the mass of the robots
                    # new velocity of robo1
                    newVelX1 = (int(round(robo.v_vector.x())) * (robo.mass - robot.mass) + (2 * robot.mass * int(round(robot.v_vector.x())))) / (
                            robo.mass + robot.mass)
                    newVelY1 = (int(round(robo.v_vector.y()))* (robo.mass - robot.mass) + (2 * robot.mass * int(round(robot.v_vector.y())))) / (
                            robo.mass + robot.mass)

                    # new velocity of robo2
                    newVelX2 = (int(round(robot.v_vector.x())) * (robot.mass - robo.mass) + (2 * robo.mass * int(round(robo.v_vector.x())))) / (
                            robo.mass + robot.mass)
                    newVelY2 = (int(round(robot.v_vector.y())) * (robot.mass - robo.mass) + (2 * robo.mass * int(round(robo.v_vector.y())))) / (
                            robo.mass + robot.mass)

                    newV_1 = QVector2D(newVelX1, newVelY1)
                    newV_2 = QVector2D(newVelX2, newVelY2)

                    robo.position.__iadd__(newV_1)

                    robot.position.__iadd__(newV_2)

            else: self.teleport(target, robo)
```
Es werden die neuen Geschwindigkeiten ausgerechnet, um die neue Position der Roboter zu berechnen. Wenn z.B. beide in entegengesetze Richtungen sich bewegen und kollidieren, würden sich dessen Geschwindigkeiten in dem Moment aufheben (wenn beide Massen auch gleich sind).

**Teleport**
```python             
    def teleport(self, target, robot):

        if robot != target:
            distance = self.distanceTwoPoints(int(round(robot.position.x())) + robot.radius,
                                              int(round(robot.position.y())) + robot.radius,
                                              int(round(target.position.x())) + target.radius,
                                              int(round(target.position.y())) + target.radius)

            if distance <= target.radius + robot.radius:

                if  int(round(target.position.x())) > 500 and  int(round(target.position.y())) < 500:

                    robot.position = QVector2D(100,850)

                elif int(round(target.position.x())) > 500 and int(round(target.position.y())) > 500:
                    robot.position = QVector2D(100,100)

                elif int(round(target.position.x())) < 500 and int(round(target.position.y())) < 500:
                    robot.position = QVector2D(850,850)


                elif int(round(target.position.x())) < 500 and int(round(target.position.y())) > 500:
                    robot.position = QVector2D(850,100)
```
Hier werden die Roboter je nach auftreffen mit dem Target in eine bestimmte Position des Spielfelds teleportiert. Das Spielfeld wird dabei in 4 Quadranten unterteilt. Treffen sich Chaser und Target im Quadranten links unten, dann wird der Chaser in das Quadrant rechts oben teleportiert. Dabei wurden bestimmte Positionen in den jeweiligen Quadranten festgelegt.

**Steuerungs Methoden** 
```python             
 #brings Rotation to a halt
    def Stabilize(self):
        while self.v_alpha != 0:
            if self.v_alpha > 0:
                self.a_alpha = -0.5
            elif self.v_alpha < 0:
                self.a_alpha = 0.5
        self.a_alpha=0

    def ReStart(self):
            if self.v_vector.x() == self.v_vector.y() == 0:
                self.a_alpha= 0.7
                time.sleep(GameStep)
                self.a=1
                self.Stabilize()

    def velocity(self):
        return math.sqrt(math.pow(self.v_vector.x(),2) + math.pow(self.v_vector.y(),2))
```


**Flüchtender Roboter** 
```python             
class RoboTypeRun(BaseRobot):  
    def run(self):
        while True:
            self.a = 1
            time.sleep(GameStep)
            for ID in range(2, 5,1):
                if self.position.distanceToPoint(self.RobotList[ID]) < 150:
                    #check where Chaser is
                    self.checkChase(ID)
                    time.sleep(0.5)
                    self.Stabilize()
            self.ReStart()
```
**Die CheckChase Methode**

Diese Methode prüft wo der Verfolger ist, und in welche Richtung gelenkt werden muss 
```python             
    def checkChase(self, ID):
        xEnemy = self.RobotList[ID].x()
        yEnemy = self.RobotList[ID].y()

        xSelf = self.position.x()
        ySelf = self.position.y()

        spot = ''
        action =''

        #search position of enemy
        if xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'TopLeft'
        elif xEnemy >= xSelf and yEnemy <= ySelf:
            spot = 'TopRight'
        elif xEnemy <= xSelf and yEnemy >= ySelf:
            spot = 'BotLeft'
        elif xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'BotRight'

        #check direktion (rough)
        #right -> 0° up -> 90° left -> 180° down -> 270°
        view = ''

        if  0 <= self.alpha <= 90:
            view = 'TopRight'
        elif 90 <= self.alpha <= 180:
            view = 'TopLeft'
        elif 180 <= self.alpha <= 270:
            view = 'BotLeft'
        elif 270 <= self.alpha <= 360:
            view = 'BotRight'

        #determin turn-type
        if view == spot:
            #hard Turn
            action = 'hard Turn'
        elif (view == 'TopRight' and spot == 'BotLeft') or (view == 'TopLeft' and spot == 'TopRight') or (view == 'BotRight' and spot == 'TopLeft') or (view == 'BotLeft' and spot == 'TopRight'):
            #no turn
            action = 'no Turn'
        elif (view == 'TopRight' and spot == 'TopLeft') or (view == 'BotRight' and spot == 'TopRight') or (view == 'BotLeft' and spot == 'BotRight') or (view == 'TopLeft' and spot == 'BotLeft'):
            #right turn
            action = 'right Turn'
        else:
            #left turn
            action = 'left Turn'

        print(action)
        
        if action == 'hard Turn':
            self.a_alpha = 2
        elif action == 'no Turn':
            self.a_alpha = 0
        elif action == 'left Turn':
            self.a_alpha = 0.7
        elif action == 'right Turn':
            self.a_alpha = -0.7
```

**Verfolgender Roboter 1**
```python             
    def run(self):
        while True:
            self.a = 1
            time.sleep(GameStep)
            if self.position.distanceToPoint(self.RobotList[1]) < 250:
                #check where Chaser is
                self.lookTarget(1)
                time.sleep(0.5)
                self.Stabilize()
            self.ReStart()
```

**Die LookTarget Methode** 

Diese Methode prüft wo der Verfolger ist, und in welche Richtung gelenkt werden muss 
```python             
    def lookTarget(self, ID):
        #Based on check Chase Method

        xEnemy = self.RobotList[ID].x()
        yEnemy = self.RobotList[ID].y()

        xSelf = self.position.x()
        ySelf = self.position.y()

        spot = ''
        action =''
        #search position of enemy
        if xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'TopLeft'
        elif xEnemy >= xSelf and yEnemy <= ySelf:
            spot = 'TopRight'
        elif xEnemy <= xSelf and yEnemy >= ySelf:
            spot = 'BotLeft'
        elif xEnemy <= xSelf and yEnemy <= ySelf:
            spot = 'BotRight'

        #check direktion (rough)
        #right -> 0° up -> 90° left -> 180° down -> 270°
        view = ''

        if  0 <= self.alpha <= 90:
            view = 'TopRight'
        elif 90 <= self.alpha <= 180:
            view = 'TopLeft'
        elif 180 <= self.alpha <= 270:
            view = 'BotLeft'
        elif 270 <= self.alpha <= 360:
            view = 'BotRight'

        #determin turn-type
        if view == spot:
            #hard Turn
            action = 'no Turn'
        elif (view == 'TopRight' and spot == 'BotLeft') or (view == 'TopLeft' and spot == 'TopRight') or (view == 'BotRight' and spot == 'TopLeft') or (view == 'BotLeft' and spot == 'TopRight'):
            #no turn
            action = 'hard Turn'
        elif (view == 'TopRight' and spot == 'TopLeft') or (view == 'BotRight' and spot == 'TopRight') or (view == 'BotLeft' and spot == 'BotRight') or (view == 'TopLeft' and spot == 'BotLeft'):
            #left turn
            action = 'left Turn'
        else:
            #right turn
            action = 'right Turn'

        print(action)
        
        if action == 'hard Turn':
            self.a_alpha = 2
        elif action == 'no Turn':
            self.a_alpha = 0
        elif action == 'left Turn':
            self.a_alpha = 0.7
        elif action == 'right Turn':
            self.a_alpha = -0.7
```

## Week 5 - Interaktionen zwischen Server und Roboterklasse

**Collision** 

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
                
        self.moveAgain(robo)

def moveAgain(self, robo):
    if robo.v == 0:
        robo.alpha = robo.alpha +180
        
    robo.v += 0.1                

```
Nachdem der Robote ein obstacle wahrgenommen hat, wurde die Geschwindigkeit v auf null gesetzt. Um den Roboter wieder fahren zu lassen, aber wir eine einfache Funktion moveAgain() entworden, die bei einer Geschwindigkeit von null den Roboter um 180° drehen und langsam wieder an Geschwindigkeit zu nehmen soll.


**Roboterkoordinaten senden** 

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

Wir haben die Roboterclass um ein weiteres Attribut erweitert welches eine Liste mit den RoboterPositionen enthält. </br>
In jedem Tick werden in die Liste die neuen Positionen aller Roboter eingefügt, jedem zehnten Tick wird die Liste an die Roboter übergeben.
```python
        self.RobotList=[]
        for robot in self.robots:
            self.RobotList.append ([robot.xPosition, robot.yPosition])

        if self.tickCount % 10 == 0:
            #print('send Robot Pos')
            for robot in self.robots:
                robot.RoboList = self.RobotList
```

## Week 4 - Roboter und Threads 

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


## Week 3 - Roboter im Spielfeld
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
![Grid](/BlogIMG/02_Spielfeld_mit_outer_Ring.png)

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
**Steuerung mit keypressEvent**

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


## Week 2 - Chessboard 
**drawBlock methode:**
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
