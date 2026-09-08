import sensor, image, time
import gc, utime
import micropython
import LPF2
from machine import Pin
from pyb import LED
micropython.alloc_emergency_exception_buf(200)

# ---------------- Color thresholds ----------------
# Format: (L_min, L_max, A_min, A_max, B_min, B_max)
# Index 0 -> RED, Index 1 -> GREEN.  This list order defines the colour ID:
#   colour 0 = red, colour 1 = green
red_threshold   = (14, 52, 45, 80, 10, 60)   # red block
red_threshold_l = (5,40,5,60,0,45) # red block darkened
red_threshold_r = (5,40,10,60,0,45) # red block darkened
green_threshold = (12, 40, -40,  -5,  -5, 35)   # green block
black_threshold = (0, 35, -15, 15, -10, 20)
white_threshold = (55, 85, -10, 20, -15, 15)
pink_threshold = (25, 40, 45, 60, 5, 35)
thresholds = [red_threshold, green_threshold, red_threshold_l,  red_threshold_r]
#(0,0,0,0,0,0)
#Define the middle ROI
mid_roi = (130, 50, 60, 40)
mid_roi3 = (70, 90, 180, 60)
mid_roi2 = (70, 150, 180, 50)
white_roi = (70, 100, 180, 100)

mid = (60, 150, 200, 60)

# ---------------- Caamera setup ----------------
sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)       # Format: RGB565
sensor.set_framesize(sensor.QVGA)         # Size: QVGA (320 x 240)
sensor.set_auto_gain(True)               # MUST be OFF for stable colour tracking
sensor.set_auto_whitebal(True)           # MUST be OFF for stable colour tracking
clock = time.clock()                      # Clock object to track the FPS

# ---------------- LUMP / LPF2 setup ----------------
# We send 4 x Int16 values: [X, Y, colour, count]  -> 8 bytes (a clean power of 2)
#   X      : centre x of the chosen block (0..320), 0 if none
#   Y      : centre y of the chosen block (0..240), 0 if none
#   colour : 0 = red, 1 = green, -1 = no block detected
#   count  : total number of red+green blocks seen this frame
modes = [LPF2.mode('OpenMV-ALL', size=8, type=LPF2.DATA16, format='3.0'),]
DataToSend = [0, 0, 0, 0, 0, 0, 0, 0]                # X, Y, colour, count
lpf2 = LPF2.Prime_LPF2(3, 'P4', 'P5', modes, 62, timer=4, freq=10)
lpf2.initialize()

# ---------------- Main loop ----------------
while True:
    # If the LEGO brick is not connected, re-initialise
    if not lpf2.connected:
        LED(1).off()
        LED(2).off()
        LED(3).on()
        lpf2.sendTimer.deinit()
        utime.sleep_ms(50)
        lpf2.initialize()
    else:

        clock.tick()
        img = sensor.snapshot()
        # Black out the top strip (beyond the game field) so its background
        # noise can never form a blob. Must be done BEFORE find_blobs().
        img.draw_rectangle((0, 0, 320, 50), color=(0, 0, 0), fill=True)
        # img.draw_rectangle(60, 200, 200, 40, color=(0, 0, 0), fill=True)
        blobs = img.find_blobs(thresholds, area_threshold=300, pixels_threshold=600)



        # --- MID ROI ---
        mid_blobs = img.find_blobs([black_threshold], roi=mid_roi, pixels_threshold=5, area_threshold=5, merge=True)
        mid_black_pixels = sum([b.pixels for b in mid_blobs])
        mid_total_pixels =  mid_roi[2] *  mid_roi[3]
        mid_black_percent = ( mid_black_pixels /  mid_total_pixels) * 100 #180


        # --- MID ROI2 ---
        mid_blobs2 = img.find_blobs([black_threshold], roi=mid_roi2, pixels_threshold=5, area_threshold=5, merge=True)
        mid_black_pixels2 = sum([b.pixels for b in mid_blobs2])
        mid_total_pixels2 =  mid_roi2[2] *  mid_roi2[3]
        mid_black_percent2 = ( mid_black_pixels2 /  mid_total_pixels2) * 100 #120

        # --- MID ROI3 ---
        mid_blobs3 = img.find_blobs([black_threshold], roi=mid_roi3, pixels_threshold=5, area_threshold=5, merge=True)
        mid_black_pixels3 = sum([b.pixels for b in mid_blobs3])
        mid_total_pixels3 =  mid_roi3[2] *  mid_roi3[3]
        mid_black_percent3 = ( mid_black_pixels3 /  mid_total_pixels3) * 100

        # # Draw the MID ROI box on the IDE preview (blue outline)
        img.draw_rectangle(mid_roi, color=(0, 0, 255))
        img.draw_rectangle(mid_roi2, color=(0, 0, 255))
        img.draw_rectangle(mid_roi3, color=(0, 0, 255))

        max_size    = 0
        block_x     = 0
        block_y     = 0
        block_color = -1      # -1 = nothing found
        count       = 0

        for b in blobs:
            if b.code & 1 or b.code & 4 or b.code & 8:
                color = 0                # red
                draw_col = (255, 0, 0)
            elif b.code & 2:
                color = 1                 # green
                draw_col = (0, 255, 0)
            else:

                continue

            # Density (extent) = blob pixels / bounding-box area. A solid block
            # sits near 1.0; ragged background noise is much lower. Only blobs
            # that fill at least 80% of their bounding box qualify.
            if b.code & 1:
                print("red1")
                print (b.density)
            elif b.code & 4:
                print("red2")
                print (b.density)
            elif b.code & 8:
                print("red3")
                print (b.density)
            elif b.code & 2:
                print("green")
                print (b.density)

            if b.density < 0.63  and b.code & 1:
                continue
            if b.density < 0.63 and b.code & 2:
                continue
            if b.density < 0.55 and (b.code & 4 or b.code & 8):
                continue
            if b.area < 600:
                continue
            if b.w/b.h > 0.95:
                continue
            if (mid_black_percent3 > 60) and b.y < 80:
                continue
            if mid_black_percent2 >= 50 and b.y < 90:
                continue
            if mid_black_percent3 >= 80 and b.y < 150:
                continue

            # Debug drawing on the IDE preview
            img.draw_rectangle(b.rect, color=draw_col)
            # img.draw_cross(b.cx(), b.cy(), color=draw_col)
            count += 1

            # Keep the largest blob = the closest / most relevant block
            if b.cy > block_y:
                max_size    = b.area
                block_x     = b.cx
                block_y     = b.cy
                block_color = color

            if block_color == -1:
                LED(1).off()
                LED(2).off()
                LED(3).off()
            elif block_color == 0:
                LED(1).on()
                LED(2).off()
                LED(3).off()
            else:
                LED(1).off()
                LED(2).on()
                LED(3).off()



        mid_black_percent = max(mid_black_percent, mid_black_percent2) if count == 0 else mid_black_percent2
        img.draw_string((1, 1), "X:%d Y:%d Color:%d Count:%d Black:%d FPS:%d" %
                (block_x, block_y, block_color, count, mid_black_percent, int(clock.fps())))



        DataToSend = [block_x, block_y, block_color, int(mid_black_percent)]

        # print (block_x, block_y, block_color, count, max_size)
        # Send the data to the Spike Prime hub
        if lpf2.current_mode == 0:
            lpf2.load_payload('Int16', DataToSend)
