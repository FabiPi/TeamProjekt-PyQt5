class Bullet(object):
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


    def drawBullet(self, br):
        br.setBrush(QColor(255, 255, 250))
        br.drawEllipse(self.position.x() - (0.5 * Bullet_Size),self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)

    def moveBullet(self):
        self.position.__iadd__(self.velocity)

    def bulletShape(self):
        shape = QPainterPath()
        shape.addEllipse(self.position.x() - (0.5 * Bullet_Size) , self.position.y() - (0.5 * Bullet_Size), Bullet_Size, Bullet_Size)
        return shape

    def one_hit(self, robo):
        if self.bulletShape().intersects(robo.roboShape()):
            return True
        else: pass

        
        
        
'''
    # Funktion | Zeichnen von Bullet #
    def drawBullet(self, Bullet, br):
        br.setBrush(Server.colors["yellow"])
        br.setPen(Server.colors["black"])
        br.drawEllipse(int(round(Bullet.position.x())), int(round(Bullet.position.y())), BULLET_SIZE, BULLET_SIZE)

        # Flugrichtung bzw. Richtungsvektor
        xPos = math.cos(math.radians(Robots.alpha))
        yPos = - math.sin(math.radians(Robots.alpha))


    def fire_Bullet(self):
        # fire bullet if other robot is in view

        # set bullet position so it is where the other robo is

        # add bullet to list for later remove

        pass

'''

# TODO: If Robo1-Blickwinkel intersects Robo2-Position ==> drawBullet
# and move it with constant Robo.alpha and Robo.speed [While (CheckIfBulletOutOfSpielFeld = FALSE) do moveBullet)

######################
