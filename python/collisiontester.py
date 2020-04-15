"""collisiontester controller."""

"""This program has a maybe slightly different than expected. It works by sending the robot along a path 
searching for dead ends with a turn priority of left, right, forward. It uses a stack to keep track of the current options for """


# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import *
from queue import LifoQueue
import math

# create the Robot instance.
robot = Robot()

max_speed = math.tau


first_run = ''
second_run = ''
this_run = 0

try:
    first_run = open('run1.txt')
    this_run += 1
except Exception:
    pass

try:
    second_run = open('run2.txt')

# get the time step of the current world.
timestep = 64

path_stack = LifoQueue()
ps=[]
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(timestep)

left_motor = robot.getMotor('left wheel motor')
right_motor = robot.getMotor('right wheel motor')
compass = robot.getDevice('compass')
compass.enable()
t_sense = robot.getDevice('')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

class Walls:
    def __init__(self,in_l,in_f,in_r):
        self.left = in_l
        self.front = in_f
        self.right = in_r


def check_walls(sensors):
    templeft = sensors[5] > 80
    tempfront = sensors[7] > 80 and sensors[0] > 80
    tempright = sensors[3] > 80
    return Walls(templeft,tempfront,tempright)


# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller

'''Webots suggests that this just be run from a while loop, but that's disgusting and recursion is better'''


def make_your_move(in_dir, in_rotation):
    option_stack = []
    found_trophy = False
    if in_dir == 'l':
        wb_motor_set_position(right_motor,-1.5708)
        wb_motor_set_position(left_motor,-1.5708)
    elif in_dir=='r':
        wb_motor_set_position(right_motor,1.5708)
        wb_motor_set_position(left_motor,1.5708)

    while check_walls.front == True:
        if option_stack:
            found_trophy = make_your_move(option_stack.pop())
        if found_trophy == True:
            path_stack.push(in_dir)
            return True
        elif found_trophy == False and option_stack: #apparently lists have an implicit boolean value for whether they're empty or not. Neat
            found_trophy = make_your_move(option_stack.pop())



while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    psValues=[]
    for i in range(8):
        psValues.append(ps[i].getValue())


    found_obs = check_walls(psValues)





    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
