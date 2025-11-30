# Python Project - Intel RealSense D435i Launcher

This repository contains all the material and tools developed for working with the Intel RealSense D435i depth camera, including:

- A technical description of the device  
- Installation and setup instructions  
- Requirements and constraints for correct operation  
- A Python-based launcher program (`launcher.py`)  
- Details about the output data format  

---

## Repository Structure

```
main_repository/
│
├── description.pdf
├── launcher.py
├── LICENSE
└── README.md
```

The goal of this project is to provide a complete setup, executable Python launcher, and technical documentation for acquiring:

- **Depth data**
- **Color data**
- **IMU measurements** (accelerometer + gyroscope)

using the Intel RealSense D435i.

The project allows users to:

- Correctly install the RealSense SDK  
- Start recordings via a Python script from the terminal  
- Automatically save output data in structured `.csv` files  
- Validate parameters such as serial number, duration, and filename  

---

# 1. System Description

The Intel RealSense D435i is an advanced depth camera designed for applications requiring accurate 3D environmental perception.

## 1.1 Main Features

- Stereo depth sensor using dual IR cameras  
- Depth range: **0.2 m to ~10 m**  
- Wide Field of View: **86° × 57° × 94°**  
- Integrated **6DoF IMU** (accelerometer + gyroscope)  
- High resolution & frame rate  
  - Depth: up to **1280×720 @ 30 FPS**  
  - RGB: up to **1920×1080**  
- Dedicated Intel D4 vision processor  
- Compact and robust design suitable for robotics  

## 1.2 Applications

- Autonomous robotics  
- AR/VR motion tracking  
- Security and surveillance  
- Healthcare monitoring  
- Industrial inspection and automation  

## 1.3 Advantages

- High precision depth sensing  
- Integrated motion tracking  
- Robust performance across lighting conditions  
- SDK support for multiple programming languages  

---

# 2. Requirements for Correct Operation

Correct functioning of the D435i requires meeting hardware, software, and environmental specifications.

## 2.1 System Requirements

### **Hardware**
- Intel i5 or higher  
- ≥ 4 GB RAM (≥ 8 GB recommended)  
- USB 3.1 (USB 2.0 possible but limited)

### **Operating Systems**
- Windows 10/11 (64-bit)  
- Ubuntu 16.04+  
- macOS (partial limitations)

### **Software**
- Intel RealSense SDK 2.0  
- Support for C++, Python, OpenCV, ROS  

## 2.2 Constraints

- Optimal performance in **medium lighting**  
- Maximum reliable depth: ~10 m  
- Operating temperature: **0°C to 35°C**  
- Sensitive to IR interference  
- Not dustproof/waterproof without external housing  

## 2.3 Additional Notes

- Calibration may be required  
- Synchronization needed when used with external sensors  

---

# 3. Installation & Setup

## 3.1 Using the RealSense SDK

Instructions include:

- Installing SDK on Windows or Linux  
- Cloning and building `librealsense`  
- Verifying device recognition (`lsusb`, Device Manager)  
- Running **Intel RealSense Viewer**  
- Keeping firmware and SDK updated  

---

## 3.2 Using the Python Launcher (`launcher.py`)

Before running the program, install the required Python libraries:
```bash
pip install numpy
pip install pyrealsense2
```

Check Python installation:
```bash
python --version
```

Run the program:
```bash
python launcher.py [arguments]
```

### Accepted Optional Arguments (any order)

- **Camera serial number** (12 digits)  
- **Recording duration** (seconds)  
- **Output file name** (letters or alphanumeric, starting with a letter)

If any parameter is missing or invalid, the launcher will request it interactively.

---

## During Execution, the Program:

- Displays **depth and color preview**  
- Highlights the **IR dot** on the central sensor  
- Saves four CSV files:
  1. [name] depth data.csv
  2. [name] color data.csv
  3. [name] accel data.csv
  4. [name] gyro data.csv

---

# 4. Usage Instructions

The program may request:

- Valid **serial number** (12 digits)  
- Valid **output filename**  
- Whether to manually set recording duration  
- **Duration in seconds (>0)**  

Invalid inputs trigger an error and a new prompt.

If all arguments are correctly provided in the command line, **no interaction is required**.

---

# 5. Output Description

The `.csv` files contain all acquired depth, color, and IMU data.

## 5.1 Depth & Color Data Fields

- Timestamp (`aaaammgg_hhmmss_mmm`)  
- Frame number  
- Minimum / average / maximum distance (mm)  
- Bits per pixel  
- Bytes per pixel  
- Frame width & height  
- Stride in bytes  

## 5.2 Accelerometer & Gyroscope Data Fields

- Timestamp  
- Frame number  
- Common fields (min/avg/max distance)  
- X, Y, Z values  
  - Acceleration: **m/s²**  
  - Angular velocity: **rad/s**  
- Orientation (rad)  
- Magnitude (total acceleration/velocity)  

---

# Running the Project

Once setup is complete:

1. Connect the **Intel RealSense D435i**  
2. Install required libraries  
3. Run:
```bash
python launcher.py
```
4. Provide inputs if requested
5. Retrieve output CSV files in the data/ folder
