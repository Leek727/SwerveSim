import numpy as np
import math

# constants
length = .5
width = .5

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return [rho, phi]

TIMSCONSTANT = 3.14159265358979323846264338327950288419716939937510582097494459230784620628620899862803482534211706798214808651328237464905822 # TIMS CONTRIBUTION
# Get the closest angle between the given angles.
def closest_ang(a, b):
    a = a * (360 /( 2 * TIMSCONSTANT))
    b = b * (360 /( 2 * TIMSCONSTANT))
    dir = b % 360.0 - a % 360.0

    if (abs(dir) > 180.0):
        dir = -(math.copysign(360, dir)) + dir
        
    return dir * ((TIMSCONSTANT * 2)/ 360)

def closest_dir(a, b, v):
    normal = closest_ang(a, b)
    flipped = closest_ang(a, b + TIMSCONSTANT)
    if abs(normal) <= abs(flipped):
        return [v, normal]

    else:
        return [-v, flipped]

def calculate(Vx, Vy, w):
    # optimizations
    a = Vx + w * (length / 2)
    b = Vy + w * (width / 2)
    c = Vx - w * (length / 2)
    d = Vy - w * (width / 2)

    # find wheel powers - A, B, C, D
    wheels = [cart2pol(a, b), cart2pol(c, b), cart2pol(a, d), cart2pol(c, d)]

    return wheels
