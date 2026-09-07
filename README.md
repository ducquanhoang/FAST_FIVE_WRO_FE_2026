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
| Photo | Specifications 
* Connector: LEGO® Power Functions 2.0 (LPF2)
* Voltage range: 5–9V (SPIKE Hub nominal: 7.2V)
* No-load speed: ~175 RPM (team measurement, vs ~135 RPM for the stock SPIKE-branded Large Angular Motor)
* Feedback: integrated rotation/position sensor||  |
| ----- | --------------- | ----------------- |
Specifications
* Connector: LEGO® Power Functions 2.0 (LPF2)
* Voltage range: 5–9V (SPIKE Hub nominal: 7.2V)
* No-load speed: ~175 RPM (team measurement, vs ~135 RPM for the stock SPIKE-branded Large Angular Motor)
* Feedback: integrated rotation/position sensor|

Reason for Selection

Higher RPM than the stock SPIKE motor, for faster lap times on the flat competition arena.
Smaller footprint with more mounting-hole positions on the case, giving flexibility in where it sits on the chassis.
Built-in rotation sensor gives closed-loop feedback for encoder-based distance/angle control (see Enc_cal, MotorB_degree in §5).

### 2.2 Steering

### 2.3 Chassis Design

---

## 3. Power and Sense Management

### 3.1 Power Source

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
