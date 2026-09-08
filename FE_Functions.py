from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task
from pybricks.iodevices import PUPDevice
from MXLineT_Lib import*

### cau hinh robot
hub = PrimeHub()
global  Line_count, Line_color, steer_old   # Khai bao ten cac motor
Line_count = 0
Line_color = 0
hub.system.set_stop_button(Button.BLUETOOTH)          
hub.speaker.volume(50)  

Camera = PUPDevice(Port.F)
                      
move = Motor(Port.B, Direction.COUNTERCLOCKWISE)      #move 
steer = Motor(Port.A, Direction.COUNTERCLOCKWISE)                                  #Steer 

s1 = ColorSensor(Port.E)                                    # cam bien di line ben trai
sL = UltrasonicSensor(Port.D)                                    # cam bien di line ben phai
sR = UltrasonicSensor(Port.C)                                    # cam bien doc mau

# # gia tri tho cua cam bien
sLraw = PUPDevice(Port.D)                                  
sRraw = PUPDevice(Port.C)
s1raw = PUPDevice(Port.E)
            
Wd = 5.6 #Wheel diameter cm
Width = 18.4 #cm
timer = StopWatch()
timerA = StopWatch(); timerD = StopWatch(); 
cal = 360 / Wd / 3.14
gear = 2.14

# #chuyen doi gia tri quang duong cm sang degree
def Enc_cal(dist):
    temp=0
    temp=dist*cal/gear
    return(temp)

def dist_cal(enc):
    temp=0
    temp=enc/cal*gear
    return(temp)

def NumberLimit_Clamp(InputNumber, Lower_Number, Upper_Number):
    if InputNumber >= Upper_Number:
        return Upper_Number
    elif InputNumber <= Lower_Number: return Lower_Number
    else:
        return InputNumber

def Battery():
    battery = NumberLimit_Clamp(hub.battery.voltage(), 6900 , 8300)
    percent = (battery-6900) / 14
    return(percent)

def Color_read():
    color = 0
    rgb = s1raw.read(5)
    r = rgb[0]; g = rgb[1]; b = rgb[2]; w = rgb[3]
    if b > 1.5*r: color = -1 
    elif r > 1.5*g: color = 1
    return color

def Color_line_count(color):
    global  Line_count, Line_color
    if color == -1 and Line_color != -1: 
        Line_count += 1; Line_color = -1
    elif color == 1 and Line_color != 1:
        Line_count += 1; Line_color = 1
    return Line_count
    
def Move(pwr):
    move.dc(pwr)

def Move_cm(pwr, cm, stop):
    Enc = move.angle()
    move.reset_angle(0)
    deg = Enc_cal(cm)
    while abs(move.angle()) < deg:
        Move(pwr)
    if stop: move.brake()
    move.reset_angle(Enc + move.angle())

def Move_enc(pwr, enc, stop):
    Enc = move.angle()
    move.reset_angle(0)
    while abs(move.angle()) < enc:
        Move(pwr)
    if stop: move.brake()
    move.reset_angle(Enc + move.angle())

def Ultra_err(dist):
    if sL.distance() < dist and sR.distance() < dist:
        err = sR.distance() - sL.distance() 
    elif sL.distance() < dist:
        err = dist - sL.distance()
    elif sR.distance() < dist:
        err = sR.distance() - dist
    else: err = 0
    return(err)

def Steer_err(corner):
    global  Line_count, Line_color
    temp = 90*(Line_count // 2) + (Line_count % 2) * corner
    # print("target:", temp, "line count:", Line_count, "Line_color:", Line_color )
    return temp

# motor move
def MotorB_On(pwr):
    motorB.dc(pwr)

def MotorB_Stop(brake):
    if brake:
        motorB.hold()
    else:
        motorB.Stop()

def MotorB_Time(pwr, sec, brake, isWait=True):
    motorB.run_time(pwr*11, sec*1000, wait=isWait)
    if not brake: motorB.stop()

def MotorB_Degs(pwr,degs, brake, isWait=True):
    motorB.run_angle(pwr*11, degs, wait=isWait)
    if not brake: motorB.stop()
    Flag = True
    return(Flag)

def MotorB_degree(pB,degree):
    Enc_B = motorB.angle()
    motorB.reset_angle(0)
    motorC.brake()
    while abs(motorB.angle()) < degree:
        motorB.dc(pB)
    Enc_B = Enc_B + pB/abs(pB)*motorB.angle()
    motorB.reset_angle(Enc_B)

def MotorB_smooth(start_pB,pB,degree):
    Enc_B = motorB.angle()
    motorB.reset_angle(0)
    motorC.brake()
    while abs(motorB.angle()) < degree:
        temp_lp = (abs(motorB.angle())/degree)*(pB-start_pB)+start_pB
        #temp_lp = start_pB + (pB - start_pB)*(abs(motorB.angle())/degree)
        motorB.dc(temp_lp)
    Enc_B = Enc_B + pB/abs(pB)*motorB.angle()
    motorB.reset_angle(Enc_B)
        
def MotorB_3step(start_pB,pB,end_pB,Accel_degree,Total_Degree,Decel_degree,Balance_degree):
    Enc_B = motorB.angle()
    MotorB_smooth(start_pB,pB,Accel_degree)
    Temp_move = abs(motorB.angle()- Enc_B)
    MotorB_degree(pB,(Total_Degree - Decel_degree - Temp_move - Balance_degree))
    MotorB_smooth(pB,end_pB,Decel_degree)
    Temp_move = abs(motorB.angle()- Enc_B)
    MotorB_degree(pB,(Total_Degree - Temp_move))

def MotorB_Angle(MinPwr, MaxPwr, angle, brake):
    temp = hub.imu.heading() + angle
    error = ReTheta(temp)
    if abs(error) >= 45:
        sign = -abs(error)/error
        MotorB_smooth(sign*MinPwr,sign*NumberLimit_Clamp((error-5)*2,MinPwr,MaxPwr), 30)
    error = ReTheta(temp)
    while abs(error)>0.5:
        error=ReTheta(temp)
        controller = error*2
        if abs(controller) < MinPwr and controller != 0:
            controller= abs(controller)/controller*MinPwr
        elif abs(controller) > MaxPwr:
            controller= abs(controller)/controller*MaxPwr
        motorB.dc(-controller)

    if brake: motorB.hold()

def MotorB_dist(pwr,dist):
    encB=Enc_cal(dist)
    MotorB_degree(pwr,encB)

def MotorB_smooth_dist(start_pB,pB,dist):
    encB=Enc_cal(dist)
    MotorB_smooth(start_pB,pB,encB)

def MotorB_3step_dist(start_pB,pB,end_pB,Accel,Total,Decel,Balance):
    encAccel=Enc_cal(Accel)
    encTotal=Enc_cal(Total)
    encDecel=Enc_cal(Decel)
    encBalance=Enc_cal(Balance)
    MotorB_3step(start_pB,pB,end_pB,encAccel,encTotal,encDecel,encBalance)

#Gyro
def Theta():
    compass = ((hub.imu.heading() % 360) + 360) % 360 
    #theta = 0 - compass if compass <= 180 else 360 - compass
    theta = compass if compass <= 180 else compass - 360
    return theta 

def Compass():
    compass = ((hub.imu.heading() % 360) + 360) % 360
    return compass

def ReTheta(angle):
    compass = (((hub.imu.heading()-angle) % 360) + 360) % 360 
    #theta = 0 - compass if compass <= 180 else 360 - compass
    theta = compass if compass <= 180 else compass - 360
    return theta 
