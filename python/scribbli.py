from controller import Robot, DistanceSensor, Motor
import math
import csv

'''@author Ethan Fison'''

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

robot = Robot()

# initialize devices
# ps = []
# psNames = [
#     'ps0', 'ps1', 'ps2', 'ps3',
#     'ps4', 'ps5', 'ps6', 'ps7'
# ]

# for i in range(8):
#     ps.append(robot.getDistanceSensor(psNames[i]))
#     ps[i].enable(TIME_STEP)

bleftMotor = robot.getMotor('back left motor')
brightMotor = robot.getMotor('back right motor')
fleftMotor = robot.getMotor('front left motor')
frightMotor = robot.getMotor('front right motor')

bleftMotor.setPosition(float('inf'))
fleftMotor.setPosition(float('inf'))
frightMotor.setPosition(float('inf'))
brightMotor.setPosition(float('inf'))

bleftMotor.setVelocity(0.0)
fleftMotor.setVelocity(0.0)
brightMotor.setVelocity(0.0)
frightMotor.setVelocity(0.0)

pen = robot.getPen('pen')

rightEncoder=robot.getPositionSensor('front right encoder')
rightEncoder.enable(TIME_STEP)
compass = robot.getCompass('compass')
compass.enable(TIME_STEP)



def angle_math(cur,ang):
    tor = cur + ang
    if tor < 0.0:
        tor += 360.0
    if tor > 360.0:
        tor -= 360.0
    return tor



def get_bearing():
    compData=compass.getValues()
    rad = math.atan2(compData[0],compData[2])
    bearing = (rad-1.5708)/math.pi*180.0
    if bearing < 0.0:
        bearing += 360.0
    return bearing


def slow45right():
    starting_angle=get_bearing()
    while not (angle_math(starting_angle,43.6) <= get_bearing() <= angle_math(starting_angle,47.4)):
        print(get_bearing())
        robot.step(TIME_STEP)
        frightMotor.setVelocity(0)
        fleftMotor.setVelocity(.45*MAX_SPEED)
        brightMotor.setVelocity(0)
        bleftMotor.setVelocity(.45*MAX_SPEED)
    fleftMotor.setVelocity(0)
    frightMotor.setVelocity(0)
    bleftMotor.setVelocity(0)
    brightMotor.setVelocity(0)


def slow45left():
    starting_angle=get_bearing()
    while not (angle_math(starting_angle,-47.4) <= get_bearing() <= angle_math(starting_angle,-43.6)):
        print(get_bearing())
        robot.step(TIME_STEP)
        frightMotor.setVelocity(.45*MAX_SPEED)
        fleftMotor.setVelocity(0)
        brightMotor.setVelocity(.45*MAX_SPEED)
        bleftMotor.setVelocity(0)
    fleftMotor.setVelocity(0)
    frightMotor.setVelocity(0)
    bleftMotor.setVelocity(0)
    brightMotor.setVelocity(0)

def slow90left():
    slow45left()
    slow45left()

def slow90right():
    slow45right()
    slow45right()

def move_set_dist(in_dist):
    start_dist = rightEncoder.getValue()
    while (rightEncoder.getValue()-start_dist)<in_dist:
        print(rightEncoder.getValue()-start_dist)
        robot.step(TIME_STEP)
        leftSpeed  = MAX_SPEED
        rightSpeed = MAX_SPEED
        fleftMotor.setVelocity(leftSpeed)
        frightMotor.setVelocity(rightSpeed)
        bleftMotor.setVelocity(leftSpeed)
        brightMotor.setVelocity(rightSpeed)
    fleftMotor.setVelocity(0)
    frightMotor.setVelocity(0)
    bleftMotor.setVelocity(0)
    brightMotor.setVelocity(0)


def initialize():
    base_velo = .1*MAX_SPEED
    fleftMotor.setVelocity(base_velo)
    frightMotor.setVelocity(base_velo)
    bleftMotor.setVelocity(base_velo)
    brightMotor.setVelocity(base_velo)
    robot.step(TIME_STEP)
    fleftMotor.setVelocity(0)
    frightMotor.setVelocity(0)
    bleftMotor.setVelocity(0)
    brightMotor.setVelocity(0)
    robot.step(TIME_STEP)



def make_waves():
    initialize()
    pen.write(True)
    move_set_dist(12)
    for i in range(4):
        slow45right()
        move_set_dist(3)
        slow90left()
        move_set_dist(3)
        slow45right()
    move_set_dist(12)


# move_set_dist(10)

make_waves()