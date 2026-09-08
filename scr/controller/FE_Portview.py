from FE_Functions import*
print("\x1b[H\x1b[2J",end="")
motorB.reset_angle(0)
motorC.reset_angle(0)
Time_End = StopWatch()
print("\x1b[H\x1b[2J",end="")
while True: 

    print("Battery:",str(hub.battery.voltage()/1000)[0:3],"/8.0 (V)", str(hub.battery.voltage()/10 / 8), "%")
    print("--gyro--")
    heading = hub.imu.heading()
    print("gyro:",heading,"degs")
    print("Compass:", Compass())
    print("Theta:",Theta())
    print("ThetaXY:", ReTheta(0))

    print("--CAM--")
    val = Camera.read(0) #purple_x, purple_y , orange_x, orange_y
    print(val)
    print("*purple*/ x:", val[0], "y:",val[1]//10, "quantity:",val[1]%10)
    print("*orange*/ x:", val[2], "y:",val[3]//10, "quantity:",val[3]%10)

    print("--Sensor--")
    print("Ultra_left/Ultra_right:", sL.distance(),"/", sR.distance())
    print("ultra raw:", sLraw.read(0), "/", sRraw.read(0))
    print("colorsensor raw:", s1raw.read(5))

    print("--motor--")
    print("Move_EncB:",motorB.angle(),"Steer_EncC:",motorC.angle())

    if (Button.CENTER in hub.buttons.pressed()):
        hub.speaker.beep(698, 200)
        motorB.reset_angle(0)
        motorC.reset_angle(0)
        wait(1000)
    wait(1000)
    print("\x1b[H\x1b[2J",end="")

