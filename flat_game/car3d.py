import random
import math
import numpy as np

from vpython import *

class GameState():
    def __init__(self):
        self.scene = display(title='Examples of Tetrahedrons', x=0, y=0, width=600, height=600, center=vector(0,0,0), background=vector(0,0,0))

        Nobstale = 11  # change this to have more or fewer atoms
        # Typical values
        L = 1 # container is a cube L on a side
        gray = color.gray(0.7) # color of edges of container
        mass = 4E-3/6E23 # helium mass
        r_car = 0.007 # wildly exaggerated size of helium atom
        r_obstale = 0.1
        r_sensor =  0.005
        self.dt = 0.005
        #the limitation of space
        d = L/2+r_obstale
        r = 0.005
        boxbottom = curve(color=gray, radius=r)
        boxbottom.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d)])
        boxtop = curve(color=gray, radius=r)
        boxtop.append([vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,d,-d), vector(-d,d,-d)])
        vert1 = curve(color=gray, radius=r)
        vert2 = curve(color=gray, radius=r)
        vert3 = curve(color=gray, radius=r)
        vert4 = curve(color=gray, radius=r)
        vert1.append([vector(-d,-d,-d), vector(-d,d,-d)])
        vert2.append([vector(-d,-d,d), vector(-d,d,d)])
        vert3.append([vector(d,-d,d), vector(d,d,d)])
        vert4.append([vector(d,-d,-d), vector(d,d,-d)])
        #define the car and the obstales
        self.car = sphere (color = color.green, radius = r_car, make_trail=False, retain=20)
        self.obstales = []
        self.opos = []
        for i in range(Nobstale):
            x =L*random()-L/2
            y = L*random()-L/2
            z = L*random()-L/2
            self.obstales.append(sphere(pos=vector(x,y,z), radius=r_obstale, color=gray))
            self.opos.append(vector(x,y,z))
        self.car.v = vector (-0.005, -0.0025, +0.075)
        #side = side - thk*0.5 - car.radius
        self.side = d - r*0.5 - self.car.radius
    def frame_step(self, action):
        if action == 0:
            self.car.v.x += 0.05
        elif action == 1:
            self.car.v.y += 0.05
        elif action == 2:
            self.car.v.z += 0.05
        while True:
            rate(200)
            self.car.pos = self.car.pos + self.car.v*self.dt
            if not (self.side > self.car.pos.x > -self.side):
                self.car.v.x = -self.car.v.x
            if not (self.side > self.car.pos.y > -self.side):
                self.car.v.y = -self.car.v.y
            if not (self.side > self.car.pos.z > -self.side):
                self.car.v.z = -self.car.v.z

if  __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((np.random.randint(0,3)))
