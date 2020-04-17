from controller import Robot, DistanceSensor, Motor

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

MAX_TURN_CHECKS = 38
TURN_DELAY = 15
JUNCTION_WINDOW = 2

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


def continuous_left():
    wall_counter = 0
    while robot.step(TIME_STEP) != -1:
        psValues = []
        print('turning left')
        for i in range(8):
            psValues.append(ps[i].getValue())
        print('left',psValues[5])
        print('right',psValues[2])
        left_open = psValues[5] < 55
        right_open = psValues[2] < 63# or psValues[7] > 80
        leftSpeed =.1 * MAX_SPEED
        rightSpeed = MAX_SPEED
        if not right_open and not left_open:
            wall_counter+=1
            print('Left checks:',wall_counter)
        if wall_counter == MAX_TURN_CHECKS:
            return
        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)



def continuous_right():
    wall_counter = 0
    while robot.step(TIME_STEP) != -1:
        psValues = []
        print('turning right')
        for i in range(8):
            psValues.append(ps[i].getValue())
        print('left',psValues[5])
        print('right',psValues[2])
        left_open = psValues[5] < 63
        right_open = psValues[2] < 55
        leftSpeed = MAX_SPEED
        rightSpeed = .1 * MAX_SPEED
        if not right_open and not left_open:
            wall_counter+=1
            print('Right checks;', wall_counter)
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
        



def turn_already_checked(inputs):
    return False


# feedback loop: step simulation until receiving an exit event
wait_for_junction = 0
time_between_ticks = 0
add_delay = False
while robot.step(TIME_STEP) != -1:

    # read sensors outputs
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    print('left',psValues[5])
    print('right',psValues[2])
        #print(i,psValues[i])
    # detect obstacles
    right_obstacle = psValues[1] > 75.0
    left_obstacle = psValues[6] > 75.0
    front_obstacle = psValues[0] > 75 and psValues[7] > 75
    #print(psValues[5])
    left_open = psValues[5] < 66
    right_open = psValues[2] < 66
    # initialize motor speeds at 50% of MAX_SPEED.
    leftSpeed  = 0.5 * MAX_SPEED
    rightSpeed = 0.5 * MAX_SPEED
    # modify speeds according to obstacles


    if wait_for_junction > 0:
        wait_for_junction += 1
        print("junction delay:", wait_for_junction)


    if time_between_ticks == TURN_DELAY:
        add_delay = False
        time_between_ticks = 0
        #wait_for_junction = 0
    if add_delay:
        time_between_ticks+=1
        print('delay:', time_between_ticks)


    if time_between_ticks == 0:
        
        if wait_for_junction > JUNCTION_WINDOW:   
                        
            if left_open and right_open:
                wait_for_junction = 0
                add_delay = True
                continuous_left()
                if turn_already_checked('potato'):
                    continuous_right()
            elif left_open:
                wait_for_junction = 0
                add_delay = True
                continuous_left()
            elif right_open:
                wait_for_junction = 0
                add_delay = True
                continuous_right()
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
    else: 
        leftSpeed = .1 * MAX_SPEED
        rightSpeed = .1 * MAX_SPEED
    # write actuators inputs
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)