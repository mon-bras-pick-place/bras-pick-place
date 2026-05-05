# MuJoCo Pick and Place Simulation - 6DOF Robot Arm

ROS 2 Jazzy Jalisco project simulating a 6-DOF robotic arm (uFactory Lite6) performing pick-and-place operations in MuJoCo.

## 🎥 Demo
Watch the robot arm perform a pick-and-place operation:

![Pick and Place Demo](demo/RECORD.gif)

The robot arm picks up a red box from a table and places it on a green target zone.

## 📋 Prerequisites
- Ubuntu 24.04
- ROS 2 Jazzy Jalisco
- Python 3.12+
- MuJoCo 3.7+

## 🛠️ Installation

### 1. Install MuJoCo
```bash
pip3 install mujoco --break-system-packages
```

### 2. Clone and Build
```bash
cd ~/ros2_ws/src
git clone <your-repo-url>
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select mon_bras_pick_place --symlink-install
source install/setup.bash
```

## 🚀 Running the Simulation

### Option 1: Direct MuJoCo Simulation (Simplest)
```bash
source ~/ros2_ws/install/setup.bash
ros2 run mon_bras_pick_place pick_place
```

### Option 2: ROS 2 Controlled
```bash
# Terminal 1: Start simulation
source ~/ros2_ws/install/setup.bash
ros2 run mon_bras_pick_place pick_place

# Terminal 2: Send pick-and-place commands
source ~/ros2_ws/install/setup.bash
ros2 run mon_bras_pick_place ros_control
```

## 🎮 What You'll See
- MuJoCo viewer opens showing:
  - uFactory Lite6 6-DOF robot arm
  - Table with red box (pickup target)
  - Green cylinder (drop zone)
- Robot automatically performs pick-and-place sequence
- Smooth interpolated movements between positions

## 📁 Project Structure
```
mon_bras_pick_place/
├── mon_bras_pick_place/      # Python source code
│   ├── pick_place_node.py    # Main simulation with MuJoCo
│   └── ros_control_node.py   # ROS 2 trajectory commander
├── models/                    # uFactory Lite6 3D models
│   ├── lite6.xml
│   └── assets/
├── worlds/                    # MuJoCo scene files
│   └── lite6_scene.xml
├── config/                    # ROS 2 controller config
│   └── controllers.yaml
└── setup.py                   # Package configuration
```

## 🔧 Robot Specifications
- **Model:** uFactory Lite6
- **Degrees of Freedom:** 6
- **Control Method:** Joint position control
- **Simulation Engine:** MuJoCo 3.7+

## 📝 Sequence Steps
1. Move arm above box
2. Lower to grasp position
3. Close gripper (simulated)
4. Lift box
5. Move to drop zone
6. Lower to place position
7. Open gripper (simulated)
8. Return to home position

## 👩‍💻 Author
Yasmine

## 📄 License
Apache-2.0

## 🙏 Acknowledgments
- uFactory Lite6 model from DeepMind MuJoCo Menagerie
- ROS 2 Jazzy Jalisco
- MuJoCo Physics Simulator
