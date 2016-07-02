import numpy as np
from math import *
from vpython import *

class GameState():
    def __init__(self, target):
        scene = canvas(title='Examples of Tetrahedrons', x=0, y=0, width=600, height=600, center=vector(0,0,0))
        self.target = target
        Nobstale = 4  # change this to have more or fewer atoms
        # Typical values
        L = 1 # container is a cube L on a side
        gray = color.gray(0.7) # color of edges of container
        self.r_car = 0.027 # wildly exaggerated size of helium atom
        self.r_obstale = 0.2
        self.r_sensor =  0.0095
        self.initial_pos = vector(-0.25,-0.22,-0.24)
        self.dt = 1


        #the limitation of space
        d = L/2 + self.r_obstale
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
        self.target_ball = sphere(pos= self.target, color = color.blue, radius = self.r_car, make_trail=False)

        self.obstales = []
        self.sensor_arms = []

        for i in range(Nobstale):
            x =L*random()-L/2
            y = L*random()-L/2
            z = L*random()-L/2
            self.obstales.append(sphere(pos=vector(x,y,z), radius=self.r_obstale, color=gray))

        #side = side - thk*0.5 - car.radius
        self.side = d - r*0.5 - self.r_car

        self.show_sensor = True
        self.initialed =  False
        # self.initialed =  True
        self.crashed = False
        self.collision = False
        self.edge = False

        self.car = None
        self.zero = vector(0,0,0)
        frame = self.make_frame()
        print(frame)
        # print(self.car)
        # self.f = compound(frame)
        self.v = vector(0, 0, 0)
        # self.f.pos = self.initial_pos

    def make_frame(self):
        frame = []
        self.car = sphere(pos=self.zero, color = color.green, radius = self.r_car, make_trail=True, retain=20)
        frame.append(self.car)
        if not self.initialed:
           for i in range(0,6):
               sonar_arm = self.make_sonar_arm(self.car.pos, self.r_car, 0)
               sonar_arm_temp = []
               for sensor in sonar_arm:
                   sen = sensor.rotate(origin=self.car.pos, axis=vector(0,1,0), angle=i*2*pi/6)
                   sonar_arm_temp.append(sensor)
               self.sensor_arms.append(sonar_arm_temp)
           for i in range(1,6):
               sonar_arm = self.make_sonar_arm(self.car.pos,self.r_car, 0)
               sonar_arm_temp = []
               for sensor in sonar_arm:
                   sen = sensor.rotate(origin=self.car.pos, axis=vector(0,0,1), angle=i*2*pi/6)
                   sonar_arm_temp.append(sensor)
               self.sensor_arms.append(sonar_arm_temp)
           # for i in range(1,6):
           #     sonar_arm = self.make_sonar_arm(self.car.pos,self.r_car, 0)
           #     sonar_arm_temp = []
           #     for sensor in sonar_arm:
           #         sen = sensor.rotate(origin=self.car.pos, axis=vector(0,1,1), angle=i*2*pi/6)
           #         sonar_arm_temp.append(sen)
           #     self.sensor_arms.append(sonar_arm_temp)
           # for i in range(1,6):
           #     sonar_arm = self.make_sonar_arm(self.car.pos,self.r_car, 0)
           #     sonar_arm_temp = []
           #     for sensor in sonar_arm:
           #         sen = sensor.rotate(origin=self.car.pos, axis=vector(0,1,-1), angle=i*2*pi/6)
           #         sonar_arm_temp.append(sen)
           #     self.sensor_arms.append(sonar_arm_temp)
           # for i in range(1,6):
           #     sonar_arm = self.make_sonar_arm(self.car.pos,self.r_car, 1)
           #     sonar_arm_temp = []
           #     for sensor in sonar_arm:
           #         sen = sensor.rotate(origin=self.car.pos, axis=vector(1,0,1), angle=i*2*pi/6)
           #         sonar_arm_temp.append(sen)
           #     self.sensor_arms.append(sonar_arm_temp)
           # for i in range(1,6):
           #     sonar_arm = self.make_sonar_arm(self.car.pos,self.r_car, 1)
           #     sonar_arm_temp = []
           #     for sensor in sonar_arm:
           #         sen = sensor.rotate(origin=self.car.pos, axis=vector(-1,0,1), angle=i*2*pi/6)
           #         sonar_arm_temp.append(sen)
           #     self.sensor_arms.append(sonar_arm_temp)
           # for i in range(1,6):
           #     sonar_arm = self.make_sonar_arm(self.car.pos,self.r_car, 2)
           #     sonar_arm_temp = []
           #     for sensor in sonar_arm:
           #         sen = sensor.rotate(origin=self.car.pos, axis=vector(1,1,0), angle=i*2*pi/6)
           #         sonar_arm_temp.append(sen)
           #     self.sensor_arms.append(sonar_arm_temp)
           # for i in range(1,6):
           #     sonar_arm = self.make_sonar_arm(self.car.pos,self.r_car, 2)
           #     sonar_arm_temp = []
           #     for sensor in sonar_arm:
           #         sen = sensor.rotate(origin=self.car.pos, axis=vector(-1,1,0), angle=i*2*pi/6)
           #         sonar_arm_temp.append(sen)
           #     self.sensor_arms.append(sonar_arm_temp)

           self.initialed = True

        for sensor_arm in self.sensor_arms:
            for sensor in sensor_arm:
                sen = sensor
                frame.append(sen)
        # print(len(frame))
        return frame

    def frame_step(self, action):

        if action == 0:
            self.v.x += 0.004
        elif action == 1:
            self.v.y += 0.004
        elif action == 2:
            self.v.z += 0.004
        elif action == 3:
            self.v.x -= 0.004
        elif action == 4:
            self.v.y -= 0.004
        elif action == 5:
            self.v.z -= 0.004

    #while True:
        # rate(200)
        self.v = norm(self.v)/50

        self.f.pos = self.f.pos + self.v*self.dt

        readings = self.get_sonar_readings(self.sensor_arms, self.obstales)
        #print(len(readings))
        #print(readings)
        distance = mag2(self.f.pos-self.target)
        self.car.color = color.green
        if self.car_is_crashed(readings):
            self.crashed = True
            self.car.color = color.red
            reward = -600
            self.recover_from_crash(self.v)
        elif distance < 0.006:
            self.car.color = color.yellow
            print("get target")
            reward = 5000
            self.f.pos = self.initial_pos
            self.v = vector(0,0,0)
        else:
            reward = -100 + int(self.sum_readins(readings) / 20) + 100/distance
        readings.append(distance)
        state = np.array([readings])
        return reward, state

    def sum_readins(self,readings):
        tot = 0
        for i in readings:
            tot += i
            return tot
    def recover_from_crash(self,v):
        if self.crashed:
#            self.edge = False
            self.f.pos = self.initial_pos
            self.v = vector(0,0,0)
            # self.initialed = False
            # self.sensor_arms = []
            self.collision = False
            self.crashed = False

    def car_is_crashed(self, readings):
        for i in readings:
            if i != 0:
                continue
            else:
                return True
        return False

    def check_collision(self, sensor, obstales):
        for obstale in obstales:
            d = obstale.pos-sensor.pos - self.f.pos
            if mag2(d) < (self.r_sensor + self.r_obstale)**2:
                return True
        return False
    def check_edge(self, sensor):
        if not (self.side > sensor.pos.x + self.f.pos.x > -self.side):
            return True
        elif not (self.side > sensor.pos.y + self.f.pos.y > -self.side):
            return True
        elif not (self.side > sensor.pos.z + self.f.pos.z > -self.side):
            return True
        else:
            return False
    def get_sonar_readings(self, sensor_arms, obstales):
        readings = []
        for sensor_arm in sensor_arms:
            appened = False
            i = 0
            for sensor in sensor_arm:
                self.collision = self.check_collision(sensor, obstales)
                self.edge = self.check_edge(sensor)
                if self.collision or self.edge:
                    readings.append(i)
                    appened = True
                    break
                i += 1
            if not appened:
                readings.append(i)
        return readings

    def update_sonar_arm(self,sensor_arms, v):
        interval = 0.005  # Default spread.
        arm_points = []

        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for sensor_arm in sensor_arms:
            for sensor in sensor_arm:
                sensor.pos = sensor.pos + v*self.dt
                if not (self.side > sensor.pos.x > -self.side and self.side > sensor.pos.y > -self.side and self.side > sensor.pos.z > -self.side ):
                    sensor.visible = False
                else:
                    sensor.visible = True

    def make_sonar_arm(self, pos, r_car, condition):
        interval = 0.03  # Default spread.
        arm_points = []
        sensor_arm = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        if condition == 0:
            for i in range(0, 30):
                arm_points.append(vector(r_car + pos.x + (interval * i), pos.y, pos.z))
        elif condition == 1:
            for i in range(0, 30):
                arm_points.append(vector(pos.x, r_car + pos.y + (interval * i), pos.z))
        elif condition == 2:
            for i in range(0, 30):
                arm_points.append(vector(pos.x, pos.y, r_car + pos.z + (interval * i)))
        for point in arm_points:
            sensor_arm.append(sphere(pos=point, radius=self.r_sensor, color=color.white))
        return sensor_arm

# if __name__ == "__main__":
#     game_state = GameState(vector(0.3,0.4,0.66))
#     while True:
#         game_state.frame_step((np.random.randint(0,6)))

