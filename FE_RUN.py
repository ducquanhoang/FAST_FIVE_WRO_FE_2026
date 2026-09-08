from FE_Functions import*

hub = PrimeHub()
global ep, es
ep = 0
es = 0
steer.reset_angle()
def portview():
    move.reset_angle(0)
    while True:
        print("_________    Battery     _________")
        print("battery voltage:", hub.battery.voltage()/1000)
        print("battery percentage:", Battery())
        print("_________    Motor       _________")
        print("steer enc:", steer.angle())
        print("move enc:", move.angle())
        print("move dist:", dist_cal(move.angle()))
        print("_________    Gyro        _________")
        print("gyro:", ReTheta(0))  
        print("_________    Ultrasonic  _________")
        print("Left Ultra:", sL.distance())
        print("Right Ultra:", sR.distance())
        print("_________    color     _________")
        color = 0
        rgb = s1raw.read(5)
        r = rgb[0]; g = rgb[1]; b = rgb[2]; w = rgb[3]
        if b > 1.5*r: color = -1 
        elif r > 1.5*g: color = 1
        print("R:", r, "G:", g,"B:", b,"W:", w,)
        print("color:", color)
        print("_________    camera      _________")
        val = Camera.read(0)
        print("color:", val[2])
        print("x/y:", val[0], "/", val[1])
        print("mid black percentage:", val[3])
        if val[1] >=150: 
            if val[2] == 0: angle =NumberLimit_Clamp((val[0]-160)*0.25 + 30,-85,85)
            else: angle =NumberLimit_Clamp((val[0]-160)*0.25 - 30,-85,85)
        else: angle = (val[0]-160)*0.25
        print("angle:", angle)
        wait(500)
        print("\x1b[H\x1b[2J",end="")

def Steer(angle):
    global ep, es
    error = angle - steer.angle()
    es = error + es
    controller = error* + es*0.1 
    steer.dc(controller)
    ep = error
    wait(10)

def SteerObs(angle):
    global ep, es 
    error = angle - NumberLimit_Clamp(steer.angle(), -90, 90)
    if abs(error) < 2.5: es = 0
    else: es = error + es
    controller = error*2.5# + (error - ep)*2 # + es* 0.01
    steer.dc(controller)
    ep = error
    #print("error:", error, "ep:", ep, "es:", es, "controller:", controller)
    wait(10)

def main_open():
    hub.imu.reset_heading(0)
    direction = 0
    Line_count = 0
    steer.run_target(2000, 0, Stop.HOLD, True)
    while Line_count < 24:
        color = Color_read()
        Line_count = Color_line_count(color)
        if direction == 0:
            direction = color
        angle = ReTheta(Ultra_err(170)+ Steer_err(65)*direction)
        if abs(angle) < 20: 
            pwr = 100
        else: 
            pwr = 70
        Move(pwr)
        Steer(angle)

    move.reset_angle(0)
    while move.angle() < 600:
        color = Color_read()
        Line_count = Color_line_count(color)
        if direction == 0:
            direction = color
        angle = ReTheta(Ultra_err(180)+ Steer_err(60)*direction)
        if abs(angle) < 20: 
            pwr = 100
        else: 
            pwr = 70
        # Move(pwr)
        Steer(angle)

    move.dc(0)

def main_obstacle():
    hub.imu.reset_heading(0)
    move.reset_angle(0)
    steer.run_target(2500, 0, Stop.HOLD, True)
    wait(500)
    steer.reset_angle()
    state = 1
    temp = 0
    count = 0
    direction = 0
    Line_count = 0  
    #state: 
    #1- No block, run normally(open round) until robot detects a block;  
    #2- See red/green block and run straight to it (abs(x-160)<=5) until y > 90
    #3- go to (offset angle +- 30) deg for 170 degs or black > 60.
    while Line_count < 25:

        color = Color_read()
        Line_count = Color_line_count(color)
        val = Camera.read(0)
        x = val[0]; y = val[1]; block = val[2]; black = val[3] 
        if direction == 0:
            direction = color

        angle = Ultra_err(150)+ Steer_err(80)*direction 

        if state == 1:
            if block != -1: state = 2
            else: temp = angle

        elif state == 2:
            if y >86: state = 3; move.reset_angle(0)
            elif x == 0: angle = temp
            elif abs(x - 160) > 2.5:
                angle = angle + (x-160)*0.3; temp = angle
            else: 
                temp = angle

        elif state == 3:
            if black > 60: state = 4; move.reset_angle(0)
            elif abs(move.angle()) > 245: state = 1
            elif block == 0: angle = NumberLimit_Clamp(temp + 80, angle - 90, angle + 90)
            else: angle = NumberLimit_Clamp(temp - 80, angle - 90, angle + 90)

        elif state == 4:
            if black > 70 or abs(move.angle()) >= 245: state = 1
        print(angle,"//", block, "//", state)
        
        target = NumberLimit_Clamp(ReTheta(angle), -73, 73)
        # print("line_count:", Line_count, "//dir:",direction,"//ultra:", Ultra_err(200),"//steer:",Steer_err(90), "angle:",angle, "//state:", state, "//color:", block )   
        # print("val:", val, "retheta:", ReTheta(angle), "steer:", steer.angle(), "move:", move.angle())
        # wait(200)
        # print("\x1b[H\x1b[2J",end="")
        pwr = 75 if abs(target) < 20 else 70
        Move(pwr)
        SteerObs(target)
        

    # move.reset_angle(0)
    # while move.angle() < 600:
        # color = Color_read()
        # Line_count = Color_line_count(color)
        # if direction == 0:
        #     direction = color
        # angle = ReTheta(Cam_err(90,direction))
        # if abs(angle) < 20: 
        #     pwr = 95
        # else: 
        #     pwr = 70
        # Move(pwr)
        # Steer(angle)
    move.dc(0)


# sL.lights.on(100)
# sR.lights.on(100)
main_obstacle()
#main_open()
#portview()
    