import pygame
import numpy as np
from swerve import *
import random
from pygame.locals import *


pygame.init()

width, height = 500, 500
# Set up the drawing window
screen = pygame.display.set_mode([width, height])

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

class swerve_module:
    def __init__(self, x, y, v, phi):
        self.x = x
        self.y = y
        self.v = v
        self.phi = phi

    def draw(self):
        #print(self.v)
        endpoint = pol2cart(25, self.phi)

        width = int(self.v*10) + 2
        color = (255, 0, 0)
        start = (self.x - endpoint[0], self.y + endpoint[1])
        end = (self.x + endpoint[0], self.y - endpoint[1])

        pygame.draw.line(screen, color, start, end, width)
        pygame.draw.circle(screen, color, start, 1.5 * width ** .5)
        pygame.draw.circle(screen, color, end,  1.5 * width ** .5)

# init wheels
A = swerve_module(100, 100, 0, .5 * 3.141592)
B = swerve_module(100, 400, 0, .5 * 3.141592)
C = swerve_module(400, 100, 0, .5 * 3.141592)
D = swerve_module(400, 400, 0, .5 * 3.141592)

joystick = False
try:
    joy = pygame.joystick.Joystick(0)
    print(joy.get_name())
    joy.init()
    joystick = True

except:
    pass

w = 0
running = True
while running:
    # close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))


    if joystick:
        Vx = -joy.get_axis(0)
        Vy = joy.get_axis(1)
        w = -joy.get_axis(2)
    else:
        Vx = -1 + (pygame.mouse.get_pos()[0] / width) * 2
        Vy = -1 + (1 - pygame.mouse.get_pos()[1] / height) * 2
        left, middle, right = pygame.mouse.get_pressed()
        w += .03 * ((left - right) - w)

    if Vx+Vy+w == 0:
        continue

    a,b,c,d = calculate(Vx, Vy, w)

    # proportional control
    A.phi += .01 * closest_dir(A.phi, a[1], A.v)[1]
    B.phi += .01 * closest_dir(B.phi, b[1], B.v)[1]
    C.phi += .01 * closest_dir(C.phi, c[1], C.v)[1]
    D.phi += .01 * closest_dir(D.phi, d[1], D.v)[1]
    #print(closestAng(A.phi, a[1]), closestAng(B.phi, b[1]), closestAng(C.phi, c[1]), closestAng(D.phi, d[1]))

    A.v = a[0]
    B.v = b[0]
    C.v = c[0]
    D.v = d[0]
    

    A.draw()
    B.draw()
    C.draw()
    D.draw()

    
    pygame.display.flip()

pygame.quit()
