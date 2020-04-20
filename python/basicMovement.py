from controller import Robot, DistanceSensor, Motor
import math

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

MAX_TURN_CHECKS = 37
TURN_DELAY = 10
JUNCTION_WINDOW = 2

IGNORE_FW_WALLS = False

# create the Robot instance.
robot = Robot()

# initialize devices
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(TIME_STEP)

leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)
rightEncoder=robot.getPositionSensor('right wheel sensor')
leftEncoder=robot.getPositionSensor('left wheel sensor')
rightEncoder.enable(TIME_STEP)
leftEncoder.enable(TIME_STEP)
compass = robot.getCompass('compass')
compass.enable(TIME_STEP)


rel_x = 0
rel_y = 0
last_enc=0


junction_coords = []
bad_turns = []

def continuous_left():
    wall_counter = 0
    while robot.step(TIME_STEP) != -1:
        psValues = []
        # print('turning left')
        for i in range(8):
            psValues.append(ps[i].getValue())
        # print('left',psValues[5])
        # print('right',psValues[2])
        left_open = psValues[5] < 55
        right_open = psValues[2] < 63# or psValues[7] > 80
        leftSpeed =.1 * MAX_SPEED
        rightSpeed = MAX_SPEED
        if psValues[7] > 120:
            return
        if not right_open and not left_open:
            wall_counter+=1
            # print('Left checks:',wall_counter)
        if wall_counter == MAX_TURN_CHECKS:
            return
        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)



def continuous_right():
    wall_counter = 0
    while robot.step(TIME_STEP) != -1:
        psValues = []
        #print('turning right')
        for i in range(8):
            psValues.append(ps[i].getValue())
        # print('left',psValues[5])
        # print('right',psValues[2])
        left_open = psValues[5] < 63
        right_open = psValues[2] < 55
        leftSpeed = MAX_SPEED
        rightSpeed = .1 * MAX_SPEED
        if psValues[0] > 120:
            return
        if not right_open and not left_open:
            wall_counter+=1
            # print('Right checks;', wall_counter)
        if wall_counter == MAX_TURN_CHECKS:
            return
        rightMotor.setVelocity(rightSpeed)
        leftMotor.setVelocity(leftSpeed)


def one_eighty():
    forward_counter = 0
    while robot.step(TIME_STEP) != -1:
        psValues = []
        for i in range(8):
            psValues.append(ps[i].getValue())
        front_obstacle = psValues[0] > 75 and psValues[7] > 75
        if not front_obstacle:
            forward_counter += 1
        if forward_counter == 20:
            return
        rightMotor.setVelocity(-MAX_SPEED)
        leftMotor.setVelocity(MAX_SPEED)
        

def update_coords(rads, current_encoding, previous_encoding):
    global rel_x
    global rel_y
    delta_encoding = current_encoding-previous_encoding
    rel_x+=(delta_encoding*math.cos(rads))
    rel_y+=(delta_encoding*math.sin(rads))


def buildJunctionSubarray(inx,iny):
    inx_low=inx-2
    inx_high=inx+2
    iny_low=iny-2
    iny_high=iny+2
    subarray = [inx_low,inx_high,iny_low,iny_high]
    junction_coords.append(subarray)
    print('Turn at', inx,',',iny,"marked once")




def convertLameVectorToCoolRadians(vector):
    rad = math.atan2(vector[0],vector[2])
    return rad

def turn_already_checked(inx,iny):
    global junction_coords
    for sub in junction_coords:
        if (inx > sub[0] and inx < sub[1])and(iny > sub[2] and iny < sub[3]):
            bad_turns.append(sub)
            print('Turn at', inx,',',iny,"marked bad")
            return True


# feedback loop: step simulation until receiving an exit event
wait_for_junction = 0
time_between_ticks = 0
add_delay = False
while robot.step(TIME_STEP) != -1:
    compass_data = compass.getValues()
    bearing = convertLameVectorToCoolRadians(compass_data)
    # print(bearing)

    # read sensors outputs
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    rEnc = int(rightEncoder.getValue())
    lEnc = int(leftEncoder.getValue())
    update_coords(bearing,lEnc,last_enc)
    # print('Coords:',rel_x,',',rel_y)
    #print('Right encoder:',rEnc)
    #print('Left encoder:', lEnc)
    # print('left',psValues[5])
    # print('right',psValues[2])
        #print(i,psValues[i])
    # detect obstacles
    right_obstacle = psValues[1] > 85.0
    left_obstacle = psValues[6] > 85.0
    front_obstacle = psValues[0] > 80 and psValues[7] > 80
    #print(psValues[5])
    left_open = psValues[5] < 66
    right_open = psValues[2] < 66
    # initialize motor speeds at 50% of MAX_SPEED.
    leftSpeed  = 0.5 * MAX_SPEED
    rightSpeed = 0.5 * MAX_SPEED
    # modify speeds according to obstacles


    if wait_for_junction > 0:
        wait_for_junction += 1
        # print("junction delay:", wait_for_junction)


    if time_between_ticks == TURN_DELAY:
        add_delay = False
        time_between_ticks = 0
        #wait_for_junction = 0
    if add_delay:
        time_between_ticks+=1
        # print('delay:', time_between_ticks)


    if time_between_ticks == 0:
        
        if wait_for_junction > JUNCTION_WINDOW:   
                        
            if left_open and right_open:
                wait_for_junction = 0
                add_delay = True
                continuous_right()
                # if turn_already_checked():
                #     continuous_left()
                if not  turn_already_checked(rel_x,rel_y):
                    buildJunctionSubarray(rel_x,rel_y)              
            elif left_open:
                wait_for_junction = 0
                add_delay = True
                continuous_left()
                if not  turn_already_checked(rel_x,rel_y):
                    buildJunctionSubarray(rel_x,rel_y)
            elif right_open:
                wait_for_junction = 0
                add_delay = True
                continuous_right()
                if not  turn_already_checked(rel_x,rel_y):
                    buildJunctionSubarray(rel_x,rel_y)
        elif left_open or right_open and wait_for_junction == 0:
            wait_for_junction +=1
    if wait_for_junction == 0:    
        if front_obstacle and left_obstacle and right_obstacle:
            add_delay
            one_eighty()
        if left_obstacle:
            # turn right
            leftSpeed  += 0.5 * MAX_SPEED
            rightSpeed -= 0.5 * MAX_SPEED
        elif right_obstacle:
            # turn left
            leftSpeed  -= 0.5 * MAX_SPEED
            rightSpeed += 0.5 * MAX_SPEED
    # else: 
    #     leftSpeed = .1 * MAX_SPEED
    #     rightSpeed = .1 * MAX_SPEED
    # write actuators inputs
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
    last_enc = lEnc