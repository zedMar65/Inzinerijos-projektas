# Import stuff
import pygame
import time
import math
import sys
pygame.init()

# IMPORTANT NOTE: 1px on acreen is equal to 0.1 meter,
# sx/sy = screen size, xc, yc = center of screen, t = time, define font and screenm running condition for stopping
sx = 1000
sy = 800
xc = sx/2
yc = sy/2
t = 0.01
pi = 3.1415
screen = pygame.display.set_mode([sx, sy])
font = pygame.font.SysFont(None, 25)
running = True
current_path = __file__[:-7]
cone_img = pygame.image.load(current_path+r"\img\cone.png")
tank_img = pygame.image.load(current_path+r"\img\tank.png")
engine_img = pygame.image.load(current_path+r"\img\engine.png")
fire_img = pygame.image.load(current_path+r"\img\fire.png")


# something something idk // another intake: a derivative class for stuff that should be had (parent'n child) dat was mistake
def img_blit(r, h, x, y, rot, img):
        screen.blit(pygame.transform.rotate(pygame.transform.scale(img, (r*2*10, h*10)), rot), (x-r*10, y-h*10))

def drag(cone_height, cone_radius, altitude, speed, mass, cone_temperature):
    # Constants
    g = 9.81   # gravitational acceleration in m/s^2
    rho0 = 1.225   # air density at sea level in kg/m^3
    T0 = 288.15   # standard temperature at sea level in K
    R = 8.31447   # universal gas constant in J/mol*K
    M = 0.029    # molar mass of air in kg/mol
    A = math.pi * cone_radius**2   # cross-sectional area of the cone in m^2
    Cd = 0.5   # drag coefficient for a cone
    
    # Calculating air density, temperature, and pressure at altitude
    L = 0.0065   # temperature lapse rate in K/m
    if altitude <= 11000:
        T = T0 - L * altitude
        p = 101325 * (T/T0)**(-g*M/(R*L))
    elif altitude <= 25000:
        T = 216.65
        p = 22632.06 * math.exp(-g*M*(altitude-11000)/(R*T))
    elif altitude <= 47000:
        T = 216.65 + L * (altitude-25000)
        p = 2480.32 * (T/216.65)**(-g*M/(R*L))
    elif altitude <= 53000:
        T = 282.65
        p = 120.32 * math.exp(-g*M*(altitude-47000)/(R*T))
    elif altitude <= 71000:
        T = 282.65 - L * (altitude-53000)
        p = 51.97 * (T/282.65)**(-g*M/(R*L))
    else:
        return 0, 0   # altitude out of range
    
    rho = p / (R/M * T)
    
    # Calculating drag force
    Fd = 0.5 * Cd * rho * speed**2 * A
    
    # Calculating change in temperature due to drag force
    delta_T = Fd**2 * (cone_height * math.pi * cone_radius**2) / (2 * mass * rho * cone_temperature)*0.01
    
    # Updating cone temperature
    new_temperature = cone_temperature - delta_T
    
    # Returning drag force and new temperature
    return Fd, new_temperature


class cone:
    def __init__(self, r, h):
        # mass if the cone is made out of aluminum
        self.r = r
        self.h = h
        self.x = 0
        self.y = 0
        self.s = 0
        self.m = math.pi * r * math.sqrt(r**2 + h**2) + math.pi * r**2 * 0.01 * 2700
        self.t = 15 #calculate this, IDK
        self.rot = 0
    def draw(self, a, v, rot):
        
        img_blit(self.r, self.h, self.x, self.y, rot, cone_img)
        data = drag(self.h, self.r, a, self.s, self.m, self.t)
        self.f_drag = data[0]
        self.t = data[1]
        # pygame.draw.polygon(screen, (25, 25, 25), [(self.x-self.r*10, self.y), (self.x+self.r*10, self.y), (self.x, self.y-self.h*10)])
    
        
class tank:
    def __init__(self, r, h):
        self.burn_time = 120
        self.x = 0
        self.y = 0
        self.r = r
        self.h = h
        self.m = r**2*math.pi*h*1700*self.burn_time/120
        self.rot = 0
    def draw(self, a, v, rot):
        self.m = self.r**2*math.pi*self.h*1700*self.burn_time/120
        img_blit(self.r, self.h, self.x, self.y+self.h*10/2, self.rot, tank_img)
        # pygame.draw.polygon(screen, (25, 25, 25), [(self.x-self.r*10, self.y-self.h/2*10), (self.x+self.r*10, self.y-self.h/2*10), (self.x+self.r*10, self.y+self.h/2*10), (self.x-self.r*10, self.y+self.h/2*10)])
class nosil:
    def __init__(self, r, h):
        self.x = 0
        self.y = 0
        self.r = r
        self.h = h
        self.m = math.pi * r * math.sqrt(r**2 + h**2) + math.pi * r**2 * 0.01 * 2700
        self.rot = 0
    def draw(self, a, v, rot):
        
        # pygame.draw.polygon(screen, (25, 25, 25), [(self.x-self.r*10, self.y+10), (self.x+self.r*10, self.y+10), (self.x, self.y-self.h*10+10)])
        if ship.f>0:
            screen.blit(pygame.transform.scale(fire_img, (self.r*2*10, 200)), (self.x-self.r*10, self.y))
        screen.blit(pygame.transform.scale(engine_img, (self.r*2*10, self.h*10)), (self.x-self.r*10, self.y))
        # img_blit(self.r, self.h, self.x, self.y*10, self.rot, engine_img)

# class rocket is a fizick calculating object, it doesnt move, it alaways stays at the center of the screen.
class Rocket:
    # set all variables for the rocket, t = temperature, x/y = location, xz/yz = size of rocket, m = mass of rocket calculated for a cylinder full of rocket fuel, f = force, a = acc, s = speed. 
    def __init__(self, x, y, f, s, a, t, parts):
        self.t = t
        self.x = x
        self.y = y
        self.m = 0.000000000000000001
        self.f = f
        self.a = a
        self.s = s
        self.parts = parts
        self.m = 0
        self.rot = 0
        for i in range(len(self.parts)):
            self.m+=self.parts[i][0].m
    # calculates the fizics and moves the object acordingly, detects if is impact with earth, resets force to 0, ALL FIZICS IN HERE
    def push(self, f):
        self.f = f
    def update(self):
        self.t = self.parts[0][0].t
        self.m = 0
        for i in range(len(self.parts)):
            self.parts[i][0].s = self.s
            self.m+=self.parts[i][0].m
        
        # detects impact
        # *doesnt
        # calculates g acceleration, y/10, becouse y is in pixels and the ath should be counted with meters
        self.g = -(5.97*1000000000000000000000000*6.67*0.00000000001)/((self.y/10+6.371*1000000)*(self.y/10+6.371*1000000))
        # add other forces when fizics are expanded, like drag
        self.a = ((self.g*self.m)+self.f)/self.m
        # * 0.01 becouse 0.01 second has passed
        self.s += self.a*0.01 
        # * 10, becouse i need to move 10 px for ewery meter
        self.y += self.s*0.01*10
        for i in range(len(self.parts)):
            self.parts[i][0].x = xc
            self.parts[i][0].y = yc-self.parts[i][1]
            self.parts[i][0].draw(self.y, self.s, self.rot)
        if self.y<310:
            self.s = 0
            self.y = 311
    def burn(self):
        if self.parts[1][0].burn_time>0:
            self.push(13000000)
            self.parts[1][0].burn_time-=0.01
    def rotate(self, degrees):
        self.rot = degrees
def update(ship):
    screen.fill((100, 100, 100))
    ship.update()
    x = ship.x
    y = ship.y
    pygame.draw.rect(screen, (100, 255, 100), pygame.Rect(0, 300+y, 1500, 400))
    screen.blit(font.render("t = "+str(round(t, 1))+", m = "+str(round(ship.m, 1))+", g = "+str(round(ship.g, 1))+", a = "+str(round(ship.a, 1))+", s = "+str(round(ship.s, 1))+", y = "+str(round(ship.y, 1))+", f = "+str(round(ship.f, 1))+", x = "+str(round(ship.x, 1))+", temp. = "+str(round(ship.t, 1)), True, (255, 255, 255)), (5, 5))
    ship.f = 0
    return y
# intintant simuliacija reik kazkaip leis tuos parts pasirinkt
Parts = [[cone(1.5, 5), 200], [tank(1.5, 40), 0], [nosil(1.5, 1), -200]]             
ship = Rocket(xc, yc, 0, 0, 0, 15, Parts)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if pygame.key.get_pressed()[pygame.K_w]:
        # do something
        time.sleep(0)
    ship.burn()
    update(ship)
    time.sleep(0.01)
    pygame.display.flip()
    t+=0.01
pygame.quit()