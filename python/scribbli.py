from controller import *
import math

'''@author Ethan Fison'''

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

robot = Robot()

'''Gathering up all of the components that get used'''
bleftMotor = robot.getMotor('wheel3')
brightMotor = robot.getMotor('wheel4')
fleftMotor = robot.getMotor('wheel1')
frightMotor = robot.getMotor('wheel2')

bleftMotor.setPosition(float('inf'))
fleftMotor.setPosition(float('inf'))
frightMotor.setPosition(float('inf'))
brightMotor.setPosition(float('inf'))

bleftMotor.setVelocity(0.0)
fleftMotor.setVelocity(0.0)
brightMotor.setVelocity(0.0)
frightMotor.setVelocity(0.0)

rightEncoder=robot.getPositionSensor('front right encoder')
rightEncoder.enable(TIME_STEP)
compass = robot.getCompass('compass')
compass.enable(TIME_STEP)


'''This is commented out because it keeps crashing my program'''
pen=robot.getPen('pen')
# pen.write(True)



def angle_math(ang):
    tor = ang
    if tor < 0.0:
        tor += 360.0
    if tor > 360.0:
        tor -= 360.0
    return tor

'''This tries to correct for the 4.2 degree wedge centered at north that the turns can't do checks at'''
def compare_angles(initial_angle,to_comp,bound):
    raw_lb=initial_angle+(bound-1.4)
    raw_ub=initial_angle+(bound+1.2)
    lb=angle_math(raw_lb)
    ub=angle_math(raw_ub)
    if lb>=357.4 or ub<=2.6:
        if to_comp<360.0:
            ub=lb+2.6
        elif to_comp>0:
            lb=ub-2.6
    
    return (lb<=to_comp<=ub)

def get_bearing():
    compData=compass.getValues()
    rad = math.atan2(compData[0],compData[2])
    bearing = (rad-1.5708)/math.pi*180.0
    if bearing < 0.0:
        bearing += 360.0
    return bearing


'''
45 degree turns in either direction. The small time step makes it hard to get a truly continuous read off
of the compass, so I have these use ranges that should get close enough to 45 to work. This was the best solution
I could find to the robot infinitely spinning. Doesn't work all that well when the turn would pass over the 0/360 degree mark
'''

def slow45right():
    starting_angle=get_bearing()
    print(starting_angle)
    while not (compare_angles(starting_angle,get_bearing(),45)):
        print(starting_angle,get_bearing())
        robot.step(TIME_STEP)
        frightMotor.setVelocity(0)
        fleftMotor.setVelocity(.4*MAX_SPEED)
        brightMotor.setVelocity(0)
        bleftMotor.setVelocity(.4*MAX_SPEED)
    fleftMotor.setVelocity(0)
    frightMotor.setVelocity(0)
    bleftMotor.setVelocity(0)
    brightMotor.setVelocity(0)


def slow45left():
    starting_angle=get_bearing()
    while not (compare_angles(starting_angle,get_bearing(),-45)):
        print(starting_angle,get_bearing())
        robot.step(TIME_STEP)
        frightMotor.setVelocity(.3*MAX_SPEED)
        fleftMotor.setVelocity(0)
        brightMotor.setVelocity(.3*MAX_SPEED)
        bleftMotor.setVelocity(0)
    fleftMotor.setVelocity(0)
    frightMotor.setVelocity(0)
    bleftMotor.setVelocity(0)
    brightMotor.setVelocity(0)


'''
The below two functions just call 45 degree turns twice, which should get close enough to a 90 degree
to get the desired result. There is some imprecision because the small time step doesn't allow for 
continuous compass reads
'''

def slow90left():
    slow45left()
    slow45left()

def slow90right():
    slow45right()
    slow45right()

'''
Title pretty much says it all. Uses encorder data from the front right wheel to move
by a delta of in_dist
'''
def move_set_dist(in_dist):
    start_dist = rightEncoder.getValue()
    while (rightEncoder.getValue()-start_dist)<in_dist:
        #print(rightEncoder.getValue()-start_dist)
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

'''Moves the robot by a very small amount so none of the sensors report null'''
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
    #pen.write(True)



'''Simple repeated calls to make the robot move in four wave patterns'''
def make_waves():
    initialize()
    move_set_dist(12)
    for i in range(4):
        slow45right()
        move_set_dist(3)
        slow90left()
        move_set_dist(3)
        slow45right()
    move_set_dist(11)


# move_set_dist(10)

'''This is effectively the main for this program'''
make_waves()