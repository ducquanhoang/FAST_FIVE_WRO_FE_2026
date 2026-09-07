# Name_WRO_FE_2026
## WRO Future Engineers - Robotics Project Documentation

### Our team
| Photo | Member Name     | Role & Experience |
| ----- | --------------- | ----------------- |
| ![Uploading image.png…]()| Nguyễn Tự Tuyển | ...               |
| ...   | Hoàng Đức Quân  | ...               |

## Table of Contents
- [1. Overview](#1-overview)
  - [1.1 About the Project](#11-about-the-project)
  - [1.2 Robot Images](#12-robot-images)
- [2. Mobility Management](#2-mobility-management)
  - [2.1 Drive System](#21-drive-system)
  - [2.2 Steering](#22-steering)
  - [2.3 Chassis Design](#23-chassis-design)
- [3. Power and Sense Management](#3-power-and-sense-management)
  - [3.1 Power Source](#31-power-source)
  - [3.2 Sensors and Camera](#32-sensors-and-camera)
  - [3.3 Processing Units](#33-processing-units)
  - [3.4 Port / Wiring Map](#34-port--wiring-map)
  - [3.5 Power Consumption](#35-power-consumption)
- [4. Obstacle Management](#4-obstacle-management)
  - [4.1 Open Challenge](#41-open-challenge)
  - [4.2 Obstacle Challenge](#42-obstacle-challenge)
  - [4.3 Parallel Parking](#43-parallel-parking)
- [5. Source Code](#5-source-code)
  - [5.1 Code Overview](#51-code-overview)
  - [5.2 Code Structure](#52-code-structure)
  - [5.3 Upload / Run Instructions](#53-upload--run-instructions)
- [6. List of Components](#6-list-of-components)
- [7. 3D Model Files](#7-3d-model-files)
- [8. Building Instructions](#8-building-instructions)

---

## 1. Overview

### 1.1 About the Project

This project of ours is a self‑driving car for the WRO Future Engineers category. The car's a vehicle that can finish the Open Challenge, which asks for three laps on a random track without touching a wall. The car can also complete the Obstacle Challenge, which requires three laps while reading green traffic signs and then doing parallel parking. 

This is the year our team has competed in this category, so much of the project involved learning engineering and programming skills from scratch.

Our robot is built on a custom LEGO Technic + 3D-printed (PLA) chassis, in a rear-wheel differential-drive, Ackermann front-steer configuration, controlled by a LEGO® Education SPIKE™ Prime Hub and a Matrix Robotics M-Vision Cam for onboard image processing. Design priorities, in order, were: a low center of gravity for stability, a lightweight structure to reduce motor strain, and a minimal footprint for maneuverability.

### 1.2 Robot Images

---

## 2. Mobility management
Design objective: Our chassis is built around 3 goals: stability (keep a low, balanced center of gravity so the robot doesn’t tip or wobble to the side during hard turns or sudden acceleration, and a steady drive base for the camera), efficiency (a lightweight structure so the drive motor isn't fighting excess mass), and maneuverability (a compact footprint that can navigate tight corners and obstacles without sacrificing control).
Motor: LEGO® Technic™ Large Angular Motor (drives the rear differential)
### 2.1 Drive System

Specifications
* Connector: LEGO® Power Functions 2.0 (LPF2)
* Voltage range: 5–9V (SPIKE Hub nominal: 7.2V)
* No-load speed: ~175 RPM (team measurement, vs ~135 RPM for the stock SPIKE-branded Large Angular Motor)
* Feedback: integrated rotation/position sensor|

Reason for Selection

Higher RPM than the stock SPIKE motor, for faster lap times on the flat competition arena.
Smaller footprint with more mounting-hole positions on the case, giving flexibility in where it sits on the chassis.
Built-in rotation sensor gives closed-loop feedback for encoder-based distance/angle control.

### 2.2 Steering
Motor: LEGO® Technic™ Large Angular Motor + 1:1 gearbox

Specifications
* Connector: LPF2
* Voltage range: 5–9V
* Stall torque: ~40 N·cm with the 1:1 gearbox (team measurement, vs ~25 N·cm for the stock SPIKE Angular Motor)
* Feedback: integrated rotation/position sensor, used for heading/angle-based turns (`MotorB_Angle`)
* Reason for Selection :Highest available stall torque among LEGO Powered Up motors, needed to move the Ackermann linkage under load.
Position feedback lets steering angle be driven and held precisely rather than open-loop.

Ackermann steering:
When a car turns, the inner and outer front wheels trace circles of different radii, so they need to point at different angles. The inner wheel turns sharper than the outer one. Our steering linkage approximates this relationship so all four wheels roll cleanly with minimal sideways scrubbing, which improves turning accuracy and cuts down on friction losses. 

Why does this happen geometrically?
For a vehicle to corner without any wheel sliding sideways, every wheel has to travel along a circular arc, and all of those arcs must share one common center point: the instantaneous center of rotation (ICR). A wheel only rolls cleanly when its axle points directly at that center. Because our rear axle is fixed, both rear wheels share the same axis line, which pins the ICR somewhere along the extension of that line. The two front wheels then have to angle themselves so their own axle lines also converge on that same point and since the inner front wheel is physically closer to the ICR, it has to turn through a tighter circle, meaning a larger steering angle than the outer wheel. 

The math behind it: for wheelbase L, track width T, and inner/outer steering angles δᵢ and δₒ, the condition that keeps both front axle lines meeting the rear axle line at one point works out to:
cot(δₒ) − cot(δᵢ) = T / L
This relationship isn't linear; the required gap between the two angles grows a lot faster than the angles themselves. At a shallow ~10° steering input the difference between inner and outer angle is only about 1°, but near full lock (~30°) that gap widens to 8° or more. If we'd built a rigid linkage that just kept both wheels parallel, it would look almost correct while driving straight or gently curving, and be badly wrong exactly when precision matters most: sharp corners or a parking maneuver.

Wheels: 49.5 mm SPIKE wheels (front)

Small diameter for agility and quick direction changes at the steered wheels.

Considerations

Even with the 1:1 gearbox, torque at the steering linkage was tighter than expected after the first v2 build - a candidate area to revisit (e.g. a different gear ratio or linkage geometry) if we find the robot under-steering at speed.
### 2.3 Chassis Design

Main chassis: LEGO SPIKE Prime Hub, drive and steering motors, ultrasonic sensors, line sensor, structural connectors, and wheel assemblies. 
Rear camera assembly: A structure to hold the Matrix Camera M-Vision AI Cam. 

Why We Put the Camera to the Rear: 
Raising the camera and pushing it toward the rear gives the vision system a much wider field of view, which lets the robot spot the wall and obstacles earlier and more consistently. The trade-off is that a tall mast sitting up high introduces a real risk of tipping the robot, so we had to design the robot so it doesn't tip or wobble to the side during hard turns or sudden acceleration.

Keeping the Elevated Camera From Tipping the Robot: 
To make sure the taller rear mast wouldn't make the robot unstable, we ran a basic static-moment analysis using the rear wheels' contact line with the ground as the pivot point. We compared two moments: 
M₁ - the restoring moment from the main chassis (its mass × its distance from the pivot)
M₂ - the overturning moment from the rear mast/counterweight assembly (its mass × its distance from the pivot)
The robot will stay upright as long as M₁ ≥ M₂, i.e., as long as the main chassis's moment is greater than or equal to the rear assembly's moment. 

Since the main chassis's mass and position are essentially locked in (the hub, motors, and sensors don't move), the only variable we could actually control was the rear assembly. So we minimized both its mass and its distance from the pivot: the camera mount itself, which accounts for most of the rear assembly's weight, sits as close to the pivot as the design allows.


## 3. Power and Sense Management

### 3.1 Power Source

**Battery:** SPIKE Prime rechargeable Li-ion Hub Battery

**Specifications**
- Type: rechargeable lithium-ion, charged in-hub via micro-USB
- Capacity: ~2,000–2,100 mAh (per LEGO Education spare-part listings)
- Working range used in our firmware: 6,900–8,300 mV (see `Battery()` in §5), consistent with a 2-cell Li-ion pack

| Component | Voltage | Current (typical) | Current (peak) | Power (typical) |
|---|---|---|---|---|
| Hub | 7.2 V | 1.0 A | 1.5 A | 7.2 W |
| Camera | 5 V | 0.15 A | 0.3 A | 0.75 W |
| Ultrasonic ×2 | 5 V | 0.04 A | 0.06 A | 0.2 W |
| Drive motors ×2 | 7.2 V | 1.0 A | 2 A | 7.2 W |
| **Total** | | **2.19 A** | **3.86 A** | **15.35 W** |

The battery powers the SPIKE Prime Hub directly; the Hub in turn supplies all motors and sensors over their LPF2 leads, and the M-Vision Cam over its dedicated 5V cable - no separate step-up/step-down conversion is needed anywhere in the system, since the camera's 5V input matches the Hub's output.

Our firmware reads `hub.battery.voltage()`, clamps it to the 6,900–8,300 mV working range, and converts it to a 0–100% estimate so we can catch a low-charge robot before a run.

**Considerations**

Because everything runs off one Hub battery with no separate motor supply, our power architecture is much simpler than a Raspberry Pi-class system (no MOSFET power-switching, no DC-DC boost converter, no separate motor driver IC) - the tradeoff is that we're bound to whatever voltage/current the Hub itself can deliver.
### 3.2 Sensors and Camera

### 3.3 Processing Units

### 3.4 Port / Wiring Map

### 3.5 Power Consumption

---

## 4. Obstacle Management

### 4.1 Open Challenge

### 4.2 Obstacle Challenge

### 4.3 Parallel Parking

---

## 5. Source Code

### 5.1 Code Overview

### 5.2 Code Structure

### 5.3 Upload / Run Instructions

---

## 6. List of Components

---

## 7. 3D Model Files

---

## 8. Building Instructions
