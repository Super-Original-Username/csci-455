"""collisiontester controller."""

"""
his program has a maybe slightly different than expected. It works by sending the robot along a path 
searching for dead ends with a turn priority of left, right, forward. It uses a stack to keep track of 
the current options for a path, and ends with a valid path based off of the first turn that doesn't lead
to a dead end. It does this twice, trying a different path in its second run. Of the two runs, the path 
with the least number of turns is picked as the final path for run 3.
"""


# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import *
from queue import LifoQueue
import math

# create the Robot instance.
robot = Robot()

max_speed = math.tau # I chose to use tau instead of pi because I'm a rebel and like unnecessary challenges
base_speed = max_speed/2


def get_file_length(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

first_run = ''
second_run = ''
this_run = 1

try:
    first_run = open('run1.txt')
    print("Data from run one found")
    this_run = 2
    try:
        second_run = open('run2.txt')
        print("Data from run two found, calculating faster route")
        this_run = 3
    except:
        pass
except: # we don't actually care if a file isn't found, since that probably just means this is a new run
    pass



# get the time step of the current world. (physics frames)
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
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
left_encoder = robot.getPositionSensor('left wheel sensor')
right_encoder = robot.getPositionsensor('right wheel sensor')
right_encoder.enable(timestep)
left_encoder.enable(timestep)

compass = robot.getDevice('compass')
compass.enable()
t_sense = robot.getDevice('')

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
        right_motor.setPosition(-max_speed/4)
        left_motor.setPosition(-max_speed/4)
    elif in_dir=='r':
        right_motor.setPosition(max_speed/4)
        left_motor.setPosition(max_speed/4)

    # initial check for available turns
    sensor_status = check_walls()
    turn_available = sensor_status[0] or sensor_status[2]


    while check_walls().front == True:
        if option_stack:
            found_trophy = make_your_move(option_stack.pop())
        if found_trophy == True:
            path_stack.push(in_dir)
            return True
        elif found_trophy == False and option_stack: #apparently lists have an implicit boolean value for whether they're empty or not. Neat
            found_trophy = make_your_move(option_stack.pop())



def incremental_mover(param_list):
    while robot.step(timestep) != -1:
        psValues=[]
        motor_positions = []
        for i in range(8):
            psValues.append(ps[i].getValue())
        left_motor.setVelocity(base_speed)
        right_motor.setVelocity(-base_speed)
        motor_positions.append(left_encoder.getValue())
        motor_positions.append(right_encoder.getValue())
        for i in motor_positions:
            print(i)




incremental_mover([])


# while robot.step(timestep) != -1:
#     psValues=[]
#     for i in range(8):
#         psValues.append(ps[i].getValue())
    
    


#     # found_obs = check_walls(psValues)
#     # incremental_mover([found_obs])





#     # Process sensor data here.

#     # Enter here functions to send actuator commands, like:
#     #  motor.setPosition(10.0)
#     pass

# Enter here exit cleanup code.


if this_run == 3: # clears out run files so we can relearn the position of the gem
    remove('run1.txt')
    remove('run2.txt')