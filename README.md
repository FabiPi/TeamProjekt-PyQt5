## Week 9 - Zusatzfeatures und Finalisierung des Programms
**Menu**<br/>
Um unser Spielfeld ein bisschen aufzufrischen, haben wir uns entschieden ein Menu zu konstruieren. Dabei haben wir vor allem mit QWidget gearbeitet, um neue Fenster bzw. windows zu kreiieren. Unser Konzept basiert auf der Idee ein start screen, ein start menu einzuführen. In dem start menu kann man dann mithilfe von verschiedenen Buttons verschiedene Aktionen durchführen. Wir haben einmal einen Button start Game, options, instruction bzw. how to play, credits und einen quite Button. 
Zunächst wurde den die Konstuktionen von oben unabhängig vom GameBoard erstellt.

Für den start screen haben wir uns zunächst einfach ein neues QWidget geschaffen:
```python
class Game (QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(800, 336)
        Server.center(self)
        self.setWindowTitle("Welcome")

        self.enter = QPushButton("enter", self)
        self.enter.move(360,280)
        self.enter.resize(80, 25)
        self.enter.clicked.connect(self.gameMenu)
        self.enter.setStyleSheet("background-color: rgb(240,255,255); font: bold 15px; color: black;")

        self.show()

    def gameMenu(self):
        self.startM = start_Menu()
        self.close()
        
```
Dieses window besitzt einen Button mit dem man das start menu betreten kann. Nach betreten des start menu soll sich dann das window schließe, welches wir mithilfe von self.close() erzielt haben.

Als nächstes haben wir uns dem start menu gewidmet. Auch hier haben wir ein neues window geschaffen, dass die nötigen Buttons zur Weiterleitung besitzt.

```python
class start_Menu(QWidget):

    WIDTH = 500
    HEIGHT = 666

    XPosStart = 70
    YPosStart = 60

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Start Menu')
        Server.center(self)

        # switch to gameboard
        self.button1 = QPushButton('Start Game', self)
        self.button1.move(self.XPosStart, self.YPosStart)
        self.button1.clicked.connect(self.startGame)

        # switch to options
        self.button2 = QPushButton('Options', self)
        self.button2.clicked.connect(self.Options)
        self.button2.move(self.XPosStart, 2 * self.YPosStart)

        # switch to howtoplay
        self.button3 = QPushButton('How to Play', self)
        self.button3.clicked.connect(self.How2Play)
        self.button3.move(self.XPosStart, 3 * self.YPosStart)

        # switch to credits
        self.button4 = QPushButton('Credits', self)
        self.button4.clicked.connect(self.Credits)
        self.button4.move(self.XPosStart, 4 * self.YPosStart)

        # quite game
        self.button5 = QPushButton('Quit', self)
        self.button5.clicked.connect(self.close)
        self.button5.move(self.XPosStart, 5 * self.YPosStart)
        
        self.show()
        
    def Instance(self):
        self.gBoard = Server.SpielFeld()
        return self.gBoard

    def startGame(self):
        self.Instance().start()
        self.close()

    def Options(self):
        self.opt = OptionField()
        self.close()

    def How2Play(self):
        self.instructions = How2PlayText()
        self.close()

    def Credits(self):
        self.authors = CreditText()
        self.close()

    def closeEvent(self, event):
        self.close()

    def Back2Menu(self):
        self.sMenu = start_Menu()
        self.close()

```

Hier ist das erste Mal gewesen, dass wir eine Verbindung zum GameBoard erstellt haben, indem wir es mithilfe der Methode startGame eine Instanze aufrufen.

Im weiteren Schritt wurden, dann ganz ähnlich auch die windows für option, how to play, credits geschaffen. Die alle mit einem back Button ausgestattet sind. 

```python

class OptionField(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUI()

    def InitUI(self):
        self.resize(800, 500)
        self.setWindowTitle('Options')
        Server.center(self)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(200, 450)

        self.show()
        
    def Back2Menu(self):
            start_Menu.Back2Menu(self)
```
```python 
class CreditText(QWidget):

    def __init__(self):
        super(CreditText, self).__init__()

        self.initUI()

    def initUI(self):
        self.resize(self.image.width(), self.image.height())
        self.setWindowTitle('Credits')
        Server.center(self)

        self.back = QPushButton('back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(350,330)

        self.show()

    def Back2Menu(self):
            start_Menu.Back2Menu(self)
```           

```python 
class How2PlayText(QWidget):

    def __init__(self):
        super(How2PlayText, self).__init__()

        self.initUI()

    def initUI(self):
        self.resize(self.image.width(), self.image.height())
        self.setWindowTitle('How to Play')
        Server.center(self)

        self.back = QPushButton('back', self)
        self.back.clicked.connect(self.Back2Menu)
        self.back.move(350,330)

        self.show()

    def Back2Menu(self):
            start_Menu.Back2Menu(self)
``` 

Nachdem sozusagen das Grundgerüst fertig war, haben wir uns an die Detail Aufgaben gekümmert. Zunächst war es die Idee, ein pause menu im Spiel zu schaffen, mit dem man dann bestimmte Interaktion durchführen konnte. Nach vielen Versuchen, haben wir die Idee dann aufgeben muss, da es uns ansonsten zeitlich nicht gereicht hätte. 

Als Ersatz haben wir dann im Spiel das pause menu durch ein pause message box geändert. In anderen Worten, mit der Taste P kann man während des Spiel pausieren. Man wird dann gefragt, ob man das Spiel beenden oder fortsetzen möchte.

```python

    def keyPressEvent(self, event):
        if not self.isStarted:
            super(SpielFeld, self).keyPressEvent(event)
            return

        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_P:
                self.pause()
                return

        else:
            super(SpielFeld, self).keyPressEvent(event)

    def Message(self):
        msgBox = QMessageBox()

        msgBox.setWindowTitle("Pause Screen")
        msgBox.setIconPixmap(QPixmap('textures/Board/pauseEmoji.png'))
        msgBox.setText("Your in the pause screen. \n Do you want to continue? \n")

        # set Buttons
        msgBox.addButton(QMessageBox.Yes)
        msgBox.addButton(QMessageBox.No)

        # change backgroundstyle
        p = self.palette()
        p.setColor(self.backgroundRole(), colors["white smoke"])
        msgBox.setPalette(p)
        msgBox.exec_()

        return msgBox

    def pause(self):

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        print(self.isPaused)

        if self.isPaused:
            self.timer.stop()

            # switch to pause screen
            self.msgBox = self.Message().result()
            if self.msgBox == QMessageBox.No:
                self.startMenu = Menu.start_Menu()
                self.close()
            else:
                self.isPaused = False
                self.timer.start(FPS, self)
        else:
            self.timer.start(FPS, self)

        self.update()
```
Das Prinzip vom pausieren haben wir uns vom Tutorial Tetris abgeschaut, falls da Detailfragen bestehen, siehe http://zetcode.com/tutorials/javagamestutorial/tetris/. 

Als nächsten großen Schritt wollten wir in den Optionen die Texturen im Spiel verändern. Dazu mussten wir erstmal uns überlegen wie genau wir das machen wollen. Für die Präsentation an den Spieler haben wir uns für eine tab-Darstellung entschieden, um eine weites Spektrum an Option da zu bieten. Letzten Endes haben wir uns für eine Grafik und Game Tab entschieden. Dazu haben wir eine neue Klasse TableWidget geschaffen. 

```python

class TableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Game")
        self.tabs.addTab(self.tab2, "Graphic")

        # Create game tab
        self.tab1.layout = QHBoxLayout()

        self.gameG = Spellcards()
        self.bulG = BulletCol()

        # add new content to tab1
        self.tab1.layout.addWidget(self.bulG)
        self.tab1.layout.addWidget(self.gameG)

        self.tab1.setLayout(self.tab1.layout)


        # create content grafic tab
        self.tab2.layout = QHBoxLayout()

        # add wallG to tab3
        self.wallG = wallTexture()
        self.tab2.layout.addWidget(self.wallG)


        # add floorG to tab3
        self.floorG = floorTexture()
        self.tab2.layout.addWidget(self.floorG)

        # add all layouts to tab3
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

```
Für jeden Tab wurde ein Layout geschaffen und in diesem Layout wurde dann mithilfe von QGroupBox die Auswahlbuttons erzeugt. 
Man kann sagen, dass es eine sehr vielschichtige Arbeit war.

Anhand eines Beispiel können wir das Prinzip von der Texturenänderung demonstrieren. Als Beispiel fangen wir mit dem wall textures an.

```python

class wallTexture(QWidget):
    def __init__(self):
        super().__init__()

        # set wall texture layout
        self.wallG = QGroupBox(self)

        # set button layout
        self.button_layout1 = QVBoxLayout()

        # create buttons
        self.texture1 = QRadioButton("Metall wall")
        self.texture2 = QRadioButton("Red wall")
        self.texture3 = QRadioButton("Mosaik wall")

        self.btn = QPushButton("Select")
        self.btn.setStyleSheet('background-color: white')

        self.currentRBtn = self.texture1

        self.label = QLabel(self)

        # change style of lettering
        self.style = QFont()
        self.style.setBold(True)
        self.label.setFont(self.style)

        self.chk_RBtn()

        self.iniUt()

    def iniUt(self):

        self.wallG.setTitle("Texture Wall")

        # adjust icons on buttons
        self.texture1.setIcon(QIcon(Server.wallTextures["Metall wall"]))
        self.texture2.setIcon(QIcon(Server.wallTextures["Red wall"]))
        self.texture3.setIcon(QIcon(Server.wallTextures["Mosaik wall"]))

        self.button_layout1.addWidget(self.texture1)
        self.button_layout1.addWidget(self.texture2)
        self.button_layout1.addWidget(self.texture3)
        self.button_layout1.addWidget(self.btn)
        self.button_layout1.addWidget(self.label)

        # add button layout in wall layout
        self.wallG.setLayout(self.button_layout1)

        # set wall texture box semi-transparent
        self.wallG.setStyleSheet('background-color: rgba(255, 255, 255, 0.5);')

        # click buttons
        self.texture1.clicked.connect(lambda: self.currBtn_clk(self.texture1))
        self.texture2.clicked.connect(lambda: self.currBtn_clk(self.texture2))
        self.texture3.clicked.connect(lambda: self.currBtn_clk(self.texture3))


        self.btn.clicked.connect(lambda: self.btn_clk(self.currentRBtn))


    # show new setting, after returing to options
    def chk_RBtn(self):
        global CurWall

        self.texture2.setChecked(False)
        self.texture3.setChecked(False)
        self.texture3.setChecked(False)

        if CurWall == "Metall wall":
            self.texture1.setChecked(True)


        elif CurWall == "Red wall":
            self.texture2.setChecked(True)

        elif CurWall == "Mosaik wall":
            self.texture3.setChecked(True)

        else:
            self.texture1.setChecked(True)

        self.label.setText('currently used\n' + CurWall)
        self.label.update()


    def currBtn_clk(self, button):
        self.currentRBtn = button


    def btn_clk(self, button):
        global CurWall
        print(button.text() + ' clicked')

        if button == self.texture1:
            Server.wtexture = "Metall wall"
            CurWall = "Metall wall"

        elif button == self.texture2:
            Server.wtexture = "Red wall"
            CurWall = "Red wall"

        elif button == self.texture3:
            Server.wtexture = "Mosaik wall"
            CurWall = "Mosaik wall"
        else:
            pass

        self.label.setText("You selected: \n" + button.text())
        QtGui.QGuiApplication.processEvents()
```
Da QGroupbox keine Widgets aufnimmt, musste zunächst ein neues Layout für die Buttons geschaffen werden. Danach haben wir den Buttons zugeordnet, dass bei einem Klick wir ein Signal bekommen, um zu erfassen, welcher Button unser aktueller Button ist. 
Dafür haben wir die Methode currBtn_clk implementiert. Als nächstes wollen wir mit dem Signal schauen, welche texture ausgewählt worden ist, dazu haben wir dann btn_clk implementiert. Diese Methode gibt dann ein Signal in Form einer Variable an das GameBoard weiter. 
```python

# selected wall texture
wtexture = "Metall wall"
```

Im GameBoard haben wir dann eine library erzeugt und eine Methode geschrieben, die die Textur ändert.

```python
    def changeWall(self, name):

        if name == "Metall wall":
            Menu.CurWall = "Metall wall"
            return QPixmap(wallTextures["Metall wall"])

        elif name == "Red wall":
            Menu.CurWall = "Red wall"
            return QPixmap(wallTextures["Red wall"])

        elif name == "Mosaik wall":
            Menu.CurWall = "Mosaik wall"
            return QPixmap(wallTextures["Mosaik wall"])
        else:
            pass
```
Diese gibt verändert eine andere Variabel aus der Menu Klasse, um die gewählt Einstellung zu speichern und bei erneutem Betreten in die Optionenn anzuzeigen.

Nach diesem Prinzip haben wir es für die floor texturen, bullet-wall collision und spellcards gemacht.

Im nächsten Schritt haben wir an der Optik gearbeitet. Für den start screen und start menu haben wir dann ein animierte gif eingesetzt, die sich gut ergänzt haben.  Für die gifs haben wir mithilfe von https://wiki.python.org/moin/PyQt/Movie%20splash%20screen eine painter Methode geschaffen.

Dafür haben wir mit QMovie gearbeitet:

```python

class Game (QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(800, 336)
        Server.center(self)
        self.setWindowTitle("Welcome")

        self.enter = QPushButton("enter", self)
        self.enter.move(360,280)
        self.enter.resize(80, 25)
        self.enter.clicked.connect(self.gameMenu)
        self.enter.setStyleSheet("background-color: rgb(240,255,255); font: bold 15px; color: black;")

        # create background animated gif
        self.movie = QMovie("textures/Background/Red.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        # select the music track
        pygame.mixer.music.load(playlist["Track 5"])
        # loops the music
        pygame.mixer.music.play(-1, 0.0)

        self.show()


    def gameMenu(self):
        self.startM = start_Menu()
        self.movie.stop()
        self.close()

    def paintEvent(self, event):
        # after every changed image, refresh the background with the currentPixmap
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)
```

Im weiteren haben wir dann noch einen Sound eingebaut mithilfe von pygame, welches installiert werden muss. Aber damit kann man dann schöne Schleifen machen.

Zum Schluss haben wir dann noch die anderen windows mit Details gefüllt.


**Spellcards**<br/>
Um die "Spellcards" oder "Spezialfähigkeiten" der Roboter zu implementieren haben wir uns zuerst überlegt, wie man die Bullet-Class die erweitern muss um andere Typen von Schüssen zu realisieren. <br/>
```python
class Bullet(object):
    #add Attributes
    #-Direction (alhpa)
    #-Velocity (non vector)
    #-type
    #-time
    #-owner
    def __init__(self, position, speed, alpha, time, delay, bulType, owner):
        self.position = position
        self.speed = speed
        self.alpha = alpha
        self.bulType = bulType
        self.time = time
        self.delay = delay
        self.owner = owner
        self.BulletTextures = {0:QPixmap('textures/Bullets/Standart.png'), #Standart
                               #Spellcard1
                               1:QPixmap('textures/Bullets/GreenOrb.png'), #Green 1
                               2:QPixmap('textures/Bullets/BlueOrb.png'), #Blue 1
                               3:QPixmap('textures/Bullets/RedOrb.png'), #Red
                               4:QPixmap('textures/Bullets/GreenOrb.png'), #Green 2
                               5:QPixmap('textures/Bullets/BlueOrb.png'), #Blue 2
                               #Spellcard2
                               6:QPixmap('textures/Bullets/GreenOrb.png'), #GreenOrb
                               7:QPixmap('textures/Bullets/BlueOrb.png'), #BlueOrb
                               8:QPixmap('textures/Bullets/Star01.png'), #Star1
                               9:QPixmap('textures/Bullets/Star02.png'), #Star2
                               10:QPixmap('textures/Bullets/Star03.png'), #Star3
                               11:QPixmap('textures/Bullets/Star04.png'), #Star4
                               ...
                               }

```
Wir haben die Class so erweitert, dass sie nun auch Attribute für: eine Richtung, die Geschwindigkeit (nicht als Vektor), eine Lebensdauer, einen Besitzer und einen Typ hat (Später wurde auch noch ein Delay eingefügt welcher hilft Bullets verzögert zu starten). <br/>
Auch die Robot-Class wurde um ein Attribut, ein "Cool Down", erweitert, welcher ähnlich wie die "reload-time" von shoot funktioniert, nur auf die Spellcards bezogen.
<br/>
Die eigentliche Implementation der Spellcards findet in 2 Schritten statt, einmal die initiale Erstellung der Bullets in der Robot-Class, und einmal in der Move-Bullet-Methode der Bullet-Class um die Bullets entsprechend zu bewegen.
<br/>
Zuerst aber haben wir einmal die Shoot Methode der Roboter in eine Create-Bullet und Shoot Methode unterteilt, um auch außerhalb von Shoot auf die Erstellung einer Bullet zugreifen zu können.
<br/>
```python
#in Robot-Class

def shoot(self):
        #Values
        LifeTime = 100
        
        if self.reload == 0 and self.deathTime == 0:
            Bullet1 = self.createBullet(0,LifeTime, 0, self.alpha, self.v,0,0)

            self.BulList.append(Bullet1)
            self.reload = RELOAD_TIME
...
def createBullet(self, bulletType, life, delayT, alpha, addSpeed, offset, target):
        
        #Position
        bulletpos = QVector2D(self.position.x(),self.position.y())
        #velocity
        speed = Bullet.Bullet_Speed + addSpeed
        #velocity based on angle
        GesX = math.cos(math.radians(alpha)) * speed
        GesY = - math.sin(math.radians(alpha)) * speed
        #set Bullet to middle of Robot
        OffsetVector = QVector2D((self.radius-2)/2,(self.radius-2)/2)
        bulletpos.__iadd__(OffsetVector)
        #set bullet to edge in firing direction
        OffsetX = math.cos(math.radians(alpha)) * (self.radius + offset)
        OffsetY = - math.sin(math.radians(alpha)) * (self.radius + offset)
        OffsetVector = QVector2D(OffsetX,OffsetY)
        bulletpos.__iadd__(OffsetVector)

        if target != 0:
            #Calculate Target Alpha
            target_x = target.x()
            target_y = target.y()

            pos_x = bulletpos.x()
            pos_y = bulletpos.y()


            #Berechnung Blickrichtung
            delta_x = target_x - pos_x
            delta_y = target_y - pos_y
            target_alpha = -math.degrees(math.atan2(delta_y, delta_x)) % 360

        else:
            target_alpha = alpha

        #create Bullet
        Bullet1 = Bullet.Bullet(bulletpos, speed, target_alpha, life, delayT, bulletType, self.robotid)
        return Bullet1
```
<br/>
Die Shoot-Methode ruft nun einfach die createBullet-Methode auf um eine Standart Bullet zu erschaffen.
<br/>
Die createBulletMethode hat nun auch ein paar neue Parameter erhalten, um die neuen Attribute der Bullets korrekt zu setzen.
bulletType, life, delayT sind dabei recht selbsterklärend und geben den Typ, die Lebensdauer und den Delay der Bullet an. Bei alpha handelt es sich um die Position im Bezug zum Roboter, also in welcher Richtung des Roboters die Bullet erstellt werden soll (0° wäre hier nach Links). AddSpeed gibt der Bullet eine zusätzliche Geschwindigkeit (dies wird nur in Shoot verwendet um die RoboterGeschwindigkeit zu berücksichtigen). Offset gibt die Distanz zum Roboter an mit welcher die Bullet gespawnt werden soll (6 wäre hierbei der Standart-Wert um direkt neben dem Roboter zu erscheinen). Target gibt ein optionales Ziel für die Bullets an (siehe Spellcard 3) steht hier eine 0 so wird der alhpa-Wert von vorher benutzt.
<br/>
Die einzelnen "Spellcards" rufen nun die create Bullet-Methode mit verschiedenen Parametern auf um verschiedene Muster zu schaffen.

```python
#in Robot-Class
def spellcard1(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            Repetitions = 10
            LifeTime = 90
            alpha1 = self.alpha
            alphaStep = 45
                  
            #Create Bullets
            for delay in range(0, Repetitions, 1):
                for n in range(0, 8, 1):
                    self.BulList.append(self.createBullet(1,LifeTime, delay*4, (alpha1 + n*alphaStep),0,6,0))
                    self.BulList.append(self.createBullet(4,LifeTime, delay*4, (alpha1 + n*alphaStep),0,6,0))

            self.coolDown = 150
```
Viele der Spellcards sind vom Prinzip ähnlich aufgebaut. 
<br/>
Zuerst wird, wie bei Shoot auch, sichergestell dass der Roboter am Leben ist und auch bereit ist die Spellcard zu benutzen.
<br/>
Anschließend werden einige Werte definiert welche Später an createBullet gegeben werden.
Repetitions gibt an wie oft eine einzelne Bullet wiederholt wird, Lifetime wie oben, alpha1 ist die Blickrichtung des Roboters und alphaStep gibt an wie groß der Winkel zwischen den einzelnen Bullets ist (da wir hier in 8 Richtungen Schießen möchten ist alphaStep = 45°).
<br/>
Die einzelnen Bullets werden dann in einer For-Schleife erstellt, die erste Schleife ist hierbei für die Wiederholungen und die 2te Schleife für die verschiedenen Richtungen.
<br/>

Um die Bullets jetzt auf eine gewünschte weiße bewegen zu können wurde die MoveBullet-Methode der Bullet-Class angepasst.
```python
#in Bullet-Class
def moveBullet(self): #export Spellcards later in extra Method
        
        #Spellcard 1    (Star Pattern)
        if  1<= self.bulType <= 5:
            self.Spellcard01()

            
        #Spellcard 2    (Circles into Random stars)
        elif  6<= self.bulType <= 7: #8 to 13 have standart movement
            self.Spellcard02()

        #Spellcard 3    (Circle into Target Aim)
        elif self.bulType == 14:
            self.Spellcard03()


        #Spellcard 4    (Random Delay Split)
        elif 15 <= self.bulType <= 16:
            self.Spellcard04()

        #Spellcard 5    (Circle Star)
        elif 17 <= self.bulType <= 19: # 20,21 have standart movement
            self.Spellcard05()

        #Spellcard 6    (Spiral)
        elif 22 <= self.bulType <= 26:
            self.Spellcard06()

        #Spellcard 7    (Star - sweep - Star)
        elif 27 <= self.bulType <= 29:
            self.Spellcard07()

        #Standart Behavior does not change speed/angle
        #=> if shot not defined, or Standart dont change anything
        GesX = math.cos(math.radians(self.alpha)) * self.speed
        GesY = - math.sin(math.radians(self.alpha)) * self.speed  
        SpeedVector = QVector2D(GesX,GesY)
        self.position.__iadd__(SpeedVector)
```
Hier wird nun anhand des Bullet-Types festgelegt ob die Bullet einige ihrer Werte ändern soll. (Ist ein Bullet-Type nicht definiert, oder Type0 (standart Bullet) so wird einfach die Geschwindigkeit auf den Positionsvektor addiert)
<br/>
```python
#in Bullet-Class
    def Spellcard01(self):
        if self.bulType == 1:
            if self.time == 60:
                self.alpha =  (self.alpha - 90) % 360
                self.bulType = 2            
            
        elif self.bulType == 2:
            if self.time == 30:
                self.alpha =  (self.alpha + 90) % 360
                self.bulType = 3

        elif self.bulType == 4:
            if self.time == 60:
                self.alpha =  (self.alpha + 90) % 360
                self.bulType = 5            
            
        elif self.bulType == 5:
            if self.time == 30:
                self.alpha =  (self.alpha - 90) % 360
                self.bulType = 3
        
```
Um eine Bullet nach einer bestimmten Zeit zu ändern wird immer ihre LifeTime betrachtet (welche in jedem Tick um 1 reduziert wird).
Hier wird z.B. die Richtung der Bullet um 90° geändert und ihr Type verändert.
<br/>
Nach diesen Änderungen wird die normale Move-Methode weiter ausgeführt und die neue Position der Bullet bestimmt.
<br/>
Hier noch eine 2te "Spellcard" mit anderem Verhalten:
</br>
```python
#in Robot-Class
    def spellcard3(self):
        if self.coolDown == 0 and self.deathTime == 0:
            #Values
            BulletAmmount = 30
            Repetitions = int(round(BulletAmmount/2))
            LifeTime = 400 + 4*Repetitions
            
            #Calculate Angles
            alpha1 = self.alpha
            alphaStep = 360 / BulletAmmount
            
            #Calculate Target
            DistTo2 = QVector2D(self.position.x() - self.RobotList[2].x(), self.position.y() - self.RobotList[2].y())
            DistTo3 = QVector2D(self.position.x() - self.RobotList[3].x(), self.position.y() - self.RobotList[3].y())
            DistTo4 = QVector2D(self.position.x() - self.RobotList[4].x(), self.position.y() - self.RobotList[4].y())
            Distance2 = DistTo2.x()*DistTo2.x() + DistTo2.y() * DistTo2.y()
            Distance3 = DistTo3.x()*DistTo3.x() + DistTo3.y() * DistTo3.y()
            Distance4 = DistTo4.x()*DistTo4.x() + DistTo4.y() * DistTo4.y()
            
            closest = min(Distance2, Distance3, Distance4)

            if closest == Distance2:
                #print("darkBlue")
                target = 2
            elif closest == Distance3:
                #print("lightBlue")
                target = 3
            elif closest == Distance4:
                #print("orange")
                target = 4
                
            #Create Bullets
            for i in range(0,Repetitions,1):
                self.BulList.append(self.createBullet(14,LifeTime - 4*i, 4*i, (alpha1 + i*alphaStep) % 360 ,0 ,50,self.RobotList[target]))
                self.BulList.append(self.createBullet(14,LifeTime - 4*i, 4*i, (alpha1 + 180 + i*alphaStep) % 360 ,0 ,50,self.RobotList[target]))
            
            self.coolDown = 250
```
Diese Spellcard soll auf den Roboter zielen der am wenigsten entfernt ist.
<br/>
Dazu definieren wir erstmal wieder ein paar Werte die wir später benötigen. Wir verwenden hier zusätzlich noch ein BulletAmmount welcher genau angibt wie viele Bullets wir haben möchten.
<br/>
Anschließend berechnen wir aus der PositionsListe des Roboters den Gegner der am nächsten zu unserem Roboter liegt und merken uns dessen Koordinaten.
<br/>
Da wir hier nun ein Ziel haben wird unser Target-Parameter der createBullet-Methode auf ein genaues Ziel gesetzt, nähmlich die Koordinaten des Gegners.
Die createBullet-Methode berechnet nun das alpha das die Bullet benötigt um auf den Gegner zu zielen.
```python
#in createBullet
        if target != 0:
            #Calculate Target Alpha
            target_x = target.x()
            target_y = target.y()

            pos_x = bulletpos.x()
            pos_y = bulletpos.y()


            #Berechnung Blickrichtung
            delta_x = target_x - pos_x
            delta_y = target_y - pos_y
            target_alpha = -math.degrees(math.atan2(delta_y, delta_x)) % 360

        else:
            target_alpha = alpha
```
Die MoveBullet-Methode zu dieser Spellcard sieht folgendermaßen aus:
```python
#in Bullet-Class
    def Spellcard03(self):
        if self.bulType == 14:
            if self.time > 400:
                self.speed = 0
            elif self.time == 400:
                self.speed = 5
```
Hier wird einfach erste eine kurze Zeit gewartet, bis sich die Bullets bewegen.
<br/>

Um die Bullets mit den richtigen Visuals auszustatten haben wir ein BulletTextures-Dictionary welches den Typ einer Bullet auf eine Grafik abbildet.
```python
BulletTextures = {0:QPixmap('textures/Bullets/Standart.png'), #Standart
                               #Spellcard1
                               1:QPixmap('textures/Bullets/GreenOrb.png'), #Green 1
                               2:QPixmap('textures/Bullets/BlueOrb.png'), #Blue 1
                               3:QPixmap('textures/Bullets/RedOrb.png'), #Red
                               4:QPixmap('textures/Bullets/GreenOrb.png'), #Green 2
                               5:QPixmap('textures/Bullets/BlueOrb.png'), #Blue 2
                               #Spellcard2
                               6:QPixmap('textures/Bullets/GreenOrb.png'), #GreenOrb
                               7:QPixmap('textures/Bullets/BlueOrb.png'), #BlueOrb
                               8:QPixmap('textures/Bullets/Star01.png'), #Star1
                               9:QPixmap('textures/Bullets/Star02.png'), #Star2
                               10:QPixmap('textures/Bullets/Star03.png'), #Star3
                               11:QPixmap('textures/Bullets/Star04.png'), #Star4
                               12:QPixmap('textures/Bullets/Star05.png'), #Star5
                               13:QPixmap('textures/Bullets/Star06.png'), #Star6                               
                               #Spellcard3
                               14:QPixmap('textures/Bullets/Kunai.png'), #Kunai
                               #Spellcard4
                               15:QPixmap('textures/Bullets/BlackCircle.png'), #BlackMain
                               16:QPixmap('textures/Bullets/PurpleBullet.png'), #Purple Splits
                               #Spellcard5
                               17:QPixmap('textures/Bullets/RedSeal.png'), #RedSeal
                               18:QPixmap('textures/Bullets/RedSeal.png'), #RedSeal
                               19:QPixmap('textures/Bullets/RedSeal.png'), #RedSeal
                               20:QPixmap('textures/Bullets/BlueSeal.png'), #BlueSeal
                               21:QPixmap('textures/Bullets/GreenSeal.png'), #GreenSeal
                               #Spellcard6
                               22:QPixmap('textures/Bullets/Butterfly.png'), #Butterfly
                               23:QPixmap('textures/Bullets/Butterfly.png'), #Butterfly
                               24:QPixmap('textures/Bullets/Butterfly.png'), #Butterfly
                               25:QPixmap('textures/Bullets/BlueOrb.png'), #BlueOrb
                               26:QPixmap('textures/Bullets/RedOrb.png'), #RedOrb
                               #Spellcard7
                               27:QPixmap('textures/Bullets/Kunai.png'), #Kunai
                               28:QPixmap('textures/Bullets/Kunai.png'), #Kunai
                               29:QPixmap('textures/Bullets/Star05.png'), #purpleStar
                               }
```
In der Draw-Methode wird nun einfach die Textur auf den entsprechenden Typ gesetzt. Des weiteren haben wir auch noch dafür gesorgt dass sich die Bullets auch entsprechend ihrem alpha drehen.
```python
#in Bullet-Class
    def drawBullet(self, br):
    
        #Set Rotation, place etc
        texture = self.BulletTextures[self.bulType]
        br.save()
        br.translate(self.position.x() + 0.5 * Bullet_Size, self.position.y() + 0.5 * Bullet_Size)
        br.rotate(-self.alpha)
        source = QRectF(0, 0, Bullet_Size, Bullet_Size)
        target = QRectF(-Bullet_Size/2, -Bullet_Size/2,
                Bullet_Size, Bullet_Size)
        #Draw
        br.drawPixmap(target, texture, source)
        br.restore()

```
Da viele der Speelcards große Bereiche abdecken war es notwendig dafür zu sorgen dass man sich nicht selbst abschießt, die wurde über das owner Attribut der Bullets gelöst (If Abfrage: RobotId == Owner).
Bulletst kollidieren jetzt nur mit einem Roboter wenn dieser nicht der Owner ist.

Um die Spellcards besser sehen zu können haben wir in den Optionen des Menüs noch eine Einstellung um die Bullet-Wall-Collision zu deaktivieren.

<br/>

**Bomb Pick-Up System**<br/>
Inspirert von einem Power-Up System, wirkt bei jeder Kollision mit der Bomb ein Effekt auf den Roboter. Auf dem Spielfeld tauchen nacheinander eine grüne oder rote Bomb, die mit 50/50 Chance gewählt werden. Beide haben separate Draw Methoden:
```python
def drawBomb(self, qp):        
    texture = QPixmap('textures/bomb.jpg')

    qp.drawPixmap(self.bombPosition[self.currentBombPos][0], self.bombPosition[self.currentBombPos][1], texture)

def drawRedBomb(self,qp):
    texture = QPixmap('textures/redbomb.jpg')

    qp.drawPixmap(self.bombPosition[self.currentBombPos][0], self.bombPosition[self.currentBombPos][1], texture)
```
Die möglichen Positionen auf dem Spielfeld werden in einem Dictionary gespiechert. <br/>
Damit das Auftauchen der Bombs auch funktioniert, wird ein separater Timer benötigt, der ab Anfang anfängt runterzuzählen (bzw. neu startet, wenn die Bombe aufgehoben wird)
```python
def reduceBombTime(self):
    if self.bombTime != 0:
        self.bombTime -= 1
        
        if self.bombTime == 0:
            self.bombTime = BOMB_TIMER
            self.randomizeBombIcon()
            self.setNextBombPos()
```
Beim Pick-Up wird die Position der Bombe auf die nächste Position im Dictionary gesetzt (mit *setNextBombPos*). <br/>
Um zu entscheiden, ob eine rote oder grüne Bombe erscheint, gibt es eine *randomizeBombIcon()*-Funktion, die die globale Variable *bombStatus* zufällig auf 'green' oder 'red' setzt. Dieser Status wird dann an den PaintEvent weiter gegeben, wo mit if-Abfragen geprüft wird, ob *drawBomb* oder *drawRedBomb* ausgeführt werden soll.
```python
def randomizeBombIcon(self):
    number = random.randint(1, 2)

    if number == 1:
        self.bombStatus = 'green' 
    elif number == 2:
        self.bombStatus = 'red'
```
Um die Kollision des Robos mit der Bomb zu prüfen, wird die gleiche Funktionsstruktur benutzt wie bei Bullet-Kollision. <br/>
**Sound**<br/>
Zur Speicherung und Abspielen von Sounds verwenden wir den *pygame.mixer*. Dieser erlaubt uns mehrere Sounds gleichzeitig abzuspielen, ohne die Anderen abzubrechen. Hiermit werden verschieden Sounds für die Spellcards, Death-Sound und Hintergrundmusik erzeugt.
Je nach Bedarf werden die per *pygame.mixer.Sound('PATH')* geladen und mit pygame.mixer.Sound.play('NAME') abgespielt.
<br/>

**Updated Visuals**
Wir haben nun auch Texturen für die Roboter eingefügt, welche sich mit dem alpha der Roboter drehen.
```python
#in Spielfeld-Class
def drawRobo(self, Robo, br):

        # Set Rotation, place etc
        texture = self.RoboTextures[Robo.texture]
        br.save()
        br.translate(Robo.position.x() + Robo.radius, Robo.position.y() + Robo.radius)
        br.rotate(-Robo.alpha)
        source = QRectF(0, 0, 2 * Robo.radius, 2 * Robo.radius)
        target = QRectF(-Robo.radius, -Robo.radius,
                        2 * Robo.radius, 2 * Robo.radius)
        # Draw
        br.drawPixmap(target, texture, source)
        br.restore()
```
Dazu haben wir die drawRobo-Methode etwas verändert.
<br/>
Außerdem haben wir ein weiteres kleines Extra für die Backgrounds eingebaut.
Wir zeichnen den Ground nun als 1 Textur und die walls anschließend darauf.
Dies ermöglicht uns mehr Freiheit mit dem Ground und lässt uns diesen z.B bewegen.
```python
#in Spielfeld-Class
def drawField(self, qp):
        qp.setPen(Qt.NoPen)
        texture = self.floorTexture
        if ftexture == "Background Dirt" or  ftexture == "Background Pattern" or ftexture == "Background Sakura" or  ftexture == "Background Water":
            qp.drawPixmap(- ((self.tickCount/2) % 1000), - ((self.tickCount/2) % 1000), texture)
        else:
            qp.drawPixmap(0,0, texture)
        #Draw the PlayField
        for i in range(0, 100, 1):
            for j in range(0, 100, 1):
                    if SpielFeld.PlayFieldAR[i][j]==1:
                        texture = self.wallTexture
                        self.BarrierList.append(texture)
                        qp.drawPixmap(i*10, j*10, texture)
```
Das erreichen wir indem wir eine größere Textur in regelmäßigen Abständen an verschobenen Koordinaten Zeichnen.

## Week 8 - Robo-Keystrokes & Death-Timer
**Keystrokes**
```python
while True:
    self.msleep(100)
    if keyboard.is_pressed('w'):
        print('W-Key')
        self.robot.a = 0.01

    if keyboard.is_pressed('s'):
        print('S-Key')
        self.robot.a = -0.01

    if keyboard.is_pressed('a'):
        print('A-Key')
        self.robot.a_alpha = 0.1

    if keyboard.is_pressed('d'):
        print('D-Key')
        self.robot.a_alpha = -0.1

    if keyboard.is_pressed('j'):
        print('J-Key')
        self.robot.shoot()
```
Per 'keyboard'-packet sind wir in der Lage die Keystrokes an den zu steuernden Robo weiter zu geben. Für jeden möglichen Key besitzt die Robo-Methode ein if-Fall, der bestimmte zugeordnete Befehle per Knopf ausführen kann. Der Sleep-Befehl liegt aus Performanz-Gründen vor. <br/>

**Death-Timer**

```python
for bul in SpielFeld.Bullets:
    bul.moveBullet()
    if self.BulletBarrierCollision(bul):
       SpielFeld.Bullets.remove(bul)
    for robot in self.robots:
        if bul.one_hit(robot):
            if robot.robotid == 1 and robot.immuneTime == 0:
                robot.deathTime = DEATH_TIME
            elif robot.robotid != 1:
                self.teleport_bullet(robot)
            SpielFeld.Bullets.remove(bul)
```
Jeder Roboter besitzt eine deathTime, die auf die Konstante DEATH_TIME gesetzt werden kann, sobald er getroffen wird. Obwohl alle Robos dieses Attribut haben, nutzt diese zurzeit nur der Hunter. <br/>
Um es zu vermeiden, dass die deathTime wieder hochgezählt wird, obwohl der Robo außerkraftgesetzt ist, haben wir auch eine immuneTime implementiert. immuneTime und deathTime werden auf gleiche Weise runtergezählt per:
```python
# Death Counter (Down) {see Constants}
def reduceDeathTime(self,Robot):
    if Robot.deathTime != 0:
        Robot.deathTime -= 1
        if Robot.deathTime == 0:
            Robot.immuneTime = IMMUNE_TIME

def reduceImmuneTime(self,Robot):
    if Robot.immuneTime != 0:
        Robot.immuneTime -= 1
```
**Target mit FOV**

Für das targeting haben wir hier jetzt unser FOV genutzt. Dafür haben wir zunächst ein neues Attribut ViewList in Robots angelegt.

```python
                            # Position, Distanz zueinander, Blickwinkel, seen
        self.ViewList = {1 : [ QVector2D(0,0), 0, 0, False],
                         2 : [ QVector2D(0,0), 0, 0, False],
                         3 : [ QVector2D(0,0), 0, 0, False],
                         4 : [ QVector2D(0,0), 0, 0, False]}
 ```
 
Diese Liste gibt uns die aktuelle Position des gesichteten Roboters wieder, die Distanz zueinander, den Blickwinkel des gesichteten Roboters und ob wir den Roboter noch im Blickfeld haben oder nicht.
 
Mithilfe dieser ViewList können wir nun unser Target ausmachen. Dafür konstruieren wir uns die Methode:

```python
    def aimTargetView(self, target):
        # who is my target
        target_id = target

        # is my target in my FOV?
        if self.ViewList[target_id][3]:

            # Yes, chase him
            target_alpha = self.ViewList[target_id][2]

            self.moveChase(target_alpha)

        # no, turn around and wait
        else:
            self.v = 0
            self.a_alpha = 2
```

Diese Methode schaut zunächst, wer mein Target ist. Dann schaut sie in die ViewList, ob das Target im Sichtfeld ist. Wenn ja, dann ist es in der Liste bei seen mit True gekennzeichnet und wenn nicht, dann mit False. Bei gesichtetem Target wird auf dessen Alpha-Wert zugegriffen und mithilfe der moveChase Methode die Target-Position ermittelt und es bewegt sich darauf zu und schießt in die Richtung. Wird nichts gesichtet, dann dreht sich der Roboter im Kreis und wartet auf sein Ziel.

```python

    def moveChase(self, tarAlpha):
        target_alpha = tarAlpha

        if target_alpha < 180:
            if  target_alpha+180 < self.alpha or target_alpha > self.alpha:
                # turn left
                self.a_alpha = 0.5

## Week 8 - Steuerung durch Tastatur
see Week 8 Branch, Presentation contains newest version </br>
**Keyboard**

            else:
                # turn right
                self.a_alpha = -0.5
        else:
            if  target_alpha > self.alpha >= ((target_alpha+180)% 360):
                # turn left
                self.a_alpha = 0.5

            else:
                # turn right
                self.a_alpha = -0.5
                
 ```


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
